from extractor import Course, get_time, DAYS_MAP
from utils.levenshtein_distance import get_minimum_distant_code

def build_courses_from_image(data: list[list[str]]) -> list[Course]:
    courses = []
    cols = [get_time(x) for x in data[0][1:]]

    for row in data[1:]:
        day = DAYS_MAP.get(row[0], row[0])
        cells = row[1:]
        prev: Course | None = None

        for index, cell in enumerate(cells):
            text = cell.strip()
            if not text: # encountered empty cell: either commit the prev course or skip
                if prev:
                    # Previous slot ended
                    courses.append(prev)
                    prev = None
                continue
    
            code = text.split()[0].strip() if '\n' in text else text[:7]
            code = code.upper()
            if code == "CS10001":
                code = "CS10003"
            code = get_minimum_distant_code(code)
            location = text[len(code):].strip()
            cell_duration = 1
    
            if prev and code == prev.code: # encounterd a continuation of the previous course
                prev.duration += cell_duration
            else:
                if prev: # encountered a new course, commit the previous course
                    courses.append(prev)
                # reinstantiate the prev course

                start_time = cols[index]
                if(prev and prev.cell_dur>1):
                    start_time+=prev.cell_dur-1

                prev = Course(code=code, name="", day=day,
                              start_time=start_time,
                              location=location)
                prev.get_name()
                prev.duration = cell_duration
                prev.cell_dur = cell_duration

        # end of the day: commit the last course
        if prev:
            courses.append(prev)
    
    return courses
