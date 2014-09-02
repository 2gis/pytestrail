# coding=utf-8
from unittest import TestCase
from docstring_parser import get_section, get_test_title, get_suite, get_test_steps
from test_data.sample_tests import Tests


class TestGetSection(TestCase):
    def test_get_section(self):
        section = get_section(Tests.test_something_cool)
        self.assertEqual(section, 'The Lost Broken Bones',
                         "Section must be 'The Lost Broken Bones'. Got '%s' instead." % section)

    def test_get_section_without_docstring(self):
        section = get_section(Tests.this_is_not_test_method)
        self.assertIsNone(section, "Section must be 'None'. Got '%s' instead." % section)


class TestGetName(TestCase):
    def test_get_title(self):
        title = get_test_title(Tests.test_something_cool)
        self.assertEqual(title, 'Blood Pressure', "Title must be 'Blood Pressure'. Got '%s' instead." % title)

    def test_get_title_without_title_definition(self):
        title = get_test_title(Tests.test_with_no_title)
        self.assertEqual(title, 'test_with_no_title', "Title must be 'test_with_no_title'. Got '%s' instead." % title)

    def test_get_title_without_docstring(self):
        title = get_test_title(Tests.this_is_not_test_method)
        self.assertIsNone(title, "Title must be 'None'. Got '%s' instead." % title)


class TestGetSuite(TestCase):
    def test_get_suite(self):
        suite = get_suite(Tests.test_something_cool)
        self.assertEqual(suite, 'Useless Id', "Suite must be 'Useless Id'. Got '%s' instead." % suite)

    def test_get_suite_negative(self):
        suite = get_suite(Tests.test_with_no_title)
        self.assertIsNone(suite, "Suite must be 'None'. Got '%s' instead." % suite)


class TestGetSteps(TestCase):
    def test_get_steps(self):
        expected_steps = [{'content': '- Get friends\n- Get Playstation\n', 'expected': 'Fun in progress\n'}]
        steps = get_test_steps(Tests.test_something_cool)
        self.assertEqual(expected_steps, steps, "Steps must be '%s'. Got '%s' instead." % (expected_steps, steps))

    def test_get_steps_without_docstring(self):
        steps = get_test_steps(Tests.this_is_not_test_method)
        self.assertIsNone(steps, "Steps must be 'None'. Got '%s' instead" % steps)

    def test_get_steps_without_result(self):
        expected_steps = [{'content': '- Get friends\n- Get Playstation\n', 'expected': ''}]
        steps = get_test_steps(Tests.test_steps_with_no_result)
        self.assertEqual(expected_steps, steps, "Steps must be '%s'. Got '%s' instead." % (expected_steps, steps))

    def test_get_steps_with_multiple_results(self):
        expected_steps = [{'content': '- Get friends\n- Get Playstation\n', 'expected': 'Fun in progress\n'},
                          {'content': '- Get sixpack\n', 'expected': 'ОР написано по-русски\n'}]
        steps = get_test_steps(Tests.test_steps_with_multiple_results)
        self.assertEqual(expected_steps, steps, "Steps must be '%s'. Got '%s' instead." % (expected_steps, steps))

    def test_get_steps_without_steps_definition(self):
        steps = get_test_steps(Tests.test_without_steps)
        self.assertEqual(steps, [], "Steps must be 'None'. Got '%s' instead." % steps)

    def test_get_steps_with_equals_sign(self):
        expected_steps = [
            {'content': '- Get sixpack\n- Get friends\n- Get Playstation\n',
             'expected': 'Fun in progress\nHardcore gaming\n'}]
        steps = get_test_steps(Tests.test_with_no_title)
        self.assertEqual(expected_steps, steps, "Steps must be '%s'. Got '%s' instead." % (expected_steps, steps))