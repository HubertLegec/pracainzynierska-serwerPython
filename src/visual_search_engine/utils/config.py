import configparser


def load_config(path):
    """Loads loads configuration from file"""
    config_parser = configparser.RawConfigParser()
    config_parser.read(path)
    return transform_config_to_dict(config_parser)


def transform_config_to_dict(config):
    """Transforms configuration object to python dictionary"""
    result_dictionary = {}
    for section in config.sections():
        result_dictionary[section] = {}
        for k, v in config.items(section):
            result_dictionary[section][k] = str_to_number(section, k, config)
    return result_dictionary


def str_to_number(section, option, config):
    """Casts string to float or integer if possible. If not returns string"""
    converters = [config.getint, config.getfloat]
    for converter in converters:
        try:
            return converter(section, option)
        except ValueError:
            pass
    return config[section][option]
