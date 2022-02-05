import math

X_STEP = math.sqrt(3) / 2
Y_STEP = 0.5


def to_isometric(pos: tuple[int, int, int]):
    x, y, z = pos
    i_x = (x * X_STEP) + (y * 0) + (z * -X_STEP)
    i_y = (x * -Y_STEP) + (y * 1) + (z * -Y_STEP)
    return (i_x, i_y)


def to_screen(
    pos: tuple[int, int, int], screen_width: int, screen_height: int, block_size: float
):
    i_x, i_y = to_isometric(pos)
    half = block_size // 2.0

    middle_x = screen_width // 2.0 + half
    middle_y = screen_height // 2.0

    s_x = middle_x + i_x * (half)
    s_y = middle_y + i_y * (half)

    return (s_x, s_y)
