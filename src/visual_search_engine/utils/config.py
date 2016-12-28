import configparser
import logging


class ConfigLoader:
    log = logging.getLogger('vse.ConfigLoader')

    @classmethod
    def load_config(cls, path):
        """Loads loads configuration from file"""
        cls.log.info('Load config from path: ' + path)
        config_parser = configparser.RawConfigParser()
        config_parser.read(path)
        return cls._transform_config_to_dict(config_parser)

    @classmethod
    def _transform_config_to_dict(cls, config):
        """Transforms configuration object to python dictionary"""
        result_dictionary = {}
        for section in config.sections():
            result_dictionary[section] = {}
            for k, v in config.items(section):
                result_dictionary[section][k] = cls._str_to_number(section, k, config)
        return result_dictionary

    @classmethod
    def _str_to_number(cls, section, option, config):
        """Casts string to float or integer if possible. If not returns string"""
        converters = [config.getint, config.getfloat]
        for converter in converters:
            try:
                return converter(section, option)
            except ValueError:
                pass
        return config[section][option]
