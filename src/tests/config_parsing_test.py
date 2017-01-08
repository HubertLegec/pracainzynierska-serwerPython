import configparser
import unittest

from visual_search_engine.utils import ConfigLoader


class ConfigParserTest(unittest.TestCase):
    """Tests parsing of config file - checks if it is mapped to python dictionary properly"""

    @classmethod
    def setUpClass(cls):
        config_file = 'integration_resources/test_config.ini'
        cls.config = ConfigLoader.load_config(config_file)

    def test_file_parsing(self):
        correct_config = {
            'web': {
                'images': 'integration_resources/images.json'
            },
            'logging': {
                'console_logs': 'yes',
                'file_logs': 'no',
                'console_log_level': 'DEBUG',
                'file_log_level': 'INFO',
                'log_file': 'logs'
            },
            'extractor': {
                'algorithm': 'SURF'
            },
            'matcher': {
                'norm_type': 4,
                'matcher_type': 'BFMatcher'
            },
            'ranker': {
                'mode': 'SIMPLE',
                'method': 'CHI_SQUARED_ALT'
            },
            'vocabulary': {
                'max_descriptors': 40000,
                'cluster_count': 500
            },
            'database': {
                'connection_string': 'mongodb://vseApp:vse123@ds035975.mlab.com:35975/vse_test',
                'db_name': 'vse_test',
                'mode': 'create'
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
