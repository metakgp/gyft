from utils import get_cookies
from requests import Session

headers = {
    'timeout': '20',
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu "
                  "Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36",
}

ERP_TIMETABLE_URL = "https://erp.iitkgp.ac.in/Acad/student/view_stud_time_table.jsp"
COURSES_URL = "https://erp.iitkgp.ac.in/Academic/student_performance_details_ug.htm"

# For Days
days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}


def scrape_timetable(session: Session, timetable_details: dict, coursepage_details: dict):
    cookie = get_cookies(s, timetable_details)
    r = s.post(ERP_TIMETABLE_URL, cookies=cookie, headers=headers, data=timetable_details)

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
                timetable_dict[days[i]][times[time]] = list(
                    (tds[a].find('b').text[:7], tds[a].find('b').text[7:], int(tds[a]['colspan'])))
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
    sub_dict = {k: v.replace("&amp;", "&") for k, v in sub_dict.items()}  # replacing &amp; with &

    # add course name to dict
    for day in timetable_dict.keys():
        for time in timetable_dict[day]:
            if timetable_dict[day][time][0] == "CS10001":
                timetable_dict[day][time][0] = "CS10003"
            course_code = timetable_dict[day][time][0]
            timetable_dict[day][time].append(sub_dict[course_code])

    return timetable_dict
