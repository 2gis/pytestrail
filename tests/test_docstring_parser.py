from unittest import TestCase
from docstring_parser import get_section
from test_data.sample_tests import Tests


class TestGetSection(TestCase):
    def test_get_section(self):
        section = get_section(Tests.test_something_cool)
        self.assertEqual(section, 'The Lost Broken Bones',
                         "Section must be 'The Lost Broken Bones'. Got '%s' instead." % section)

    def test_get_section_negative(self):
        section = get_section(Tests.this_is_not_test_method)
        self.assertIsNone(section, "Section must be 'None'. Got '%s' instead."%section)