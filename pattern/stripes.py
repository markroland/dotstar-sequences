import math

def stripes(color_1, color_2, number_of_leds, num_stripes = 6):

    # Initialization. Fill an array of length "number_of_leds" with zeros
    pixels = [(0, 0, 0)] * number_of_leds

    # fill "pixels" with calculated RGB tuples
    for i in range(number_of_leds):
        pixels[i] = color_1
        if (math.floor(i/(number_of_leds/num_stripes)) % 2):
            pixels[i] = color_2

    return pixels
