import argparse
import logging
from visual_search_engine.config import load_config
from visual_search_engine.file_utils import load
from visual_search_engine.web.web_app import start
from visual_search_engine import VisualSearchEngine


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
    logging.basicConfig(filename=log_file, log_level=getattr(logging, log_level))


if __name__ == '__main__':
    params = parse_parameters()
    configuration = load_config(params.config)
    vocabulary = load(params.vocabulary)
    search_engine = VisualSearchEngine(vocabulary, configuration)
    config_logger(configuration)
    logging.debug('debug')
    logging.info('info')
    logging.warning('warning')
    start(search_engine, configuration.web.host, configuration.web.port, params.debug)


