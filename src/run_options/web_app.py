import argparse
import logging
import os

from visual_search_engine.utils import load

from visual_search_engine import VisualSearchEngine
from visual_search_engine.config import load_config
from visual_search_engine.utils.logger_utils import get_logger
from visual_search_engine.web.web_app import start, configure
from visual_search_engine.matcher import MatcherProvider


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
        log_file = config['current_directory'] + config['web']['log_file']
    log = get_logger('web', logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    log.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, log_level))
    log.addHandler(ch)
    return log


def load_files_to_repository(config, search_engine):
    files_dir = config['web'].get('files_dir', None)
    if files_dir:
        search_engine.add_images_in_batch(config['current_directory'] + files_dir)


def load_app(params, autostart=False):
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    configuration = load_config(params.config)
    configuration['current_directory'] = curr_dir
    vocabulary = load(curr_dir + params.vocabulary)
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

