from sense_hat import SenseHat


def main():
    sense = SenseHat()
    sense.set_rotation(180)
    try:
        while True:
            direction = find_dir(sense.compass)
            sense.show_message(direction)
    except:
        sense.clear()


def find_dir(deg):
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW',
                  'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']
    index = round(deg/22.5)
    return directions[index]


if __name__ == '__main__':
    main()

