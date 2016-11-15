import os
import server
import unittest
import tempfile
import inspect
import json

class ServerTestCase(unittest.TestCase):
    def setUp(self):
        """Run before every test."""
        self.app = server.app.test_client()

    def tearDown(self):
        """Run after every test."""
        pass

    def test_a_thing(self):
        # rv = self.app.get('/')
        # print([name for name, thing in inspect.getmembers(rv)])
        pass

    def test_root_should_error_without_proper_body(self):
        """Should respond with 400 if the POST has no body."""
        response = self.app.post('/')
        assert response.status_code == 400

    def test_non_json_request_body(self):
        """Should respond with 400 if provided with non-json Content-Type."""
        response = self.app.post('/', content_type='plain/text')
        assert response.status_code == 400

    def test_non_invalid_key_in_json_body(self):
        """Should respond with 400 if provided with invalid POST data."""
        bad_data = json.dumps({'someotherkey': 'Some other key value'})
        response = self.app.post('/',
                                 data=bad_data,
                                 content_type='application/json')
        assert response.status_code == 400

    def test_non_invalid_simulation(self):
        """Should respond with 400 if provided with invalid XML."""
        bad_data = json.dumps({'simulation': 'Not valid XML'})
        response = self.app.post('/',
                                 data=bad_data,
                                 content_type='application/json')
        assert response.status_code == 400

    # Should respond with 400 if the XML isn't a valid simulation configuration
    # Should respond with 200 if the XML is a valid simulation
    # Should respond with simulation results

    # def test_good_request(self):
        # """Should respond with simulation results."""
        # data = json.dumps({'simulation': 'Some simulation'})
        # response = self.app.post('/',
                                 # data=data,
                                 # content_type='application/json')

        # assert response.status_code is 200

if __name__ == '__main__':
    unittest.main()
