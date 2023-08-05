# -*- coding: utf-8 -*-
"""
    test
    ~~~~

    Flask-Cors tests module
"""

from tests.base_test import FlaskCorsTestCase, AppConfigTest
from flask import Flask

try:
    # this is how you would normally import
    from flask.ext.cors import *
except:
    # support local usage without installed package
    from flask_cors import *


class HeadersTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Welcome!'

        @self.app.route('/test_list')
        @cross_origin(headers=["Foo", "Bar"])
        def test_list():
            return 'Welcome!'

        @self.app.route('/test_string')
        @cross_origin(headers="Foo")
        def test_string():
            return 'Welcome!'

        @self.app.route('/test_set')
        @cross_origin(headers=set(["Foo", "Bar"]))
        def test_set():
            return 'Welcome!'

    def test_default(self):
        for resp in self.iter_responses('/test_default'):
            self.assertTrue(resp.headers.get(ACL_HEADERS) is None,
                            "Default should have no allowed headers")

    def test_list_serialized(self):
        ''' If there is an Origin header in the request,
            the Access-Control-Allow-Origin header should be echoed back.
        '''
        for resp in self.iter_responses('/test_list'):
            self.assertEqual(resp.headers.get(ACL_HEADERS), 'Bar, Foo')

    def test_string_serialized(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be echoed back.
        '''
        for resp in self.iter_responses('/test_string'):
            self.assertEqual(resp.headers.get(ACL_HEADERS), 'Foo')

    def test_set_serialized(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be echoed back.
        '''
        resp = self.get('/test_set')
        self.assertEqual(resp.headers.get(ACL_HEADERS), 'Bar, Foo')


class AppConfigHeadersTestCase(AppConfigTest, HeadersTestCase):
    def __init__(self, *args, **kwargs):
        super(AppConfigHeadersTestCase, self).__init__(*args, **kwargs)

    def test_list_serialized(self):
        self.app.config['CORS_HEADERS'] = ['Foo', 'Bar']

        @self.app.route('/test_list')
        @cross_origin()
        def test_list():
            return 'Welcome!'

        super(AppConfigHeadersTestCase, self).test_list_serialized()

    def test_string_serialized(self):
        self.app.config['CORS_HEADERS'] = 'Foo'

        @self.app.route('/test_string')
        @cross_origin()
        def test_string():
            return 'Welcome!'

        super(AppConfigHeadersTestCase, self).test_string_serialized()

    def test_set_serialized(self):
        self.app.config['CORS_HEADERS'] = set(["Foo", "Bar"])

        @self.app.route('/test_set')
        @cross_origin()
        def test_set():
            return 'Welcome!'
        super(AppConfigHeadersTestCase, self).test_set_serialized()

    def test_default(self):
        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Welcome!'
        super(AppConfigHeadersTestCase, self).test_default()


if __name__ == "__main__":
    unittest.main()
