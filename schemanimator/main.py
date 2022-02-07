# #!/usr/bin/python3

from animator import Animator
from loguru import logger
from renderer import Renderer
from schematic import Schematic
import pyglet
import settings


@logger.catch
def run():
    settings.init()

    logger.debug("Debug mode: {mode}", mode=settings.DEBUG_MODE)
    logger.debug("Input file: {file}", file=settings.SCHEM_NAME)
    logger.debug("Output file: {file}", file=settings.OUTPUT_FILE_NAME)

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
