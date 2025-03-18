#!/usr/bin/env python3

from custom_timer import Timer
from settings import *
from ship import Ship
from menu_stuff import Button
from stars import Star
from laser import Laser
from meteor import Meteor


# state and window setup
game_state = {
  "splash_screen": True,
  "title_screen": False,
  "title_settings": False,
  "gameplay": False,
  "game_over": False,
}

set_config_flags(FLAG_WINDOW_RESIZABLE)
init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Galaga Lookin Ahh")
set_window_min_size(256, 144)
set_exit_key(KEY_NULL)

target = load_render_texture(GAME_WIDTH, GAME_HEIGHT)
set_texture_filter(target.texture, TEXTURE_FILTER_BILINEAR)

screen_camera = Camera2D()
screen_camera.offset = Vector2(GAME_WIDTH / 2, GAME_HEIGHT / 2)
screen_camera.target = Vector2(GAME_WIDTH / 2, GAME_HEIGHT / 2)
screen_camera.zoom = 1

res_scale = 1

if GAME_HEIGHT == 144:
  res_scale = 7.5

if GAME_HEIGHT == 240:
  res_scale = 4.5

if GAME_HEIGHT == 360:
  res_scale = 3

if GAME_HEIGHT == 480:
  res_scale = 2.25

if GAME_HEIGHT == 720:
  res_scale = 1.5

if GAME_HEIGHT == 1080:
  res_scale = 1

screen_camera.zoom /= res_scale

# audio imports
init_audio_device()
set_master_volume(0.4)
title_theme = load_music_stream("audio/sea_shanty_2.mp3")

can_fire_laser = True

