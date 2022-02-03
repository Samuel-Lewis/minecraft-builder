import logging
import pyglet


ASSET_FOLDER = "../assets"
MISSING_NAME = "missing"

pyglet.resource.path = [ASSET_FOLDER]


class ImageLoader:
    def __init__(self):
        self.images = {}
        self.missing = None

    def get_namespace(self, id):
        namespace, name = id.split(":")
        return namespace, name

    def fetch_missing_image(self):
        if self.missing is None:
            self.missing = pyglet.resource.image(f"{MISSING_NAME}.png")
        return self.missing

    def fetch_resource(self, id):
        try:
            logging.debug("Loading image %s", id)
            namespace, name = self.get_namespace(id)
            image = pyglet.resource.image(f"{namespace}/{name}.png")
            self.images[id] = image
            return image
        except:
            logging.error("Failed to load image %s", id)
            return self.fetch_missing_image()

    def get_image(self, block):
        id = block.get("id")
        if id in self.images:
            return self.images[id]
        else:
            image = self.fetch_resource(id)
            self.images[id] = image
            return image
