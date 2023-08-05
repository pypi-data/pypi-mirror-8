import sys

from collections import defaultdict
from contextlib import contextmanager
from functools import partial
from io import BytesIO

import blinker

from fresco.compat import unquote, urlparse
from fresco.request import Request
from fresco.response import Response
from fresco.util.urls import normpath
from fresco.util.wsgi import unicode_to_environ

from fresco.exceptions import ResponseException
from fresco.requestcontext import context
from fresco.routing import (GET, ExtensiblePattern, RouteCollection,
                            RouteNotFound)
from fresco.options import Options

__all__ = ('FrescoApp', 'urlfor')


class FrescoApp(RouteCollection):
    """\
    Fresco application class.
    """

    #: The default class to use for URL pattern matching
    pattern_class = ExtensiblePattern

    #: A stdlib logger object, or None
    logger = None

    #: Class to use to instantiate request objects
    request_class = Request

    def __init__(self, views=None, path=None):

        super(FrescoApp, self).__init__()

        from fresco.middleware import context_middleware

        #: A list of (middleware, args, kwargs) tuples
        self._middleware = []

        #: Middleware layers applied after any middleware added through
        #: :meth:`add_middleware`.
        self.core_middleware = [partial(context_middleware, frescoapp=self)]

        #: The WSGI application. This is generated when the first request is
        #: made.
        self._wsgi_app = None

        #: An options dictionary, for arbitrary application variables or
        #: configuration
        self.options = Options()

        self.signal_ns = blinker.Namespace()

        #: Sent when a request matches a route, immediately before the view is
        #: invoked.
        #: Receivers will be passed: app, route, view, request
        self.route_matched = self.signal_ns.signal('route_matched')

        #: Sent after a view function is invoked, before the response
        #: object is output.
        #: Receivers will be passed: app, view, request and response
        self.view_finished = self.signal_ns.signal('view_finished')

        if views:
            if path is None:
                path = '/'
            self.include(path, views)

    def __call__(self, environ, start_response):
        """\
        Call the app as a WSGI application
        """
        if self._wsgi_app is None:
            self._wsgi_app = self._make_wsgi_app()
        return self._wsgi_app(environ, start_response)

    def __str__(self):
        """\
        String representation of the application and its configured routes
        """
        s = '<%s\n' % self.__class__.__name__
        for route in self.__routes__:
            s += '    ' + str(route)
        s += '>'
        return s

    def view(self, routecollection=None, request=None, path=None, method=None):
        try:
            routecollection = routecollection or self
            request = request or context.request
            method = method or request.method
            path = path or request.path_info
            error_response = None

            context.app = self
            environ = request.environ
            environ['fresco.app'] = self

            if path:
                path = normpath(path)
            else:
                path = '/'
        except ResponseException as e:
            return e.response

        for traversal in routecollection.get_routes(path, method, request):
            try:
                route = traversal.route
                environ['wsgiorg.routing_args'] = (traversal.args,
                                                   traversal.kwargs)
                view = route.getview()
                context.view_self = getattr(view, '__self__', None)

                if self.logger:
                    self.logger.info("matched route: %s %r => %r",
                                     request.method, path, view)

                context.route_traversal = traversal
                self.route_matched.send(self, route=route, view=view,
                                        request=request)

                response = route.getdecoratedview()(*traversal.args,
                                                    **traversal.kwargs)
            except ResponseException as e:
                if e.is_final:
                    return e.response
                error_response = error_response or e.response
            else:
                self.view_finished.send(self, view=view, request=request,
                                        response=response)
                return response

        # A route was matched, but an error was returned
        if error_response:
            return error_response

        # Is this a head request?
        if method == 'HEAD':
            response = self.view(routecollection, request, path, GET)
            if 200 <= response.status_code < 300:
                return response.replace(content=[], content_length=0)
            return response

        # Is the URL matched by another HTTP method?
        methods = self.get_methods(routecollection, request, path)
        if methods:
            return Response.method_not_allowed(methods)

        # Is the URL just missing a trailing '/'?
        if path[-1] != '/':
            for _ in self.get_methods(routecollection, request, path + '/'):
                return Response.redirect_permanent(path + '/')

        return Response.not_found()

    def get_methods(self, routecollection, request, path):
        """\
        Return the HTTP methods valid in routes to the given path
        """
        methods = set()
        for route, _, _, _ in routecollection.get_routes(path, None):
            if route.predicate and not route.predicate(request):
                continue
            methods.update(route.methods)
        return methods

    def add_middleware(self, middleware, *args, **kwargs):
        """\
        Add a WSGI middleware layer
        """
        if self._wsgi_app:
            raise AssertionError("Cannot add middleware: "
                                 "application is now receiving requests")
        self._middleware.append((middleware, args, kwargs))

    def _raw_wsgi_app(self, environ, start_response):
        return self.view(self, self.request_class(environ))(environ,
                                                            start_response)

    def _make_wsgi_app(self, app=None):
        app = app or self._raw_wsgi_app
        for middleware, args, kwargs in self._middleware:
            app = middleware(app, *args, **kwargs)
        for middleware in self.core_middleware:
            app = middleware(app)
        return app

    def urlfor(self, viewspec, *args, **kwargs):
        """\
        Return the url for the given view name or function spec

        :param viewspec: a view name, a reference in the form
                         ``'package.module.viewfunction'``, or the view
                         callable itself.
        :param _scheme: the URL scheme to use (eg 'https' or 'http').
        :param _netloc: the network location to use (eg 'localhost:8000').
        :param _script_name: the SCRIPT_NAME path component
        :param _query: any query parameters, as a dict or list of
                        ``(key, value)`` tuples.
        :param _fragment: a URL fragment to append.

        All other arguments or keyword args are fed to the ``pathfor`` method
        of the pattern.
        """
        scheme = kwargs.pop('_scheme', None)
        netloc = kwargs.pop('_netloc', None)
        query = kwargs.pop('_query', {})
        script_name = kwargs.pop('_script_name', None)
        fragment = kwargs.pop('_fragment', None)

        request = context.request
        traversal = context.get('route_traversal')
        if traversal and traversal.collections_traversed:
            collections_traversed = traversal.collections_traversed
        else:
            collections_traversed = [(self, '')]

        exc = None
        for collection, base_path in collections_traversed[::-1]:
            try:
                path = base_path + \
                        collection.pathfor(viewspec, request=request,
                                           *args, **kwargs)
            except RouteNotFound as e:
                exc = e
                continue
            return request.make_url(scheme=scheme, netloc=netloc,
                                    SCRIPT_NAME=script_name,
                                    PATH_INFO=path,
                                    parameters='',
                                    query=query, fragment=fragment)
        raise exc or RouteNotFound(viewspec)

    def view_method_not_found(self, valid_methods):
        """
        Return a ``405 Method Not Allowed`` response.

        Called when a view matched the pattern but no HTTP methods matched.
        """
        return Response.method_not_allowed(valid_methods)

    @contextmanager
    def requestcontext(self, url='http://localhost/', environ=None,
                       wsgi_input=b'', **kwargs):
        """
        Return the global :class:`fresco.requestcontext.RequestContext`
        instance, populated with a new request object modelling default
        WSGI environ values.

        Synopsis::

            >>> app = FrescoApp()
            >>> with app.requestcontext('http://www.example.com/view') as c:
            ...     print c.request.url
            ...
            http://www.example.com/view

        Note that ``url`` must be properly URL encoded.
        """
        url = urlparse(url)
        netloc = url.netloc
        user = ''
        if '@' in netloc:
            user, netloc = netloc.split('@', 1)

        if ':' in user:
            user, _ = user.split(':')[0]

        if isinstance(wsgi_input, bytes):
            wsgi_input = BytesIO(wsgi_input)

        env_overrides = environ or {}
        for key, value in kwargs.items():
            key = key.replace('wsgi_', 'wsgi.')
            if '.' not in key:
                # value must be a python native str, whatever that means
                if not isinstance(value, str):
                    value = unicode_to_environ(value)
            env_overrides[key] = value

        environ = {
            'REQUEST_METHOD': 'GET',
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'SERVER_PROTOCOL': 'HTTP/1.0',
            'HTTP_HOST': netloc or 'localhost',
            'SCRIPT_NAME': '',
            'PATH_INFO': unicode_to_environ(unquote(url.path)),
            'REMOTE_ADDR': '127.0.0.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': url.scheme or 'http',
            'wsgi.input': wsgi_input,
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': True,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
        }
        if url.scheme == 'https':
            environ['HTTPS'] = 'on'
            environ['SERVER_PORT'] = '443'

        if user:
            environ['REMOTE_USER'] = user

        if url.query:
            environ['QUERY_STRING'] = url.query

        environ.update(env_overrides)

        if getattr(self, '_fakewsgiapp', None) is None:
            def _fakewsgiapp(environ, start_response):
                start_response('200 OK', [])
                yield b''
            self._fakewsgiapp = self._make_wsgi_app(_fakewsgiapp)

        # Invoke a fake wsgi app wrapped in all middleware layers. This
        # executes any middleware, which may have side effects which are
        # expected downstream (eg setting environ keys)
        wsgi_iter = self._fakewsgiapp(environ, lambda *a, **kw: None)
        next(wsgi_iter)
        yield context

        # Exhaust the iterator and close up
        list(wsgi_iter)
        getattr(wsgi_iter, 'close', lambda: None)()


def collect_keys(items):
    """
    [(k1, v1), (k1, v2), (k2, v3)] -> [(k1, [v1, v2]), (k2, [v3])]
    """
    d = defaultdict(list)
    for key, value in items:
        d[key].append(value)
    return d.items()


def urlfor(*args, **kwargs):
    """\
    Convenience wrapper around :meth:`~fresco.core.FrescoApp.urlfor`.
    """
    return context.app.urlfor(*args, **kwargs)
