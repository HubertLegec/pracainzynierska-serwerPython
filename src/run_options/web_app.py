import argparse
import logging

from visual_search_engine import VisualSearchEngine
from visual_search_engine.bow import MatcherProvider
from visual_search_engine.utils import load
from visual_search_engine.utils.config import load_config
from visual_search_engine.web_app import start, configure


def parse_parameters(default_vocabulary, default_config):
    parser = argparse.ArgumentParser(description='Visual search engine', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--config', type=str, metavar='PATH',
                        help='Path to configuration file', default=default_config)
    parser.add_argument('-v', '--vocabulary', type=str, metavar='PATH',
                        help='Path to file with vocabulary', default=default_vocabulary)
    parser.add_argument('-d', '--debug', action='store_true', help='run in debug mode', default=False)
    return parser.parse_args()


def config_logger(config):
    log_level = 'INFO'
    if config['web']['log_level']:
        log_level = config['web']['log_level']
    log_file = 'log'
    if config['web']['log_file']:
        log_file = config['web']['log_file']
    log = logging.getLogger('web')
    log.setLevel(log_level)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s: %(name)s - %(levelname)s : %(message)s'))
    log.addHandler(fh)
    return log


def load_files_to_repository(config, search_engine):
    files_dir = config['web'].get('files_dir', None)
    if files_dir:
        search_engine.add_images_in_batch(files_dir)


def load_app(params, autostart=False):
    configuration = load_config(params.config)
    vocabulary = load(params.vocabulary)
    log = config_logger(configuration)
    search_engine = VisualSearchEngine(vocabulary, configuration)
    load_files_to_repository(configuration, search_engine)
    log.info('Web server start...')
    if autostart:
        start(
            search_engine,
            vocabulary,
            configuration.get('matcher', MatcherProvider.DEFAULT_FLANN__PARAMS),
            configuration['web']['host'],
            configuration['web']['port'],
            params.debug
        )
    else:
        return configure(
            search_engine,
            vocabulary,
            configuration.get('matcher', MatcherProvider.DEFAULT_FLANN__PARAMS)
        )


if __name__ == '__main__':
    params = parse_parameters('vocabulary', 'config.ini')
    app = load_app(params, True)
