import cv2
import numpy
from visual_search_engine.image_loader import *

IMAGE_MAX_SIZE = 800
IMAGE_MIN_SIZE = 400


def load_grayscale_img(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ImgLoadError(path)
    return resize_image(img)


def load_grayscale_image_from_buffer(buffer):
    if len(buffer) == 0:
        raise ImgLoadError()
    img = cv2.imdecode(numpy.frombuffer(buffer, numpy.uint8), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ImgLoadError()
    return resize_image(img)


def resize_image(image, path_to_file=''):
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

