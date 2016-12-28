import argparse

from visual_search_engine.utils import LogFactory
from visual_search_engine.utils import ConfigLoader
from visual_search_engine.utils import FileUtils
from visual_search_engine.utils import ImageLoader
from visual_search_engine.bow import ExtractorProvider
from visual_search_engine.bow import BOW


def parse_parameters():
    parser = argparse.ArgumentParser(description='Visual search engine', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--config', type=str, metavar='PATH', required=True,
                        help='Path to configuration file')
    parser.add_argument('-s', '--save', type=str, metavar='PATH', required=True,
                        help='Path to result file with vocabulary')
    parser.add_argument('-i', '--images', type=str, metavar='PATH', required=True,
                        help='Path to file with descriptors')
    return parser.parse_args()


if __name__ == "__main__":
    params = parse_parameters()
    config = ConfigLoader.load_config(params.config)
    log = LogFactory.get_logger(config)
    extractorConfig = config['extractor']
    extractor = ExtractorProvider.get_extractor(extractorConfig)
    images_directory = FileUtils.normalize_dir_path(params.images)
    log.info('Loading images...')
    files = ImageLoader.get_all_jpg_paths_from_dir(images_directory)
    images = ImageLoader.load_grayscale_images(images_directory)
    log.info('Generating vocabulary...')
    vocabulary_config = config['vocabulary']
    vocabulary = BOW.generate_vocabulary(images, extractor, vocabulary_config, log)
    log.info("Saving vocabulary of size " + str(len(vocabulary)) + " to '" + params.save + "'")
    FileUtils.save(params.save, vocabulary)
    log.info('Vocabulary saved.')
