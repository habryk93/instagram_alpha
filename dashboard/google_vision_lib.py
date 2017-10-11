import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


class GoogleVision(object):

    file_path = None
    client = None

    def __init__(self, abs_file_path):
        self.file_path = abs_file_path
        self.client = vision.ImageAnnotatorClient()

    def __get_image(self):
        image = None
        if os.path.isfile(self.file_path):
            with io.open(self.file_path, 'rb') as image_file:
                content = image_file.read()
                image = types.Image(content=content)

        return image

    def __get_detection(self, detection):
        image = self.__get_image()
        if image:
            response = getattr(self.client, '{}_detection'.format(detection))(image=image)
            return getattr(response, '{}_annotations'.format(detection))
        return []

    def get_image_labels(self):
        return self.__get_detection('label')

    def get_image_landmarks(self):
        return self.__get_detection('landmark')
