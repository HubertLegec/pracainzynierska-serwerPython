import os
from visual_search_engine.repository.repository import Repository
from visual_search_engine.repository.error import DuplicatedRepositoryEntryError, NoSuchRepositoryEntryError
from visual_search_engine.file_utils import save


class SimpleRepository(Repository):
    def __init__(self, repository_path='index/'):
        self.elements = {}
        Repository.__init__(self, repository_path)

    def find(self, histogram):
        return self.elements.items()

    def add(self, name, image, histogram):
        if name in self.elements.keys():
            raise DuplicatedRepositoryEntryError(name)
        save(self.repository_dir + name, image)
        self.elements[name] = histogram

    def remove(self, name):
        if name not in self.elements.keys():
            raise NoSuchRepositoryEntryError(name)
        del self.elements[name]
        os.remove(self.repository_dir + name)