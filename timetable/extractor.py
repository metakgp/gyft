import json
from dataclasses import dataclass

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString, PageElement

with open("full_location.json") as data_file:
    full_locations = json.load(data_file)

DAYS_MAP = {'Mon': "Monday", 'Tue': "Tuesday", 'Wed': "Wednesday", 'Thur': "Thursday", 'Fri': "Friday", 'Sat': "Saturday"}

@dataclass
class Course:
    code: str
    name: str
    day: str
    start_time: int
    location: str
    duration: int = 0

    def get_location(self) -> str:
        # TODO: more logic to specify other locations if possible
        if ('NC' in self.location or 'NR' in self.location) and (
                self.location[:2] + self.location[3]) in full_locations.keys():
            return full_locations[self.location[:2] + self.location[3]]
        if self.location in full_locations.keys():
            return full_locations[self.location]
        return self.location

    @property
    def title(self) -> str:
        if 'NC' in self.location or 'NR' in self.location:
            return f"[{self.location}] {self.name.title()}"
        return self.name.title()

    @property
    def end_time(self) -> int:
        return self.duration + self.start_time

def create_timings(_table: Tag | NavigableString) -> list[int]:
    r""" Creates a list of timings in 24 hours format - [8, ..., 12, 14, ..., 17]"""
    headings = _table.find_all(
        'td',
        {
            'class': 'tableheader',
            'style': 'padding-top:5px;padding-bottom:5px;padding-left:7px;padding-right:7px',
            'nowrap': ''
        }
    )

    get_hour = lambda t: int(t.get_text().split(':')[0])

    return [
        get_hour(time) + 12 if
        get_hour(time) < 6 else
        get_hour(time) for
        time in headings if time.get_text() != 'Day Name'
    ]

def build_courses(html: str, course_names: dict) -> list[Course]:
    r"""
    Build a list of Course objects from the html timetable
    Args:
        html: html code of the timetable returned by the server
        course_names: mapping of course codes to course names

    Returns:
        list of Course objects
    """
    courses = []
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'border': '1', 'cellpadding': '0', 'cellspacing': '0'})

    timings = create_timings(table)
    rows = table.find_all('tr')
    for row in rows:
        day_cell: PageElement = row.find('td', {'valign': 'top'})
        if not day_cell:
            continue
        day = DAYS_MAP.get(day_cell.get_text(), day_cell.get_text())

        # This is the previously parsed course/time slot. Used to merge timeslots occurring adjacent to each other and initialize course objects
        prev: Course | None = None
        cells = [cell for cell in row.find_all('td') if cell.attrs.get('valign') != 'top']

        for index, cell in enumerate(cells):
            # Empty cell means either previous class just ended or no class is scheduled
            if cell.get_text().strip() == "":
                if prev:
                    # Previous slot ended
                    courses.append(prev)
                    prev = None
                continue

            code = cell.get_text()[:7].strip()
            if not code: continue   # continue if cell has no course in it

            # Special exception: CS10003 is the actual code, but it is written as CS10001 in the timetable
            if code == "CS10001":
                code = "CS10003"

            location = cell.get_text()[7:]
            cell_duration = int(cell.attrs.get('colspan'))

            # Either new class started just after previous one or previous class is continued
            if prev:
                # If previous class is same as current class, add the duration to the previous class
                if code == prev.code:
                    prev.duration += cell_duration
                # The previous class is different from the current one, meaning previous class ended. Clean up, add to
                # list and initialize a new course object for the current class
                else:
                    courses.append(prev)
                    prev = Course(
                        code=code,
                        name=course_names[code],
                        day=day,
                        start_time=timings[index],
                        location=location,
                        duration=cell_duration
                    )
            # New class started after break
            else:
                prev = Course(
                    code=code,
                    name=course_names[code],
                    day=day,
                    start_time=timings[index],
                    location=location,
                    duration=cell_duration
                )

            # Day ended, add the last class
            if index == len(cells) - 1:
                courses.append(prev)
                prev = None
    return courses
