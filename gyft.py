import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from bs4 import BeautifulSoup as bs
import sys
import re

#### Parsing from commmand line
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-user', type = str, help = "Username")
parser.add_argument('-pwd', type = str, help = "Password")
args = parser.parse_args()
#### Parsing ends

ERP_HOMEPAGE_URL = 'https://erp.iitkgp.ernet.in/IIT_ERP3/'
ERP_LOGIN_URL = 'https://erp.iitkgp.ernet.in/SSOAdministration/auth.htm'
ERP_SECRET_QUESTION_URL = 'https://erp.iitkgp.ernet.in/SSOAdministration/getSecurityQues.htm'



headers = {
    'timeout': 20,
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}

s = requests.Session()
r = s.get(ERP_HOMEPAGE_URL)
soup = bs(r.text, 'html.parser')
sessionToken = soup.find_all(id='sessionToken')[0].attrs['value']
r = s.post(ERP_SECRET_QUESTION_URL, data={'user_id': args.user},
           headers = headers)
secret_question = r.text
print (secret_question)
secret_answer = input("What is the answer?\n")
login_details = {
    'user_id': args.user,
    'password': args.pwd,
    'answer': secret_answer,
    'sessionToken': sessionToken,
    'requestedUrl': 'https://erp.iitkgp.ernet.in/IIT_ERP3',
}
r = s.post(ERP_LOGIN_URL, data=login_details,
           headers = headers)
ssoToken = re.search(r'\?ssoToken=(.+)$',
                     r.history[1].headers['Location']).group(1)

ERP_TIMETABLE_URL = "https://erp.iitkgp.ernet.in/Acad/student/view_stud_time_table.jsp"

timetable_details = {
    'ssoToken': ssoToken,
    'module_id': '16',
    'menu_id': '40',
}

abc = s.post('https://erp.iitkgp.ernet.in/Acad/student/view_stud_time_table.jsp', headers=headers, data=timetable_details)
cookie_val = None
for a in s.cookies:
    if (a.path == "/Acad/"):
        cookie_val = a.value

cookie = {
    'JSESSIONID': cookie_val,
}
r = s.post('https://erp.iitkgp.ernet.in/Acad/student/view_stud_time_table.jsp',cookies = cookie, headers=headers, data=timetable_details)

soup = bs(r.text, 'html.parser')
rows_head = soup.findAll('table')[2]
rows = rows_head.findAll('tr')
times = []

##### For timings

for a in rows[0].findAll('td'):
    if ('AM' in a.text or 'PM' in a.text):
        times.append(a.text)

#### For timings end
days = {}
#### For day
days[1] = "Monday"
days[2] = "Tuesday"
days[3] = "Wednesday"
days[4] = "Thursday"
days[5] = "Friday"
days[6] = "Saturday"
#### For day end

timetable_dict = {}

for i in range(1, len(rows)):
    timetable_dict[days[i]] = {}
    tds = rows[i].findAll('td')
    time = 0
    for a in range(1, len(tds)):
        txt = tds[a].find('b').text.strip()
        if (len(txt) >= 7):
            timetable_dict[days[i]][times[time]] = (tds[a].find('b').text[:7],tds[a].find('b').text[7:], int(tds[a]._attr_value_as_string('colspan')))
        time = time + int(tds[a]._attr_value_as_string('colspan'))

import json
with open('data.txt', 'w') as outfile:
    json.dump(timetable_dict, outfile, indent = 4, ensure_ascii=False)