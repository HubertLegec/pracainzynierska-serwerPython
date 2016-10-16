import unittest
import json
import cv2

from visual_search_engine import VisualSearchEngine
from visual_search_engine.image_loader import load_grayscale_images
from visual_search_engine.bow import BOW
from visual_search_engine.config import load_config
from visual_search_engine.web import web_app
from visual_search_engine.web import ImageRepository
from visual_search_engine.web import Searcher
from tests.utils import get_image_name_from_url


class VseRestApiTest(unittest.TestCase):
    """Tests VSE Rest API - checks if server returns proper messages and codes"""
    TEST_IMAGE_1 = 'test_file_1.jpg'
    TEST_IMAGE_2 = 'test_file_2.jpg'

    @classmethod
    def setUpClass(cls):
        with open(cls.TEST_IMAGE_1, 'rb') as file1:
            cls.test_img_1 = file1.read()
        with open(cls.TEST_IMAGE_2, 'rb') as file2:
            cls.test_img_2 = file2.read()
        extractor = cv2.xfeatures2d.SIFT_create()
        images = load_grayscale_images([cls.TEST_IMAGE_1])
        cls.vocabulary = BOW.generate_vocabulary(images, 200, extractor)
        config = load_config('test_config.ini')
        search_engine = VisualSearchEngine(cls.vocabulary, config)
        cls.app = web_app.app
        cls.app.testing = True
        cls.api = web_app.api
        cls.api.add_resource(Searcher, '/find', '/find/<int:limit>',
                             resource_class_kwargs={'api': cls.api, 'search_engine': search_engine})
        cls.api.add_resource(ImageRepository, '/upload/<path:name>',
                             resource_class_kwargs={'api': cls.api, 'search_engine': search_engine})
        cls.app_context = web_app.app.app_context()

    @classmethod
    def setUp(cls):
        cls.app_context.push()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDown(cls):
        cls.app_context.pop()

    def test_should_return_empty_result_list(self):
        result = self.client.get('/find', data=self.test_img_1, headers={'Content-Type': 'application/octet-stream'})
        self.assertEqual(200, result.status_code)
        self.assert_result_contains(result, [])

    def test_should_return_list_with_the_same_image(self):
        upload_result = self.upload_image(self.TEST_IMAGE_2, self.test_img_2)
        self.assert_added(upload_result)
        upload_result = self.upload_image(self.TEST_IMAGE_1, self.test_img_1)
        self.assert_added(upload_result)
        find_result = self.client.get('/find',
                                      data=self.test_img_1,
                                      headers={'Content-Type': 'application/octet-stream'})
        self.assertEqual(200, find_result.status_code)
        self.assert_result_contains(find_result, [self.TEST_IMAGE_1, self.TEST_IMAGE_2])

    def assert_added(self, response):
        self.assertEqual(201, response.status_code, msg='HTTP Status')
        msg = json.loads(response.data.decode())
        self.assertEqual(msg, {'message': 'Image added'}, msg='JSON message')

    def assert_result_contains(self, response, image_list):
        msg = json.loads(response.data.decode())
        names_without_urls = [get_image_name_from_url(url) for url in msg['images']]
        self.assertEqual(names_without_urls, image_list)

    def upload_image(self, name, image):
        return self.client.post('/upload/' + name, data=image, headers={'Content-Type': 'application/octet-stream'})


if __name__ == '__main__':
    unittest.main()
