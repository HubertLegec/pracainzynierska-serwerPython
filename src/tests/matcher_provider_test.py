import unittest

from tests.utils import get_object_name_with_package
from visual_search_engine import MatcherProvider


class MatcherProviderTest(unittest.TestCase):

    def test_get_default_matcher(self):
        matcher = MatcherProvider.get_matcher()
        matcher_name = get_object_name_with_package(matcher)
        self.assertEqual('cv2.FlannBasedMatcher', matcher_name)

    def test_get_custom_matcher(self):
        config = {
            'norm_type': 4,
            'matcher_type': 'BFMatcher'
        }
        matcher = MatcherProvider.get_matcher(config)
        matcher_name = get_object_name_with_package(matcher)
        self.assertEqual('cv2.BFMatcher', matcher_name)

if __name__ == '__main__':
    unittest.main()