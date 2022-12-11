from sense_hat import SenseHat
from PIL import Image, ImageChops
import numpy as np
import time

sense = SenseHat()

# load a PNG from file
img = Image.open('0.png')

for i in [45, 90, 135, 180, 225, 270, 315, 360]:
	rotated = img.rotate(i)

	# Invert the pixel values
	inverted = ImageChops.invert(rotated)

	# Convert to Numpy array
	inv_arry = np.array(inverted)
	# flatten rows and columns
	flatter = inv_arry.reshape(64,4)
	# remove the alpha value from RGBA
	new = flatter[:, 0:3]
	# Write to matrix array
	sense.set_pixels(new)
	time.sleep(1)

sense.clear()
