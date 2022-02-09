from loguru import logger
from nbtschematic import SchematicFile
import isometric
import nbt

IGNORE_LIST = [
    "minecraft:air",
    "minecraft:void_air",
    "minecraft:cave_air",
    "minecraft:barrier",
]
SLICE_BUFFER = 1


class Schematic:
    def __init__(self, in_file: str, slice_count: int):
        self.in_file = in_file
        self.slice_count = slice_count
        self.slices = [{} for _ in range(self.slice_count)]
        self.load_file()
        self.map_space()
        self.pos_meta = isometric.find_extremeties(self.slices)

    def load_file(self):
        self.sf = SchematicFile.load(self.in_file).get("Schematic")
        logger.info("Loaded schematic file %s" % self.in_file)
        logger.info(
            "Dimensions {width}w x {height}h x {length}l",
            width=int(self.sf.get("Width")),
            height=int(self.sf.get("Height")),
            length=int(self.sf.get("Length")),
        )
        logger.trace("Properties: {keys}", keys=self.sf.keys())
        self.palette = {value: key for (key, value) in self.sf.get("Palette").items()}

    def get_block_global(self, pos: tuple[int, int, int]):
        c = self.global_cord_to_index(pos)
        if c > self.sf.get("Length") * self.sf.get("Width") * self.sf.get("Height"):
            logger.error(
                "Position {pos} out of bounds (index {index})", pos=pos, index=c
            )
            return None
        return self.palette.get(self.sf.get("BlockData")[c])

    def at(self, pos: tuple[int, int, int], slice=0):
        return self.slices[slice].get(pos)

    def global_cord_to_index(self, pos: tuple[int, int, int]):
        x, y, z = pos
        return (x + self.sf.get("Width") * z) + (
            self.sf.get("Width") * self.sf.get("Length") * y
        )

    def should_include(self, id: str):
        return id not in IGNORE_LIST

    def global_to_slice(self, global_pos: tuple[int, int, int]):
        x, y, z = global_pos

        slice_index = x // (self.slice_width + SLICE_BUFFER)
        x = x - (slice_index * (self.slice_width + SLICE_BUFFER)) - SLICE_BUFFER
        y -= SLICE_BUFFER
        z -= SLICE_BUFFER
        return (slice_index, (x, y, z))

    def map_space(self):
        logger.debug("Mapping schematic space")

        global map_count
        map_count = 0

        def write(global_pos: tuple[int, int, int], nbt_name: str):
            global map_count
            nbt_data = nbt.parse(nbt_name)
            slice_index, pos = self.global_to_slice(global_pos)

            if not self.should_include(nbt_data.get("id")):
                return

            if pos in self.slices[slice_index]:
                logger.warning(
                    "Skipping duplicate mapping at {global_pos}. {meta}",
                    global_pos=global_pos,
                    meta={
                        "pos": pos,
                        "slice": slice_index,
                        "new_nbt": nbt_data.get("nbt"),
                        "existing": self.slices[slice_index][pos]
                        .get("nbt_data")
                        .get("nbt"),
                    },
                )
            else:
                map_count += 1
                self.slices[slice_index][pos] = {
                    "nbt_data": nbt_data,
                    "pos": pos,
                    "global_pos": global_pos,
                    "slice": slice_index,
                }

        logger.debug("Mapping blocks")

        for g_y in range(self.global_height - SLICE_BUFFER):
            y = g_y + SLICE_BUFFER
            for g_z in range(self.global_length - (SLICE_BUFFER * 2)):
                z = g_z + SLICE_BUFFER
                for s in range(self.slice_count):
                    for g_x in range(self.slice_width):
                        x = (s * (self.slice_width + SLICE_BUFFER)) + g_x + SLICE_BUFFER
                        p = (x, y, z)
                        write(p, self.get_block_global(p))

        ### DISABLED until can figure out an entity layer or reduced conflicts
        # if "Entities" in self.sf:
        #     logger.debug("Mapping entities")
        #     offset_x, offset_y, offset_z = self.sf.get("Offset")
        #     for e in self.sf.get("Entities"):
        #         nbt_name = str(e.get("Id"))
        #         x = math.floor(e.get("Pos")[0]) - offset_x
        #         y = math.floor(e.get("Pos")[1]) - offset_y
        #         z = math.floor(e.get("Pos")[2]) - offset_z
        #         write((x, y, z), nbt_name)

        logger.info(
            "Mapped {map_count} positions, across {slices} slices",
            map_count=map_count,
            slices=len(self.slices),
        )

    @property
    def global_width(self):
        return self.sf.get("Width")

    @property
    def global_height(self):
        return self.sf.get("Height")

    @property
    def global_length(self):
        return self.sf.get("Length")

    # slice heights
    @property
    def slice_width(self):
        border = (self.slice_count + 1) * SLICE_BUFFER
        return (self.global_width - border) // self.slice_count

    @property
    def slice_height(self):
        # top buffer only
        return self.global_height - SLICE_BUFFER

    @property
    def slice_length(self):
        # back and front buffer
        return self.global_length - (SLICE_BUFFER * 2)
