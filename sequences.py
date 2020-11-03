import colorsys
import math

def rotate_list(my_list, position):
    return my_list[position:] + my_list[:position]

# - https://observablehq.com/@mbostock/sinebow
#   - https://krazydad.com/tutorials/makecolors.php
#     - http://basecase.org/env/on-rainbows
def get_sinebow_colors(spectrum_steps = 255 * 6):

    r = 0;
    g = 0;
    b = 0;

    # Initialize result array
    spectrum_colors = [0] * spectrum_steps

    # Loop through full spectrum one time
    for loop_step in range(spectrum_steps):

        r = math.sin((2*math.pi) * (loop_step/spectrum_steps + 0)) * 127.0 + 128
        g = math.sin((2*math.pi) * (loop_step/spectrum_steps + 0) + (2.0 * (math.pi)/3.0)) * 127.0 + 128
        b = math.sin((2*math.pi) * (loop_step/spectrum_steps + 0) + (4.0 * (math.pi)/3.0)) * 127.0 + 128

        spectrum_colors[loop_step] = (int(r), int(g), int(b))

    # Shift the values to match get_spectrum_colors
    # This is arbitrary and not required, but it makes these 2 techniques line up
    spectrum_colors.reverse();
    spectrum_colors = rotate_list(spectrum_colors, -31)

    return spectrum_colors

def get_spectrum_colors(spectrum_steps = 255 * 6):
    """Create an array of RGB tuples that define a spectrum of colors (Red, Yellow, Green, Cyan, Blue, Magenta)

    Keyword arguments:
    spectrum_steps -- The number of distinct colors in the spectrum
    """

    # Define the maximum value for the RGB values
    max_value = 255

    # Define the number of bands in the spectrum (Red, Yellow, Green, Cyan, Blue, Magenta)
    spectrum_bands=6

    # Initialize RGB values
    r = 0
    g = 0
    b = 0

    # Initialize result array
    spectrum_colors = [0] * spectrum_steps

    # Loop through full spectrum one time
    for loop_step in range(spectrum_steps):

        # Divide the spectrum into 6 segments (Red, Yellow, Green, Cyan, Blue, Magenta)
        spectrum_band = math.floor(loop_step/(spectrum_steps/spectrum_bands))
        if spectrum_band == 0:
            r = max_value
            g = max_value * (loop_step - (0/spectrum_bands) * spectrum_steps) / (spectrum_steps/spectrum_bands) # ramp up
            b = 0
        elif spectrum_band == 1:
            r = max_value - max_value * (loop_step - (1/spectrum_bands) * spectrum_steps) / (spectrum_steps/spectrum_bands) # ramp down
            g = max_value
            b = 0
        elif spectrum_band == 2:
            r = 0
            g = max_value
            b = max_value * (loop_step - (2/spectrum_bands) * spectrum_steps) / (spectrum_steps/spectrum_bands) # ramp up
        elif spectrum_band == 3:
            r = 0
            g = max_value - max_value * (loop_step - (3/spectrum_bands)*spectrum_steps) / (spectrum_steps/spectrum_bands) # ramp down
            b = max_value
        elif spectrum_band == 4:
            r = max_value * (loop_step - ((4/spectrum_bands)*spectrum_steps)) / (spectrum_steps/spectrum_bands) # ramp up
            g = 0
            b = max_value
        elif spectrum_band == 5:
            r = max_value
            g = 0
            b = max_value - max_value * (loop_step - (5/spectrum_bands)*spectrum_steps) / (spectrum_steps/spectrum_bands) # ramp down

        spectrum_colors[loop_step] = (int(r), int(g), int(b))

    return spectrum_colors

# ROYGBIV
def get_rainbow_colors(method):

    # Method 1: Pre-set
    if method == 1:
        return [
            (255,0,0),
            (255,165,0),
            (255,255,0),
            (0,128,0),
            (0,0,255),
            (75,0,130),
            (238,130,238)
        ]

    # Method 2: Calculated (not very good)
    # [(255, 0, 0), (255, 218, 0), (72, 255, 0), (0, 255, 145), (0, 145, 255), (72, 0, 255), (255, 0, 218)]
    rainbow = [(0,0,0)] * 7
    for i in range(7):
        color = colorsys.hsv_to_rgb(i/7, 1, 1);
        rainbow[i] = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
    # print(rainbow)

    return rainbow

# Draw one pixel that moves across the LED strip
def one_dot(number_of_leds, offset):

    # Initialization. Fill an array of length "number_of_leds" with zeros
    strip_colors = [(2,2,2)] * number_of_leds

    # Turn on selected LED pixel
    strip_colors[offset] = (255,255,255)

    return strip_colors

# Draw two pixels that moves across the LED strip (circle) opposite of each other
def opposite_dots(number_of_leds, offset):

    # Fill all to black (off)
    strip_colors = [(0, 0, 0)] * number_of_leds

    # Turn on selected LED pixel
    strip_colors[offset] = (255,255,255)

    # Turn on LED opposite of that one
    opposite = (offset + int(number_of_leds/2)) % number_of_leds
    strip_colors[opposite] = (255,255,255)

    return strip_colors

# Draw 2 different halvs of color (non rotating)
def halves(number_of_leds, offset):

    # Fill all to black (off)
    strip_colors = [(255, 0, 0)] * number_of_leds

    # Fill first half of LEDs with different color
    for i in range(int(number_of_leds/2)):
        strip_colors[i] = (0,0,255)

    return strip_colors

# Alternate pixels between 2 colors
def stripes_spin(color_1, color_2, number_of_leds, offset, num_stripes = 6):

    # Initialization. Fill an array of length "number_of_leds" with zeros
    strip_colors = [(0, 0, 0)] * number_of_leds

    # fill "strip_colors" with calculated RGB tuples
    for i in range(number_of_leds):
        strip_colors[i] = color_1
        if (math.floor(i/(number_of_leds/num_stripes)) % 2):
            strip_colors[i] = color_2

    # Rotate colors
    strip_colors = rotate_list(strip_colors, offset)

    return strip_colors

# Fade through all the colors of the spectrum
def spectrum_fade(number_of_leds, offset, spectrum_colors):

    # Fill an array of length "number_of_leds" with zeros
    return [spectrum_colors[offset]] * number_of_leds

# Slide the spectrum across the strip
def spectrum_slide(number_of_leds, offset, spectrum_colors):

    # Initialization. Fill an array of length "number_of_leds" with zeros
    strip_colors = [0] * number_of_leds

    # "dots" can't be assigned directly because it's a "dostar" object, not an array
    # strip_colors = rotate_list(strip_colors, offset)
    for i in range(number_of_leds):
        index = (offset + i) % len(spectrum_colors)
        strip_colors[i] = spectrum_colors[index]

    return strip_colors

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
