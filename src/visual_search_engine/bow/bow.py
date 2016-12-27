import cv2
import logging


class BOW:
    DEFAULT_CONFIG = {
        'cluster_count': 300,
        'max_descriptors': 3000
    }
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
    def generate_vocabulary(cls, images, extractor, vocabulary_config, logger=log):
        config = {**cls.DEFAULT_CONFIG, **vocabulary_config}
        cluster_count = config['cluster_count']
        max_descriptors = config['max_descriptors']
        logger.info('generate vocabulary for images')
        logger.info('cluster size: ' + str(cluster_count))
        logger.info('max descriptors size: ' + str(max_descriptors))
        bow_trainer = cv2.BOWKMeansTrainer(cluster_count)
        counter = 1
        img_size = len(images)
        descriptors_count = 0
        for img in images:
            logger.info('add descriptors from image ' + str(counter) + ' of ' + str(img_size))
            descriptors = extractor.detectAndCompute(img, None)[1]
            logger.info('descriptors size: ' + str(len(descriptors)))
            descriptors_count += len(descriptors)
            bow_trainer.add(descriptors)
            if descriptors_count > max_descriptors:
                break
            counter += 1
        return bow_trainer.cluster()
