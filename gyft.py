import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup as bs
import json
import iitkgp_erp_login.erp as erp
import logging

updated_codes = False

with open('dept_codes.json') as f:
    dept_codes = json.load(f)

headers = {
    'timeout': '20',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}

s = requests.Session()

_, ssoToken = erp.login(headers, s)
print()


ERP_TIMETABLE_URL = "https://erp.iitkgp.ac.in/Acad/student/view_stud_time_table.jsp"
COURSES_URL = "https://erp.iitkgp.ac.in/Acad/timetable_track.jsp?action=second&dept={}"

timetable_details = {
    'ssoToken': ssoToken,
    'module_id': '16',
    'menu_id': '40',
}

def scrape_courses(courses, dept):
    # find dept code from dept_codes
    DEPT_URL = COURSES_URL.format(dept)
    r = s.get(DEPT_URL, headers=headers)
    soup = bs(r.text, 'html.parser')
    parentTable = soup.find('table', {'id': 'disptab'})

    rows = parentTable.find_all('tr')

    for row in rows[1:]:
        if 'bgcolor' in row.attrs:
            continue 
        cells = row.find_all('td')  
        course_code = cells[0].text.strip()
        course_name = cells[1].text.strip()

        if course_code in courses[dept]:
            courses[dept][course_code] = course_name
            logging.info(" {} - {}".format(course_code, course_name))


# This is just a hack to get cookies. TODO: do the standard thing here
abc = s.post(ERP_TIMETABLE_URL, headers=headers, data=timetable_details)
cookie_val = None
for a in s.cookies:
    if (a.path == "/Acad/"):
        cookie_val = a.value

cookie = {
    'JSESSIONID': cookie_val,
}
r = s.post(ERP_TIMETABLE_URL, cookies = cookie, headers=headers, data=timetable_details)

soup = bs(r.text, 'html.parser')
rows_head = soup.findAll('table')[2]
rows = rows_head.findAll('tr')
times = []


# Delete the rows that doesn't have tableheader, basically without a weekday
del_rows = []
for i in range(1, len(rows)):
    HeaderRows = rows[i].findAll("td", {"class": "tableheader"})
    # print(HeaderRows)
    if len(HeaderRows) == 0:
        del_rows.append(i)

for index_del in sorted(del_rows, reverse=True):
    del rows[index_del]


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
        if not tds[a].find('b'):
            continue
        txt = tds[a].find('b').text.strip()
        if (len(txt) >= 7):
            timetable_dict[days[i]][times[time]] = list((tds[a].find('b').text[:7],tds[a].find('b').text[7:], int(tds[a]['colspan'])))
        time = time + int(tds[a]['colspan'])


def merge_slots(in_dict):
    for a in in_dict:
        in_dict[a] = sorted(in_dict[a])
        for i in range(len(in_dict[a]) - 1, 0, -1):
            if (in_dict[a][i][0] == in_dict[a][i-1][0] + in_dict[a][i-1][1]):
                in_dict[a][i-1][1] = in_dict[a][i][1] + in_dict[a][i-1][1]
                in_dict[a].remove(in_dict[a][i])
        in_dict[a] = in_dict[a][0]
    return (in_dict)


for day in timetable_dict.keys():
    subject_timings = {}
    for time in timetable_dict[day]:
        flattened_time = int(time[:time.find(':')])
        if (flattened_time < 6):
            flattened_time += 12
        if (not timetable_dict[day][time][0] in subject_timings.keys()):
            subject_timings[timetable_dict[day][time][0]] = []
        subject_timings[timetable_dict[day][time][0]].append([flattened_time, timetable_dict[day][time][2]])
    subject_timings = merge_slots(subject_timings)
    for time in list(timetable_dict[day].keys()):
        flattened_time = int(time[:time.find(':')])
        if (flattened_time < 6):
            flattened_time += 12
        if (not flattened_time == subject_timings[timetable_dict[day][time][0]][0]):
            del (timetable_dict[day][time])
        else:
            timetable_dict[day][time][2] = subject_timings[timetable_dict[day][time][0]][1]

courses = {}
# grouping courses by dept
for day in timetable_dict.keys():
    for time in timetable_dict[day]:
        timetable_dict[day][time].append(" ")
        course_code = timetable_dict[day][time][0]
        course_dept = course_code[:2] 
        try:
            dept_code = dept_codes[course_dept]
        except:
            dept_code = input("Enter the 2 letter dept code for {}: ".format(course_dept))
            print()
            dept_codes[course_dept] = dept_code
            updated_codes = True

        if dept_code not in courses.keys():
            courses[dept_code] = {}
        if course_code not in courses[dept_code].keys():
            courses[dept_code][course_code] = ''


# scraping course names deptwise
for dept in courses.keys():
    try: 
        scrape_courses(courses,dept)
    except:
        print()
        logging.error(" Error while scraping course names for course letter code {}".format(dept))
        logging.info(" You can manually add the course names while executing generate_ics.py")
        print()

# add course code to dict
for day in timetable_dict.keys():
    for time in timetable_dict[day]:
        course_code = timetable_dict[day][time][0]
        dept_code = dept_codes[course_code[:2]]
        timetable_dict[day][time][3] = courses[dept_code][course_code]


with open('data.txt', 'w') as outfile:
    json.dump(timetable_dict, outfile, indent = 4, ensure_ascii=False)

if updated_codes:
    with open('dept_codes.json', 'w') as outfile:
        json.dump(dept_codes, outfile, indent = 4, ensure_ascii=False)
    print("\nThe dept_codes.json file has been updated with the new dept codes. Please send a PR to the repo with the updated file.")

print ("\nTimetable saved to data.txt file. You can generate the ICS file now by running generate_ics.py.\n")
