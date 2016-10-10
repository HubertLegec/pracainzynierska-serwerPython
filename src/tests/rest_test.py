import unittest
import json
import cv2

from visual_search_engine import VisualSearchEngine
from visual_search_engine import load_grayscale_images, BOW
from visual_search_engine.config import load_config
from visual_search_engine.web import web_app
from visual_search_engine.web.repository import ImageRepository
from visual_search_engine.web.search import Searcher


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
        msg = json.loads(result.data.decode())
        self.assertEqual(200, result.status_code)
        self.assertEqual({'images': []}, msg)

    def test_should_return_list_with_the_same_image(self):
        upload_result = self.client.post('/upload/test_image.jpg',
                                         data=self.test_img_1,
                                         headers={'Content-Type': 'application/octet-stream'})
        self.assert_added(upload_result)
        find_result = self.client.get('/find',
                                      data=self.test_img_1,
                                      headers={'Content-Type': 'application/octet-stream'})
        self.assertEqual(200, find_result.status_code)

    def assert_added(self, response):
        self.assertEqual(201, response.status_code, msg='HTTP Status')
        msg = json.loads(response.data.decode())
        self.assertEqual(msg, {'message': 'Image added'}, msg='JSON message')


if __name__ == '__main__':
    unittest.main()