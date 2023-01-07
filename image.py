from sense_hat import SenseHat
from PIL import Image, ImageChops
import numpy as np
import time

sense = SenseHat()

# load a PNG from file
img = Image.open('0.png')

for i in np.linspace(0,360,17):
    # Rotate and invert the pixel values
    inverted = ImageChops.invert(img.rotate(angle=i, fillcolor=(255,255,255)))

    # Convert to Numpy array and flatten rows and columns
    flatter = np.array(inverted).reshape(64,4)
    # remove alpha value from RGBA and write to matrix array
    sense.set_pixels(flatter[:, 0:3])
    time.sleep(1)

sense.clear()
