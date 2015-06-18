#!/usr/bin/env python

import unittest

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


if __name__ == "__main__":
    unittest.main()
