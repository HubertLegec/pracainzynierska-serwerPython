import unittest

from tests.utils import get_object_name_with_package
from visual_search_engine.ranker import RankerProvider


class RankerProviderTest(unittest.TestCase):
    def test_get_default_ranker(self):
        ranker = RankerProvider.get_ranker()
        ranker_name = get_object_name_with_package(ranker)
        method = ranker.method
        self.assertEqual('visual_search_engine.ranker.simple_ranker.SimpleRanker', ranker_name)
        self.assertEqual('CHI_SQUARED_ALT', method)

    def test_get_tfidf_ranker(self):
        config = {
            'mode': 'TFIDF',
            'method': 'CORRELATION'
        }
        ranker = RankerProvider.get_ranker(config)
        ranker_name = get_object_name_with_package(ranker)
        method = ranker.method
        self.assertEqual('visual_search_engine.ranker.tfidf_ranker.TFIDFRanker', ranker_name)
        self.assertEqual('CORRELATION', method)
