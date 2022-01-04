import base64
from PIL import Image
from io import BytesIO

filename = input()

with open(filename, 'r') as f:
    im = Image.open(BytesIO(base64.b64decode(f.read())))

im.save(filename.replace('.txt', '.jpg'), 'JPEG')
