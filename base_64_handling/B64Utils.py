import base64
from io import BytesIO

from PIL import Image


def b64ToImage(encoded) -> Image:
    return Image.open(BytesIO(base64.b64decode(encoded)))


# def imageToB64(img: Image) -> bytes:
#     return base64.b64encode(img)
