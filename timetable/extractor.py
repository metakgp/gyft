from dataclasses import dataclass

from bs4 import BeautifulSoup


# # For Days
# days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
#
#
# def scrape_timetable(session: ERPSession):
#     r = session.post(session.ERP_TIMETABLE_URL, cookies=True, data=session.get_timetable_details())
#
#     soup = bs(r.text, 'html.parser')
#     rows_head = soup.findAll('table')[2]
#     rows = rows_head.findAll('tr')
#     times = []
#
#     # Delete the rows that doesn't have tableheader, basically without a weekday
#     del_rows = []
#     for i in range(1, len(rows)):
#         header_rows = rows[i].findAll("td", {"class": "tableheader"})
#         if len(header_rows) == 0:
#             del_rows.append(i)
#
#     for index_del in sorted(del_rows, reverse=True):
#         del rows[index_del]
#
#     # For timings
#     for a in rows[0].findAll('td'):
#         if 'AM' in a.text or 'PM' in a.text:
#             times.append(a.text)
#
#     timetable_dict = {}
#
#     for i in range(1, len(rows)):
#         timetable_dict[days[i]] = {}
#         tds = rows[i].findAll('td')
#         time = 0
#         for a in range(1, len(tds)):
#             if not tds[a].find('b'):
#                 continue
#             txt = tds[a].find('b').text.strip()
#             if len(txt) >= 7:
#                 timetable_dict[days[i]][times[time]] = list(
#                     (tds[a].find('b').text[:7], tds[a].find('b').text[7:], int(tds[a]['colspan'])))
#             time = time + int(tds[a]['colspan'])
#
#     def merge_slots(in_dict):
#         for a in in_dict:
#             in_dict[a] = sorted(in_dict[a])
#             for i in range(len(in_dict[a]) - 1, 0, -1):
#                 if in_dict[a][i][0] == in_dict[a][i - 1][0] + in_dict[a][i - 1][1]:
#                     in_dict[a][i - 1][1] = in_dict[a][i][1] + in_dict[a][i - 1][1]
#                     in_dict[a].remove(in_dict[a][i])
#             in_dict[a] = in_dict[a][0]
#         return in_dict
#
#     for day in timetable_dict.keys():
#         subject_timings = {}
#         for time in timetable_dict[day]:
#             flattened_time = int(time[:time.find(':')])
#             if flattened_time < 6:
#                 flattened_time += 12
#             if not timetable_dict[day][time][0] in subject_timings.keys():
#                 subject_timings[timetable_dict[day][time][0]] = []
#             subject_timings[timetable_dict[day][time][0]].append([flattened_time, timetable_dict[day][time][2]])
#         subject_timings = merge_slots(subject_timings)
#         print(subject_timings)
#         for time in list(timetable_dict[day].keys()):
#             flattened_time = int(time[:time.find(':')])
#             if flattened_time < 6:
#                 flattened_time += 12
#             if not flattened_time == subject_timings[timetable_dict[day][time][0]][0]:
#                 del (timetable_dict[day][time])
#             else:
#                 timetable_dict[day][time][2] = subject_timings[timetable_dict[day][time][0]][1]
#                 print(timetable_dict[day][time][2])
#
#     # get course names
#     r = session.post(session.COURSES_URL, data=session.get_coursepage_details())
#     sub_dict = {item["subno"]: item["subname"] for item in r.json()}
#     sub_dict = {k: v.replace("&amp;", "&") for k, v in sub_dict.items()}  # replacing &amp; with &
#
#     # add course name to dict
#     for day in timetable_dict.keys():
#         for time in timetable_dict[day]:
#             if timetable_dict[day][time][0] == "CS10001":
#                 timetable_dict[day][time][0] = "CS10003"
#             course_code = timetable_dict[day][time][0]
#             timetable_dict[day][time].append(sub_dict[course_code])
#
#     return timetable_dict


@dataclass
class Course:
    code: str
    name: str
    day: str
    start_time: int
    location: str
    end_time: int | None = None

    def get_location(self):
        if 'NC' in self.location or 'NR' in self.location:
            # TODO: Return full location
            pass
        return self.location

    def get_duration(self):
        return self.end_time - self.start_time


def build_courses(html, course_names) -> list[Course]:
    courses = []
    days = {'Mon': "Monday", 'Tue': "Tuesday", 'Wed': "Wednesday", 'Thur': "Thursday", 'Fri': "Friday",
            'Sat': "Saturday"}
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'border': '1', 'cellpadding': '0', 'cellspacing': '0'})

    def create_timings_dict(table) -> list:
        r"""# Creates a list of timings in 24 hours format - [8, .., 12, 14, .., 17]"""
        headings = table.find_all('td', {'class': 'tableheader',
                                         'style': 'padding-top:5px;padding-bottom:5px;padding-left:7px;padding-right'
                                                  ':7px',
                                         'nowrap': ''})
        timings = [int(time.get_text().split(':')[0]) + 12 if int(time.get_text().split(':')[0]) < 6 else int(
            time.get_text().split(':')[0]) for time in headings if time.get_text() != 'Day Name']
        return timings

    timings = create_timings_dict(table)
    rows = table.find_all('tr')
    for row in rows:
        day_cell = row.find('td', {'valign': 'top'})
        if not day_cell:
            continue
        day = days[day_cell.get_text()]
        prev: Course | None = None
        for index, cell in enumerate(cell for cell in row.find_all('td') if cell.attrs.get('valign') != 'top'):
            if cell.get_text() == ' ':
                if prev:
                    prev.end_time = timings[index]
                    courses.append(prev)
                prev = None
            elif prev:
                if cell.get_text()[:7] == prev.code:
                    print(cell.get_text()[:7])
                    continue
                else:
                    prev.end_time = timings[index]
                    courses.append(prev)
                    prev = Course(code=cell.get_text()[:7], name=course_names[cell.get_text()[:7]], day=day,
                                  start_time=timings[index],
                                  location=cell.get_text()[7:])
            else:
                prev = Course(code=cell.get_text()[:7], name=course_names[cell.get_text()[:7]], day=day,
                              start_time=timings[index],
                              location=cell.get_text()[7:])
    return courses
