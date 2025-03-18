from settings import *
from sprites import Sprite2D


class Ship(Sprite2D):
  def __init__(self, pos: Vector2 = Vector2(0, 0), direction: Vector2 = Vector2(0, 0), speed: int = 0):
    self.texture = load_texture("images/spaceship.png")
    super().__init__(self.texture, pos, direction, speed)
    self.collision_rec = Rectangle(
      self.pos.x,
      self.pos.y,
      self.texture.width,
      self.texture.height
    )
        

  def update(self, delta):
    self.direction.x = int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT))
    self.direction.y = int(is_key_down(KEY_DOWN)) - int(is_key_down(KEY_UP))
    self.direction = Vector2Normalize(self.direction)

    if self.pos.x >= 1920 - self.texture.width:
      self.direction.x = -1

    elif self.pos.x <= 0:
      self.direction.x = 1

    if self.pos.y >= 1080 - self.texture.height:
      self.direction.y = -1

    elif self.pos.y <= 0:
      self.direction.y = 1

    self.pos.x += self.speed * self.direction.x * delta
    self.pos.y += self.speed * self.direction.y * delta

    self.collision_rec = Rectangle(
      self.pos.x,
      self.pos.y,
      self.texture.width,
      self.texture.height
    )
