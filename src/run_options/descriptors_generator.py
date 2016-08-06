import glob
import pickle
import argparse
from visual_search_engine import *
from visual_search_engine.config import load_config


def parse_parameters():
    parser = argparse.ArgumentParser(description='Visual Search Engine', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--config', type=str, metavar='PATH', required=True, help='Path to configuration file')
    parser.add_argument('-s', '--save', type=str, metavar='PATH', required=True,
                        help='Path to result file with vocabulary')
    parser.add_argument('-i', '--images', type=str, metavar='PATH', required=True,
                        help='Path to directory with input images')
    parser.add_argument('-m', '--maxDescriptors', type=int, dest='maxDescriptors',
                        help='Maximum number of generated descriptors')
    return parser.parse_args()


def save_descriptors(descriptors, fileName):
    with open(fileName, 'wb') as f:
        pickle.dump(descriptors, f, pickle.HIGHEST_PROTOCOL)
        print("Saved " + str(len(descriptors)) + " descriptors to '" + fileName + "'")


def get_max_descriptors(optional_limit):
    if optional_limit:
        return optional_limit
    return DEFAULT_MAX_DESCRIPTORS


FILE_PATTERN = '*.jpg'
DEFAULT_MAX_DESCRIPTORS = 2000

if __name__ == "__main__":
    params = parse_parameters()
    config = load_config(params.config)
    descriptors = []
    extractor = ExtractorProvider.get_extractor(config['extractor'])
    images_directory = params.images
    files = sorted(glob.glob(images_directory + FILE_PATTERN))
    number_of_descriptors = 0
    max_descriptors = get_max_descriptors(params.maxDescriptors)
    for fileName in files:
        try:
            image = load_grayscale_img(fileName)
            single_img_descriptors = extractor.detectAndCompute(image, None)[1]
            descriptors.extend(single_img_descriptors)
            number_of_descriptors += len(single_img_descriptors)
            if number_of_descriptors > max_descriptors:
                break
        except SearchEngineError as e:
            print(e.message)
    save_descriptors(descriptors, params.save)
