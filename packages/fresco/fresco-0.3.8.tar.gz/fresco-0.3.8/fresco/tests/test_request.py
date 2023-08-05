# coding=UTF-8

from io import BytesIO
from nose.tools import assert_equal, assert_raises

from fresco import FrescoApp, exceptions
from fresco.tests import fixtures

context = FrescoApp().requestcontext


class TestRequestProperties(object):

    def test_url_script_name_only(self):
        with context(SCRIPT_NAME='/foo/bar', PATH_INFO='') as c:
            assert_equal(c.request.url, "http://localhost/foo/bar")

    def test_url_script_name_path_info(self):
        with context(SCRIPT_NAME='/foo/bar', PATH_INFO='/baz') as c:
            assert_equal(c.request.url, "http://localhost/foo/bar/baz")

    def test_url_normalizes_host_port(self):
        with context(HTTP_HOST='localhost:80') as c:
            assert_equal(c.request.url, "http://localhost/")
        with context(HTTP_HOST='localhost:81') as c:
            assert_equal(c.request.url, "http://localhost:81/")

    def test_url_normalizes_host_ssl_port(self):
        with context(environ={'wsgi.url_scheme': 'https'},
                     HTTP_HOST='localhost:443') as c:
            assert_equal(c.request.url, "https://localhost/")

    def test_url_ignores_server_port_if_host_header_present(self):
        with context(environ={'wsgi.url_scheme': 'https', 'SERVER_PORT': '81'},
                     HTTP_HOST='localhost') as c:
            assert_equal(c.request.url, "https://localhost/")

    def test_as_string(self):
        with context('http://example.org/foo?bar=baz') as c:
            assert_equal(str(c.request),
                         '<Request GET http://example.org/foo?bar=baz>')

    def test_url_returns_full_url(self):
        with context('http://example.org/foo?bar=baz') as c:
            assert_equal(c.request.url, 'http://example.org/foo?bar=baz')

    def test_path_returns_correct_path_when_script_name_empty(self):
        with context(SCRIPT_NAME='', PATH_INFO='/foo/bar') as c:
            assert_equal(c.request.path, '/foo/bar')

    def test_path_returns_correct_path(self):
        with context(SCRIPT_NAME='/foo', PATH_INFO='/bar') as c:
            assert_equal(c.request.path, '/foo/bar')

    def test_query_decodes_unicode(self):
        with context('/?q=%C3%A0') as c:
            assert_equal(c.request.query['q'], b'\xc3\xa0'.decode('utf8'))

    def test_form_decodes_unicode(self):
        with context('/?q=%C3%A0') as c:
            assert_equal(c.request.form['q'], b'\xc3\xa0'.decode('utf8'))


class TestPathEncoding(object):

    def test_url_is_quoted(self):

        with context(SCRIPT_NAME=fixtures.wsgi_unicode_path,
                     PATH_INFO='') as c:
            assert c.request.url == 'http://localhost' + \
                                        fixtures.quoted_unicode_path

    def test_application_url_is_quoted(self):

        with context(SCRIPT_NAME=fixtures.wsgi_unicode_path,
                     PATH_INFO='') as c:
            assert c.request.application_url == 'http://localhost' + \
                                                fixtures.quoted_unicode_path

    def test_parsed_url_is_quoted(self):
        with context(SCRIPT_NAME=fixtures.wsgi_unicode_path,
                     PATH_INFO='') as c:
            assert c.request.parsed_url.path == fixtures.quoted_unicode_path

    def test_path_is_unquoted(self):
        with context(SCRIPT_NAME=fixtures.wsgi_unicode_path,
                     PATH_INFO='') as c:
            assert c.request.path == fixtures.unquoted_unicode_path

    def test_script_name_is_unquoted(self):
        with context(SCRIPT_NAME=fixtures.wsgi_unicode_path,
                     PATH_INFO='') as c:
            assert c.request.script_name == fixtures.unquoted_unicode_path

    def test_path_info_is_unquoted(self):
        with context(PATH_INFO=fixtures.wsgi_unicode_path) as c:
            assert c.request.path_info == fixtures.unquoted_unicode_path

    def test_invalid_path_info_encoding_raises_bad_request(self):
        with context(PATH_INFO=fixtures.misquoted_wsgi_unicode_path) as c:
            assert_raises(exceptions.BadRequest, lambda: c.request.path_info)

    def test_invalid_script_name_encoding_raises_bad_request(self):
        with context(SCRIPT_NAME=fixtures.misquoted_wsgi_unicode_path) as c:
            assert_raises(exceptions.BadRequest, lambda: c.request.script_name)


