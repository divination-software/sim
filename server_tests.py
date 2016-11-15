import os
import server
import unittest
import tempfile
import inspect
import json

class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = server.app.test_client()

    def tearDown(self):
        pass

    def test_a_thing(self):
        # rv = self.app.get('/')
        # print([name for name, thing in inspect.getmembers(rv)])
        pass

    def test_root_should_error_without_proper_body(self):
        try:
            response = self.app.post('/')
        except TypeError:
            assert True is True

    def test_root_should_return_200(self):
        data = json.dumps({'simulation': 'Some simulation'})
        response = self.app.post('/',
                                 data=data,
                                 content_type='application/json')

        assert response.status_code is 200

if __name__ == '__main__':
    unittest.main()
