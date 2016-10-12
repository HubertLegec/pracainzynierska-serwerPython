import argparse
import logging

from utils.file_utils import load

from visual_search_engine import VisualSearchEngine
from visual_search_engine.config import load_config
from visual_search_engine.utils.logger_utils import get_logger
from visual_search_engine.web.web_app import start


def parse_parameters():
    parser = argparse.ArgumentParser(description='Visual search engine', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--config', type=str, metavar='PATH', required=True, help='Path to configuration file')
    parser.add_argument('-v', '--vocabulary', type=str, metavar='PATH', required=True,
                        help='Path to file with vocabulary')
    parser.add_argument('-d', '--debug', action='store_true', help='run in debug mode')
    return parser.parse_args()


def config_logger(config):
    log_level = 'INFO'
    if config['web']['log_level']:
        log_level = config['web']['log_level']
    log_file = 'log'
    if config['web']['log_file']:
        log_file = config['web']['log_file']
    log = get_logger('web', logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    log.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, log_level))
    log.addHandler(ch)
    return log


def load_files_to_repository(config, search_engine):
    files_dir = config['web']['files_dir']
    if files_dir:
        search_engine.add_images_in_batch(files_dir)


if __name__ == '__main__':
    params = parse_parameters()
    configuration = load_config(params.config)
    vocabulary = load(params.vocabulary)
    log = config_logger(configuration)
    search_engine = VisualSearchEngine(vocabulary, configuration)
    load_files_to_repository(configuration, search_engine)
    log.info('Web server start...')
    start(search_engine, configuration['web']['host'], configuration['web']['port'], params.debug)