class TestMakeURL(object):

    def assert_equal_with_query(self, url1, url2):
        if '?' not in url1:
            return assert_equal(url1, url2)

        base1, _, q1 = url1.partition('?')
        base2, _, q2 = url2.partition('?')
        assert_equal(base1, base2)
        assert_equal(sorted(q1.split(';')), sorted(q2.split(';')))

    def test_it_returns_request_url(self):
        with context(SCRIPT_NAME='/script', PATH_INFO='/pathinfo') as c:
            assert_equal(c.request.make_url(),
                         'http://localhost/script/pathinfo')

    def test_it_doesnt_double_quote_request_url(self):
        with context(SCRIPT_NAME='/script name', PATH_INFO='/path info') as c:
            assert_equal(c.request.make_url(),
                         'http://localhost/script%20name/path%20info')

    def test_it_doesnt_double_quote_supplied_path_info(self):
        with context() as c:
            assert_equal(c.request.make_url(PATH_INFO='/x y'),
                         'http://localhost/x%20y')

    def test_can_replace_path(self):
        with context(SCRIPT_NAME='/script', PATH_INFO='/pathinfo') as c:
            assert_equal(c.request.make_url(path='/foo bar'),
                         'http://localhost/foo%20bar')

    def test_it_joins_path(self):
        with context(SCRIPT_NAME='/script name', PATH_INFO='/path info/') as c:
            assert_equal(c.request.make_url(path='a/b c'),
                         'http://localhost/script%20name/path%20info/a/b%20c')

    def test_query_not_included_by_default(self):
        with context(QUERY_STRING='query=foo') as c:
            assert_equal(c.request.make_url(),
                         'http://localhost/')

    def test_query_dict(self):
        with context() as c:
            self.assert_equal_with_query(
                c.request.make_url(query={'a': 1, 'b': '2 3'}),
                'http://localhost/?a=1;b=2+3')

    def test_query_kwargs(self):
        with context() as c:
            self.assert_equal_with_query(
                c.request.make_url(query={'a': 1}, b=2),
                'http://localhost/?a=1;b=2')

    def test_unicode_path(self):
        e = b'\xc3\xa9'.decode('utf8')  # e-acute
        with context() as c:
            assert_equal(c.request.make_url(path=e),
                         'http://localhost/%C3%A9')

    def test_unicode_path_info(self):
        e = b'\xc3\xa9'.decode('utf8')  # e-acute
        with context() as c:
            assert_equal(c.request.make_url(PATH_INFO=e),
                         'http://localhost/%C3%A9')

    def test_unicode_query(self):
        e = b'\xc3\xa9'.decode('utf8')  # e-acute
        with context() as c:
            assert_equal(c.request.make_url(query={'e': e}),
                         'http://localhost/?e=%C3%A9')

    def test_it_quotes_paths(self):
        with context() as c:
            assert_equal(c.request.make_url(path='/a b'),
                         'http://localhost/a%20b')

    def test_replace_query_replaces_existing(self):
        with context(QUERY_STRING='a=1') as c:
            assert_equal(c.request.make_url(query_replace={'a': '2'}),
                         'http://localhost/?a=2')

    def test_replace_query_adds_new_value(self):
        with context(QUERY_STRING='a=1') as c:
            self.assert_equal_with_query(
                c.request.make_url(query_replace={'b': '2'}),
                'http://localhost/?a=1;b=2')

    def test_add_query_doesnt_replace_existing(self):
        with context(QUERY_STRING='a=1') as c:
            self.assert_equal_with_query(
                c.request.make_url(query_add={'a': '2'}),
                'http://localhost/?a=1;a=2')

    def test_add_query_works_on_specified_query(self):
        with context(QUERY_STRING='a=1') as c:
            assert_equal(c.request.make_url(query='', query_add={'a': '2'}),
                         'http://localhost/?a=2')

    def test_add_query_does_not_mutate_request_query(self):
        with context(QUERY_STRING='a=1') as c:
            c.request.make_url(query_add={'a': '2'})
            assert list(c.request.query.allitems()) == [('a', '1')]


