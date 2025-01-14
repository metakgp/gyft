import pytesseract
import math

class Rectangle:
  def __init__(self, x, y, w, h):
    self.x = x
    self.y = y
    self.w = w
    self.h = h

  def contains(self, rect):
    return (
        self.x <= rect.x and
        self.x + self.w >= rect.x + rect.w and
        self.y <= rect.y and
        self.y + self.h >= rect.y + rect.h
    )

  def is_contained(self, rect):
    return rect.contains(self)

  def get_text(self, img):
    sub_img = img[self.y:self.y+self.h, self.x:self.x+self.w]
    config = """
    --oem 3 --psm 6 -c tessedit_char_whitelist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:- '
    """.strip()
    return pytesseract.image_to_string(sub_img, lang='eng', config=config).strip()

  
  def get_centre(self):
    return (self.x + self.w // 2, self.y + self.h // 2)
  
  def angle_line_centres(self, rect):
    x1, y1 = self.get_centre()
    x2, y2 = rect.get_centre()
    return math.atan2(abs(y2 - y1), abs(x2 - x1))