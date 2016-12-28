import configparser
import unittest

from visual_search_engine.utils import ConfigLoader


class ConfigParserTest(unittest.TestCase):
    """Tests parsing of config file - checks if it is mapped to python dictionary properly"""

    @classmethod
    def setUpClass(cls):
        config_file = 'test_config.ini'
        cls.config = ConfigLoader.load_config(config_file)

    def test_file_parsing(self):
        correct_config = {
            'logging': {
                'console_logs': 'yes',
                'file_logs': 'yes',
                'console_log_level': 'DEBUG',
                'file_log_level': 'INFO',
                'log_file': 'logs'
            },
            'extractor': {
                'algorithm': 'SIFT'
            },
            'matcher': {
                'norm_type': 4,
                'matcher_type': 'BFMatcher'
            },
            'ranker': {},
            'repository': {
                'directory': './index/'
            },
            'vocabulary': {
                'max_descriptors': 2500,
                'cluster_count': 250
            }
        }
        self.assertEqual(correct_config, self.config)

    def test_casting_str_to_number(self):
        config = configparser.RawConfigParser()
        config.add_section('matcher')
        config.set('matcher', 'algorithm', 'BFMatcher')
        config.set('matcher', 'norm_type', '4')
        self.assertEqual(4, ConfigLoader._str_to_number('matcher', 'norm_type', config))
        self.assertEqual('BFMatcher', ConfigLoader._str_to_number('matcher', 'algorithm', config))
