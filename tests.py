#!/usr/bin/env python

import json
import time
import datetime
import unittest

import utils
from api import app


class TestAPIApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_404_page(self):
        rv = self.app.get('/404/')
        self.assertEqual(rv.status_code, 404)

    def test_static_text_file_request(self):
        rv = self.app.get('/robots.txt')
        self.assertTrue(rv.data)
        self.assertEqual(rv.status_code, 200)
        rv.close()


class TestUtils(unittest.TestCase):

    def test_remove_utm(self):
        url = utils.remove_utm('http://127.0.0.1/index?q=index&utm_source=1'
                               '&utm_medium=2&utm_campaign=3#body')
        self.assertEqual(url, 'http://127.0.0.1/index?q=index#body')

    def test_custom_json_encoder(self):
        data = {
            'datetime.time': datetime.date(2015, 1, 1)
        }
        json_dump = json.dumps(data, cls=utils.CustomJSONEncoder)
        self.assertEqual(json_dump, '{"datetime.time": "2015-01-01"}')


if __name__ == "__main__":
    unittest.main()
