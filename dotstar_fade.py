# Adafruit Dotstar RGB LED Strip Fade
#
# Fade all pixels from one color to another

# Import required libraries
import board
import adafruit_dotstar
from sequences import *
import random
import time

def random_color():
    return random.randrange(0, 255)
    # return random.randrange(1, 7) * 32

def fade_component(start, finish, step, steps):
    if (start > finish):
        value = start - ((start - finish) * (step / (steps-1)))
    else:
        value = start + ((finish - start) * (step / (steps-1)))
    return value

# Specify number of pixels
number_of_leds = 119;

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = adafruit_dotstar.DotStar(board.SCK, board.MOSI, number_of_leds, brightness=0.5, auto_write=False)

# Frame period in seconds
frame_delay = 0.03

# Number of steps between 2 colors
steps = 50

# Initialize output color array
dot_colors = [(255,255,255)] * number_of_leds

# Initialize starting colors
colors_start = [(255,255,255)] * number_of_leds

# Random colors
# for i in range(number_of_leds):
#     colors_start[i] = ((random_color(), random_color(), random_color()))
#     # print(colors_start[i][0], colors_start[i][1], colors_start[i][2], sep="\t")

colors_start = get_sinebow_colors(number_of_leds)

# Ending colors
colors_end = [(0,0,255)] * number_of_leds

# Set brightness
dots.brightness = 0.5

# Loop through steps
for x in range(0, steps):

    # Initialize array
    for i in range(number_of_leds):

        # Calculate color components
        r = fade_component(colors_start[i][0], colors_end[i][0], x, steps)
        g = fade_component(colors_start[i][1], colors_end[i][1], x, steps)
        b = fade_component(colors_start[i][2], colors_end[i][2], x, steps)

        # Assign RGB to all LEDs
        dot_colors[i] = (int(r), int(g), int(b))

        # Debugging
        # if x == steps - 1:
            # print(i, dot_colors[i][0], dot_colors[i][1], dot_colors[i][2], sep="\t")

    # Debugging
    # print(color_1[1], colors_end[1], sep="\t")
    # print(dot_colors[118][0], dot_colors[118][1], dot_colors[118][2], sep="\t")

    # Assign colors to Dotstar object
    for i in range(number_of_leds):
        dots[i] = dot_colors[i]

    # Render LEDs
    dots.show()

    # Delay before iterating through loop
    time.sleep(frame_delay)
