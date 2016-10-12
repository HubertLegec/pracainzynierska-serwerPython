import atexit
import os
from abc import abstractmethod

from visual_search_engine.utils import remove_dir, normalize_dir_path


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
