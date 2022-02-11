from schematic import Schematic
import easing_functions as ef
from loguru import logger
import math
import numpy as np
import settings

BUFFER_FRAMES = 60
BLOCK_FRAMES = 30
BLOCK_FRAME_OVERLAP = BLOCK_FRAMES // 2
EASE_POS = ef.QuadEaseOut(start=-1, end=0, duration=BLOCK_FRAMES)
EASE_OPACITY = ef.QuadEaseOut(start=0, end=255, duration=BLOCK_FRAMES)


class Animator:
    def __init__(self, schematic: Schematic):
        self.schematic = schematic
        self.diffs = self.get_diffs(schematic)
        self.slice_starts = self.get_slice_starts(self.diffs)
        self.end_frame = self.slice_starts[-1]
        logger.info("Animation length (frames): {frames}", frames=self.end_frame)

    def get_diffs(self, schematic):
        last_slice = []
        diffs = []
        for i in range(len(schematic.slices)):
            slice = schematic.slices[i]
            keys = list(slice.keys())
            diff = list(set(keys) - set(last_slice))
            if settings.SNAKE_ANIMATION:
                diff = self.snake_order(diff, slice)
            else:
                diff = self.flat_order(diff)
            diffs.append(diff)
            last_slice = keys
        return diffs

    def flat_order(self, diffs):
        return sorted(diffs, key=lambda p: (p[1], p[0], p[2]))

    def snake_order(self, diffs, slice):
        sorted_diffs = list(map(lambda x: slice.get(x), self.flat_order(diffs)))

        if len(sorted_diffs) <= 2:
            return list(map(lambda p: p.get("pos"), sorted_diffs))

        snake_diffs = [sorted_diffs.pop(0)]
        while len(sorted_diffs) > 1:
            latest = snake_diffs[-1]
            l_x, l_y, l_z = latest.get("pos")
            latest_type = latest.get("id")

            # get neighbours
            def dist_func(rhs):
                p_x, p_y, p_z = rhs.get("pos")
                dist = math.sqrt((p_x - l_x) ** 2 + (p_y - l_y) ** 2 + (p_z - l_z) ** 2)
                # 4 connectedness
                return dist <= 1.0

                # 8 connectedness
                # return dist <= 1.5

            neighbours = list(filter(dist_func, sorted_diffs))
            filtered_neighbours = list(
                filter(lambda p: p.get("id") == latest_type, neighbours)
            )

            query = [*filtered_neighbours, *neighbours, *sorted_diffs]
            next_block = query.pop(0)
            snake_diffs.append(next_block)
            sorted_diffs.remove(next_block)

        snake_diffs.append(sorted_diffs[-1])

        return list(map(lambda p: p.get("pos"), snake_diffs))

    def get_slice_starts(self, diffs):
        slice_starts = [0]
        for diff in diffs:
            length = BUFFER_FRAMES * 2
            length += (len(diff) - 1) * (BLOCK_FRAMES - BLOCK_FRAME_OVERLAP)
            length += BLOCK_FRAMES  # last blocks plays out completely
            length += slice_starts[-1]
            slice_starts.append(length)
        return slice_starts

    def calc_slice(self, frame: int):
        frame = np.array([frame])
        inds = np.digitize(frame, self.slice_starts)
        if len(inds) == 0:
            logger.error(
                "Could not find frame {frame} in slice_starts {slice_starts}",
                frame=frame,
                slice_starts=self.slice_starts,
            )
        return inds[0] - 1

    def update(self, frame: int):
        if frame >= self.end_frame:
            logger.debug("Animation finished")
            return ([], False)

        blocks = []
        slice = self.calc_slice(frame)
        local_frame = frame - self.slice_starts[slice]
        new_blocks = self.diffs[slice]

        for y in range(self.schematic.slice_height):
            for z in range(self.schematic.slice_length):
                for x in range(self.schematic.slice_width):
                    p = (x, y, z)
                    b = self.schematic.at(p, slice)
                    if b is None:
                        continue

                    render_pos = b.get("pos")
                    opacity = 255

                    if p in new_blocks:
                        index = new_blocks.index(p)
                        opacity = 0
                        entry_frame = (
                            (index * BLOCK_FRAMES)
                            - (index * BLOCK_FRAME_OVERLAP)
                            + BUFFER_FRAMES
                        )
                        delta = min(local_frame - entry_frame, BLOCK_FRAMES)
                        if delta < 0:
                            continue
                        opacity = EASE_OPACITY(delta)
                        e_x, e_y, e_z = render_pos
                        render_pos = (e_x, e_y - EASE_POS(delta), e_z)

                    b["render_pos"] = render_pos
                    b["opacity"] = opacity
                    blocks.append(b)

        return (blocks, True)
