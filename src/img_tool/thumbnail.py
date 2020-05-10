from typing import NamedTuple

from PIL import Image, ImageFilter
from PIL.PngImagePlugin import PngImageFile


class Size(NamedTuple):
    width: int
    height: int

    @classmethod
    def from_tuple(cls, size):
        return cls(*size)

    @classmethod
    def from_img(cls, img):
        return cls(*img.size)


def zoom(img, percent):
    n = percent / 100
    size = tuple(int(0.5 + (i * n)) for i in img.size)
    return img.resize(size)


def get_center_dox(img, target_size: Size):
    w, h = img.size
    left = (w - target_size.width) / 2
    top = (h - target_size.height) / 2
    right = (w + target_size.width) / 2
    bottom = (h + target_size.height) / 2
    return tuple(map(int, (left, top, right, bottom)))


def crop_center(img, target_size: Size):
    box = get_center_dox(img, target_size)
    return img.crop(box)


def paste_center(img, small_img):
    box = get_center_dox(img, Size.from_img(small_img))
    return img.paste(small_img, box)


def composite_thumbnail(input_path, output_path):
    canvas_size = Size(1920, 1440)
    # print('canvas', canvas_size)

    origin_img: PngImageFile = Image.open(input_path)
    # print('origin', Size.from_img(origin_img))

    zoom_img = zoom(origin_img, 118.98)
    zoom_size = Size.from_img(zoom_img)
    # print('zoom', zoom_size)
    # zoom_img.save('zoom.jpg')

    # crop center
    crop_img = crop_center(zoom_img, Size(canvas_size.width, zoom_size.height))
    # print('crop', Size.from_tuple(crop_img.size))
    # im.save('tmp.jpg', format='JPEG', quality=100)

    bg_img = zoom(
        crop_img,
        (canvas_size.height / crop_img.height) * 100  # crop_img 의 높이가 canvas_img 의 높이와 같아지도록 확대
    )
    bg_img = crop_center(bg_img, canvas_size)
    bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=7))

    paste_center(bg_img, crop_img)
    bg_img.save(output_path, format='JPEG', quality=100, dpi=(300, 300))
