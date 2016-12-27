import glob
import logging
import os
import numpy

from .bow import BOWProvider
from .error import SearchEngineError
from .utils import load_grayscale_image_from_buffer, load_grayscale_img
from .ranker import RankerProvider
from .repository import RepositoryProvider
from .utils import get_image_name_from_url, load_file_bytes

__version__ = 0.1


class VisualSearchEngine:
    FILE_PATTERN = '*.jpg'

    def __init__(self, vocabulary, configuration={}):
        self.bow = BOWProvider.get_bow(vocabulary, configuration['extractor'], configuration['matcher'])
        self.repository = RepositoryProvider.get_repository(configuration['repository'])
        self.ranker = RankerProvider.get_ranker(configuration['ranker'])
        self.log = logging.getLogger('web.VSE')

    def find(self, image, limit=5):
        self.log.info("Find images request with limit " + str(limit))
        img = load_grayscale_image_from_buffer(image)
        self.log.info('Image loaded from buffer')
        histogram = self.bow.generate_histogram(img)
        return self.find_by_histogram(histogram, limit)

    def find_by_histogram(self, histogram, limit=5):
        self.log.info('histogram: ' + numpy.array_str(histogram))
        return self.ranker.rank(histogram, self.repository, limit)

    def add_new_image(self, image, name):
        self.log.info('Add new image with name ' + name + ' request')
        img = load_grayscale_image_from_buffer(image)
        histogram = self.bow.generate_histogram(img)
        self.repository.add(name, image, histogram)
        self.ranker.update(self.repository)

    def add_images_in_batch(self, images_dir):
        if not os.path.isdir(images_dir):
            raise IOError("The folder " + images_dir + " doesn't exist")
        self.log.info('Adding all jpg images from directory: ' + images_dir)
        files = sorted(glob.glob1(images_dir, VisualSearchEngine.FILE_PATTERN))
        counter = 0
        self.log.info('There is ' + str(len(files)))
        for fileName in files:
            try:
                self.log.info('Processing image:' + fileName)
                img_path = images_dir + '/' + fileName
                grayscale_image = load_grayscale_img(img_path)
                image = load_file_bytes(img_path)
                histogram = self.bow.generate_histogram(grayscale_image)
                name_without_dir = get_image_name_from_url(fileName)
                self.repository.add(name_without_dir, image, histogram)
                counter += 1
                self.log.info('Image added to repository: ' + fileName)
            except SearchEngineError as e:
                self.log.error(e.message)
        self.log.info('Number of images added: ' + str(counter))
        self.ranker.update(self.repository)

    def remove_image(self, name):
        self.log.info('Remove image with name ' + name + ' request')
        self.repository.remove(name)
        self.ranker.update(self.repository)
        pass
