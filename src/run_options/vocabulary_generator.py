import argparse
import logging
import glob

from visual_search_engine.utils import get_logger
from visual_search_engine.utils import save
from visual_search_engine.utils import load_config
from visual_search_engine.utils import normalize_dir_path
from visual_search_engine.utils import load_grayscale_images
from visual_search_engine.bow import ExtractorProvider
from visual_search_engine.bow import BOW

# ------------ logger -----------------
log = get_logger('vocabulary_generator', logging.INFO)
# -------------------------------------

FILE_PATTERN = '*.jpg'


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
    config = load_config(params.config)
    extractorConfig = config['extractor']
    extractor = ExtractorProvider.get_extractor(extractorConfig)
    images_directory = normalize_dir_path(params.images)
    log.info('Loading images...')
    files = sorted(glob.glob(images_directory + FILE_PATTERN))
    images = load_grayscale_images(images_directory, log)
    log.info('Generating vocabulary...')
    vocabulary_config = config['vocabulary']
    vocabulary = BOW.generate_vocabulary(images, extractor, vocabulary_config, log)
    log.info("Saving vocabulary of size " + str(len(vocabulary)) + " to '" + params.save + "'")
    save(params.save, vocabulary)
    log.info('Vocabulary saved.')
