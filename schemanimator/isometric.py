import logging
import math

X_STEP = math.sqrt(3) / 2
Y_STEP = 0.5


def to_isometric(pos):
    x, y, z = pos
    i_x = (x * X_STEP) + (y * 0) + (z * -X_STEP)
    i_y = (x * -Y_STEP) + (y * 1) + (z * -Y_STEP)
    return (i_x, i_y)


def to_screen(pos, screen_width, screen_height, block_size):
    i_x, i_y = to_isometric(pos)

    middle_x = screen_width / 2.0
    middle_y = screen_height / 2.0

    s_x = middle_x + i_x * (block_size / 2.0)
    s_y = middle_y + i_y * (block_size / 2.0)

    return (s_x, s_y)
