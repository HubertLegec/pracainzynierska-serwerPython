import io
import json
import unittest
from collections import namedtuple

from run_options.web_app import load_app
from .utils import get_image_name_from_url, get_resource_path
from visual_search_engine.utils import FileUtils


class VseRestApiTest(unittest.TestCase):
    """Tests VSE Rest API - checks if server returns proper messages and codes"""
    TEST_IMAGE_1 = get_resource_path('test_images/test_file_1.jpg')

    @classmethod
    def setUpClass(cls):
        cls.test_img_1 = FileUtils.load_file_bytes(cls.TEST_IMAGE_1)
        Params = namedtuple('Params', 'debug', 'vocabulary', 'config')
        Params.config = 'integration_resources/test_config.ini'
        Params.vocabulary = 'integration_resources/vocabulary'
        Params.debug = False
        cls.app = load_app(Params, False)
        cls.app.testing = True
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    def setUp(self):
        self.client = self.app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def test_should_return_vocabulary(self):
        result = self.client.get('/data/vocabulary')
        self.assertEqual(200, result.status_code)
        body = json.loads(result.data.decode())
        self.assertEqual(500, body['size'])
        self.assertEqual(64, body['rowSize'])
        vocabulary = body['vocabulary']
        self.assertEqual(500, len(vocabulary))

    def test_should_return_openCV_config(self):
        result = self.client.get('/data/openCvConfig')
        self.assertEqual(200, result.status_code)
        body = json.loads(result.data.decode())
        self.assertEqual('BFMatcher', body['matcher_type'])
        self.assertEqual(4, body['norm_type'])
        self.assertEqual('cv2.xfeatures2d_SURF', body['extractor'])

    def test_should_return_list_with_similar_images(self):
        find_result = self.client.post('/find', buffered=True,
                                       data=dict(image=(io.BytesIO(self.test_img_1), 'testImg.jpg')),
                                       headers={'Content-Type': 'multipart/form-data'})
        self.assertEqual(200, find_result.status_code)
        self.assert_result_contains(find_result, ['ukbench00004.jpg', 'ukbench00007.jpg', 'ukbench00005.jpg', 'ukbench00006.jpg'])

    def assert_result_contains(self, response, image_list):
        msg = json.loads(response.data.decode())
        names_without_urls = [get_image_name_from_url(img['url']) for img in msg['images']]
        self.assertEqual(names_without_urls, image_list)
