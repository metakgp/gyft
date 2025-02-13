from timetable.image_parser.Models.rectangle import Rectangle


def sort_rows(rectangles: list[Rectangle], threshold_height: int):
    rows = []
    row = []
    back = -1
    for rec in rectangles:
        if back == -1:
            row.append(rec)
            back = rec.y
        elif abs(back - rec.y) < threshold_height:
            row.append(rec)
            back = rec.y
        else:
            rows.append(row)
            row = [rec]
            back = -1

    if len(row): rows.append(row)
    rows.reverse()
    for row in rows:
        row.sort(key=lambda x: x.x)
    return rows