# Adafruit Dotstar RGB LED Strip
#
# Cycle through many sequence patterns

# Import required libraries
import sys
import argparse
import board
import adafruit_dotstar as dotstar
import time
from sequences import *

def fade_component(start, finish, step, steps):
    if (start > finish):
        value = start - ((start - finish) * (step / (steps-1)))
    else:
        value = start + ((finish - start) * (step / (steps-1)))
    return value

def fade_colors(colors_1, colors_2):

    steps = 50

    # Loop through steps
    for x in range(0, steps):

        # Initialize array
        for i in range(number_of_leds):

            # Calculate color components
            r = fade_component(colors_1[i][0], colors_2[i][0], x, steps)
            g = fade_component(colors_1[i][1], colors_2[i][1], x, steps)
            b = fade_component(colors_1[i][2], colors_2[i][2], x, steps)

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

    return

# Parse input
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--brightness", type=float, help="Set the LED brigtness, 0.0 to 1.0")
parser.add_argument("-d", "--delay", type=float, help="Set the frame delay in seconds")
args = parser.parse_args()

# Set Brightness
brightness = 0.5
if args.brightness:
    if float(args.brightness) > 0.0 and float(args.brightness) <= 1.0:
        brightness = args.brightness

# Set time delay between frames
frame_delay = 0.03;
if args.delay:
    if float(args.delay) > 0.0 and float(args.delay) <= 1.0:
        frame_delay = args.delay

# Specify number of pixels
number_of_leds = 119;

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, number_of_leds, brightness=0.8, auto_write=False)

# Initialize position
offset = 0

new_sequence = 1

# Count revolutions
revolutions = 0;
steps_per_revolution = int(number_of_leds)

# Load an list of RGB colors for every possible color
spectrum_colors = get_sinebow_colors(number_of_leds)

# Debugging
# for loop_step in range(spectrum_steps):
    # print(spectrum_colors[loop_step][0], spectrum_colors[loop_step][1], spectrum_colors[loop_step][2], sep="\t")

# Initialize list
dot_colors = [0] * number_of_leds

# Turn on sequence
dot_colors = [(0, 0, 0)] * number_of_leds
for i in range(number_of_leds):
    dots.brightness = brightness
    dot_colors[i] = spectrum_colors[i]
    for i in range(number_of_leds):
        dots[i] = dot_colors[i]
    dots.show()
    time.sleep(0.01)
time.sleep(2)

# Loop forever
time_0 = time.time()
while True:

    time_now = time.time()

    if (time_now - time_0) < 5:

        dot_colors = [(255, 255, 255)] * number_of_leds
        brightness = breathe(number_of_leds, offset)

    elif (time_now - time_0) < 10:


        new_dot_colors = halves(number_of_leds, offset)

        if new_sequence == 1:
            prev_dot_colors = dot_colors
            fade_colors(prev_dot_colors, new_dot_colors)
            new_dot_colors = dot_colors
            new_sequence = 0


    else:

        break;

    # Set brightness
    dots.brightness = brightness

    # Assign pattern colors to Dotstar object
    for i in range(number_of_leds):
        dots[i] = dot_colors[i]

    # Render LEDs
    dots.show()

    # Count total revolutions
    # if (offset + 1) == steps_per_revolution:
        # revolutions += 1

    # Increment offset
    offset = (offset + 1) % steps_per_revolution

    # Stop after 1 revolution
    # if revolutions == 1:
        # quit()

    # Delay before iterating through loop
    time.sleep(frame_delay)

# Turn Off Sequence
brightness_start = brightness
fade_off_frames = 20
for i in range(fade_off_frames):
    dots.brightness = brightness - (brightness_start * (i/fade_off_frames))
    dots.show()
    time.sleep(frame_delay)
dots.deinit()
quit()
