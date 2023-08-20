import json
from dataclasses import dataclass
import datetime
from bs4 import BeautifulSoup

with open("full_location.json") as data_file:
    full_locations = json.load(data_file)


@dataclass
class Course:
    code: str
    name: str
    day: str
    start_time: int
    location: str
    end_time: int | None = None

    def get_location(self):
        if ('NC' in self.location or 'NR' in self.location) and (
                self.location[:2] + self.location[3]) in full_locations.keys():
            return full_locations[self.location[:2] + self.location[3]]
        if self.location in full_locations.keys():
            return full_locations[self.location]
        return self.location

    def get_duration(self):
        return self.end_time - self.start_time

    @property
    def title(self):
        if 'NC' in self.location or 'NR' in self.location:
            return f"[{self.location}] {self.name.title()}"
        return self.name.title()


def build_courses(html, course_names: dict) -> list[Course]:
    r"""
    Build a list of Course objects from the html timetable
    Args:
        html: html code of the timetable returned by the server
        course_names: mapping of course codes to course names

    Returns:
        list of Course objects
    """
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
