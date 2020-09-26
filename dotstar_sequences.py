# Adafruit Dotstar RGB LED Strip
#
# Display a rainbow spectrum across the range of all LEDs

# Import required libraries
import sys
import argparse
import board
import adafruit_dotstar as dotstar
import time
from sequences import *

# Parse input
parser = argparse.ArgumentParser()
parser.add_argument("pattern", type=str, choices=[
    "breathe",
    "halves",
    "halves_gradient",
    "off",
    "one_dot",
    "opposite_dots",
    "solid_white",
    "spectrum",
    "spectrum_fade",
    "spectrum_slide",
    "spectrum_straight_across",
    "spectrum_straight_across_with_rotation",
    "stripes_spin"
    ],
    help="Specify the pattern to display"
)
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

# Option 2: Using a DotStar Digital LED Strip with LEDs connected to digital pins
# dots = dotstar.DotStar(board.D6, board.D5, 120)

# Initialize position
offset = 0

# Count revolutions
revolutions = 0;
steps_per_revolution = int(number_of_leds)

# Load an array(?) of RGB colors for every possible color
spectrum_steps = int(number_of_leds)
# spectrum_steps = 255 * 6
# spectrum_colors = get_spectrum_colors(spectrum_steps)
spectrum_colors = get_sinebow_colors(spectrum_steps)

# Debugging
# for loop_step in range(spectrum_steps):
    # print(spectrum_colors[loop_step][0], spectrum_colors[loop_step][1], spectrum_colors[loop_step][2], sep="\t")

# Initialize array
dot_colors = [0] * number_of_leds

# Non-looping "sequences"
if args.pattern == "off":
    dots.deinit();
    quit();
elif args.pattern == "solid_white":
    dots.brightness = brightness
    dots.fill((255, 255, 255))
    dots.show()
    quit();
elif args.pattern == "spectrum":
    dots.brightness = brightness
    dot_colors = spectrum_colors
    for i in range(number_of_leds):
        dots[i] = dot_colors[i]
    dots.show()
    quit();

# Loop forever
while True:

    # Select pattern
    if args.pattern:
        if args.pattern == "breathe":

            dot_colors = [(255, 255, 255)] * number_of_leds
            brightness = breathe(number_of_leds, offset)

        if args.pattern == "one_dot":

            dot_colors = one_dot(number_of_leds, offset)

        elif args.pattern == "opposite_dots":

            dot_colors = opposite_dots(number_of_leds, offset)

        elif args.pattern == "halves":

            dot_colors = halves(number_of_leds, offset)

        elif args.pattern == "halves_gradient":

            dot_colors = halves_gradient(number_of_leds, offset)

        elif args.pattern == "spectrum_fade":

            steps_per_revolution = len(spectrum_colors)
            dot_colors = spectrum_fade(number_of_leds, offset, spectrum_colors)

        elif args.pattern == "spectrum_slide":

            dot_colors = spectrum_slide(number_of_leds, offset, spectrum_colors)

        elif args.pattern == "spectrum_straight_across":

            dot_colors = spectrum_straight_across(number_of_leds, offset, spectrum_colors)

        elif args.pattern == "spectrum_straight_across_with_rotation":

            dot_colors = spectrum_straight_across_with_rotation(number_of_leds, revolutions, offset, spectrum_colors)

        elif args.pattern == "stripes_spin":

            dot_colors = stripes_spin((200, 0, 0), (0,0,255), number_of_leds, offset)

    else:
        dot_colors = spectrum_straight_across(number_of_leds, offset, spectrum_colors)

    # Set brightness
    dots.brightness = brightness

    # Assign pattern colors to Dotstar object
    for i in range(number_of_leds):
        dots[i] = dot_colors[i]

    # Render LEDs
    dots.show()

    # Count total revolutions
    if (offset + 1) == steps_per_revolution:
        revolutions += 1

    # Increment offset
    offset = (offset + 1) % steps_per_revolution

    # Stop after 1 revolution
    # if revolutions == 1:
        # quit()

    # Delay before iterating through loop
    time.sleep(frame_delay)
