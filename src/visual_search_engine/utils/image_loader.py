import cv2
import numpy
import glob
import logging
import json
from . import ImgLoadError
from . import ImgSizeError


class ImageLoader:
    IMAGE_MAX_SIZE = 1000
    IMAGE_MIN_SIZE = 400
    FILE_PATTERN = '*.jpg'
    log = logging.getLogger('vse.ImageLoader')

    @classmethod
    def load_grayscale_images(cls, images_directory):
        """
        Loads collection of images from given paths
        :var: paths paths of images to load
        :return: array with loaded images
        """
        files = sorted(glob.glob1(images_directory, cls.FILE_PATTERN))
        return [cls.load_grayscale_img(images_directory + '/' + file) for file in files]

    @classmethod
    def load_grayscale_img(cls, path):
        """
        Load image from given path in grayscale mode and resize it to match max and min size
        :var: path image path
        :return: loaded image
        """
        cls.log.info('Loading image: ' + path)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ImgLoadError(path)
        return cls.resize_image(img)

    @classmethod
    def load_grayscale_image_from_buffer(cls, buffer):
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
        return cls.resize_image(img)

    @classmethod
    def resize_image(cls, image, path_to_file=''):
        """
        Resize given image if its longer edge has more than IMAGE_MAX_SIZE pixels
        Raise error if images shorter edge has less than IMAGE_MIN_SIZE pixels
        :var: image image to resize
        :var: path_to_file resized image path
        :return: resized image
        """
        height, width = image.shape[:2]
        if min(height, width) < cls.IMAGE_MIN_SIZE:
            raise ImgSizeError(path_to_file)
        longer_side = max(height, width)
        if longer_side > cls.IMAGE_MAX_SIZE:
            resize_scale = cls.IMAGE_MAX_SIZE / longer_side
            new_width = int(resize_scale * width)
            new_height = int(resize_scale * height)
            image = cv2.resize(image, new_width, new_height, interpolation=cv2.INTER_LANCZOS4)
        return image

    @classmethod
    def get_all_jpg_paths_from_dir(cls, directory):
        """
        Return array of paths to jpg images in given directory
        :param directory: directory to search for jpg in
        :return: array of paths to found jpg images
        """
        return sorted(glob.glob1(directory, cls.FILE_PATTERN))

    @classmethod
    def load_image_definitions(cls, images):
        with open(images) as json_data:
            return json.load(json_data)
