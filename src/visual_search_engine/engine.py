import glob
from visual_search_engine.error import SearchEngineError
from visual_search_engine.bow_provider import *
from visual_search_engine.repository.repository_provider import RepositoryProvider
from visual_search_engine.ranker.ranker_provider import RankerProvider
from visual_search_engine.image_loader.image_loader import load_grayscale_image_from_buffer, load_grayscale_img

__version__ = 0.1


class VisualSearchEngine:
    FILE_PATTERN = '*.jpg'
    log = logging.getLogger('web.VSE')

    def __init__(self, vocabulary, configuration):
        self.bow = BOWProvider.get_bow(vocabulary, configuration['extractor'], configuration['matcher'])
        self.repository = RepositoryProvider.get_repository(configuration['repository'])
        self.ranker = RankerProvider.get_ranker(configuration['ranker'])

    def find(self, image, limit=5):
        VisualSearchEngine.log.info("Find images request with limit " + str(limit))
        img = load_grayscale_image_from_buffer(image)
        histogram = self.bow.generate_histogram(img)
        return self.ranker.rank(histogram, self.repository, limit)

    def add_new_image(self, image, name):
        VisualSearchEngine.log.info('Add new image with name ' + name + ' request')
        img = load_grayscale_image_from_buffer(image)
        histogram = self.bow.generate_histogram(img)
        self.repository.add(name, img, histogram)
        self.ranker.update(self.repository)

    def add_images_in_batch(self, images_dir):
        VisualSearchEngine.log.info('Adding all jpg images from directory: ' + images_dir)
        files = sorted(glob.glob(images_dir + VisualSearchEngine.FILE_PATTERN))
        counter = 0
        for fileName in files:
            try:
                image = load_grayscale_img(fileName)
                histogram = self.bow.generate_histogram(image)
                self.repository.add(fileName, image, histogram)
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
