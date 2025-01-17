import cv2
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from timetable.image_parser.Classes.line import Line
from timetable.image_parser.Classes.rectangle import Rectangle
from timetable.image_parser.Utils.filter_rectangles import filter_rectangles
from timetable.image_parser.Utils.get_maximum_intersecting_column import get_maximum_intersecting_column
from timetable.image_parser.Utils.sort_rows import sort_rows


def parse_table(image):
    img = np.array(image)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 200, 200, apertureSize=3)

    lsd = cv2.createLineSegmentDetector(cv2.LSD_REFINE_ADV, sigma_scale=0.35)
    dlines = lsd.detect(edges)
    lines = [Line(x0, y0, x1, y1) for x0, y0, x1, y1 in dlines[0][:, 0]]
    imgCopy = img.copy()
    for dline in dlines[0]:
        x0 = int(round(dline[0][0]))
        y0 = int(round(dline[0][1]))
        x1 = int(round(dline[0][2]))
        y1 = int(round(dline[0][3]))
        cv2.line(imgCopy, (x0, y0), (x1, y1), (0, 255, 0), 2)


    tableStructure = np.zeros(img.shape, dtype=np.uint8)

    for line in lines:
        coordinates = line.coordinates_as_int()
        cv2.line(tableStructure, coordinates[0], coordinates[1], (255, 255, 255), 1)

    kernel = np.ones((5, 5), np.uint8)
    tableStructure = cv2.dilate(tableStructure, kernel, iterations=1)
     
    table_structure = cv2.cvtColor(tableStructure, cv2.COLOR_RGB2GRAY)
    contours, hierarchy = cv2.findContours(table_structure, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    count = 0

    rectangles = [] 

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        rectangles.append(Rectangle(x, y, w, h))

    filtered_rect = filter_rectangles(rectangles)

    rows = sort_rows(filtered_rect, img.shape[0]//20)

    columns = rows[0]


    df = [[] for _ in range(len(rows)-1)]
    for col in columns:
        for i in range(1, len(rows)):
            row = rows[i]
            intersecting_column = get_maximum_intersecting_column(row, col)
            df[i-1].append(row[intersecting_column].get_text(gray))


    columns = [col.get_text(gray) for col in columns]
    return [columns, *df]