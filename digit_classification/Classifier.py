from collections import namedtuple
from typing import Any

import cv2
import numpy as np
from keras.models import load_model
from keras_preprocessing.image import img_to_array

Image = np.ndarray
Prediction = namedtuple("Prediction", "digit confidence")


def _prepare_image(image: Image, raw) -> Any:
    raw_image = image
    if raw:
        raw_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # grayscale the image
        raw_image = cv2.threshold(raw_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]  # threshold the image
        raw_image = cv2.bitwise_not(raw_image)  # negate the image

    raw_image = cv2.resize(raw_image, (28, 28))  # resize the image
    raw_image = raw_image.astype('float') / 255.0  # normalize the color intensity to be 0-1

    # convert the image to a numpy array with proper dimensions
    return np.expand_dims(img_to_array(raw_image),
                          axis=0)


class Classifier:
    """
    This class is a classifier that uses the MNIST db to classify digit images.
    """

    def __init__(self, model_path: str):
        self.model = load_model(model_path)

    def classify(self, image: Image, raw=True):
        p = self.model.predict(_prepare_image(image, raw))
        return Prediction(p.argmax(axis=1)[0], p.max())
