import configparser
import unittest

from visual_search_engine.config import load_config, str_to_number


class ConfigParserTest(unittest.TestCase):
    """Tests parsing of config file - checks if it is mapped to python dictionary properly"""

    @classmethod
    def setUpClass(cls):
        config_file = 'test_config.ini'
        cls.config = load_config(config_file)

    def test_file_parsing(self):
        correct_config = {
            'extractor': {
                'algorithm': 'SIFT'
            },
            'matcher': {
                'norm_type': 4,
                'matcher_type': 'BFMatcher'
            },
            'ranker': {},
            'repository': {
                'type': 'SIMPLE',
                'directory': './index/'
            }
        }
        self.assertEqual(correct_config, self.config)

    def test_casting_str_to_number(self):
        config = configparser.RawConfigParser()
        config.add_section('matcher')
        config.set('matcher', 'algorithm', 'BFMatcher')
        config.set('matcher', 'norm_type', '4')
        self.assertEqual(4, str_to_number('matcher', 'norm_type', config))
        self.assertEqual('BFMatcher', str_to_number('matcher', 'algorithm', config))


if __name__ == '__main__':
    unittest.main()