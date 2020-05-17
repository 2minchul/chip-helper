import io
from typing import Union

import pyqrcode
import svgwrite
from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngImageFile
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

from imagetools import Size, get_position_from_center, Position, trim


class Ratio:
    QR_IMAGE_SIZE = 0.8458  # multiply by width
    QR_IMAGE_POSITION = (0.5, 0.4)
    HORIZON_LINE_SIZE = (0.9666, 0.0067)
    HORIZON_LINE_POSITION = (0.5, 0.7833)
    NUM_TEXT_SIZE = (0.2083, 0.0423)
    NUM_TEXT_POSITION = (0.8208, 0.93)
    MADEBY_SIZE = (0.3166, 0.0576)
    MADEBY_POSITION = (0.5, 0.8763)
    FONT_CANVAS_SIZE = (5.1915, 1.0506)


def make_qr_png(url, pixel_size: Union[int, float]) -> PngImageFile:
    with io.BytesIO() as tmp:
        qr = pyqrcode.create(url, error='Q', version=3, mode='binary')
        qr.png(tmp, scale=1, quiet_zone=0)
        tmp.seek(0)
        pil_img: PngImageFile = Image.open(tmp)
        resized_img = pil_img.resize(2 * (int(pixel_size + 0.5),))
    return resized_img


def make_number_image(n: int, font_size=80.9) -> Image:
    canvas_size = font_size * Size.from_tuple(Ratio.FONT_CANVAS_SIZE)
    dwg = svgwrite.Drawing('test.svg', size=canvas_size)
    text = f'no.{n:04}'
    params = dict(
        fill='black',
        font_size=f'{font_size}pt',
        font_family="DXGulimB-KSCpc-EUC-H",
        lengthAdjust="spacing",
        # font_weight='bold',
        kerning='5px',
        letter_spacing="4",
    )
    dwg.add(dwg.text(text, insert=('0%', '85%'), **params))
    dwg.add(dwg.text(text, insert=('1%', '85%'), **params))
    with io.StringIO() as svg:
        dwg.write(svg)
        svg.seek(0)
        svg_text = svg.read()
    with io.BytesIO() as svg:
        svg.write(svg_text.encode())
        svg.seek(0)
        drawing = svg2rlg(svg)
        img = renderPM.drawToPIL(drawing, 300)

    return trim(img)


def insert_made_by(img, made_by_path='madeby.png'):
    canvas_size = Size.from_img(img)
    with io.BytesIO() as made_by_binary:
        with open(made_by_path, 'rb') as f:
            made_by_binary.write(f.read())
        made_by_binary.seek(0)

        made_by: PngImageFile = Image.open(made_by_binary)
        made_by_size = canvas_size * Ratio.MADEBY_SIZE
        made_by = made_by.resize(made_by_size.to_int())

        made_by_pos = get_position_by_ratio(canvas_size, made_by_size, Ratio.MADEBY_POSITION)
        img.paste(made_by, made_by_pos)


def draw_number(img, n):
    canvas_size = Size.from_img(img)
    number_img = make_number_image(n)
    num_size: Size = canvas_size * Ratio.NUM_TEXT_SIZE
    number_img = number_img.resize(num_size.to_int())
    number_position = get_position_by_ratio(canvas_size, num_size, Ratio.NUM_TEXT_POSITION)
    img.paste(number_img, number_position.to_int())


def get_position_by_ratio(canvas_size: Size, image_size: Size, ratio: tuple) -> Position:
    center_position = Position(*(canvas_size * ratio))
    return get_position_from_center(center_position, image_size)


def draw_qr(img, url):
    canvas_size = Size.from_img(img)
    qr_image_base = canvas_size.width * Ratio.QR_IMAGE_SIZE
    qr_image = make_qr_png(url, qr_image_base)
    qr_position = get_position_by_ratio(canvas_size, Size.from_img(qr_image), Ratio.QR_IMAGE_POSITION)
    img.paste(qr_image, qr_position)


def draw_horizon_line(background_img: Image):
    canvas_size = Size.from_img(background_img)
    line_draw = ImageDraw.Draw(background_img)
    length, width = canvas_size * Ratio.HORIZON_LINE_SIZE
    line_center = canvas_size * Ratio.HORIZON_LINE_POSITION
    line_position = Position(*line_center)
    line_left_pos = get_position_from_center(
        line_position,
        Size(int(length), int(width))
    )
    line_right_pos = Position(line_left_pos.x + length, line_left_pos.y)
    line_draw.line([line_left_pos.to_int(), line_right_pos.to_int()], width=int(width), fill='black')


def make_qr_image(canvas_size: Size = Size(591, 738), url='http://m.site.naver.com/0wPWp', n=0):
    img = Image.new('L', size=canvas_size, color='white')
    draw_qr(img, url)
    draw_horizon_line(img)
    draw_number(img, n)
    insert_made_by(img)
    return img


if __name__ == '__main__':
    img = make_number_image(1)
    with open('../imagetools/tmp.png', 'wb') as f:
        img.save(f, format='PNG', dpi=(300, 300))
