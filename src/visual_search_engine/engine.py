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
        self.repository = Repository()
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

    def add_images(self, images, db, fs):
        if not os.path.isfile(images):
            raise IOError("The file " + images + " doesn't exist")
        img_dir = FileUtils.get_dir_from_filename(images)
        self.log.info('Adding all jpg images defined in file: ' + images + ' from dir: ' + img_dir)
        descriptions = ImageLoader.load_image_definitions(images)
        counter = 0
        self.log.info('There is ' + str(len(descriptions)) + ' images in given directory')
        for description in descriptions:
            try:
                filename = description['file']
                self.log.info('Processing image:' + filename)
                img_path = img_dir + '/' + filename
                grayscale_image = ImageLoader.load_grayscale_img(img_path)
                image = FileUtils.load_file_bytes(img_path)
                histogram = self.bow.generate_histogram(grayscale_image)
                self.repository.add(filename, histogram)
                self._save_image_in_db(db, fs, image, description, histogram)
                counter += 1
                self.log.info('Image added to repository: ' + filename)
            except SearchEngineError as e:
                self.log.error(e.message)
        self.log.info('Number of images added: ' + str(counter))
        self.ranker.update(self.repository)

    @classmethod
    def _save_image_in_db(cls, db, fs, image, description, histogram):
        file = description['file']
        fs.put(image, filename=file)
        db.images.insert_one({
            "file": file,
            "name": description['name'],
            "url": description['url'],
            "histogram": [v.item() for v in histogram]
        })
