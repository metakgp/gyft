import json
from dataclasses import dataclass

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString, PageElement

with open("full_location.json") as data_file:
    full_locations = json.load(data_file)


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
    days = {'Mon': "Monday", 'Tue': "Tuesday", 'Wed': "Wednesday", 'Thur': "Thursday", 'Fri': "Friday",
            'Sat': "Saturday"}
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'border': '1', 'cellpadding': '0', 'cellspacing': '0'})

    def create_timings(_table: Tag | NavigableString) -> list[int]:
        r""" Creates a list of timings in 24 hours format - [8, ..., 12, 14, ..., 17]"""
        headings = _table.find_all('td', {'class': 'tableheader',
                                          'style': 'padding-top:5px;padding-bottom:5px;padding-left:7px;padding-right'
                                                   ':7px', 'nowrap': ''})
        return [int(time.get_text().split(':')[0]) + 12 if int(time.get_text().split(':')[0]) < 6 else int(
            time.get_text().split(':')[0]) for time in headings if time.get_text() != 'Day Name']

    timings = create_timings(table)
    rows = table.find_all('tr')
    
    for row in rows:
        day_cell: PageElement = row.find('td', {'valign': 'top'})
        if not day_cell:
            continue
        day = days.get(day_cell.get_text(), day_cell.get_text())
    
        prev: Course | None = None
        course_duration: int = 0
        cells = [cell for cell in row.find_all('td') if cell.attrs.get('valign') != 'top']
    
        def append_prev():
            prev.duration = course_duration
            courses.append(prev)
    
        for index, cell in enumerate(cells):
            text = cell.get_text().strip()
            if not text or text in [' ', ' ']: # encountered empty cell: either commit the prev course or skip
                if prev:
                    append_prev()
                course_duration = 0
                prev = None
                continue
    
            code = text[:7] if text[:7] != "CS10001" else "CS10003" # original code is CS10003 but the timetable has CS10001
            location = text[7:]
            cell_duration = int(cell.attrs.get('colspan', 1))
    
            if prev and code == prev.code: # encounterd a continuation of the previous course
                course_duration += cell_duration
            else:
                if prev: # encountered a new course, commit the previous course
                    append_prev()
                # reinstantiate the prev course
                prev = Course(code=code, name=course_names.get(code, ""), day=day,
                              start_time=timings[index],
                              location=location)
                course_duration = cell_duration

        # end of the day: commit the last course
        if prev:
            append_prev()
    
    return courses
