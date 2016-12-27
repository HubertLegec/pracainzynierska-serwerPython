import atexit
import os

from visual_search_engine.utils import save_file_bytes
from visual_search_engine.utils import remove_dir
from visual_search_engine.utils import normalize_dir_path
from . import DuplicatedRepositoryEntryError
from . import NoSuchRepositoryEntryError


class Repository:
    def __init__(self, repository_path='index'):
        self.repository_dir = normalize_dir_path(repository_path)
        remove_dir(repository_path)
        os.makedirs(repository_path)
        self.elements = {}
        atexit.register(remove_dir, repository_path)

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

    def get_all(self):
        """Returns all images from repository"""
        return self.elements.items()
