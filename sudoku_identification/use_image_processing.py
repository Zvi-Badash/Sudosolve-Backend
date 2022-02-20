import cv2
import imutils

import sudoku_image_processing

image = cv2.imread('img.jpeg')
image = imutils.resize(image, width=600)

for r in sudoku_image_processing.analyze_image(image, debug=False):
    print(r)
