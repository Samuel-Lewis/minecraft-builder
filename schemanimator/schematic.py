from nbtschematic import SchematicFile
import isometric
import logging
import math

LOG = logging.getLogger(__name__)

IGNORE_LIST = [
    "minecraft:air",
    "minecraft:void_air",
    "minecraft:cave_air",
    "minecraft:barrier",
]
SLICE_BUFFER = 1


def nbt_split(nbt_name: str):
    if "[" not in nbt_name:
        return nbt_name, {}
    id, attrs = nbt_name.split("[")
    attrs = attrs[:-1]
    attrs = attrs.split(",")
    attrs = {a.split("=")[0]: a.split("=")[1] for a in attrs}
    for k in attrs:
        if attrs[k] == "true":
            attrs[k] = True
        elif attrs[k] == "false":
            attrs[k] = False
    return id, attrs


class Schematic:
    def __init__(self, in_file: str, slice_count: int):
        self.in_file = in_file
        self.slice_count = slice_count
        self.load_file()
        self.slices = []
        self.map_space()
        self.pos_meta = isometric.find_extremeties(self.slices)

    def load_file(self):
        self.sf = SchematicFile.load(self.in_file).get("Schematic")
        LOG.info("Loaded schematic file %s", self.in_file)
        LOG.info(
            "Dimensions %dw x %dh x %dl",
            self.sf.get("Width"),
            self.sf.get("Height"),
            self.sf.get("Length"),
        )
        LOG.debug("Properties: %s", self.sf.keys())
        self.palette = {value: key for (key, value) in self.sf.get("Palette").items()}

    def get_block_global(self, pos: tuple[int, int, int]):
        c = self.global_cord_to_index(pos)
        if c > self.sf.get("Length") * self.sf.get("Width") * self.sf.get("Height"):
            LOG.error("Position [%s] out of bounds (index %d)", pos, c)
            return None
        return self.palette.get(self.sf.get("BlockData")[c])

    def at(self, pos: tuple[int, int, int], slice=0):
        return self.slices[slice].get(pos)

    def get_slice_pos(self, pos: tuple[int, int, int]):
        x, y, z = pos
        slice_index = x // self.width
        s_x = x - (slice_index * self.width)
        return (slice_index, (s_x, y, z))

    def global_cord_to_index(self, pos: tuple[int, int, int]):
        x, y, z = pos
        return (x + self.sf.get("Width") * z) + (
            self.sf.get("Width") * self.sf.get("Length") * y
        )

    def should_include(self, id: str):
        return id not in IGNORE_LIST

    def map_space(self):
        LOG.debug("Mapping schematic space")
        self.slices = [{} for _ in range(self.slice_count)]

        global map_count
        map_count = 0

        def write(global_pos: tuple[int, int, int], nbt_name: str, passed_attrs={}):
            global map_count
            slice_index, pos = self.get_slice_pos(global_pos)

            id, id_attrs = nbt_split(nbt_name)
            attrs = {**id_attrs, **passed_attrs}
            if self.should_include(id):
                print(id, attrs, pos, slice_index)
                if pos in self.slices[slice_index]:
                    LOG.warn(
                        "Duplicate mapping at %s. %s"
                        % (
                            global_pos,
                            {
                                "pos": pos,
                                "slice": slice_index,
                                "new_nbt": nbt_name,
                                "existing": self.slices[slice_index][pos].get("id"),
                            },
                        )
                    )
                    old_attrs = self.slices[slice_index][pos].get("attrs")
                    self.slices[slice_index][pos]["attrs"] = {**old_attrs, **attrs}
                else:
                    map_count += 1
                    self.slices[slice_index][pos] = {
                        "id": id,
                        "nbt": nbt_name,
                        "attrs": attrs,
                        "pos": pos,
                        "global_pos": global_pos,
                        "slice": slice_index,
                    }

        LOG.debug("Mapping blocks")
        for x in range(self.global_width):
            for y in range(self.global_height):
                for z in range(self.global_length):
                    p = (x, y, z)
                    write(p, self.get_block_global(p))

        ### DISABLED until can figure out an entity layer or reduced conflicts
        # if "Entities" in self.sf:
        #     LOG.debug("Mapping entities")
        #     offset_x, offset_y, offset_z = self.sf.get("Offset")
        #     for e in self.sf.get("Entities"):
        #         nbt_name = str(e.get("Id"))
        #         x = math.floor(e.get("Pos")[0]) - offset_x
        #         y = math.floor(e.get("Pos")[1]) - offset_y
        #         z = math.floor(e.get("Pos")[2]) - offset_z
        #         write((x, y, z), nbt_name)

        LOG.info("Mapped %d positions, across %d slices", map_count, len(self.slices))

    @property
    def global_width(self):
        return self.sf.get("Width")

    @property
    def global_height(self):
        return self.sf.get("Height")

    @property
    def global_length(self):
        return self.sf.get("Length")

    @property
    def width(self):
        return self.global_width // self.slice_count

    @property
    def height(self):
        return self.global_height

    @property
    def length(self):
        return self.global_length
