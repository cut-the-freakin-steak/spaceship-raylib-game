from settings import *

class Button:
  def __init__(self, x: float, y: float, width: float, height: float, empty: bool = True):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.empty = empty
    self.button = Rectangle(self.x, self.y, self.width, self.height)


  def draw(self, color: Color, font: Font, font_size: int, text: str = None, text_dimensions: Vector2 = None):
    if self.empty:
      draw_rectangle_lines_ex(self.button, 10, color)

    else:
      draw_rectangle_rec(self.button, color)
    
    if text is not None:
      draw_text_ex(
        font,
        text,
        Vector2(self.x + (self.width / 2) - (text_dimensions.x / 2),
                self.y + (self.height / 2) - (text_dimensions.y / 2)),
        font_size,
        7.0,
        color
      )
