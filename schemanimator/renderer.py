import logging
import pyglet
import ffmpeg


class Renderer(pyglet.window.Window):
    def __init__(self, width, height, inputFile, outputFile):
        super(Renderer, self).__init__(width=width, height=height)
        pyglet.clock.schedule_interval(self.update, 0.1)
        self.clear()
        self.display_content = []
        self.frame = 0
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.process2 = (
            ffmpeg.input(
                "pipe:",
                format="rawvideo",
                pix_fmt="rgb24",
                s="{}x{}".format(width, height),
                r=60,
            )
            .vflip()
            .output(f"{outputFile}", pix_fmt="yuv420p", loglevel="quiet", r=60)
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )

    def update(self, dt):
        self.frame += 1

    def on_draw(self):
        self.clear()
        for c in self.display_content:
            c.draw()

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
        texture = (
            pyglet.image.get_buffer_manager()
            .get_color_buffer()
            .get_texture()
            .get_image_data()
        )
        format = "RGBA"
        pitch = texture.width * len(format)
        pixels = texture.get_data(format, pitch)
        self.process2.stdin.write(pixels)

    def on_key_press(self, symbol, modifiers):
        logging.debug("Key pressed: %s", symbol)
        if symbol == pyglet.window.key.ESCAPE:
            self.stop()

    def stop(self):
        self.process2.stdin.close()
        self.process2.wait()
        pyglet.app.exit()

    def queue(self, c):
        self.display_content = c
