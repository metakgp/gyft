from timetable.image_parser.Models.rectangle import Rectangle

def get_maximum_intersecting_column(row: list[Rectangle], rect):
    max_intersect = -1
    max_intersect_i = 0
    for i in range(len(row)):
        r = row[i]
        intersect = 0
        x11, x12, x21, x22 = r.x, r.x + r.w, rect.x, rect.x + rect.w
        if x12 > x21 and x22 > x11: intersect = min(x12, x22) - max(x11, x21)
        if intersect > max_intersect:
            max_intersect = intersect
            max_intersect_i = i
    return max_intersect_i
