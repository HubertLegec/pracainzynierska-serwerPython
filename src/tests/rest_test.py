import io
import json
import unittest
import cv2

from .utils import get_image_name_from_url, get_resource_path
from visual_search_engine import VisualSearchEngine
from visual_search_engine import configure
from visual_search_engine.bow import BOW
from visual_search_engine.bow import MatcherProvider
from visual_search_engine.utils import ImageLoader
from visual_search_engine.utils import ConfigLoader
from visual_search_engine.utils import FileUtils


class VseRestApiTest(unittest.TestCase):
    """Tests VSE Rest API - checks if server returns proper messages and codes"""
    TEST_IMAGE_1 = get_resource_path('test_images/test_file_1.jpg')
    TEST_IMAGE_2 = get_resource_path('test_images/test_file_2.jpg')

    @classmethod
    def setUpClass(cls):
        cls.test_img_1 = FileUtils.load_file_bytes(cls.TEST_IMAGE_1)
        cls.test_img_2 = FileUtils.load_file_bytes(cls.TEST_IMAGE_2)
        extractor = cv2.xfeatures2d.SIFT_create()
        images = ImageLoader.load_grayscale_images('test_images')
        config = ConfigLoader.load_config('test_config.ini')
        cls.vocabulary = BOW.generate_vocabulary(images, extractor, config)
        matcher_config = config.get('matcher', MatcherProvider.DEFAULT_FLANN__PARAMS)
        search_engine = VisualSearchEngine(cls.vocabulary, config)
        cls.app = configure(search_engine, cls.vocabulary, matcher_config)
        cls.app.testing = True
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    def setUp(self):
        self.client = self.app.test_client()
        self.client.delete('/upload/test_file_1.jpg')
        self.client.delete('/upload/test_file_2.jpg')

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def test_should_return_vocabulary(self):
        result = self.client.get('/data/vocabulary')
        self.assertEqual(200, result.status_code)
        # TODO - improve test

    def test_should_return_extractor(self):
        result = self.client.get('/data/extractor')
        self.assertEqual(200, result.status_code)
        # TODO - improve test

    def test_should_return_matcher(self):
        result = self.client.get('/data/matcher')
        self.assertEqual(200, result.status_code)
        # TODO - improve test

    def test_should_return_empty_result_list(self):
        result = self.client.post('/find', buffered=True, data=dict(image=(io.BytesIO(self.test_img_1), 'testImg.jpg')),
                                  headers={'Content-Type': 'multipart/form-data'})
        self.assertEqual(200, result.status_code)
        self.assert_result_contains(result, [])

    def test_should_return_list_with_the_same_image(self):
        upload_result = self.upload_image(self.TEST_IMAGE_2, self.test_img_2)
        self.assert_added(upload_result)
        upload_result = self.upload_image(self.TEST_IMAGE_1, self.test_img_1)
        self.assert_added(upload_result)
        find_result = self.client.post('/find', buffered=True,
                                       data=dict(image=(io.BytesIO(self.test_img_1), 'testImg.jpg')),
                                       headers={'Content-Type': 'multipart/form-data'})
        self.assertEqual(200, find_result.status_code)
        self.assert_result_contains(find_result, [self.TEST_IMAGE_1, self.TEST_IMAGE_2])

    def assert_added(self, response):
        self.assertEqual(201, response.status_code, msg='HTTP Status')
        msg = json.loads(response.data.decode())
        self.assertEqual(msg, {'message': 'Image added'}, msg='JSON message')

    def assert_result_contains(self, response, image_list):
        msg = json.loads(response.data.decode())
        names_without_urls = [get_image_name_from_url(img['url']) for img in msg['images']]
        self.assertEqual(names_without_urls, [FileUtils.get_filename_from_path(img) for img in image_list])

    def upload_image(self, name, image):
        return self.client.post(
            '/upload/' + FileUtils.get_filename_from_path(name),
            data=image,
            headers={'Content-Type': 'application/octet-stream'}
        )

