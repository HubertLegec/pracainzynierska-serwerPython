import numpy
from . import DuplicatedRepositoryEntryError
from . import NoSuchRepositoryEntryError


class Repository:
    def __init__(self):
        self.elements = {}
        self.mongo = None
        self.loaded = False

    def add(self, name, histogram):
        """
        Adds given image to repository if there is no element with the same name
        :var: name inserted element name
        :var: histogram calculated image histogram
        :raise: DuplicatedRepositoryEntryError if repository already has element with given name
        """
        if name in self.elements.keys():
            raise DuplicatedRepositoryEntryError(name)
        self.elements[name] = histogram

    def add_and_save(self, name, histogram, image, url=""):
        if not self.loaded:
            self.load()
        if name in self.elements.keys():
            raise DuplicatedRepositoryEntryError(name)
        self.elements[name] = histogram
        self.mongo.save_file(name, image)
        self.mongo.db.images.insert_one({
            "name": name,
            "url": url,
            "histogram": [v.item() for v in histogram]
        })

    def remove(self, name):
        """
        Removes element with given name from repository if name is present, raises error otherwise
        :param name: name of element that should be removed
        """
        if not self.loaded:
            self.load()
        if name not in self.elements.keys():
            raise NoSuchRepositoryEntryError(name)
        del self.elements[name]

    def get_all(self):
        """Returns all images from repository"""
        if not self.loaded:
            self.load()
        return self.elements.items()

    def get(self, name):
        if not self.loaded:
            self.load()
        return self.mongo.send_file(name)

    def set_db(self, mongo, loaded):
        self.mongo = mongo
        self.loaded = loaded

    def load(self):
        for image in self.mongo.db.images.find({}):
            name = image['name']
            histogram = self.array_to_numpy_array(image['histogram'])
            self.elements[name] = histogram
        self.loaded = True

    @classmethod
    def array_to_numpy_array(cls, array):
        return numpy.array(array, numpy.float32)