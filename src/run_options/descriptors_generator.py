from optparse import OptionParser


def parse_execution_options():
    parser = OptionParser()
    parser.add_option('-c', '--config', action='store', dest='config', help='Path to configuration file')
    parser.add_option('-s', '--save', action='store', dest='saveTo', help='Path to result file with vocabulary')
    parser.add_option('-i', '--images', action='store', dest='imagesPath', help='Path to directory with input images')
    parser.add_option('-m', '--maxDescriptors', action='store', type='int', dest='maxDescriptors',
                      help='Maximum number of generated descriptors')
    return parser.parse_args()


if __name__ == "__main__":
    (options, args) = parse_execution_options()
    descriptors = []
    # TODO implement this method
