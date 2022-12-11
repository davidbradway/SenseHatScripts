from sense_hat import SenseHat
from PIL import Image, ImageChops
import numpy as np

sense = SenseHat()
sense.rotation = 180

# load a PNG from file
img = Image.open('0.png')
# Invert the pixel values
inverted = ImageChops.invert(img)
# Convert to Numpy array
inv_arry = np.array(inverted)
# flatten rows and columns
flatter = inv_arry.reshape(64,4)
# remove the alpha value from RGBA
new = flatter[:, 0:3]
# Write to matrix array
sense.set_pixels(new)
