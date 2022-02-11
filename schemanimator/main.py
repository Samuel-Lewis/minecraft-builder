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
    logger.debug("Schematic path: {file}", file=settings.SCHEM_PATH)

    schematic = Schematic(settings.SCHEM_PATH, settings.SLICES)
    animator = Animator(schematic)
    Renderer(
        animator=animator,
        width=settings.SCREEN_WIDTH,
        height=settings.SCREEN_HEIGHT,
    )

    pyglet.app.run()


if __name__ == "__main__":
    run()