def main() -> None:
  # game declarations
  font = get_font_default()

  splash_screen_timer = Timer(4, False, True, state_splash_to_title)
  splash_alpha_in = 0
  splash_alpha_out = 255
  splash_eoo_out = 0

  global ship
  ship = Ship(Vector2(0, 0), Vector2(0, 0), PLAYER_SPEED)
  ship.pos = Vector2(
    (GAME_WIDTH / 2) - (ship.texture.width / 2),
    (GAME_HEIGHT / 2) - (ship.texture.height / 2),
  )

  global score
  score = 0

  stars = {Star() for i in range(25)}

  lasers = []
  laser_shot_timer = Timer(0.45, False, False, on_laser_shot_timer_timeout)
  global can_fire_laser
  can_fire_laser = True

  global meteors
  meteors = []
  meteor_timer = Timer(METEOR_TIMER_DURATION, True, True, on_meteor_timer_timeout)

  while not window_should_close():
    # UPDATES
    delta = get_frame_time()

    # window and mouse stuff
    scale = min(get_screen_width() / GAME_WIDTH, get_screen_height() / GAME_HEIGHT)

    # get the actual, real mouse position
    actual_mouse = get_mouse_position()

    # transform the mouse position to game space
    mouse = Vector2(0, 0)
    mouse.x = (actual_mouse.x - (get_screen_width() - (GAME_WIDTH * scale)) * 0.5) / scale
    mouse.y = (actual_mouse.y - (get_screen_height() - (GAME_HEIGHT * scale)) * 0.5) / scale

    # adjust for camera zoom and offset
    mouse.x = (mouse.x - screen_camera.offset.x) / screen_camera.zoom + screen_camera.offset.x
    mouse.y = (mouse.y - screen_camera.offset.y) / screen_camera.zoom + screen_camera.offset.y

    # DRAWING
    # actual drawing
    begin_texture_mode(target)
    clear_background(BG_COLOR)
    begin_mode_2d(screen_camera)

    if game_state["gameplay"]:
      update_music_stream(title_theme)

      if is_key_pressed(KEY_ESCAPE):
        state_gameplay_to_title()

      # gameplay updates
      ship.update(delta)

      for star in stars:
        star.draw()

      meteor_timer.update()
      for meteor in meteors:
        if meteor.pos.y >= 2000:
          meteors.remove(meteor)

        if check_collision_recs(ship.collision_rec, meteor.collision_rec):
          state_gameplay_to_game_over()

        meteor.update(delta)
        meteor.draw()

      # gameplay drawing      
      laser_shot_timer.update()
      if is_key_pressed(KEY_Z):
        if can_fire_laser:
          lasers.append(Laser(ship.pos))
          laser_shot_timer.activate()
          can_fire_laser = False

      for laser in lasers:
        for meteor in meteors:
          if check_collision_recs(laser.collision_rec, meteor.collision_rec):
            lasers.remove(laser)
            meteors.remove(meteor)
            score += 1

        if laser.pos.y <= -200:
          lasers.remove(laser)

        laser.update(delta)
        laser.draw()

      ship.draw()

      # draw score text last so everything is under it in-game
      score_text_dimensions = measure_text_ex(font, str(score), 100, 7.0)
      draw_text_ex(
        font,
        str(score),
        Vector2(
          int((GAME_WIDTH / 2) - (score_text_dimensions.x / 2)),
          scale_y(70)
        ),
        100,
        7.0,
        RAYWHITE
      )


    elif game_state["game_over"]:
      update_music_stream(title_theme)
      title_text_dimensions = measure_text_ex(font, "whoopsie daisy, you die", 100, 7.0)

      # draw death text
      draw_text_ex(
        font,
        "whoopsie daisy, you die",
        Vector2(
          int((GAME_WIDTH / 2) - (title_text_dimensions.x / 2)),
          scale_y(245)
        ),
        100,
        7.0,
        WHITE
      )

      button_dimensions = Vector2(500, 150)
      play_button = Button(
        int((GAME_WIDTH / 2) - (button_dimensions.x / 2)),
        scale_y(465),
        title_button_dimensions.x,
        title_button_dimensions.y,
        True,
      )

      button_alpha = 255

      # if the mouse is hovering over the button, make it more transparent
      if check_collision_point_rec(mouse, play_button.button):
        button_alpha = 175
        if is_mouse_button_pressed(0):
          state_game_over_to_gameplay()

      text_dimensions = measure_text_ex(font, "try again", 75, 7)
      play_button.draw(Color(245, 245, 245, button_alpha), font, 75, "try again", text_dimensions)


    elif game_state["title_screen"]:
      update_music_stream(title_theme)
      title_text_dimensions = measure_text_ex(font, "i dont even know yet", 100, 7.0)

      # draw title text
      draw_text_ex(
        font,
        "i dont even know yet",
        Vector2(
          int((GAME_WIDTH / 2) - (title_text_dimensions.x / 2)),
          scale_y(245)
        ),
        100,
        7.0,
        WHITE
      )

      # BUTTONS
      # play button
      title_button_dimensions = Vector2(500, 150)
      play_button = Button(
        int((GAME_WIDTH / 2) - (title_button_dimensions.x / 2)),
        scale_y(465),
        title_button_dimensions.x,
        title_button_dimensions.y,
        True,
      )

      play_button_alpha = 255

      # if the mouse is hovering over the button, make it more transparent
      if check_collision_point_rec(mouse, play_button.button):
        play_button_alpha = 175
        if is_mouse_button_pressed(0):
          state_title_to_gameplay()

      play_text_dimensions = measure_text_ex(font, "play", 75, 7)
      play_button.draw(Color(245, 245, 245, play_button_alpha), font, 75, "play", play_text_dimensions)

      settings_button = Button(
        int((GAME_WIDTH / 2) - (title_button_dimensions.x / 2)),
        scale_y(685),
        title_button_dimensions.x,
        title_button_dimensions.y,
        True
      )

      settings_button_alpha = 255

      # if the mouse is hovering over the button, make it more transparent
      if check_collision_point_rec(mouse, settings_button.button):
        settings_button_alpha = 175
        if is_mouse_button_pressed(0):
          state_title_to_settings()

      settings_text_dimensions = measure_text_ex(font, "settings", 75, 7)
      settings_button.draw(
        Color(245, 245, 245, settings_button_alpha),
        font,
        75,
        "settings",
        settings_text_dimensions
      )


    elif game_state["title_settings"]:
      update_music_stream(title_theme)

      if is_key_pressed(KEY_ESCAPE):
        state_settings_to_title()

      settings_text_dimensions = measure_text_ex(font, "there's nothing here lol i gave up", 100, 7.0)

      # draw settings text
      draw_text_ex(
        font,
        "there's nothing here lol i gave up",
        Vector2(
          int((GAME_WIDTH / 2) - (settings_text_dimensions.x / 2)),
          scale_y(245)
        ),
        100,
        7.0,
        WHITE
      )

    elif game_state["splash_screen"]:
      text_dimensions = measure_text_ex(font, "splash screen oooo", 80, 7.0)
      if is_key_pressed(KEY_ENTER):
        state_splash_to_title()

      if get_time() - splash_screen_timer.start_time <= 2:
        draw_text_ex(
          font,
          "splash screen oooo",
          Vector2(int((GAME_WIDTH / 2) - (text_dimensions.x / 2)),
                  scale_y(400)),
          80,
          7.0,
          Color(245, 245, 245, splash_alpha_in)
        )

        if splash_alpha_in < 255:
          splash_alpha_in += 1

      else:
        if splash_eoo_out % 2 == 0:
          if splash_alpha_out > 0:
            splash_alpha_out -= 1

        splash_eoo_out += 1

        draw_text_ex(
          font,
          "splash screen oooo",
          Vector2(int((GAME_WIDTH / 2) - (text_dimensions.x / 2)),
                  scale_y(400)),
          80,
          7.0,
          Color(245, 245, 245, splash_alpha_out)
        )

        splash_screen_timer.update()

    end_mode_2d()
    end_texture_mode()

      # drawing the "texture" which we use for our resolution window
    begin_drawing()
    clear_background(BLACK)

    draw_texture_pro(
      target.texture,
      Rectangle(0, 0, target.texture.width, -target.texture.height),
      Rectangle(
        (get_screen_width() - (GAME_WIDTH * scale)) * 0.5,
        (get_screen_height() - (GAME_HEIGHT * scale)) * 0.5,
        GAME_WIDTH * scale,
        GAME_HEIGHT * scale,
      ),
      Vector2(0, 0),
      0,
      WHITE,
    )

    end_drawing()

  # unload the texture we were using for the resolution window
  unload_render_texture(target)
  # unload the music stream that plays our title music
  unload_music_stream(title_theme)
  close_window()


