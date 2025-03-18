from settings import *


class Laser:
  def __init__(self, pos: Vector2):
    self.texture = load_texture("images/laser.png")
    self.ship_texture = load_texture("images/spaceship.png") 
    self.sfx = load_sound("audio/laser.wav")
    set_sound_volume(self.sfx, 0.75)
    play_sound(self.sfx)
    self.pos = Vector2(pos.x + (self.ship_texture.width / 2 - 4.5), pos.y)
    self.collision_rec = Rectangle(
      self.pos.x,
      self.pos.y,
      self.texture.width,
      self.texture.height
    )


  def update(self, delta):
    self.pos.y -= LASER_SPEED * delta
    self.collision_rec.y -= LASER_SPEED * delta


  def draw(self):
    draw_texture_ex(self.texture, self.pos, 0.0, 1, WHITE)
