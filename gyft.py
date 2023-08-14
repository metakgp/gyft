import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup as bs
import json
import os.path as osp
import iitkgp_erp_login.erp as erp
import argparse
from dates import SEM_BEGIN
from generate_ics import generate_ICS
from add_events import create_calendar
from del_events import delete_calendar

headers = {
    'timeout': '20',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}

ERP_TIMETABLE_URL = "https://erp.iitkgp.ac.in/Acad/student/view_stud_time_table.jsp"
COURSES_URL = "https://erp.iitkgp.ac.in/Academic/student_performance_details_ug.htm"

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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", 
                        help="Input file containing timetable in .txt format")
    parser.add_argument("-o", "--output",
                        help="Output file containing timetable in .ics format")
    parser.add_argument("-d", "--del-events", action="store_true", 
                        help="Delete events automatically added by the script before adding new events")
    args = parser.parse_args()
    return args

def get_cookies(s, timetable_details):
    # This is just a hack to get cookies. TODO: do the standard thing here
    abc = s.post(ERP_TIMETABLE_URL, headers=headers, data=timetable_details)
    cookie_val = None
    for a in s.cookies:
        if (a.path == "/Acad/"):
            cookie_val = a.value

    cookie = {
        'JSESSIONID': cookie_val,
    }
    return cookie

def merge_slots(in_dict):
    for a in in_dict:
        in_dict[a] = sorted(in_dict[a])
        for i in range(len(in_dict[a]) - 1, 0, -1):
            if (in_dict[a][i][0] == in_dict[a][i-1][0] + in_dict[a][i-1][1]):
                in_dict[a][i-1][1] = in_dict[a][i][1] + in_dict[a][i-1][1]
                in_dict[a].remove(in_dict[a][i])
        in_dict[a] = in_dict[a][0]
    return (in_dict)

def scrape_timetable(s, timetable_details, coursepage_details):
    cookie = get_cookies(s, timetable_details)
    r = s.post(ERP_TIMETABLE_URL, cookies = cookie, headers=headers, data=timetable_details)

    soup = bs(r.text, 'html.parser')
    rows_head = soup.findAll('table')[2]
    rows = rows_head.findAll('tr')
    times = []

    # Delete the rows that doesn't have tableheader, basically without a weekday
    del_rows = []
    for i in range(1, len(rows)):
        HeaderRows = rows[i].findAll("td", {"class": "tableheader"})
        if len(HeaderRows) == 0:
            del_rows.append(i)

    for index_del in sorted(del_rows, reverse=True):
        del rows[index_del]

    ##### For timings
    for a in rows[0].findAll('td'):
        if ('AM' in a.text or 'PM' in a.text):
            times.append(a.text)

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

    # get course names
    r = s.post(COURSES_URL, headers=headers, data=coursepage_details)
    sub_dict = {item["subno"]: item["subname"] for item in r.json()}
    sub_dict = {k: v.replace("&amp;", "&") for k, v in sub_dict.items()} # replacing &amp; with &

    # add course name to dict
    for day in timetable_dict.keys():
        for time in timetable_dict[day]:
            course_code = timetable_dict[day][time][0]
            if course_code=="CS10001":
                course_code = "CS10003"
            timetable_dict[day][time].append(sub_dict[course_code])
    
    return timetable_dict

def main():
    overwrite = True
    generate = True

    args = parse_args()

    if args.del_events:
        delete_calendar()
        gen = input("\nWould you like to generate a new timetable? (y/n): ")
        if gen.lower() == 'n':
            generate = False
    
    if generate:
        INPUT_FILENAME = args.input if args.input else "data.txt"
        OUTPUT_FILENAME = args.output if args.output else "timetable.ics"

        # check if data.txt exists
        if osp.exists(INPUT_FILENAME):
            ow = input(f"Timetable file {INPUT_FILENAME} exists. Do you want to overwrite it? (y/n): ")
            print()
            if ow.lower() == 'n':
                overwrite = False

        if overwrite:
            s = requests.Session()
            _, ssoToken = erp.login(headers, s)
            print()

            if SEM_BEGIN.month > 6:
                # autumn semester
                SEM_NO = (int(SEM_BEGIN.strftime("%y"))-int(erp.ROLL_NUMBER[:2]))*2 + 1
            else:
                # spring semester
                SEM_NO = (int(SEM_BEGIN.strftime("%y"))-int(erp.ROLL_NUMBER[:2])) + 2

            timetable_details = {
                "ssoToken": ssoToken,
                "module_id": '16',
                "menu_id": '40',
            }

            coursepage_details = {
                "ssoToken": ssoToken,
                "semno": SEM_NO,
                "rollno": erp.ROLL_NUMBER,
                "order": "asc"
            }

            timetable_dict = scrape_timetable(s, timetable_details, coursepage_details)

            with open(INPUT_FILENAME, 'w') as outfile:
                json.dump(timetable_dict, outfile, indent = 4, ensure_ascii=False)
            
            print(f"Timetable saved to {INPUT_FILENAME} file.\n")


        print("What would you like to do now?")
        print("1. Add timetable directly to Google Calendar (requires client_secret.json)")
        print("2. Generate an ICS file")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            create_calendar()
        elif choice == 2:
            generate_ICS(INPUT_FILENAME, OUTPUT_FILENAME) 
        else:
            exit()
        

if __name__ == "__main__":
    main()
