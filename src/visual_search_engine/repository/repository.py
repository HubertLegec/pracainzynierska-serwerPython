from visual_search_engine.file_utils import normalize_dir_path, remove_dir
from abc import abstractmethod
import os
import atexit


class Repository:
    def __init__(self, repository_path):
        self.repository_dir = normalize_dir_path(repository_path)
        remove_dir(repository_path)
        os.makedirs(repository_path)
        atexit.register(remove_dir, repository_path)

    @abstractmethod
    def add(self, name, image, histogram):
        pass

    @abstractmethod
    def remove(self, name):
        pass

    @abstractmethod
    def find(self, histogram):
        pass
