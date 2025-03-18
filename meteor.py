from settings import *


class Meteor:
  def __init__(self):
    self.texture = load_texture("images/meteor.png")
    self.destroy_sfx = load_sound("audio/explosion.wav")
    set_sound_volume(self.destroy_sfx, 0.25)
    # play_sound(self.destroy_sfx)
    self.pos = Vector2(randint(40, 1850), -84)
    self.direction = randint(-1, 1)
    self.x_update = 0
    self.y_update = 0
    self.collision_rec = Rectangle(
      self.pos.x,
      self.pos.y,
      self.texture.width,
      self.texture.height
    )


  def update(self, delta):
    self.x_update = randint(150, 250) * self.direction * delta
    self.y_update = randint(250, 350) * delta

    self.pos.x += self.x_update
    self.collision_rec.x += self.x_update

    self.pos.y += self.y_update
    self.collision_rec.y += self.y_update


  def draw(self):
    draw_texture_ex(self.texture, self.pos, 0.0, 1, WHITE)

