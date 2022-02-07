from animator import Animator
from loguru import logger
from pathlib import Path
import isometric
import loader
import pyglet
import settings


class Renderer(pyglet.window.Window):
    def __init__(
        self,
        animator: Animator,
        width: int,
        height: int,
    ):
        super(Renderer, self).__init__(
            width=width,
            height=height,
            vsync=False,
        )
        pyglet.clock.schedule_interval(self.update, 1.0 / 128.0)
        self.clear()
        self.activate()
        self.display_content = []
        self.animator = animator
        self.frame = 0
        self.paused = False
        self.loader = loader.ImageLoader()
        if settings.PIPE:
            Path(f"./frames/{settings.OUTPUT_FILE_NAME}").mkdir(
                parents=True, exist_ok=True
            )

    def update(self, _):
        if self.paused:
            return

        self.display_content, self.continue_anim = self.animator.update(self.frame)
        self.frame += 1

    def on_draw(self):
        if self.paused:
            return
        self.clear()

        if not self.continue_anim:
            self.stop()
            return

        pos_meta = self.animator.schematic.pos_meta
        b_horz = pos_meta["isometric"]["max"][0] - pos_meta["isometric"]["min"][0]
        b_vert = pos_meta["isometric"]["max"][1] - pos_meta["isometric"]["min"][1]
        block_size = min(self.width / b_horz, self.height / b_vert)

        for b in self.display_content:
            im = self.loader.get_image(b)
            sp = pyglet.sprite.Sprite(im)
            p = b.get("render_pos")
            opacity = b.get("opacity")
            xi, yi = isometric.to_screen(
                pos=p,
                width=self.width,
                height=self.height,
                block_size=block_size,
                pos_meta=pos_meta,
            )
            scale = block_size / im.width
            sp.update(x=xi, y=yi, scale_x=scale, scale_y=scale)
            sp.opacity = opacity
            sp.draw()

        if settings.PIPE:
            self.pipe()

        # Everything after buffer save is not rendered to png outputs
        if settings.DEBUG_MODE:
            self.debug_draw()

    def debug_draw(self):
        batch = pyglet.graphics.Batch()

        fps = int(pyglet.clock.get_fps())
        debug_text = f"""
        input file: {settings.SCHEM_NAME_SHORT}
        output file: {settings.OUTPUT_FILE_NAME}
        ---
        frame: {self.frame}
        fps: {fps}
        """
        debug_label = pyglet.text.Label(
            debug_text,
            font_name="Arial",
            font_size=12,
            anchor_y="top",
            x=10,
            y=self.height - 10,
            width=self.width - 20,
            multiline=True,
            batch=batch,
        )
        debug_label.draw()

        origin = pyglet.shapes.Arc(
            self.width // 2.0, self.height // 2.0, 5, color=(100, 0, 0), batch=batch
        )
        origin.opacity = 255 // 4.0
        origin.draw()
        vert = pyglet.shapes.Line(
            self.width // 2.0, 0, self.width // 2.0, self.height, batch=batch
        )
        vert.opacity = 255 // 4
        vert.draw()
        horz = pyglet.shapes.Line(
            0, self.height // 2.0, self.width, self.height // 2.0, batch=batch
        )
        horz.opacity = 255 // 4
        horz.draw()

    def pipe(self):
        file_num = str(self.frame).zfill(5)
        filename = f"{settings.OUTPUT_FILE_NAME}_{file_num}.png"
        pyglet.image.get_buffer_manager().get_color_buffer().save(
            Path(f"./frames/{filename}")
        )

    def on_key_press(self, symbol, modifiers):
        logger.debug(
            "Key pressed: {symbol} {modifiers}", symbol=symbol, modifiers=modifiers
        )
        if symbol == pyglet.window.key.ESCAPE:
            self.stop()
        if symbol == pyglet.window.key.SPACE:
            self.paused = not self.paused
            logger.debug("Paused: {paused}", paused=self.paused)

    def stop(self):
        logger.debug("Stopping...")
        logger.complete()
        pyglet.app.exit()
