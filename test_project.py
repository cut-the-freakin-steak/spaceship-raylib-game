from project import scale_x, scale_y, state_splash_to_title


def test_scale_x() -> None:
  assert scale_x(470) == 470
  assert scale_x(240) == 240


def test_scale_y() -> None:
  assert scale_y(120) == 120
  assert scale_y(390) == 390


def test_state_splash_to_title() -> None:
  assert state_splash_to_title() == 0 
  assert state_splash_to_title() == 0
