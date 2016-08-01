import cv2
from visual_search_engine.bow_provider import *

__version__ = 0.1


class VisualSearchEngine:
    def __init__(self, vocabulary):
        self.bow = BOWProvider.get_bow(vocabulary)