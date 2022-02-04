import schematic


class Animator:
    def __init__(self, schematic: schematic.Schematic):
        self.schematic = schematic

    def update(self, slice: int):
        blocks = []

        for w in range(self.schematic.width):
            for h in range(self.schematic.height):
                for l in range(self.schematic.length):
                    p = (w, h, l)
                    b = self.schematic.at(p, slice)
                    if b is not None:
                        b["render_pos"] = b.get("pos")
                        blocks.append(b)

        return blocks
