import pickle
from optparse import OptionParser
from visual_search_engine import *


def parse_execution_options():
    parser = OptionParser()
    parser.add_option('-c', '--config', action='store', dest='config', help='Path to configuration file')
    parser.add_option('-s', '--save', action='store', dest='saveTo', help='Path to result file with vocabulary')
    parser.add_option('-d', '--descriptors', action='store', dest='descriptors', help='Path to file with descriptors')
    return parser.parse_args()


def load_descriptors(file_name):
    with open(file_name, 'rb') as f:
        descriptors = pickle.load(f)
    return descriptors


def save_vocabulary(vocabulary, file_name):
    print("Saving vocabulary to '" + file_name + "'")
    with open(file_name, 'wb') as f:
        pickle.dump(vocabulary, f, pickle.HIGHEST_PROTOCOL)
    print('Saved.')


if __name__ == "__main__":
    (options, args) = parse_execution_options()
    descriptors = load_descriptors(options.descriptors)
    print('Generating vocabulary...')
    vocabulary = BOW.generate_vocabulary_from_descriptors(descriptors)
    save_vocabulary(vocabulary, options.save)
