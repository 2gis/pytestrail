import sys
import json
import argparse
from os.path import expanduser, expandvars

from source_files_parser import get_tests
from testrail.testrail import APIClient

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', help='Project id', type=int)
    parser.add_argument('-H', '--base_url', help='Testrail address', type=str, default='http://testrail.2gis.local/')
    parser.add_argument('-l', '--login', help='Testrail login', type=str)
    parser.add_argument('-P', '--password', help='Testrail password', type=str)
    parser.add_argument('-d', '--tests_dir', help='Tests directory', type=str, default='./tests')
    args = parser.parse_args(sys.argv)

    cl = APIClient(args.base_url)
    tests_dir = '/Users/ibakepunk/Projects/desktop4/tests/'
    tests_dir = expandvars(expanduser(args.tests_dir))
    project_id = args.project

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

    actual_cases = {}
    for x in testcases:
        actual_cases[x.title] = x

    for case_title, case_id in cases:
        if case_title not in actual_cases:
            print 'Delete case: '+case_title
            cl.delete_case(case_id)

    for testcase in testcases:
        if testcase.suite_name not in suites:
            print 'Create suite: '+testcase.suite_name
            new_suite = json.loads(cl.create_suite(project_id, testcase.suite_name))
            suites[new_suite['name']] = new_suite['id']

        if testcase.section_name not in sections:
            print 'Create section "'+testcase.section_name+'" in suite "'+testcase.suite_name+'"'
            new_section = json.loads(cl.create_section(project_id, testcase.suite_id, testcase.name))
            sections[new_section['name']] = new_section['id']

        if testcase.name in cases:
            print 'Update case: '+testcase.title
            cl.update_case(cases[testcase.title], testcase)
        else:
            print 'Create case: '+testcase.title
            cl.add_case(sections[testcase.section_name], testcase)