def on_laser_shot_timer_timeout() -> None:
  global can_fire_laser
  can_fire_laser = True


def on_meteor_timer_timeout() -> None:
  meteors.append(Meteor())


def scale_x(x) -> int:
  """Scales an X position from the original (1080p) resolution to the game resolution."""
  return int(((x * GAME_WIDTH / 1920) - screen_camera.offset.x) / screen_camera.zoom + screen_camera.offset.x)



def scale_y(y) -> int:
  """Scales a Y position from the original (1080p) resolution to the game resolution."""
  return int(((y * GAME_HEIGHT / 1080) - screen_camera.offset.y) / screen_camera.zoom + screen_camera.offset.y)


# state transition functions
def state_splash_to_title() -> None:
  game_state["splash_screen"] = False
  game_state["title_screen"] = True
  play_music_stream(title_theme)


def state_title_to_settings() -> None:
  game_state["title_screen"] = False
  game_state["title_settings"] = True


def state_settings_to_title() -> None:
  game_state["title_settings"] = False
  game_state["title_screen"] = True


def state_title_to_gameplay() -> None:
  game_state["title_screen"] = False
  game_state["gameplay"] = True


def state_gameplay_to_title() -> None:
  game_state["gameplay"] = False
  game_state["title_screen"] = True


def state_gameplay_to_game_over() -> None:
  game_state["gameplay"] = False
  game_state["game_over"] = True


def state_game_over_to_gameplay() -> None:
  game_state["game_over"] = False
  game_state["gameplay"] = True
  ship.pos = Vector2(
    (GAME_WIDTH / 2) - (ship.texture.width / 2),
    (GAME_HEIGHT / 2) - (ship.texture.height / 2),
  )
  meteors.clear()
  global score
  score = 0


if __name__ == "__main__":
  main()
