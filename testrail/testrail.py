#
# TestRail API binding for Python (API v2, available since TestRail 3.0)
#
# Learn more:
#
# http://docs.gurock.com/testrail-api2/start
# http://docs.gurock.com/testrail-api2/accessing
#
# Copyright Gurock Software GmbH. See license.md for details.
#

import urllib2, json, base64

class APIClient:
    def __init__(self, base_url):
        self.user = 'v.chapaev'
        self.password = '123qwe!'
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url + 'index.php?/api/v2/'

    #
    # Send Get
    #
    # Issues a GET request (read) against the API and returns the result
    # (as Python dict).
    #
    # Arguments:
    #
    # uri                 The API method to call including parameters
    #                     (e.g. get_case/1)
    #
    def send_get(self, uri):
        return self.__send_request('GET', uri, None)

    #
    # Send POST
    #
    # Issues a POST request (write) against the API and returns the result
    # (as Python dict).
    #
    # Arguments:
    #
    # uri                 The API method to call including parameters
    #                     (e.g. add_case/1)
    # data                The data to submit as part of the request (as
    #                     Python dict, strings must be UTF-8 encoded)
    #
    def send_post(self, uri, data):
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri
        request = urllib2.Request(url)
        if (method == 'POST'):
            request.add_data(json.dumps(data))
        auth = base64.encodestring('%s:%s' % (self.user, self.password)).strip()
        request.add_header('Authorization', 'Basic %s' % auth)
        request.add_header('Content-Type', 'application/json')

        e = None
        try:
            response = urllib2.urlopen(request).read()
        except urllib2.HTTPError as e:
            response = e.read()

        if response:
            result = json.loads(response)
        else:
            result = {}

        if e != None:
            if result and 'error' in result:
                error = '"' + result['error'] + '"'
            else:
                error = 'No additional error message received'
            raise APIError('TestRail API returned HTTP %s (%s)' %
                (e.code, error))

        return result

    def add_case(self, section_id, testcase):
        return self.send_post('add_case/'+str(section_id), testcase.to_json_dict())

    def get_suites(self, project_id):
        return self.send_get('get_suites/'+str(project_id))

    def get_sections(self, project_id, suite_id):
        return self.send_get('get_sections/'+str(project_id)+'&suite_id='+str(suite_id))

    def create_section(self, project_id, suite_id, name, parent_id=None):
        return self.send_post('add_section/'+str(project_id), dict(suite_id=suite_id, name=name, parent_id=parent_id))

    def create_suite(self, project_id, name, description=None):
        return self.send_post('add_suite/'+str(project_id), dict(name=name, description=description))

    def get_all_cases(self, project_id):
        return self.send_get('get_cases/'+str(project_id))

    def update_case(self, case_id, testcase):
        return self.send_post('update_case/'+str(case_id), testcase.to_json_dict())

    def delete_case(self, case_id):
        return self.send_post('delete_case/'+str(case_id), None)

class APIError(Exception):
    pass