import glob
import logging
import os

from .bow import BOWProvider
from .error import SearchEngineError
from .image_loader import load_grayscale_image_from_buffer, load_grayscale_img
from .ranker import RankerProvider
from .repository.repository_provider import RepositoryProvider
from .utils import get_image_name_from_url

__version__ = 0.1


class VisualSearchEngine:
    FILE_PATTERN = '*.jpg'
    log = logging.getLogger('web.VSE')

    def __init__(self, vocabulary, configuration={}):
        self.bow = BOWProvider.get_bow(vocabulary, configuration['extractor'], configuration['matcher'])
        self.repository = RepositoryProvider.get_repository(configuration['repository'])
        self.ranker = RankerProvider.get_ranker(configuration['ranker'])

    def find(self, image, limit=5):
        VisualSearchEngine.log.info("Find images request with limit " + str(limit))
        img = load_grayscale_image_from_buffer(image)
        histogram = self.bow.generate_histogram(img)
        return self.find_by_histogram(histogram, limit)

    def find_by_histogram(self, histogram, limit=5):
        return self.ranker.rank(histogram, self.repository, limit)

    def add_new_image(self, image, name):
        VisualSearchEngine.log.info('Add new image with name ' + name + ' request')
        img = load_grayscale_image_from_buffer(image)
        histogram = self.bow.generate_histogram(img)
        self.repository.add(name, img, histogram)
        self.ranker.update(self.repository)

    def add_images_in_batch(self, images_dir):
        if not os.path.isdir(images_dir):
            raise IOError("The folder " + images_dir + " doesn't exist");
        VisualSearchEngine.log.info('Adding all jpg images from directory: ' + images_dir)
        files = sorted(glob.glob1(images_dir, VisualSearchEngine.FILE_PATTERN))
        counter = 0
        for fileName in files:
            try:
                image = load_grayscale_img(images_dir + '/' + fileName)
                histogram = self.bow.generate_histogram(image)
                name_without_dir = get_image_name_from_url(fileName)
                self.repository.add(name_without_dir, image, histogram)
                counter += 1
            except SearchEngineError as e:
                VisualSearchEngine.log.error(e.message)
        VisualSearchEngine.log.info('Number of images added: ' + str(counter))
        self.ranker.update(self.repository)

    def remove_image(self, name):
        VisualSearchEngine.log.info('Remove image with name ' + name + ' request')
        self.repository.remove(name)
        self.ranker.update(self.repository)
        pass
