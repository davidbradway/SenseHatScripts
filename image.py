#!/usr/bin/python

from sense_hat import SenseHat
from PIL import Image, ImageChops
import numpy as np
import time


if __name__ == "__main__":
    sense = SenseHat()

    B = (0,0,0)
    W = (255,255,255)
    
    l = ((B,B,B,W,W,B,B,B),
         (B,B,W,W,W,W,B,B),
         (B,W,W,W,W,W,W,B),
         (W,W,W,W,W,W,W,W),
         (B,B,B,W,W,B,B,B),
         (B,B,B,W,W,B,B,B),
         (B,B,B,W,W,B,B,B),
         (B,B,B,W,W,B,B,B))
    array = np.array(l, dtype=np.uint8)
    img = Image.fromarray(array)

    for i in np.linspace(0, 360, 17):
        # Rotate the image
        rotated = img.rotate(angle=i, fillcolor=B)

        # Convert back to Numpy array and flatten rows and columns
        flatter = np.array(rotated).reshape(64, 3)

        sense.set_pixels(flatter)
        time.sleep(0.5)

    sense.clear()
