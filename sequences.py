import math

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

def rotate_list(my_list, position):
    return my_list[position:] + my_list[:position]

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
# INCOMPLETE:
def stripes_spin(number_of_leds, offset, num_stripes = 6):

    # Define colors
    color_1 = (200, 0, 0)
    color_2 = (0,0,255)

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

# Alternate pixels between 2 colors
def spectrum_slide(number_of_leds, offset, spectrum_colors):

    # Initialization. Fill an array of length "number_of_leds" with zeros
    strip_colors = [0] * number_of_leds

    # Fill dots object with values from "spectrum".
    # "dots" can't be assigned directly because it's a "dostar" object, not an array
    # strip_colors = rotate_list(strip_colors, offset)
    for i in range(number_of_leds):
        index = (offset + i) % len(spectrum_colors)
        strip_colors[i] = spectrum_colors[index]

    return strip_colors

# Alternate pixels between 2 colors
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

# Draw 2 different halves of color, with a gradient in between
# INCOMPLETE: Logic for color section not right
def halves_gradient(number_of_leds, offset):

    # Initialization. Fill an array of length "number_of_leds" with zeros
    strip_colors = [(0,0,0)] * number_of_leds

    # Fill first half of LEDs with different color
    for i in range(number_of_leds):
        if (i < int((1/4) * number_of_leds)):
            strip_colors[i] = (0,0,255)
        elif (i < int((2/4) * number_of_leds)):
            strip_colors[i] = (int(255 * ((i-29)/30)), 0, 255)
        elif (i < int((3/4) * number_of_leds)):
            strip_colors[i] = (255,0,0)
        else:
            strip_colors[0] = (0,255,0)

    return strip_colors

# Fade lights on and off, like breathing
# Human breathing is between 12-25 breathes/minute
# 15 breathes/minute is 1 breathe every 4 seconds
# With 129 LEDs a delay of 0.3 seconds (4/129) will accurately represent breathing
def breathe(number_of_leds, offset):

    # Brightness values must be between 0.0 and 1.0
    max_brightness = 0.5
    min_brightness = 0.1

    brightness = 0.5 + (0.5 * math.sin((offset / number_of_leds) * 2 * math.pi))

    brightness = brightness * (max_brightness - min_brightness) + min_brightness

    return max_brightness * brightness
