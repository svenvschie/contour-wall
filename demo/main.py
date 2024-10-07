from contourwall import ContourWall, hsv_to_rgb
from PIL import Image
import numpy as np

cw = ContourWall()

cw.new_with_ports("COM11", "COM14", "COM12", "COM13", "COM10", "COM9")

path = 'images\halloween_60x40_pixels.jpg'
image = Image.open(path).convert('RGB')
image_data = np.asarray(image)
cw.pixels[:] = image_data
cw.show()

