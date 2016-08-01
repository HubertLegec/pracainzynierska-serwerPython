import cv2


class BOW:
    def __init__(self, vocabulary, matcher, extractor):
        self.vocabulary = vocabulary
        self.extractor = extractor
        self.bowDescriptorExtractor = cv2.BOWImgDescriptorExtractor(self.extractor, matcher)
        self.bowDescriptorExtractor.setVocabulary(vocabulary)

    def __init__(self, images, cluster_size, matcher, extractor):
        self.vocabulary = BOW.generate_vocabulary(images, cluster_size, extractor)
        self.extractor = extractor
        self.bowDescriptorExtractor = cv2.BOWImgDescriptorExtractor(self.extractor, matcher)
        self.bowDescriptorExtractor.setVocabulary(self.vocabulary)

    def generate_histogram(self, image):
        features = self.extractor.detect(image)
        return self.bowDescriptorExtractor.compute(image, features)[0]

    @staticmethod
    def generate_vocabulary(images, cluster_size, extractor):
        bow_trainer = cv2.BOWKMeansTrainer(cluster_size)
        for img in images:
            bow_trainer.add(extractor.detectAndCompute(img, None)[1])
        return bow_trainer.cluster()

    @staticmethod
    def generate_vocabulary_from_descriptors(descriptors, cluster_size):
        bow_trainer = cv2.BOWKMeansTrainer(cluster_size)
        bow_trainer.add(descriptors)
        return bow_trainer.cluster()
