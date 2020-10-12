# Adafruit Dotstar RGB LED Strip
#
# Display a rainbow spectrum across the range of all LEDs

# Import required libraries
import sys
import argparse
import board
import adafruit_dotstar as dotstar
import time
import random
from sequences import *

# Parse input
parser = argparse.ArgumentParser()
parser.add_argument("pattern", type=str, choices=[
    "breathe",
    "crossing_bands",
    "halves",
    "halves_gradient",
    "off",
    "one_dot",
    "opposite_dots",
    "solid_white",
    "rainbow",
    "spectrum",
    "spectrum_fade",
    "spectrum_slide",
    "spectrum_straight_across",
    "spectrum_straight_across_with_rotation",
    "stripes_spin",
    "sweep"
    ],
    help="Specify the pattern to display"
)
parser.add_argument("-b", "--brightness", type=float, help="Set the LED brigtness, 0.0 to 1.0")
parser.add_argument("-d", "--delay", type=float, help="Set the frame delay in seconds")
args = parser.parse_args()

# Write a List of colors to the Dotstar object and then Show them
def render(colors):

    # Assign pattern colors to Dotstar object
    for i in range(number_of_leds):
        dots[i] = colors[i]

    # Render LEDs
    dots.show()

# Add the RGB components of 2 colors
def colors_add(colors_1, colors_2):

    colors = [(0,0,0)] * number_of_leds

    # Initialize array
    for i in range(number_of_leds):
        # Calculate color components
        r = min(colors_1[i][0] + colors_2[i][0], 255)
        g = min(colors_1[i][1] + colors_2[i][1], 255)
        b = min(colors_1[i][2] + colors_2[i][2], 255)

        # Assign RGB to all LEDs
        colors[i] = (int(r), int(g), int(b))

    return colors

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
dot_colors = [(0,0,0)] * number_of_leds

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

# Initialize timing
time_0 = time.time()
time_now = time_0

# Loop forever
while True:

    # Select pattern
    if args.pattern:
        if args.pattern == "breathe":

            dot_colors = [(255, 255, 255)] * number_of_leds
            brightness = breathe(number_of_leds, offset)

        elif args.pattern == "crossing_bands":

            # Color 1
            length = int(number_of_leds * 0.25)
            colors_1 = [(0, 0, 0)] * number_of_leds
            for i in range(0,length):
                intensity = round(255 * (length - i) / length)
                colors_1[i] = (0,0,intensity)
            colors_1 = rotate_list(colors_1, offset)

            # Color 2 - on "opposite" side of strip going the opposite direction
            length = int(number_of_leds * 0.25)
            colors_2 = [(0, 0, 0)] * number_of_leds
            for i in range(0,length):
                intensity = round(255 * (length - i) / length)
                colors_2[i] = (intensity,0,intensity)
            colors_2.reverse()
            colors_2 = rotate_list(colors_2, -offset)

            # Add colors
            dot_colors = colors_add(colors_1, colors_2)

            render(dot_colors)

            # Increment offset
            offset = (offset + 1) % steps_per_revolution

            # Delay before iterating through loop
            time.sleep(frame_delay * 2)

        elif args.pattern == "one_dot":

            dot_colors = one_dot(number_of_leds, offset)

        elif args.pattern == "opposite_dots":

            dot_colors = opposite_dots(number_of_leds, offset)

        elif args.pattern == "halves":

            dot_colors = halves(number_of_leds, offset)

        elif args.pattern == "halves_gradient":

            dot_colors = halves_gradient(number_of_leds, offset)

        elif args.pattern == "rainbow":

            colors = get_rainbow_colors(1)

            for i in range(number_of_leds):
                rainbow_index = math.floor((i/number_of_leds) * len(colors))
                dot_colors[i] = colors[rainbow_index]

            render(dot_colors)

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

        elif args.pattern == "sweep":

            # # Fill all to black (off)
            # dot_colors = [(0, 0, 0)] * number_of_leds

            # # Turn on selected LED pixel
            # dot_colors[offset] = (255,255,255)

            # # Turn on LED opposite of that one
            # opposite = (offset + int(number_of_leds/2)) % number_of_leds
            # dot_colors[opposite] = (255,255,255)

            # ----

            # Set random color on first iteration only
            try: random_hue
            except NameError: random_hue = random.random()

            # Define Color 1
            # color_1 = (0,64,64)
            color_1_hsv = colorsys.hsv_to_rgb(random_hue, 1.0, 1.0)
            color_1 = (int(color_1_hsv[0] * 255), int(color_1_hsv[1] * 255), int(color_1_hsv[2] * 255))

            # Define Color 2 as an offset from Color 1 around the Hue value of the HSV Color Wheel
            # color_2 = (0,0,64)
            color_2_hsv = colorsys.hsv_to_rgb((random_hue + (1/2)) % 1, 1.0, 1.0)
            color_2 = (int(color_2_hsv[0] * 255), int(color_2_hsv[1] * 255), int(color_2_hsv[2] * 255))

            # Set all
            dot_colors = [color_1] * number_of_leds

            time_now = time.time()

            position = math.sin((2*math.pi) * ((time_now - time_0) / 6))

            # # 0 to 59
            i_position = math.floor(position * (number_of_leds / 4) + (number_of_leds / 4))

            # Top Half
            # dot_colors[i_position] = color_2
            for i in range(i_position):
                dot_colors[i] = color_2

            # Bottom Half
            # dot_colors[(number_of_leds-1) - i_position] = color_2
            for i in range((number_of_leds-1) - i_position, number_of_leds-1, 1):
                dot_colors[i] = color_2

            # Optional: Change orientation for table
            degrees_rotation = -45
            dot_colors = rotate_list(dot_colors, math.floor((degrees_rotation/360) * number_of_leds))

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
