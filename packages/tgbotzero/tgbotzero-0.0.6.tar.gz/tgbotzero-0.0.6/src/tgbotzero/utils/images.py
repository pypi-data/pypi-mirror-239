from io import BytesIO
import os
import hashlib

import PIL.Image

from PIL import ImageDraw, ImageFont


def sha256(f):
    sha256_hash = hashlib.sha256()
    f.seek(0)
    for byte_block in iter(lambda: f.read(4096), b""):
        sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


class Image:
    def __init__(self, image: str = None):
        self._pil = None
        self._filename = None
        if isinstance(image, str):
            self._filename = image
            self._io = open(image, 'rb')
        elif isinstance(image, PIL.Image.Image):
            self._io = BytesIO()
            image.save(self._io, 'PNG')
            self._pil = image
        elif isinstance(image, bytes):
            self._io = BytesIO(image)
        self._io.seek(0)

    def put_text(self, text: str, color=(255, 255, 255)):
        if not self._pil:
            self._pil = PIL.Image.open(self._io)
        draw = ImageDraw.Draw(self._pil)
        width, height = self._pil.size
        font_size = 64
        font_path = os.path.join(os.path.abspath(__file__), "DejaVuSans.ttf")
        font = ImageFont.truetype(font_path, font_size)
        (left, top, right, bottom) = draw.multiline_textbbox((0, 0), text, font=font)
        scale = (width * 0.9) / (right - left)
        font_size = font_size * scale
        font = ImageFont.truetype(font_path, font_size)
        (left, top, right, bottom) = draw.multiline_textbbox((0, 0), text, font=font)
        rx = (width - (right - left)) / 2
        ry = height * 0.9 - (bottom - top)
        draw.multiline_text((rx, ry), text, fill=color, font=font)
        edited_image_stream = BytesIO()
        self._pil.save(edited_image_stream, 'PNG')
        self._io = edited_image_stream
        self._io.seek(0)
        return self


class _ImageManager:
    def __init__(self):
        self.images_tg_file_ids = {}

    def __setitem__(self, image: Image, file_id: int):
        hash = sha256(image._io)
        image._io.seek(0)
        self.images_tg_file_ids[hash] = file_id

    def __getitem__(self, image: Image):
        hash = sha256(image._io)
        image._io.seek(0)
        return self.images_tg_file_ids.get(hash, None)


_image_manager = _ImageManager()
