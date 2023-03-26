#!/usr/bin/python

import numpy as np
from PIL import Image, ImageChops
from sense_hat import SenseHat


def main():
    sense = SenseHat()
    sense.set_rotation(90)

    # load a PNG from file
    img = Image.open("0.png")

    last_direction = ""

    try:
        while True:
            direction = find_dir(sense.compass)
            # sense.show_message(direction)
            if last_direction != direction:
                show_arrow(img, sense)
                print(direction)
            last_direction = direction
    except:
        print("\n Quitting")
        sense.clear()


def find_dir(deg):
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
    return directions[index]


def show_arrow(img, sense):
    # Rotate and invert the pixel values
    inverted = ImageChops.invert(
        img.rotate(angle=sense.compass, fillcolor=(255, 255, 255))
    )
    # Convert to Numpy array and flatten rows and columns
    flat = np.array(inverted).reshape(64, 4)
    # remove alpha value from RGBA and write to matrix array
    sense.set_pixels(flat[:, 0:3])


if __name__ == "__main__":
    main()
