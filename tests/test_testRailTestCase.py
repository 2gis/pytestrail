from unittest import TestCase
from testrail.testcase import TestRailTestCase


class TestTestRailTestCase(TestCase):
    def test_to_json_dict(self):
        expected_jobject = {'priority_id': 4, 'type_id': 1, 'custom_steps_separated': [
            {'content': '- Get friends\n- Get Playstation\n', 'expected': 'OP: Fun in progress\n'},
            {'content': '- Get sixpack\n', 'expected': 'OP: More fun\n'}], 'title': 'Title'}

        case = TestRailTestCase(title='Title', section='Section', suite='Suite', steps=[
            {'content': '- Get friends\n- Get Playstation\n', 'expected': 'OP: Fun in progress\n'},
            {'content': '- Get sixpack\n', 'expected': 'OP: More fun\n'}])
        jobject = case.to_json_dict()
        self.assertEqual(jobject, expected_jobject,
                         "case.to_json_dict() must be '%s'. Got '%s' instead." % (expected_jobject, jobject))