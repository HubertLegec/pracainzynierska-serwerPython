import unittest

import cv2

from tests.utils import get_image_name_from_url, get_resource_path
from visual_search_engine import VisualSearchEngine
from visual_search_engine.bow import BOW
from visual_search_engine.utils import ImageLoader
from visual_search_engine.utils import ConfigLoader
from visual_search_engine.utils import FileUtils


class TfidfRankerIntegrationTest(unittest.TestCase):
    TEST_IMAGE_1 = get_resource_path('test_images/test_file_1.jpg')
    TEST_IMAGE_2 = get_resource_path('test_images/test_file_2.jpg')
    IMAGES_DIR = get_resource_path('integration_resources')

    @classmethod
    def setUpClass(cls):
        cls.test_img_1 = FileUtils.load_file_bytes(cls.TEST_IMAGE_1)
        cls.test_img_2 = FileUtils.load_file_bytes(cls.TEST_IMAGE_2)
        extractor = cv2.xfeatures2d.SIFT_create()
        images = ImageLoader.load_grayscale_images(get_resource_path('test_images'))
        c = ConfigLoader.load_config('tfidf_test_config.ini')
        cls.vocabulary = BOW.generate_vocabulary(images, extractor, c['vocabulary'])
        cls.searchEngine = VisualSearchEngine(cls.vocabulary, c)
        cls.searchEngine.add_images_in_batch(cls.IMAGES_DIR)

    def test_repository_has_elements(self):
        repository_items = self.searchEngine.repository.elements.items()
        self.assertEqual(16, len(repository_items))
        files = ImageLoader.get_all_jpg_paths_from_dir(self.IMAGES_DIR)
        image_names = [get_image_name_from_url(path) for path in files]
        repository_image_names = [entry[0] for entry in repository_items]
        self.assertEqual(sorted(image_names), sorted(repository_image_names))

    def test_engine_returns_suitable_elements(self):
        result = self.searchEngine.find(self.test_img_1, 4)
        self.assertTrue(4, len(result))
        expected_result = ['ukbench00004.jpg', 'ukbench00007.jpg', 'ukbench00005.jpg', 'ukbench00006.jpg']
        result_names = [pair[1] for pair in result]
        self.assertEqual(expected_result[0], result_names[0])
        self.assertEqual(4, len(set(expected_result).intersection(result_names)))
