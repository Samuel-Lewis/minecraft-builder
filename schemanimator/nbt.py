# Source: https://minecraft.fandom.com/wiki/Block_states
DEFINING_BLOCK_STATES = [
    "age",
    "attached",
    "attachment",
    "axis",
    "berries",
    "bites",
    "bottom",
    "candles",
    "charges",
    "conditional",
    "delay",
    "disarmed",
    "down",
    "drag",
    "east",
    "eggs",
    "extended",
    "eye",
    "face",
    "facing",
    "half",
    "hanging",
    "has_book",
    "has_bottle_0",
    "has_bottle_1",
    "has_bottle_2",
    "hinge",
    "honey_level",
    "in_wall",
    "inverted",
    "layers",
    "leaves",
    "level",
    "lit",
    "locked",
    "mode",
    "moisture",
    "north",
    "open",
    "orientation",
    "part",
    "pickles",
    "powered",
    "rotation",
    "sculk_sensor_phase",
    "shape",
    "shape",
    "short",
    "signal_fire",
    "south",
    "stage",
    "thickness",
    "tilt",
    "type",
    "up",
    "vertical_direction",
    "waterlogged",
    "west",
]


def parse(nbt_name: str):
    # minecraft:hopper[facing=north,fake=true]
    #   namespace: "minecraft"
    #   name: "hopper"
    #   attrs: { "facing": "north" }
    #   id: "minecraft:hopper"
    #   nbt: "minecraft:hopper[facing=north]"

    id, attrs = nbt_name.split("[") if "[" in nbt_name else (nbt_name, "")
    namespace, name = id.split(":")
    if not attrs:
        return {
            "attrs": {},
            "file_base": name,
            "id": id,
            "name": name,
            "namespace": namespace,
            "nbt": nbt_name,
        }

    attrs = attrs[:-1]
    attrs = attrs.split(",")
    attrs = sorted(attrs)

    filtered_attrs = {}
    for attr in attrs:
        key, value = attr.split("=")
        if key in DEFINING_BLOCK_STATES:
            filtered_attrs[key] = value

    nbt = f"{namespace}:{name}"
    file_base = name
    if filtered_attrs:
        nbt += (
            f"[{','.join(f'{key}={value}' for key, value in filtered_attrs.items())}]"
        )
        file_base += "_" + "_".join(
            f"{key}-{value}" for key, value in filtered_attrs.items()
        )

    return {
        "attrs": filtered_attrs,
        "file_base": file_base,
        "id": id,
        "name": name,
        "namespace": namespace,
        "nbt": nbt,
    }
