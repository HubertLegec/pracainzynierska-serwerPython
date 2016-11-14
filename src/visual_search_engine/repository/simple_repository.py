import os

from visual_search_engine.utils import save_file_bytes
from .duplicated_repository_entry_error import DuplicatedRepositoryEntryError
from .no_such_repository_entry_error import NoSuchRepositoryEntryError
from .repository import Repository


class SimpleRepository(Repository):
    def __init__(self, repository_path='index/'):
        Repository.__init__(self, repository_path)

    def find(self, histogram):
        return self.elements.items()

    def add(self, name, image, histogram):
        if name in self.elements.keys():
            raise DuplicatedRepositoryEntryError(name)
        save_file_bytes(self.repository_dir + name, image)
        self.elements[name] = histogram

    def remove(self, name):
        if name not in self.elements.keys():
            raise NoSuchRepositoryEntryError(name)
        del self.elements[name]
        os.remove(self.repository_dir + name)