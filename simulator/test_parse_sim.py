"""Test parse_sim"""

import unittest
import os
import sys
import re
from .errors import SimParseError
from .parse_sim import parse_sim

class ParseSimTestCase(unittest.TestCase):
    """Tests for simulation parser."""
    def setUp(self):
        """Run before every test."""
        pass
    def tearDown(self):
        """Run after every test."""
        pass

def assert_parse_fails(xml):
    """Assert that parsing a given XML string fails."""
    parse_failed = False
    try:
        parse_sim(xml)
    except SimParseError:
        parse_failed = True

    assert parse_failed is True

def assert_parse_succeeds(xml):
    """Assert that parsing a given XML string succeeds."""
    parse_failed = False
    try:
        parse_sim(xml)
    except SimParseError:
        parse_failed = True

    assert parse_failed is False

# ref: http://stackoverflow.com/a/2799009
def create_invalid_sim_test(xml_path):
    """Create tests for invalid simulations"""
    def do_test_expected(self):
        """Assert simulation is invalid"""
        with open(xml_path, 'r') as xml_file:
            xml = xml_file.read()
            assert_parse_fails(xml)
    return do_test_expected

# ref: http://stackoverflow.com/a/2799009
def create_valid_sim_test(xml_path):
    """Create tests for valid simulations"""
    def do_test_expected(self):
        """Assert simulation is valid"""
        with open(xml_path, 'r') as xml_file:
            xml = xml_file.read()
            assert_parse_succeeds(xml)
    return do_test_expected

# ref: http://stackoverflow.com/a/5137509
dir_path = os.path.dirname(os.path.realpath(__file__))

invalid_sim_dir_path = '%s/test_simulations/invalid' % dir_path
test_id = 0
for filename in os.listdir(invalid_sim_dir_path):
    if re.match(r'^.*\.xml$', filename):
        xml_path = "%s/%s" % (invalid_sim_dir_path, filename)

        # ref: http://stackoverflow.com/a/2799009
        test_method = create_invalid_sim_test(xml_path)
        test_method.__name__ = "test_%s" % \
            filename.replace('-', '_').replace('.xml', '')
        setattr(ParseSimTestCase, test_method.__name__, test_method)

        test_id += 1

valid_sim_dir_path = '%s/test_simulations/valid' % dir_path
test_id = 0
for filename in os.listdir(valid_sim_dir_path):
    if re.match(r'^.*\.xml$', filename):
        xml_path = "%s/%s" % (valid_sim_dir_path, filename)

        # ref: http://stackoverflow.com/a/2799009
        test_method = create_valid_sim_test(xml_path)
        test_method.__name__ = "test_%s" % \
            filename.replace('-', '_').replace('.xml', '')
        setattr(ParseSimTestCase, test_method.__name__, test_method)

        test_id += 1

if __name__ == '__main__':
    unittest.main()
