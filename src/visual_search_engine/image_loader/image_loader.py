import cv2
import numpy
from . import ImgLoadError
from . import ImgSizeError

IMAGE_MAX_SIZE = 1000
IMAGE_MIN_SIZE = 400


def load_grayscale_images(paths):
    """
    Loads collection of images from given paths
    :var: paths paths of images to load
    :return: array with loaded images
    """
    for path in paths:
        yield load_grayscale_img(path)


def load_grayscale_img(path):
    """
    Load image from given path in grayscale mode and resize it to match max and min size
    :var: path image path
    :return: loaded image
    """
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ImgLoadError(path)
    return resize_image(img)


def load_grayscale_image_from_buffer(buffer):
    """
    Load image from buffer in grayscale mode and resize it to match max and min size
    :var: buffer buffer with image bytes
    :return: loaded and resized image
    """
    if len(buffer) == 0:
        raise ImgLoadError()
    img = cv2.imdecode(numpy.frombuffer(buffer, numpy.uint8), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ImgLoadError()
    return resize_image(img)


def resize_image(image, path_to_file=''):
    """
    Resize given image if its longer edge has more than IMAGE_MAX_SIZE pixels
    Raise error if images shorter edge has less than IMAGE_MIN_SIZE pixels
    :var: image image to resize
    :var: path_to_file resized image path
    :return: resized image
    """
    height, width = image.shape[:2]
    if min(height, width) < IMAGE_MIN_SIZE:
        raise ImgSizeError(path_to_file)
    longer_side = max(height, width)
    if longer_side > IMAGE_MAX_SIZE:
        resize_scale = IMAGE_MAX_SIZE / longer_side
        new_width = int(resize_scale * width)
        new_height = int(resize_scale * height)
        image = cv2.resize(image, new_width, new_height, interpolation=cv2.INTER_LANCZOS4)
    return image

