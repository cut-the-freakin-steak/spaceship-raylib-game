from settings import *


class Star:
  def __init__(self):
    self.texture = load_texture("images/star.png")
    self.pos = Vector2(randint(0, 1920), randint(0, 1080))
    self.scale = uniform(0.5, 2)
    self.original_scale = self.scale


  def draw(self):
    draw_texture_ex(self.texture, self.pos, 0.0, self.scale, WHITE)
