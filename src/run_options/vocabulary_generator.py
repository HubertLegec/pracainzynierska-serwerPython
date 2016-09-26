import pickle
import argparse
import logging
from visual_search_engine import *
from utils.utils import get_logger

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


def load_descriptors(file_name):
    with open(file_name, 'rb') as f:
        descriptors = pickle.load(f)
    return descriptors


def save_vocabulary(vocabulary, file_name):
    log.info("Saving vocabulary to '" + file_name + "'")
    with open(file_name, 'wb') as f:
        pickle.dump(vocabulary, f, pickle.HIGHEST_PROTOCOL)
    log.info('Vocabulary saved.')


if __name__ == "__main__":
    options = parse_parameters()
    descriptors = load_descriptors(options.descriptors)
    log.info('Generating vocabulary...')
    vocabulary = BOW.generate_vocabulary_from_descriptors(descriptors, 200)
    save_vocabulary(vocabulary, options.save)
