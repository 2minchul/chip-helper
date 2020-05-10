import PIL


def get_image_size(file_path):
    image = PIL.Image.open(file_path)
    return image.size
