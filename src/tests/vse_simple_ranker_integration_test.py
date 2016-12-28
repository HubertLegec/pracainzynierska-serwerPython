import glob
import unittest

import cv2

from tests.utils import get_image_name_from_url
from visual_search_engine import VisualSearchEngine
from visual_search_engine.bow import BOW
from visual_search_engine.utils import ImageLoader
from visual_search_engine.utils import ConfigLoader


class SimpleRankerIntegrationTest(unittest.TestCase):
    TEST_IMAGE_1 = 'test_file_1.jpg'
    TEST_IMAGE_2 = 'test_file_2.jpg'
    IMAGES_DIR = './integration_resources/'

    @classmethod
    def setUpClass(cls):
        with open(cls.TEST_IMAGE_1, 'rb') as file1:
            cls.test_img_1 = file1.read()
        with open(cls.TEST_IMAGE_2, 'rb') as file2:
            cls.test_img_2 = file2.read()
        extractor = cv2.xfeatures2d.SIFT_create()
        images = ImageLoader.load_grayscale_images([cls.TEST_IMAGE_1, cls.TEST_IMAGE_2])
        cls.vocabulary = BOW.generate_vocabulary(images, 200, extractor)

    @classmethod
    def setUp(cls):
        cls.config = ConfigLoader.load_config('test_config.ini')
        cls.searchEngine = VisualSearchEngine(cls.vocabulary, cls.config)
        cls.searchEngine.add_images_in_batch(cls.IMAGES_DIR)

    def test_repository_has_elements(self):
        repository_items = self.searchEngine.repository.elements.items()
        self.assertEqual(16, len(repository_items))
        files = glob.glob(self.IMAGES_DIR + VisualSearchEngine.FILE_PATTERN)
        image_names = [get_image_name_from_url(path) for path in files]
        repository_image_names = [entry[0] for entry in repository_items]
        self.assertEqual(sorted(image_names), sorted(repository_image_names))

    def test_engine_returns_suitable_elements(self):
        result = self.searchEngine.find(self.test_img_1, 4)
        self.assertTrue(4, len(result))
        expected_result = ['ukbench00004.jpg', 'ukbench00006.jpg', 'ukbench00007.jpg', 'ukbench00005.jpg']
        self.assertEqual(expected_result, result)
