from contourwall import ContourWall, hsv_to_rgb
from PIL import Image, ImageSequence
import numpy as np
import time
from datetime import datetime

cw = ContourWall()
cw.new_with_ports("COM11", "COM14", "COM12", "COM13", "COM10", "COM9")

path = 'images/Fontys-gif.gif'

loops = 1

while True:
    time.sleep(0.5)

    current_hour = datetime.now().hour

    if 7 <= current_hour < 19:
        gif = Image.open(path)
        
        for _ in range(loops):
            for frame in ImageSequence.Iterator(gif):
                frame = frame.convert('RGB')
                image_data = np.asarray(frame)
                
                cw.pixels[:] = image_data
                cw.show()
                
                time.sleep(0.2)
    else:
        cw.clear()
        cw.show()
