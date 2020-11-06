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
from sequence.acceleration import *
from sequence.breathe import *
from sequence.clock import *
from sequence.crossing import *
from sequence.cuttlefish import *
from sequence.points import *
from sequence.fade import *
from sequence.fire import *
from sequence.random import *
from sequence.sparkle import *
from sequence.stripes import *
from sequence.textFileDemo import *
import atexit

# Parse input
parser = argparse.ArgumentParser()
parser.add_argument("sequence", type=str, choices=[
    "acceleration",
    "breathe",
    "csv",
    "clock",
    "crossing",
    "cuttlefish",
    "fade",
    "fire",
    "off",
    "on",
    "points",
    "random",
    "sparkle",
    "stripes",
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
if args.sequence == "acceleration":
    Sequence = Acceleration(NUMBER_OF_LEDS)
    Sequence.setup(6)
elif args.sequence == "breathe":
    frame_delay = 1/30
    Sequence = Breathe(NUMBER_OF_LEDS)
    Sequence.setup(0.1, 0.5)
elif args.sequence == "clock":
    frame_delay = 1/10
    Sequence = Clock(NUMBER_OF_LEDS)
    Sequence.setup(75)
elif args.sequence == "crossing":
    # frame_delay = 1/10
    Sequence = Crossing(NUMBER_OF_LEDS)
    hue_1 = random.random()
    # random_hue_2 = random.random()
    hue_2 = hue_1 + 0.5 % 1
    length_1 = int(NUMBER_OF_LEDS * 0.33)
    length_2 = int(NUMBER_OF_LEDS * 0.2)
    Sequence.setup(hue_1, hue_2, length_1, length_2)
elif args.sequence == "csv":
    frame_delay = 1/2
    Sequence = TextFileDemo(NUMBER_OF_LEDS)
    Sequence.setup()
elif args.sequence == "cuttlefish":
    Sequence = Cuttlefish(NUMBER_OF_LEDS)
    Sequence.setup()
elif args.sequence == "fade":
    Sequence = Fade(NUMBER_OF_LEDS)
    colors_start = [(0,0,255)] * NUMBER_OF_LEDS
    colors_end = [(255,255,0)] * NUMBER_OF_LEDS
    Sequence.setup("hsv", 10, colors_start, colors_end)
elif args.sequence == "fire":
    frame_delay = 1/20
    Sequence = Fire(NUMBER_OF_LEDS)
    Sequence.setup()
elif args.sequence == "off":
    dots.fill((0, 0, 0))
    dots.deinit();
    quit();
elif args.sequence == "on":
    dot_colors = [(255, 255, 255)] * NUMBER_OF_LEDS
elif args.sequence == "points":
    frame_delay = 1/20
    Sequence = Points(NUMBER_OF_LEDS)
    Sequence.setup(-1, 6, 5, (255, 0, 0))
elif args.sequence == "random":
    Sequence = Random(NUMBER_OF_LEDS)
    Sequence.setup()
elif args.sequence == "sparkle":
    Sequence = Sparkle(NUMBER_OF_LEDS)
    Sequence.setup()
elif args.sequence == "stripes":
    Sequence = Stripes(NUMBER_OF_LEDS)
    Sequence.setup(-1, 4)
elif args.sequence == "white":
    dot_colors = [(255, 255, 255)] * NUMBER_OF_LEDS


# Shutdown function to turn lights off if script exits
def shutdown():
    brightness_start = brightness
    fade_off_frames = 60
    for i in range(fade_off_frames):
        dots.brightness = brightness - (brightness_start * (i/fade_off_frames))
        dots.show()
        time.sleep(1/60)
    dots.deinit()

# Register shutdown function
atexit.register(shutdown)


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
