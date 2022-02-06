# #!/usr/bin/python3

from animator import Animator
from renderer import Renderer
from schematic import Schematic
import logging
import pyglet
import settings


def run():
    settings.init()

    log_level = logging.INFO
    if settings.DEBUG_MODE:
        log_level = logging.DEBUG

    logging.basicConfig(
        level=log_level, format="[%(asctime)s][%(levelname)s][%(name)s] %(message)s"
    )
    logging.debug("Log level: %s", log_level)
    logging.debug("Input file: %s", settings.SCHEM_NAME)
    logging.debug("Output file: %s", settings.OUTPUT_FILE_NAME)

    schematic = Schematic(settings.SCHEM_NAME, settings.SLICES)
    animator = Animator(schematic)
    Renderer(
        animator=animator,
        width=settings.SCREEN_WIDTH,
        height=settings.SCREEN_HEIGHT,
    )

    pyglet.app.run()


if __name__ == "__main__":
    run()
