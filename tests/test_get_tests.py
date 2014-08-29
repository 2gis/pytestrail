from unittest import TestCase
from source_files_parser import get_tests


class TestGetTests(TestCase):
    def test_get_tests_length(self):
        tests = get_tests('./test_data')
        self.assertEqual(1, len(tests),
                         "Must get only one test from './test_data/sample_tests.py! Got " + str(len(tests)))
