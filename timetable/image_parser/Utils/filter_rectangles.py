from timetable.image_parser.Classes.rectangle import Rectangle

# remove the rectangle which contains all the other rectangles

def filter_rectangles(rectangles: list[Rectangle]):
  max_x_rect = 0
  min_x_rect = 0
  max_y_rect = 0
  min_y_rect = 0
  for i in range(len(rectangles)):
    rect = rectangles[i]
    x, y, w, h = rect.x, rect.y, rect.w, rect.h
    if x > rectangles[i].x: max_x_rect = i
    if x < rectangles[i].x: min_x_rect = i
    if y > rectangles[i].y: max_y_rect = i
    if y < rectangles[i].y: min_y_rect = i
  set_rect = set([max_x_rect, min_x_rect, max_y_rect, min_y_rect])
  valid = [True] * len(rectangles)
  for r in set_rect:
    contains_all = True
    for i in range(len(rectangles)):
      if i == r: continue
      if not rectangles[r].contains(rectangles[i]):
        contains_all = False
        break
    if contains_all:
        valid[r] = False

  # Remove the rectangles which are contained by other rectangles
  for i in range(len(rectangles)):
      if not valid[i]: continue
      for j in range(len(rectangles)):
        if i == j: continue
        if rectangles[i].contains(rectangles[j]):
          valid[j] = False

  return [rectangles[i] for i in range(len(rectangles)) if valid[i]]