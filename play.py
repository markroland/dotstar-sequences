# Adafruit Dotstar RGB LED Strip
#
# Play requested sequence

# Import required libraries
import sys
import argparse
import board
import adafruit_dotstar as dotstar
import time
import random
from sequence.cuttlefish import *
from sequence.sparkle import *
import atexit

# Shutdown function to turn lights off if script exits
def shutdown():
    brightness_start = brightness
    fade_off_frames = 20
    for i in range(fade_off_frames):
        dots.brightness = brightness - (brightness_start * (i/fade_off_frames))
        dots.show()
        time.sleep(frame_delay)
    dots.deinit()

# Register shutdown function
atexit.register(shutdown)

# Parse input
parser = argparse.ArgumentParser()
parser.add_argument("sequence", type=str, choices=[
    "cuttlefish",
    "on",
    "sparkle",
    "white"
    ],
    help="Specify the sequence to play"
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
frame_delay = 1/60;
if args.delay:
    if float(args.delay) > 0.0 and float(args.delay) <= 1.0:
        frame_delay = args.delay

# Specify number of pixels
NUMBER_OF_LEDS = 119;

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, NUMBER_OF_LEDS, brightness=brightness, auto_write=False)

# Initialize sequence
Sequence = None
if args.sequence == "cuttlefish":
    Sequence = Cuttlefish(NUMBER_OF_LEDS)
    dot_colors = Sequence.setup()
elif args.sequence == "on":
    dot_colors = [(255, 255, 255)] * NUMBER_OF_LEDS
elif args.sequence == "sparkle":
    Sequence = Sparkle(NUMBER_OF_LEDS)
    dot_colors = Sequence.setup()
elif args.sequence == "white":
    dot_colors = [(255, 255, 255)] * NUMBER_OF_LEDS

# Loop forever updating the sequence
while True:

    try:

        # Update sequence
        if Sequence is not None:
            dot_colors = Sequence.update()

        # Assign pattern colors to Dotstar object and Render
        for i in range(len(dot_colors)):
            dots[i] = dot_colors[i]
        dots.show()

        # Delay before iterating through loop
        time.sleep(frame_delay)

    except (KeyboardInterrupt, SystemExit):
        quit()
