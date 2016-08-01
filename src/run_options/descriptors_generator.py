import glob
import pickle
from optparse import OptionParser
from visual_search_engine import *


def parse_execution_options():
    parser = OptionParser()
    parser.add_option('-c', '--config', action='store', dest='config', help='Path to configuration file')
    parser.add_option('-s', '--save', action='store', dest='saveTo', help='Path to result file with vocabulary')
    parser.add_option('-i', '--images', action='store', dest='imagesPath', help='Path to directory with input images')
    parser.add_option('-m', '--maxDescriptors', action='store', type='int', dest='maxDescriptors',
                      help='Maximum number of generated descriptors')
    return parser.parse_args()


def save_descriptors(descriptors, fileName):
    with open(fileName, 'wb') as f:
        pickle.dump(descriptors, f, pickle.HIGHEST_PROTOCOL)
        print("Saved " + str(len(descriptors)) + " descriptors to '" + fileName + "'")

FILE_PATTERN = '*.jpg'

if __name__ == "__main__":
    (options, args) = parse_execution_options()
    descriptors = []
    extractor = ExtractorProvider.get_extractor()
    images_directory = options.images
    files = sorted(glob.glob(images_directory + FILE_PATTERN))
    number_of_descriptors = 0
    for fileName in files:
        try:
            image = load_grayscale_img(images_directory + fileName)
            single_img_descriptors = extractor.detectAndCompute(image, None)[1]
            descriptors.append(single_img_descriptors)
            number_of_descriptors += len(single_img_descriptors)
            if number_of_descriptors > options.maxDescriptors:
                break
        except SearchEngineError as e:
            e.message
    save_descriptors(descriptors, options.save)