class TestResolveURL(object):

    def test_relative_path(self):
        with context(SCRIPT_NAME='/script', PATH_INFO='/pathinfo') as c:
            assert_equal(c.request.resolve_url('foo'),
                         'http://localhost/script/foo')

    def test_absolute_path_unspecified_relative(self):
        with context(SCRIPT_NAME='/script', PATH_INFO='/pathinfo') as c:
            assert_equal(c.request.resolve_url('/foo', relative='app'),
                         'http://localhost/script/foo')

    def test_absolute_path_app_relative(self):
        with context(SCRIPT_NAME='/script', PATH_INFO='/pathinfo') as c:
            assert_equal(c.request.resolve_url('/foo', relative='app'),
                         'http://localhost/script/foo')

    def test_absolute_path_server_relative(self):
        with context(SCRIPT_NAME='/script', PATH_INFO='/pathinfo') as c:
            assert_equal(c.request.resolve_url('/foo', relative='server'),
                         'http://localhost/foo')

    def test_ignores_server_port_if_host_header_present(self):
        with context(environ={'wsgi.url_scheme': 'https', 'SERVER_PORT': '81'},
                     HTTP_HOST='localhost') as c:
            assert_equal(c.request.resolve_url('/foo'),
                         'https://localhost/foo')


class TestCurrentRequest(object):

    def test_currentrequest_returns_current_request(self):
        from fresco import currentrequest
        with context() as c:
            assert currentrequest() is c.request

    def test_currentrequest_returns_None(self):
        from fresco import currentrequest
        assert currentrequest() is None


class TestFiles(object):

    filename = 'test.txt'
    filedata = '123456\n'
    boundary = '---------------------------1234'

    post_data = (
        '--{boundary}\r\n'
        'Content-Disposition: form-data; '
            'name="uploaded_file"; filename="{filename}"\r\n'
        'Content-Type: text/plain\r\n'
        '\r\n'
        '{filedata}\r\n'
        '--{boundary}'
        '--\r\n'
    ).format(boundary=boundary, filedata=filedata, filename=filename)\
     .encode('latin1')

    request_args = {'wsgi_input': post_data,
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': 'multipart/form-data; boundary=' +
                                        boundary,
                    'CONTENT_LENGTH': str(len(post_data))}

    def test_files_populated(self):

        with FrescoApp().requestcontext(**self.request_args) as c:
            request = c.request

        assert len(request.files) == 1
        assert 'uploaded_file' in request.files

    def test_file_content_available(self):

        with FrescoApp().requestcontext(**self.request_args) as c:
            request = c.request

        b = BytesIO()
        request.files['uploaded_file'].save(b)
        assert b.getvalue() == self.filedata.encode('latin1')

    def test_headers_available(self):

        with FrescoApp().requestcontext(**self.request_args) as c:
            request = c.request

        assert request.files['uploaded_file'].headers['content-type'] \
                == 'text/plain'
        assert request.files['uploaded_file'].filename == self.filename
