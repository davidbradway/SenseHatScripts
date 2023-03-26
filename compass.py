#!/usr/bin/python

import numpy as np
from PIL import Image, ImageChops
from sense_hat import SenseHat


def main():
    sense = SenseHat()
    sense.set_rotation(90)

    # load a PNG from file
    img = Image.open("0.png")

    try:
        while True:
            direction = find_dir(sense.compass, img, sense)
            # sense.show_message(direction)
            print(direction)
    except:
        print("\n Quitting")
        sense.clear()


def find_dir(deg, img, sense):
    directions = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
        "N",
    ]
    index = round(deg / 22.5)
    # Rotate and invert the pixel values
    inverted = ImageChops.invert(img.rotate(angle=deg, fillcolor=(255, 255, 255)))
    # Convert to Numpy array and flatten rows and columns
    flatter = np.array(inverted).reshape(64, 4)
    # remove alpha value from RGBA and write to matrix array
    sense.set_pixels(flatter[:, 0:3])
    return directions[index]


if __name__ == "__main__":
    main()
