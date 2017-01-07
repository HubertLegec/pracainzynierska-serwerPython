import argparse
from pymongo import MongoClient
import gridfs

from visual_search_engine import VisualSearchEngine
from visual_search_engine.utils import FileUtils
from visual_search_engine.utils import ConfigLoader
from visual_search_engine.utils import LogFactory
from visual_search_engine import start, configure


def parse_parameters(default_vocabulary, default_config):
    parser = argparse.ArgumentParser(description='Visual search engine', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--config', type=str, metavar='PATH',
                        help='Path to configuration file', default=default_config)
    parser.add_argument('-v', '--vocabulary', type=str, metavar='PATH',
                        help='Path to file with vocabulary', default=default_vocabulary)
    parser.add_argument('-d', '--debug', action='store_true', help='run in debug mode', default=False)
    return parser.parse_args()


def load_files_to_repository(config, search_engine):
    images = config['web'].get('images', None)
    db_mode = config['database'].get('mode', 'read')
    if images and db_mode == 'create':
        client = MongoClient(config['database'].get('connection_string', None))
        db = client[config['database'].get('db_name', 'vse')]
        fs = gridfs.GridFS(db)
        db.images.delete_many({})
        for i in fs.find({}):
            fs.delete(i._id)
        search_engine.add_images_in_batch(images, db, fs)


def load_app(params, auto_start=False):
    configuration = ConfigLoader.load_config(params.config)
    vocabulary = FileUtils.load(params.vocabulary)
    log = LogFactory.get_logger(configuration)
    search_engine = VisualSearchEngine(vocabulary, configuration)
    load_files_to_repository(configuration, search_engine)
    log.info('Web server start...')
    if auto_start:
        start(
            search_engine,
            vocabulary,
            configuration,
            configuration['web']['host'],
            configuration['web']['port'],
            params.debug
        )
    else:
        return configure(
            search_engine,
            vocabulary,
            configuration
        )


if __name__ == '__main__':
    params = parse_parameters('vocabulary', 'config.ini')
    app = load_app(params, True)
