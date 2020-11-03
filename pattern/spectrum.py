import math

def rotate_list(my_list, position):
    return my_list[position:] + my_list[:position]

def spectrum(type = "linear", samples = 255 * 6):
    """Create an array of RGB tuples that define a spectrum of colors (Red, Yellow, Green, Cyan, Blue, Magenta)

    Keyword arguments:
    samples -- The number of distinct colors in the spectrum
    """

    if type == "sinebow":

        return sinebow(samples)

    # Define the maximum value for the RGB values
    max_value = 255

    # Define the number of bands in the spectrum (Red, Yellow, Green, Cyan, Blue, Magenta)
    spectrum_bands=6

    # Initialize RGB values
    r = 0
    g = 0
    b = 0

    # Initialize result array
    spectrum_colors = [0] * samples

    # Loop through full spectrum one time
    for loop_step in range(samples):

        # Divide the spectrum into 6 segments (Red, Yellow, Green, Cyan, Blue, Magenta)
        spectrum_band = math.floor(loop_step/(samples/spectrum_bands))
        if spectrum_band == 0:
            r = max_value
            g = max_value * (loop_step - (0/spectrum_bands) * samples) / (samples/spectrum_bands) # ramp up
            b = 0
        elif spectrum_band == 1:
            r = max_value - max_value * (loop_step - (1/spectrum_bands) * samples) / (samples/spectrum_bands) # ramp down
            g = max_value
            b = 0
        elif spectrum_band == 2:
            r = 0
            g = max_value
            b = max_value * (loop_step - (2/spectrum_bands) * samples) / (samples/spectrum_bands) # ramp up
        elif spectrum_band == 3:
            r = 0
            g = max_value - max_value * (loop_step - (3/spectrum_bands)*samples) / (samples/spectrum_bands) # ramp down
            b = max_value
        elif spectrum_band == 4:
            r = max_value * (loop_step - ((4/spectrum_bands)*samples)) / (samples/spectrum_bands) # ramp up
            g = 0
            b = max_value
        elif spectrum_band == 5:
            r = max_value
            g = 0
            b = max_value - max_value * (loop_step - (5/spectrum_bands)*samples) / (samples/spectrum_bands) # ramp down

        spectrum_colors[loop_step] = (int(r), int(g), int(b))

    return spectrum_colors

# - https://observablehq.com/@mbostock/sinebow
#   - https://krazydad.com/tutorials/makecolors.php
#     - http://basecase.org/env/on-rainbows
def sinebow(samples = 255 * 6):

    r = 0;
    g = 0;
    b = 0;

    # Initialize result array
    spectrum_colors = [0] * samples

    # Loop through full spectrum one time
    for loop_step in range(samples):

        r = math.sin((2*math.pi) * (loop_step/samples + 0)) * 127.0 + 128
        g = math.sin((2*math.pi) * (loop_step/samples + 0) + (2.0 * (math.pi)/3.0)) * 127.0 + 128
        b = math.sin((2*math.pi) * (loop_step/samples + 0) + (4.0 * (math.pi)/3.0)) * 127.0 + 128

        spectrum_colors[loop_step] = (int(r), int(g), int(b))

    # Shift the values to match the linear spectrum
    # This is arbitrary and not required, but it makes these 2 techniques line up
    spectrum_colors.reverse();
    spectrum_colors = rotate_list(spectrum_colors, -31)

    return spectrum_colors
