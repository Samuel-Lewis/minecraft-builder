import logging
import pyglet
import os


ASSET_FOLDER = "../assets"
MISSING_NAME = "missing"

pyglet.resource.path = [ASSET_FOLDER]


class ImageLoader:
    def __init__(self):
        self.images = {}
        self.missing = pyglet.resource.image(f"{MISSING_NAME}.png")
        self.out_file = None
        self.missing_assets = set()

    def log_missing_asset(self, id):
        if id in self.missing_assets:
            return
        self.missing_assets.add(id)

        logging.warning("Failed to load image %s", id)
        if self.out_file == None:
            self.out_file = open("missing.txt", "w")
        self.out_file.write(f"{id}\n")
        self.out_file.flush()
        os.fsync(self.out_file.fileno())

    def get_namespace(self, id):
        namespace, name = id.split(":")
        return namespace, name

    def fetch_resource(self, block):
        nbt = block.get("nbt")
        id = block.get("id")
        try:
            logging.debug("Loading image %s", id)
            namespace, name = self.get_namespace(id)
            image = pyglet.resource.image(f"{namespace}/{name}.png")
            self.images[id] = image
            return image
        except:
            self.log_missing_asset(nbt)
            return self.missing

    def get_image(self, block):
        id = block.get("id")
        if id in self.images:
            return self.images[id]
        else:
            image = self.fetch_resource(block)
            self.images[id] = image
            return image
