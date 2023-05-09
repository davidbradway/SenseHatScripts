#!/usr/bin/python

import numpy as np
from PIL import Image, ImageChops
from sense_hat import SenseHat

B = (0, 0, 0)
W = (255, 255, 255)


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
    rotated = img.rotate(angle=round(sense.compass / 22.5) * 22.5, fillcolor=B)
    # Convert to Numpy array and flatten rows and columns
    flat = np.array(rotated).reshape(64, 3)
    # remove alpha value from RGBA and write to matrix array
    sense.set_pixels(flat)


def main():
    sense = SenseHat()
    sense.set_rotation(90)
    
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

    last_direction = ""

    try:
        while True:
            direction = find_dir(sense.compass)
            if last_direction != direction:
                # sense.show_message(sense.compass)
                show_arrow(img, sense)
                # print(sense.compass)
                print(direction)
                last_direction = direction
    except:
        print("\n Quitting")
        sense.clear()


if __name__ == "__main__":
    main()
