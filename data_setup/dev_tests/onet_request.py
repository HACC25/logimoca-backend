import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import base64
import json
import sys

class OnetWebService:
    def __init__(self, username, password):
            self._headers = {
                'User-Agent': 'python-OnetWebService/1.00 (bot)',
                'Authorization': 'Basic ' + base64.standard_b64encode((username + ':' + password).encode()).decode(),
                'Accept': 'application/json' }
            self.set_version()
        
    def set_version(self, version = None):
        if version is None:
            self._url_root = 'https://services.onetcenter.org/ws/'
        else:
            self._url_root = 'https://services.onetcenter.org/v' + version + '/ws/'

    def getInterestProfilerQuestions(self):
        questions = self.call('mnm/interestprofiler/questions?start=1&end=60')
        return questions
    
    def call(self, path, *query):
        url = self._url_root + path
        if len(query) > 0:
            url += '?' + urllib.parse.urlencode(query, True)
        req = urllib.request.Request(url, None, self._headers)
        handle = None
        try:
            handle = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            if e.code == 422:
                return json.load(e)
            else:
                return { 'error': 'Call to ' + url + ' failed with error code ' + str(e.code) }
        except urllib.error.URLError as e:
            return { 'error': 'Call to ' + url + ' failed with reason: ' + str(e.reason) }
        code = handle.getcode()
        if (code != 200) and (code != 422):
            return { 'error': 'Call to ' + url + ' failed with error code ' + str(code),
                    'urllib2_info': handle }
        return json.load(handle)


def get_user_input(prompt):
    result = ''
    while (len(result) == 0):
        result = input(prompt + ': ').strip()
    return result

def check_for_error(service_result):
    if 'error' in service_result:
        sys.exit(service_result['error'])

username = get_user_input('O*NET Web Services username')
password = get_user_input('O*NET Web Services password')
onet_ws = OnetWebService(username, password)

q_info = onet_ws.getInterestProfilerQuestions()
check_for_error(q_info)
print("Connected to O*NET Web Services")
print("")

# Example: Retrieve Interest Profiler questions
print("Interest Profiler Questions:")
print(q_info)
print("")

with open('dev_tests/interest_profiler_questions.json', 'w') as f:
    json.dump(q_info, f, indent=2)

# kwquery = get_user_input('Keyword search query')
# kwresults = onet_ws.call('online/search',
#                          ('keyword', kwquery),
#                          ('end', 5))
# check_for_error(kwresults)
# if (not 'occupation' in kwresults) or (0 == len(kwresults['occupation'])):
#     print("No relevant occupations were found.")
#     print("")
# else:
#     print("Most relevant occupations for \"" + kwquery + "\":")
#     for occ in kwresults['occupation']:
#         print("  " + occ['code'] + " - " + occ['title'])
#     print("")