import math

X_STEP = math.sqrt(3) / 2
Y_STEP = 0.5


def find_extremeties(slices):
    base_pos = list(slices[0].keys())[0]
    b_x, b_y, b_z = base_pos
    min_x, max_x = b_x, b_x
    min_y, max_y = b_y, b_y
    min_z, max_z = b_z, b_z

    b_i_x, b_i_y = to_isometric(base_pos)
    min_i_x, max_i_x = b_i_x, b_i_x
    min_i_y, max_i_y = b_i_y, b_i_y

    for slice in slices:
        for p in slice:
            x, y, z = p
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            min_z = min(min_z, z)
            max_z = max(max_z, z)

            i_x, i_y = to_isometric(p)
            min_i_x = min(min_i_x, i_x)
            max_i_x = max(max_i_x, i_x)
            min_i_y = min(min_i_y, i_y)
            max_i_y = max(max_i_y, i_y)

    # Block center
    c_x = (min_x + max_x) / 2
    c_y = (min_y + max_y) / 2
    c_z = (min_z + max_z) / 2

    # Iso center
    c_i_x = (max_i_x + min_i_x) / 2
    c_i_y = (max_i_y + min_i_y) / 2

    return {
        "block": {
            "max": (max_x, max_y, max_z),
            "min": (min_x, min_y, min_z),
            "center": (c_x, c_y, c_z),
        },
        "isometric": {
            "max": (max_i_x, max_i_y),
            "min": (min_i_x, min_i_y),
            "center": (c_i_x, c_i_y),
        },
    }


def to_isometric(pos: tuple[int, int, int]):
    x, y, z = pos
    i_x = (x * X_STEP) + (y * 0) + (z * -X_STEP)
    i_y = (x * -Y_STEP) + (y * 1) + (z * -Y_STEP)
    return (i_x, i_y)


def to_screen(
    pos: tuple[int, int, int],
    width: int,
    height: int,
    block_size: float,
    pos_meta: dict,
):
    i_x, i_y = to_isometric(pos)
    middle_x, middle_y = (width // 2, height // 2)
    iso_middle_x, iso_middle_y = pos_meta["isometric"]["center"]

    half = block_size / 2.0

    x = (middle_x) + (i_x - iso_middle_x - 1) * (half)
    y = (middle_y) + (i_y - iso_middle_y - 1) * (half)

    return (x, y)
