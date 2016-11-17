"""Test build_sim"""

import unittest
import os
import re
from .errors import SimBuildError
from .build_sim import build_sim

class BuildSimTestCase(unittest.TestCase):
    """Tests for simulation builder."""
    def setUp(self):
        """Run before every test."""
        pass
    def tearDown(self):
        """Run after every test."""
        pass

def assert_build_fails(xml):
    """Assert that parsing a given XML string fails."""
    build_failed = False
    try:
        build_sim(xml)
    except SimBuildError:
        build_failed = True

    assert build_failed is True

def assert_build_succeeds(xml):
    """Assert that parsing a given XML string succeeds."""
    build_failed = False
    try:
        build_sim(xml)
    except SimBuildError:
        build_failed = True

    assert build_failed is False

# ref: http://stackoverflow.com/a/2799009
def create_invalid_sim_test(path):
    """Create tests for invalid simulations"""
    def do_test_expected(self):
        """Assert simulation is invalid"""
        with open(path, 'r') as xml_file:
            xml = xml_file.read()
            assert_build_fails(xml)
    return do_test_expected

# ref: http://stackoverflow.com/a/2799009
def create_valid_sim_test(path):
    """Create tests for valid simulations"""
    def do_test_expected(self):
        """Assert simulation is valid"""
        with open(path, 'r') as xml_file:
            xml = xml_file.read()
            assert_build_succeeds(xml)
    return do_test_expected

def build_tests():
    """Dynamically generate tests based on valid/invalid XML files.

    Test XML files are stored at:
        XML which should trigger an error: ./test_simulations/invalid
        XML which should not trigger an error: ./test_simulations/valid
    """
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
            setattr(BuildSimTestCase, test_method.__name__, test_method)

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
            setattr(BuildSimTestCase, test_method.__name__, test_method)

            test_id += 1

build_tests()

if __name__ == '__main__':
    unittest.main()
