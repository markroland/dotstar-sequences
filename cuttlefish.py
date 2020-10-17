# Adafruit Dotstar RGB LED Strip
#
# Cycle through many sequence patterns

# Import required libraries
import board
import adafruit_dotstar as dotstar
import time
import colorsys
from sequences import *

def render(colors):

    # Assign pattern colors to Dotstar object
    for i in range(number_of_leds):
        dots[i] = colors[i]

    # Render LEDs
    dots.show()

def darken(color, darken):

    h = colorsys.rgb_to_hsv(color[0], color[1], color[2])[0]
    s = colorsys.rgb_to_hsv(color[0], color[1], color[2])[1]
    v = colorsys.rgb_to_hsv(color[0], color[1], color[2])[2] * darken

    # new_color = colorsys.hsv_to_rgb(h,s,v)
    new_color = colorsys.hsv_to_rgb(h,s,v)

    return (int(new_color[0]), int(new_color[1]), int(new_color[2]))

# Set Brightness
brightness = 0.5

# Set time delay between frames
frame_delay = 1/60;

# Specify number of pixels
number_of_leds = 119;

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, number_of_leds, brightness=brightness, auto_write=False)

# Load a list of RGB colors for every possible color
spectrum_colors = get_sinebow_colors(number_of_leds)

spectrum_offset = 0
brightness_offset = 0

while True:

    # Set colors based on spectrum offset
    dot_colors = [spectrum_colors[spectrum_offset]] * number_of_leds
    spectrum_offset = (spectrum_offset + 1) % len(spectrum_colors)

    # Modulate HSV lightness value

    # This needs to be a function of Pi so there are no discontinuous jumps
    brightness_offset = (math.pi / 12) * spectrum_offset
    waves = 12

    # Method 1: pulses moving in circle
    # for i in range(len(dot_colors)):
    #     lightness_coefficient = 0.6 + (0.4 * math.cos((i/(number_of_leds/waves)) * 2 * math.pi + brightness_offset))
    #     dot_colors[i] = darken(dot_colors[i], lightness_coefficient)

    # Method 2: Two halves of pulses moving in opposite directions
    for i in range(number_of_leds):
        if i < number_of_leds/2:
            lightness_coefficient = 0.6 + (0.4 * math.cos((i/(number_of_leds/waves)) * 2 * math.pi + brightness_offset))
            dot_colors[i] = darken(dot_colors[i], lightness_coefficient)
        else:
            lightness_coefficient = 0.6 + (0.4 * math.cos((i/(number_of_leds/waves)) * 2 * math.pi - brightness_offset))
            dot_colors[i] = darken(dot_colors[i], lightness_coefficient)

    # Render to LED strip
    render(dot_colors)

    # Delay before iterating through loop
    time.sleep(frame_delay)