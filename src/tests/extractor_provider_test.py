import unittest

from tests.utils import get_object_name_with_package
from visual_search_engine.bow import ExtractorProvider


class ExtractorProviderTest(unittest.TestCase):
    def test_get_default_extractor(self):
        extractor = ExtractorProvider.get_extractor()
        extractor_name = get_object_name_with_package(extractor)
        self.assertEqual('cv2.xfeatures2d_SIFT', extractor_name)

    def test_get_surf_extractor(self):
        config = {
            'algorithm': 'SURF'
        }
        extractor = ExtractorProvider.get_extractor(config)
        extractor_name = get_object_name_with_package(extractor)
        self.assertEqual('cv2.xfeatures2d_SURF', extractor_name)
