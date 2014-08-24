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

t = get_tests(tests_dir)
#t = __get_source_files(tests_dir)
print len(t)
print t[0].to_json_dict()
cl.add_case(t[0])
