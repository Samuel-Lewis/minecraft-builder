from nbtschematic import SchematicFile
import logging

IGNORE_LIST = [
    "minecraft:air",
    "minecraft:void_air",
    "minecraft:cave_air",
    "minecraft:barrier",
]


def str_to_id(name: str):
    if "[" not in name:
        return name, {}
    id, attrs = name.split("[")
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
    def __init__(self, in_file):
        self.in_file = in_file
        self.space = None
        self.load_file()

    def load_file(self):
        self.sf = SchematicFile.load(self.in_file).get("Schematic")
        logging.info("Loaded schematic file %s", self.in_file)
        logging.info(
            "Dimensions %dw x %dh x %dl",
            self.sf.get("Width"),
            self.sf.get("Height"),
            self.sf.get("Length"),
        )
        logging.debug("Properties: %s", self.sf.keys())
        # for k in sf.keys():
        #   logging.debug("%s: %s", k, sf.get(k))

        self.palette = {value: key for (key, value) in self.sf.get("Palette").items()}

    def get_block(self, pos):
        c = self.cord_to_index(pos)
        if c > self.sf.get("Length") * self.sf.get("Width") * self.sf.get("Height"):
            logging.error("Position [%s] out of bounds (index %d)", pos, c)
            return None
        return self.palette.get(self.sf.get("BlockData")[c])

    def cord_to_index(self, pos):
        x, y, z = pos
        return (x + self.sf.get("Width") * z) + (
            self.sf.get("Width") * self.sf.get("Length") * y
        )

    def should_include(self, id):
        return id not in IGNORE_LIST

    def map_space(self):
        logging.debug("Mapping schematic space")
        self.space = {}

        def write(pos, block, passed_attrs={}):
            id, id_attrs = str_to_id(block)
            attrs = {**id_attrs, **passed_attrs}
            if self.should_include(id):
                if p in self.space:
                    old_attrs = self.space[p].get("attrs")
                    self.space[p]["attrs"] = {**old_attrs, **attrs}
                else:
                    self.space[p] = {"id": id, "attrs": attrs, "pos": pos}

        logging.debug("Mapping blocks")
        for x in range(self.global_width):
            for y in range(self.global_height):
                for z in range(self.global_length):
                    p = (x, y, z)
                    write(p, self.get_block(p))

        if "TileEntities" in self.sf:
            logging.critical("No handler for TileEntities")
            for te in self.sf.get("TileEntities"):
                # todo
                pass

        if "BlockEntities" in self.sf:
            logging.debug("Mapping block entities")
            for be in self.sf.get("BlockEntities"):
                p = (
                    int(be.get("Pos")[0]),
                    int(be.get("Pos")[1]),
                    int(be.get("Pos")[2]),
                )
                id = str(be.get("Id"))
                write(p, id, be)
        logging.info("Mapped %d blocks", len(self.space))

    def at(self, pos):
        if self.space is None:
            self.map_space()

        if pos in self.space:
            return self.space[pos]
        return None

    @property
    def global_width(self):
        return self.sf.get("Width")

    @property
    def global_height(self):
        return self.sf.get("Height")

    @property
    def global_length(self):
        return self.sf.get("Length")
