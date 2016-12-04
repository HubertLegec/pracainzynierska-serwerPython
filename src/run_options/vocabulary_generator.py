import argparse
import logging

from visual_search_engine.utils.logger_utils import get_logger
from visual_search_engine.utils import save, load
from visual_search_engine.bow import BOW

# ------------ logger -----------------
log = get_logger('vocabulary_generator', logging.INFO)
# -------------------------------------


def parse_parameters():
    parser = argparse.ArgumentParser(description='Visual search engine', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--config', type=str, metavar='PATH', required=True,
                        help='Path to configuration file')
    parser.add_argument('-s', '--save', type=str, metavar='PATH', required=True,
                        help='Path to result file with vocabulary')
    parser.add_argument('-d', '--descriptors', type=str, metavar='PATH', required=True,
                        help='Path to file with descriptors')
    return parser.parse_args()


def save_vocabulary(vocabulary, file_name):
    log.info("Saving vocabulary to '" + file_name + "'")
    save(file_name, vocabulary)
    log.info('Vocabulary saved.')


if __name__ == "__main__":
    options = parse_parameters()
    descriptors = load(options.descriptors)
    log.info('Generating vocabulary...')
    vocabulary = BOW.generate_vocabulary_from_descriptors(descriptors, 200)
    save_vocabulary(vocabulary, options.save)
