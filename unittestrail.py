import json

from source_files_parser import get_tests
from testrail.testrail import APIClient
cl = APIClient('http://testrail.2gis.local/')
tests_dir = '/Users/ibakepunk/Projects/desktop4/tests/'
project_id = 52

suites = {}
for x in json.loads(cl.get_suites(project_id)):
    suites[x['name']] = x['id']

sections = {}
for x in json.loads(cl.get_sections(project_id, 0)):
    sections[x['name']] = x['id']

cases = {}
for x in json.loads(cl.get_all_cases(project_id)):
    cases[x['title']] = x['id']

testcases = get_tests(tests_dir)
for testcase in testcases:
    if testcase.suite_name not in suites:
        new_suite = json.loads(cl.create_suite(project_id, testcase.suite_name))
        suites[new_suite['name']] = new_suite['id']
    if testcase.section_name not in sections:
        new_section = json.loads(cl.create_section(project_id, testcase.suite_id, testcase.name))
        sections[new_section['name']] = new_section['id']

    if testcase.name in cases:
        cl.update_case(cases[testcase.title], testcase)
    else:
        cl.add_case(sections[testcase.section_name], testcase)
