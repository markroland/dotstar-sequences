import colorsys
import math

def rotate_list(my_list, position):
    return my_list[position:] + my_list[:position]

# Slide a color spectrum straight across the table
def spectrum_straight_across(number_of_leds, offset, spectrum_colors):

    # Initialization. Fill an array of length "number_of_leds" with zeros
    strip_colors = [0] * number_of_leds

    # Fill dots object with values from "spectrum".
    # "dots" can't be assigned directly because it's a "dostar" object, not an array
    # strip_colors = rotate_list(strip_colors, offset)
    for i in range(number_of_leds):
        if i < number_of_leds/2:
            index = (offset + i) % len(spectrum_colors)
        else:
            index = (offset + (number_of_leds - i)) % len(spectrum_colors)
        strip_colors[i] = spectrum_colors[index]

    return strip_colors

# Slide a color spectrum straight across the table, while rotating the angle of slid
def spectrum_straight_across_with_rotation(number_of_leds, revolutions, offset, spectrum_colors):

    # Initialization. Fill an array of length "number_of_leds" with zeros
    strip_colors = [0] * number_of_leds

    # Fill dots object with values from "spectrum".
    # "dots" can't be assigned directly because it's a "dostar" object, not an array
    # strip_colors = rotate_list(strip_colors, offset)
    for i in range(number_of_leds):
        if i < number_of_leds/2:
            index = (offset + i) % len(spectrum_colors)
        else:
            index = (offset + (number_of_leds - i)) % len(spectrum_colors)
        strip_colors[i] = spectrum_colors[index]

    # Rotate starting point once every revolution
    strip_colors = rotate_list(strip_colors, revolutions % math.floor(number_of_leds/2))

    return strip_colors
