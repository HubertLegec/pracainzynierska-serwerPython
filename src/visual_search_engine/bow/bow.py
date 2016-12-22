import cv2
import numpy as np
import logging


class BOW:
    log = logging.getLogger('web.BOW')

    def __init__(self, vocabulary, matcher, extractor):
        self.vocabulary = vocabulary
        self.extractor = extractor
        self.matcher = matcher
        self.bowDescriptorExtractor = cv2.BOWImgDescriptorExtractor(self.extractor, matcher)
        self.bowDescriptorExtractor.setVocabulary(vocabulary)

    def generate_histogram(self, image):
        self.log.info('generate histogram for image')
        features = self.extractor.detect(image)
        histogram = self.bowDescriptorExtractor.compute(image, features)[0]
        self.log.info('histogram ready')
        return histogram

    @classmethod
    def generate_vocabulary(cls, images, cluster_size, extractor):
        cls.log.info('generate vocabulary for images')
        bow_trainer = cv2.BOWKMeansTrainer(cluster_size)
        counter = 1
        img_size = len(images)
        for img in images:
            cls.log.info('adding descriptors from image ' + str(counter) + ' of ' + str(img_size))
            bow_trainer.add(extractor.detectAndCompute(img, None)[1])
        return bow_trainer.cluster()

    @classmethod
    def generate_vocabulary_from_descriptors(cls, descriptors, cluster_size):
        cls.log.info('generate vocabulary for descriptors')
        bow_trainer = cv2.BOWKMeansTrainer(cluster_size)
        bow_trainer.add(np.array(descriptors))
        return bow_trainer.cluster()
