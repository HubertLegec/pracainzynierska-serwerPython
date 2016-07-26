import cv2
from visual_search_engine.bow_generator import *

__version__ = 0.1


class VisualSearchEngine:
    def __init__(self, vocabulary):
        self.bow = BOWGenerator.generate(vocabulary)
