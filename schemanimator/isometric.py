import logging
import math

X_STEP = math.sqrt(3.0) / 2.0
Y_STEP = 0.5


def to_isometric(pos):
    x, y, z = pos
    s_x = (x * X_STEP) + (y * 0.0) + (z * -X_STEP)
    s_y = (x * -Y_STEP) + (y * 1.0) + (z * -Y_STEP)
    return (s_x, s_y)
