from settings import *


class Sprite2D:
    def __init__(self, texture: Texture, pos: Vector2 = Vector2(0, 0), direction: Vector2 = Vector2(0, 0), speed: int = 0):
        self.texture = texture
        self.pos = pos
        self.direction = direction
        self.speed = speed


    def update(self, delta):
        self.pos.x += self.speed * self.direction.x * delta
        self.pos.y += self.speed * self.direction.y * delta


    def draw(self):
        draw_texture_v(self.texture, self.pos, WHITE)


class AnimatedSprite2D(Sprite2D):
    def __init__(self, texture: Texture, anim_frames: list, anim_index: int, anim_speed: int = 1, pos: Vector2 = Vector2(0, 0), direction: Vector2 = Vector2(0, 0), speed: int = 0):
        super().__init__(texture, pos, direction, speed)
        self.anim_frames = anim_frames
        self.anim_index = anim_index
        self.anim_speed = anim_speed


    def update(self, delta):
        self.pos.x += self.speed * self.direction.x * delta
        self.pos.y += self.speed * self.direction.y * delta
        self.anim_index += self.anim_speed * delta


    def draw(self):
        draw_texture_v(self.anim_frames[int(self.anim_index) % len(self.anim_frames)], self.pos, WHITE)

