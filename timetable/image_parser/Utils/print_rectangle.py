import numpy as np
import cv2
from timetable.image_parser.Classes.rectangle import Rectangle

def print_rectangles(rectangles: list[Rectangle], img):
  temp = np.zeros(img.shape, dtype=np.uint8)
  temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2BGR)
  for rect in rectangles:
    cv2.rectangle(temp, (rect.x, rect.y), (rect.x + rect.w, rect.y + rect.h), (0, 255, 0), 1)
  cv2.imwrite("rectangles.jpg", temp)