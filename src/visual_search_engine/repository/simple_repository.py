import os

from visual_search_engine.utils import save_file_bytes
from . import DuplicatedRepositoryEntryError
from . import NoSuchRepositoryEntryError
from . import Repository


class SimpleRepository(Repository):
    def __init__(self, repository_path='index/'):
        Repository.__init__(self, repository_path)

    def find(self, histogram):
        """Returns all images from repository"""
        return self.elements.items()

    def add(self, name, image, histogram):
        """
        Adds given image to repository if there is no element with the same name
        :var: name inserted element name
        :var: image image to insert
        :var: histogram calculated image histogram
        :raise: DuplicatedRepositoryEntryError if repository already has element with given name
        """
        if name in self.elements.keys():
            raise DuplicatedRepositoryEntryError(name)
        save_file_bytes(self.repository_dir + name, image)
        self.elements[name] = histogram

    def remove(self, name):
        """
        Removes element with given name from repository if name is present, raises error otherwise
        :param name: name of element that should be removed
        """
        if name not in self.elements.keys():
            raise NoSuchRepositoryEntryError(name)
        del self.elements[name]
        os.remove(self.repository_dir + name)
