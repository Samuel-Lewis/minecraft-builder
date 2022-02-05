from schematic import Schematic
import easing_functions as ef
import logging
import numpy as np

BUFFER_FRAMES = 30
BLOCK_FRAMES = 30
BLOCK_FRAME_OVERLAP = BLOCK_FRAMES // 2
EASE_POS = ef.QuadEaseOut(start=-1, end=0, duration=BLOCK_FRAMES)
EASE_OPACITY = ef.QuadEaseOut(start=0, end=255, duration=BLOCK_FRAMES)

LOG = logging.getLogger(__name__)


class Animator:
    def __init__(self, schematic: Schematic):
        self.schematic = schematic
        self.diffs = self.get_diffs(schematic)
        self.slice_starts = self.get_slice_starts(self.diffs)
        self.end_frame = self.slice_starts[-1]
        LOG.info("Animation length (frames): %d" % self.end_frame)

    def get_diffs(self, schematic):
        last_slice = []
        diffs = []
        for i in range(len(schematic.slices)):
            slice = schematic.slices[i]
            keys = list(slice.keys())
            diff = list(set(keys) - set(last_slice))
            diff = sorted(
                diff, key=lambda element: (element[0], element[2], element[1])
            )
            diffs.append(diff)
            last_slice = keys
        return diffs

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
            LOG.error(
                "Could not find frame %d in slice starts, %s" % frame, self.slice_starts
            )
        return inds[0] - 1

    def update(self, frame: int):
        if frame >= self.end_frame:
            LOG.debug("Animation finished")
            return ([], False)

        blocks = []
        slice = self.calc_slice(frame)
        local_frame = frame - self.slice_starts[slice]
        new_blocks = self.diffs[slice]

        for y in range(self.schematic.height):
            for z in range(self.schematic.length):
                for x in range(self.schematic.width):
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
