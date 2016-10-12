import argparse
import glob
import logging
import pickle

from visual_search_engine import *
from visual_search_engine.config import load_config
from visual_search_engine.utils.logger_utils import get_logger

# ------------ logger -----------------
log = get_logger('descriptors_generator', logging.INFO)
# -------------------------------------


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
        log.info("Saved " + str(len(descriptors)) + " descriptors to '" + fileName + "'")


def get_max_descriptors(optional_limit):
    if optional_limit:
        return optional_limit
    return DEFAULT_MAX_DESCRIPTORS


FILE_PATTERN = '*.jpg'
DEFAULT_MAX_DESCRIPTORS = 2000

if __name__ == "__main__":
    params = parse_parameters()
    config = load_config(params.config)
    total_descriptors = []
    extractorConfig = config['extractor']
    extractor = ExtractorProvider.get_extractor(extractorConfig)
    images_directory = params.images
    log.info('Images directory: ' + images_directory)
    files = sorted(glob.glob(images_directory + FILE_PATTERN))
    number_of_descriptors = 0
    max_descriptors = get_max_descriptors(params.maxDescriptors)
    log.info('Max number of descriptors: ' + str(max_descriptors))
    for fileName in files:
        try:
            image = load_grayscale_img(fileName)
            # result[0] - keypoints
            # result[1] - descriptors : numpy array of shape Number_of_Keypoints×128
            descriptors = extractor.detectAndCompute(image, None)[1]
            total_descriptors.extend(descriptors)
            number_of_descriptors += len(descriptors)
            log.info('File: ' + fileName + ', descriptors found: ' + str(len(descriptors)))
            if number_of_descriptors > max_descriptors:
                break
        except SearchEngineError as e:
            log.error(e.message)
    save_descriptors(total_descriptors, params.save)
