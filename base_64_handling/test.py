import numpy

from B64Utils import b64ToImage
from sudoku_identification.sudoku_image_processing import analyze_image

with open('img.txt', 'r') as f:
    img = b64ToImage(f.read())
    analyze_image(numpy.asarray(img))
    img.save('decoded-img.jpeg')
