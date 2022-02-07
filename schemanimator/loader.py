from loguru import logger
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

    def log_missing_asset(self, nbt_data):
        namespace = nbt_data.get("namespace")
        file_base = nbt_data.get("file_base")
        nbt = nbt_data.get("nbt")
        file_name = f"{namespace}/{file_base}.png"
        if file_name in self.missing_assets:
            return
        self.missing_assets.add(file_name)

        logger.warning("Failed to load {file_name}", file_name=file_name)
        if self.out_file == None:
            self.out_file = open("missing.txt", "w")
        self.out_file.write(f"/isorender block {nbt}\n  {file_name}\n")
        self.out_file.flush()
        os.fsync(self.out_file.fileno())

    def fetch_resource(self, nbt_data):
        namespace = nbt_data.get("namespace")
        file_base = nbt_data.get("file_base")
        file_name = f"{namespace}/{file_base}.png"

        try:
            logger.trace("Loading image {file_name}", file_name=file_name)
            image = pyglet.resource.image(file_name)
            return image
        except:
            self.log_missing_asset(nbt_data)
            return self.missing

    def get_image(self, block):
        nbt_data = block.get("nbt_data")
        file_base = nbt_data.get("file_base")
        if file_base in self.images:
            return self.images[file_base]
        else:
            image = self.fetch_resource(nbt_data)
            self.images[file_base] = image
            return image
