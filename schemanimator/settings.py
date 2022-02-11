import argparse
from asyncio.constants import SSL_HANDSHAKE_TIMEOUT
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Convert a Minecraft schematic to an animation"
)
parser.add_argument("inputFile", type=str, nargs=1, help="The input schematic file")
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
parser.add_argument(
    "-s",
    "--slices",
    help="specify the number of slices in the schematic (default: 1)",
    nargs="?",
    default=1,
    type=int,
)
parser.add_argument(
    "-p", "--pipe", help="enable rendering to file", action="store_true"
)
parser.add_argument(
    "--snake",
    help="enable 'snake' animation, orders the entering blocks by nearest first",
    action="store_true",
)


def init():
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global SCHEM_PATH
    global SCHEM_NAME
    global DEBUG_MODE
    global SLICES
    global PIPE
    global SNAKE_ANIMATION

    args = parser.parse_args()

    SCREEN_WIDTH = args.width
    SCREEN_HEIGHT = args.height
    SCHEM_PATH = args.inputFile[0]
    SCHEM_NAME = Path(SCHEM_PATH).stem
    DEBUG_MODE = args.debug == True
    SLICES = args.slices
    PIPE = args.pipe == True
    SNAKE_ANIMATION = args.snake == True
