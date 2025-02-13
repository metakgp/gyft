import json
from dataclasses import dataclass

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString, PageElement

from utils.minimum_distant_code import get_minimum_distant_code

course_code_map = json.load(open('timetable/course_data.json'))

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
    cell_dur: int = 0

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
        name_title = self.name.title() if self.name else self.code
        if 'NC' in self.location or 'NR' in self.location:
            return f"[{self.location}] {name_title}"
        return name_title

    def get_name(self) -> str:
        if(self.name): return self.name
        self.get_code()
        self.name = course_code_map[self.code]
        return self.name
    
    def get_code(self) -> str:
        self.code = get_minimum_distant_code(self.code)
        return self.code

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

    return [
        get_time(time) for
        time in headings if time.get_text() != 'Day Name'
    ]

def get_time(time: str) -> int:
    get_hour = lambda t: int(t.split(':')[0])
    return get_hour(time) + 12 if get_hour(time) < 6 else get_hour(time)

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
        # This is the previously parsed course/time slot. Used to merge timeslots occurring adjacent to each other and initialize course objects
        day = DAYS_MAP.get(day_cell.get_text(), day_cell.get_text())
    
        prev: Course | None = None
        cells = [cell for cell in row.find_all('td') if cell.attrs.get('valign') != 'top']
    
        for index, cell in enumerate(cells):
            text = cell.get_text().strip()
            if not text: # encountered empty cell: either commit the prev course or skip
                if prev:
                    # Previous slot ended
                    courses.append(prev)
                    prev = None
                continue
    
            code = text[:7] if text[:7] != "CS10001" else "CS10003" # original code is CS10003 but the timetable has CS10001
            location = text[7:]
            cell_duration = int(cell.attrs.get('colspan', 1))
    
            if prev and code == prev.code: # encounterd a continuation of the previous course
                prev.duration += cell_duration
            else:
                if prev: # encountered a new course, commit the previous course
                    courses.append(prev)
                # reinstantiate the prev course

                start_time = timings[index]
                if(prev and prev.cell_dur>1):
                    start_time+=prev.cell_dur-1

                prev = Course(code=code, name=course_names.get(code, ""), day=day,
                              start_time=start_time,
                              location=location)
                prev.duration = cell_duration
                prev.cell_dur = cell_duration

        # end of the day: commit the last course
        if prev:
            courses.append(prev)
    
    return courses
