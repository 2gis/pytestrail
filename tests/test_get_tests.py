from unittest import TestCase
from source_files_parser import get_tests
from os.path import abspath


class TestGetTests(TestCase):
    def test_get_tests_length(self):
        path = abspath('./test_data')
        tests = get_tests(path)
        num_tests = 4
        self.assertEqual(num_tests, len(tests),
                         "Must get %i test(s) from '%s'. Got %i instead." % (num_tests, path, len(tests)))
