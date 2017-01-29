import numpy
from . import DuplicatedRepositoryEntryError
from . import NoSuchRepositoryEntryError


class Repository:
    def __init__(self):
        self.elements = {}
        self.mongo = None
        self.loaded = False

    def add(self, file, histogram):
        """
        Adds given image to repository if there is no element with the same name
        :var: name inserted element name
        :var: histogram calculated image histogram
        :raise: DuplicatedRepositoryEntryError if repository already has element with given name
        """
        self.load()
        if file in self.elements.keys():
            raise DuplicatedRepositoryEntryError(file)
        self.elements[file] = histogram

    def get_all(self):
        """Returns all images from repository.
        If not present, loads them from database first"""
        self.load()
        return self.elements.items()

    def get(self, file):
        """Returns file with given name from database.
        If file with given name is not present in db exception is thrown."""
        self.load()
        if file not in self.elements.keys():
            raise NoSuchRepositoryEntryError(file)
        return self.mongo.send_file(file)

    def get_description(self, file):
        """Returns details of image with given filename.
        If file with given name is not present in db excepiton is thrown."""
        self.load()
        if file not in self.elements.keys():
            raise NoSuchRepositoryEntryError(file)
        return self.mongo.db.images.find_one({'file': file})

    def set_db(self, mongo, loaded):
        self.mongo = mongo
        self.loaded = loaded

    def load(self):
        if not self.loaded:
            for image in self.mongo.db.images.find({}):
                file = image['file']
                histogram = self.array_to_numpy_array(image['histogram'])
                self.elements[file] = histogram
            self.loaded = True

    @classmethod
    def array_to_numpy_array(cls, array):
        return numpy.array(array, numpy.float32)