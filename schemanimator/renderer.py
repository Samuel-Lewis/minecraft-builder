import logging
import pyglet
import animator
import isometric
import loader


class Renderer(pyglet.window.Window):
    def __init__(
        self,
        animator: animator.Animator,
        width: int,
        height: int,
        inputFile: str,
        outputFile: str,
        do_pipe: bool,
    ):
        super(Renderer, self).__init__(width=width, height=height, vsync=False)
        pyglet.clock.schedule_interval(self.update, 1.0 / 128.0)
        self.clear()
        self.activate()
        self.display_content = []
        self.animator = animator
        self.frame = 0
        self.paused = False
        self.loader = loader.ImageLoader()
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.do_pipe = do_pipe

    def update(self, _):
        if self.paused:
            return

        self.display_content, self.continue_anim = self.animator.update(self.frame)
        self.frame += 1

    def on_draw(self):
        if self.paused:
            return

        self.clear()
        block_size = self.height // (self.animator.schematic.height + 1)

        if not self.continue_anim:
            self.stop()
            return

        for b in self.display_content:
            im = self.loader.get_image(b)
            sp = pyglet.sprite.Sprite(im)
            p = b.get("render_pos")
            opacity = b.get("opacity")
            xi, yi = isometric.to_screen(p, self.width, self.height, block_size)
            scale = block_size / im.width
            sp.update(x=xi, y=yi, scale_x=scale, scale_y=scale)
            sp.opacity = opacity
            sp.draw()

        self.pipe()
        self.debug_draw()

    def debug_draw(self):
        fps = int(pyglet.clock.get_fps())
        # Everything after buffer save is not rendered to png outputs
        debug_text = f"""
        input file: {self.inputFile}
        output file: {self.outputFile}
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
        )
        debug_label.draw()

    def pipe(self):
        if not self.do_pipe:
            return
        file_num = str(self.frame).zfill(5)
        pyglet.image.get_buffer_manager().get_color_buffer().save(
            f"./frames/{self.outputFile}_{file_num}.png"
        )

    def on_key_press(self, symbol, _):
        logging.debug("Key pressed: %s", symbol)
        if symbol == pyglet.window.key.ESCAPE:
            self.stop()
        if symbol == pyglet.window.key.SPACE:
            self.paused = not self.paused

    def stop(self):
        pyglet.app.exit()

    def queue(self, c):
        self.display_content = c
