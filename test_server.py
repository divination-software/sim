"""Test the Flask server which exposes the simulator."""

import unittest
import json
import main

class ServerTestCase(unittest.TestCase):
    """Tests for the server."""

    def setUp(self):
        """Run before every test."""
        self.app = main.app.test_client()

    def tearDown(self):
        """Run after every test."""
        pass

    def test_no_post_body(self):
        """Should respond with 400 if the POST has no body."""
        response = self.app.post('/')
        assert response.status_code == 400

    def test_non_json_request_body(self):
        """Should respond with 400 if provided with non-json Content-Type."""
        response = self.app.post('/', content_type='plain/text')
        assert response.status_code == 400

    def test_invalid_key_in_json_body(self):
        """Should respond with 400 if provided with invalid POST data."""
        bad_data = json.dumps({'someotherkey': 'Some other key value'})
        response = self.app.post('/',
                                 data=bad_data,
                                 content_type='application/json')
        assert response.status_code == 400

if __name__ == '__main__':
    unittest.main()
