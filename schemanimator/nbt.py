# Source: https://minecraft.fandom.com/wiki/Block_states
DEFINING_BLOCK_STATES = {
    "age": "0",
    "attached": "false",
    "attachment": "floor",
    "axis": "y",
    "berries": "false",
    "bites": "0",
    "bottom": "false",
    "candles": "1",
    "charges": "0",
    "conditional": "false",
    "delay": "1",
    "disarmed": "false",
    "down": "false",
    "drag": "true",
    "east": "false",
    "eggs": "1",
    "extended": "false",
    "eye": "false",
    "face": "wall",
    "facing": None,
    "half": None,
    "hanging": "false",
    "has_book": "false",
    "has_bottle_0": "false",
    "has_bottle_1": "false",
    "has_bottle_2": "false",
    "hinge": "left",
    "honey_level": "0",
    "in_wall": "false",
    "inverted": "false",
    "layers": "1",
    "leaves": "0",
    "level": "0",
    "lit": "false",
    "locked": "false",
    "mode": "compare",
    "moisture": "0",
    "north": "false",
    "open": "false",
    "orientation": "north_up",
    "part": "foot",
    "pickles": "1",
    "powered": "false",
    "rotation": "0",
    "sculk_sensor_phase": "cooldown",
    "shape": "north_south",
    "short": "false",
    "signal_fire": "false",
    "south": "false",
    "stage": "0",
    "thickness": "tip",
    "tilt": "none",
    "type": "normal",
    "up": "false",
    "vertical_direction": "up",
    "waterlogged": "false",
    "west": "false",
}


def parse(nbt_name: str):
    # parses nbt strings, extracting namesspace and attributes
    # only keeps attributes that are not default value and that actually cause a difference in block appearance

    # minecraft:hopper[facing=north,fake=true,waterlogged=false]
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
            default = DEFINING_BLOCK_STATES.get(key)
            if default is None or value != default:
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
