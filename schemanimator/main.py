# #!/usr/bin/python3

import schematic
import logging
import argparse
import loader
import pyglet
import math
import renderer
from isometric import to_isometric, X_STEP, Y_STEP

parser = argparse.ArgumentParser(
    description="Convert a Minecraft schematic to an animation"
)
parser.add_argument("inputFile", type=str, nargs=1, help="The input schematic file")
parser.add_argument("outputFile", type=str, nargs="?", help="The output animation file")
parser.add_argument("-d", "--debug", help="enable debug mode", action="store_true")
parser.add_argument(
    "--width",
    type=int,
    nargs="?",
    default=720,
    help="output video width (default: 720)",
)
parser.add_argument(
    "--height",
    type=int,
    nargs="?",
    default=480,
    help="output video height (default: 480)",
)

args = parser.parse_args()
OUTPUT_WIDTH = args.width
OUTPUT_HEIGHT = args.height
IN_FULL_NAME = args.inputFile[0]
IN_SHORT_NAME = IN_FULL_NAME.split("/")[-1].split(".")[0]
OUT_FULL_NAME = args.outputFile[0] if args.outputFile else IN_SHORT_NAME + ".mp4"
OUT_SHORT_NAME = OUT_FULL_NAME.split("/")[-1].split(".")[0]
DEBUG_MODE = args.debug == True

log_level = logging.INFO
if DEBUG_MODE:
    log_level = logging.DEBUG

logging.basicConfig(level=log_level, format="[%(asctime)s][%(levelname)s] %(message)s")
logging.debug("Log level: %s", log_level)
logging.debug("Input file: %s", IN_FULL_NAME)
logging.debug("Output file: %s", OUT_FULL_NAME)


def run():
    ren = renderer.Renderer(OUTPUT_WIDTH, OUTPUT_HEIGHT, IN_FULL_NAME, OUT_FULL_NAME)
    schem = schematic.Schematic(IN_FULL_NAME)
    width = schem.global_width
    height = schem.global_height

    image_loader = loader.ImageLoader()
    batch = pyglet.graphics.Batch()
    sprites = []

    blocks_across = int(OUTPUT_WIDTH / width)

    for w in range(width):
        for h in range(height):
            for l in range(2):
                p = (w, h, l)
                b = schem.at(p)

                if b is None:
                    continue
                im = image_loader.get_image(b)

                sp = pyglet.sprite.Sprite(im, batch=batch)
                xi, yi = to_isometric(p)
                scale = 1.0
                sp.update(
                    x=xi * 30.0,
                    y=yi * 30.0,
                    scale_x=30 / im.width,
                    scale_y=30 / im.width,
                )
                sprites.append(sp)

    ren.queue([batch])
    pyglet.app.run()


if __name__ == "__main__":
    run()
