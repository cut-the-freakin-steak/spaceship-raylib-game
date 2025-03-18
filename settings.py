from pyray import *
from raylib import *
from random import randint, uniform
import os
import sys

WINDOW_WIDTH: int = 1280
WINDOW_HEIGHT: int = 720
GAME_WIDTH: int = 1920
GAME_HEIGHT: int = 1080
BG_COLOR = (15, 10, 25, 255)
PLAYER_SPEED = 600
LASER_SPEED = 800
METEOR_SPEED_RANGE = [300, 400]
METEOR_TIMER_DURATION = 0.4
FONT_SIZE = 120

font = get_font_default()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


original_load_texture = load_texture

def wrapped_load_texture(path):
    return original_load_texture(resource_path(path))


load_texture = wrapped_load_texture


original_load_sound = load_sound

def wrapped_load_sound(path):
    return original_load_sound(resource_path(path))


load_sound = wrapped_load_sound


original_load_music_stream = load_music_stream

def wrapped_load_music_stream(path):
    return original_load_music_stream(resource_path(path))


load_music_stream = wrapped_load_music_stream
