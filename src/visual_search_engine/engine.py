from visual_search_engine.bow_provider import *
from visual_search_engine.repository.repository_provider import RepositoryProvider
from visual_search_engine.ranker.ranker_provider import RankerProvider
from visual_search_engine.image_loader.image_loader import load_grayscale_image_from_buffer

__version__ = 0.1


class VisualSearchEngine:
    def __init__(self, vocabulary, configuration):
        self.bow = BOWProvider.get_bow(vocabulary, configuration['extractor'], configuration['matcher'])
        self.repository = RepositoryProvider.get_repository(configuration['repository'])
        self.ranker = RankerProvider.get_ranker(configuration['ranker'])

    def find(self, image, limit=5):
        img = load_grayscale_image_from_buffer(image)
        histogram = self.bow.generate_histogram(img)
        return self.ranker.rank(histogram, self.repository, limit)

    def add_new_image(self, image, name):
        img = load_grayscale_image_from_buffer(image)
        histogram = self.bow.generate_histogram(img)
        self.repository.add(name, img, histogram)
        self.ranker.update(self.repository)

    def remove_image(self, name):
        self.repository.remove(name)
        self.ranker.update(self.repository)
        pass
