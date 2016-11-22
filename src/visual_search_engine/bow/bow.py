import cv2
import numpy as np
import logging


class BOW:
    def __init__(self, vocabulary, matcher, extractor):
        self.vocabulary = vocabulary
        self.extractor = extractor
        self.matcher = matcher
        self.bowDescriptorExtractor = cv2.BOWImgDescriptorExtractor(self.extractor, matcher)
        self.bowDescriptorExtractor.setVocabulary(vocabulary)
        self.log = logging.getLogger('web.BOW')

    def generate_histogram(self, image):
        self.log.info('generate histogram for image')
        features = self.extractor.detect(image)
        histogram = self.bowDescriptorExtractor.compute(image, features)[0]
        self.log.info('histogram ready')
        return histogram

    @staticmethod
    def generate_vocabulary(images, cluster_size, extractor):
        bow_trainer = cv2.BOWKMeansTrainer(cluster_size)
        for img in images:
            bow_trainer.add(extractor.detectAndCompute(img, None)[1])
        return bow_trainer.cluster()

    @staticmethod
    def generate_vocabulary_from_descriptors(descriptors, cluster_size):
        bow_trainer = cv2.BOWKMeansTrainer(cluster_size)
        bow_trainer.add(np.array(descriptors))
        return bow_trainer.cluster()
