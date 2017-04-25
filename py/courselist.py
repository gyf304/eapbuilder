#CSVURL = r"http://www.andrew.cmu.edu/user/yifangu/cmucourselist.csv"
JSONURL = ""
try:
    import browser
    JSONURL = '/'.join(browser.window.location['href'].split['/'][:-1]) + '/data/courselist.json'

except Exception as e:
    JSONURL = r"http://localhost:8000/data/courselist.json"

import urllib.request
import json

print('using json url {:}'.format(JSONURL))

def get_course_dict():
    result = {}
    response = urllib.request.urlopen(JSONURL)
    json_str = response.read()
    try:
        response.close()
    except AttributeError as e:
        pass
    return json.loads(json_str)
