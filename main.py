# #!/usr/bin/python3

from nbtschematic import SchematicFile
import logging
import argparse
import pyglet
import ffmpeg

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
IN_SHORT_NAME = args.inputFile[0].split("/")[-1].split(".")[0]
OUT_FULL_NAME = args.outputFile[0] if args.outputFile else IN_SHORT_NAME + ".mp4"
OUT_SHORT_NAME = OUT_FULL_NAME.split("/")[-1].split(".")[0]
DEBUG_MODE = args.debug == True

log_level = logging.INFO
if DEBUG_MODE:
    log_level = logging.DEBUG

logging.basicConfig(level=log_level, format="[%(asctime)s][%(levelname)s] %(message)s")
logging.debug("Log level: %s", log_level)
logging.debug("Input file: %s", args.inputFile[0])
logging.debug("Output file: %s", OUT_FULL_NAME)

sf = SchematicFile.load(args.inputFile[0]).get("Schematic")

logging.info("Loaded schematic file %s", args.inputFile[0])
logging.info(
    "Dimensions %dw x %dh x %dl", sf.get("Width"), sf.get("Height"), sf.get("Length")
)

logging.debug("Properties: %s", sf.keys())
for k in sf.keys():
    logging.debug("%s: %s", k, sf.get(k))

flippedPalette = {value: key for (key, value) in sf.get("Palette").items()}
schem = list(map(lambda x: flippedPalette[x], sf.get("BlockData")))

frame = 100
window = pyglet.window.Window(width=OUTPUT_WIDTH, height=OUTPUT_HEIGHT)
window.set_caption("Minecraft Schematic to Animation | %s " % IN_SHORT_NAME)
fps_display = pyglet.window.FPSDisplay(window)

furnace_image = pyglet.resource.image("assets/furnace.png")
furnace_sprite = pyglet.sprite.Sprite(furnace_image, x=50, y=50)

process2 = (
    ffmpeg.input(
        "pipe:",
        format="rawvideo",
        pix_fmt="rgb24",
        s="{}x{}".format(OUTPUT_WIDTH, OUTPUT_HEIGHT),
        r=60,
    )
    .vflip()
    .output("test.mp4", pix_fmt="yuv420p", loglevel="quiet", r=60)
    .overwrite_output()
    .run_async(pipe_stdin=True)
)


def update(_):
    global frame
    frame += 1


pyglet.clock.schedule_interval(update, 1 / 60.0)


@window.event
def on_draw():
    window.clear()
    furnace_sprite.opacity = frame
    furnace_sprite.draw()
    texture = (
        pyglet.image.get_buffer_manager()
        .get_color_buffer()
        .get_texture()
        .get_image_data()
    )
    format = "RGBA"
    pitch = texture.width * len(format)
    pixels = texture.get_data(format, pitch)
    process2.stdin.write(pixels)

    # Everything after buffer save is not rendered to png outputs
    debug_text = """
  input file: {inputFile}
  output file: {outputFile}
  ---
  frame: {frame}
  fps: {fps}
  """.format(
        frame=frame,
        fps=fps_display.label.text,
        inputFile=IN_SHORT_NAME,
        outputFile=OUT_FULL_NAME,
    )
    debug_label = pyglet.text.Label(
        debug_text,
        font_name="Arial",
        font_size=12,
        anchor_y="top",
        x=10,
        y=OUTPUT_HEIGHT - 10,
        width=OUTPUT_WIDTH - 20,
        multiline=True,
    )
    debug_label.draw()

    if frame == 255:
        process2.stdin.close()
        process2.wait()
        pyglet.app.exit()


pyglet.app.run()
