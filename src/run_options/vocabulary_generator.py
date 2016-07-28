from optparse import OptionParser
from visual_search_engine import *


def parse_execution_options():
    parser = OptionParser()
    parser.add_option('-c', '--config', action='store', dest='config', help='Path to configuration file')
    parser.add_option('-s', '--save', action='store', dest='saveTo', help='Path to result file with vocabulary')
    parser.add_option('-d', '--descriptors', action='store', dest='descriptors', help='Path to file with descriptors')
    return parser.parse_args()


if __name__ == "__main__":
    (options, args) = parse_execution_options()
    # TODO implement this method
