import tesserocr
from PIL import Image


image = Image.open('code.jpg')
print(tesserocr.image_to_text(image))




