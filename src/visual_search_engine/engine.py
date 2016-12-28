import logging
import os
import numpy

from .bow import BOWProvider
from .error import SearchEngineError
from .utils import ImageLoader
from .ranker import RankerProvider
from .repository import Repository
from .utils import FileUtils

__version__ = 1.0


class VisualSearchEngine:

    def __init__(self, vocabulary, configuration={}):
        self.bow = BOWProvider.get_bow(vocabulary, configuration['extractor'], configuration['matcher'])
        self.repository = Repository(configuration['repository']['directory'])
        self.ranker = RankerProvider.get_ranker(configuration['ranker'])
        self.log = logging.getLogger('vse.VSE')

    def find(self, image, limit=5):
        self.log.info("Find images request with limit " + str(limit))
        img = ImageLoader.load_grayscale_image_from_buffer(image)
        self.log.info('Image loaded from buffer')
        histogram = self.bow.generate_histogram(img)
        return self.find_by_histogram(histogram, limit)

    def find_by_histogram(self, histogram, limit=5):
        self.log.info('histogram: ' + numpy.array_str(histogram))
        return self.ranker.rank(histogram, self.repository, limit)

    def add_new_image(self, image, name):
        self.log.info('Add new image with name ' + name + ' request')
        img = ImageLoader.load_grayscale_image_from_buffer(image)
        histogram = self.bow.generate_histogram(img)
        self.repository.add(name, image, histogram)
        self.ranker.update(self.repository)

    def add_images_in_batch(self, images_dir):
        if not os.path.isdir(images_dir):
            raise IOError("The folder " + images_dir + " doesn't exist")
        self.log.info('Adding all jpg images from directory: ' + images_dir)
        files = ImageLoader.get_all_jpg_paths_from_dir(images_dir)
        counter = 0
        self.log.info('There is ' + str(len(files)) + ' images in given directory')
        for filename in files:
            try:
                self.log.info('Processing image:' + filename)
                img_path = images_dir + '/' + filename
                grayscale_image = ImageLoader.load_grayscale_img(img_path)
                image = FileUtils.load_file_bytes(img_path)
                histogram = self.bow.generate_histogram(grayscale_image)
                self.repository.add(filename, image, histogram)
                counter += 1
                self.log.info('Image added to repository: ' + filename)
            except SearchEngineError as e:
                self.log.error(e.message)
        self.log.info('Number of images added: ' + str(counter))
        self.ranker.update(self.repository)

    def remove_image(self, name):
        self.log.info('Remove image with name ' + name + ' request')
        self.repository.remove(name)
        self.ranker.update(self.repository)
