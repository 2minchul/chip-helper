import pyqrcode


def generate(url, path):
    img = pyqrcode.create(url, error='Q', version=3, mode='binary')
    img.png(path, scale=7, quiet_zone=0)
