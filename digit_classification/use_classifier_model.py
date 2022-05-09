import argparse
import cv2
from Classifier import Classifier

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True)
ap.add_argument("-i", "--image", required=True)
args = vars(ap.parse_args())

classifier = Classifier(args['model'])
print(classifier.classify(cv2.imread(args['image'])))
