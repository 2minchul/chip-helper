from typing import NamedTuple, Union

from PIL import Image, ImageChops


class Size(NamedTuple):
    width: int
    height: int

    @classmethod
    def from_tuple(cls, size):
        return cls(*size)

    @classmethod
    def from_img(cls, img):
        return cls(*img.size)

    def to_int(self):
        return Size(int(self.width + 0.5), int(self.height + 0.5))

    def __mul__(self, other) -> 'Size':
        if isinstance(other, (int, float)):
            return Size(other * self.width, other * self.height)
        if isinstance(other, tuple):
            return Size(other[0] * self.width, other[1] * self.height)

    __rmul__ = __mul__


class Position(NamedTuple):
    x: Union[int, float]
    y: Union[int, float]

    def to_int(self):
        return Position(int(self.x + 0.5), int(self.y + 0.5))

    def __mul__(self, other) -> 'Position':
        if isinstance(other, (int, float)):
            return Position(other * self.x, other * self.y)
        if isinstance(other, tuple):
            return Position(other[0] * self.x, other[1] * self.y)

    __rmul__ = __mul__


def get_position_from_center(center_position: Position, object_size: Size) -> Position:
    return Position(
        int((2 * center_position.x + 1 - object_size.width) / 2),
        int((2 * center_position.y + 1 - object_size.height) / 2),
    )


def trim(img, border='white'):
    bg = Image.new(img.mode, img.size, border)
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)


def get_image_size(file_path):
    image = Image.open(file_path)
    return image.size
