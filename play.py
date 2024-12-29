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
from dotenv import load_dotenv
import os
from pattern.rainbow import *
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
from sequence.spectrum import *
from sequence.stripes import *
from sequence.textFileDemo import *
from sequence.wipe import *
import atexit

supported_sequences = [
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
    "rainbow",
    "random",
    "sparkle",
    "spectrum-fade",
    "spectrum-slide",
    "spectrum-wipe",
    "stripes",
    "white",
    "wipe"
]

# Parse input
parser = argparse.ArgumentParser()
parser.add_argument("sequence", nargs='?', type=str, choices=supported_sequences,
    help="Specify the sequence to play"
)
parser.add_argument("-b", "--brightness", type=float, help="Set the LED brigtness, 0.0 to 1.0")
parser.add_argument("-d", "--delay", type=float, help="Set the frame delay in seconds")
args = parser.parse_args()

# Set defaults prior to input
load_dotenv()
NUMBER_OF_LEDS = int(os.environ.get("NUMBER_OF_LEDS"))
brightness = float(os.environ.get("DEFAULT_BRIGHTNESS"))
frame_delay = float(os.environ.get("DEFAULT_FRAME_DELAY"))

if args.sequence is None:

    print('Please select a sequence number')
    for i in range(len(supported_sequences)):
        print((i+1), ") ", supported_sequences[i], sep='')

    x = input('Selection: ')

    selected_sequence = supported_sequences[int(x) - 1]

else:

    selected_sequence = args.sequence

    # Set Brightness
    if args.brightness:
        if float(args.brightness) > 0.0 and float(args.brightness) <= 1.0:
            brightness = args.brightness

    # Set time delay between frames
    if args.delay:
        if float(args.delay) > 0.0 and float(args.delay) <= 1.0:
            frame_delay = args.delay

# Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, NUMBER_OF_LEDS, brightness=brightness, auto_write=False)

# Initialize sequence
Sequence = None
if selected_sequence == "acceleration":
    Sequence = Acceleration(NUMBER_OF_LEDS)
    Sequence.setup(6)
elif selected_sequence == "breathe":
    frame_delay = 1/30
    Sequence = Breathe(NUMBER_OF_LEDS)
    Sequence.setup(0.1, 0.5)
elif selected_sequence == "clock":
    frame_delay = 1/10
    Sequence = Clock(NUMBER_OF_LEDS)
    Sequence.setup(75)
elif selected_sequence == "crossing":
    # frame_delay = 1/10
    Sequence = Crossing(NUMBER_OF_LEDS)
    hue_1 = random.random()
    # random_hue_2 = random.random()
    hue_2 = hue_1 + 0.5 % 1
    length_1 = int(NUMBER_OF_LEDS * 0.33)
    length_2 = int(NUMBER_OF_LEDS * 0.2)
    Sequence.setup(hue_1, hue_2, length_1, length_2)
elif selected_sequence == "csv":
    frame_delay = 1/2
    Sequence = TextFileDemo(NUMBER_OF_LEDS)
    Sequence.setup("data/blink-magenta.csv")
elif selected_sequence == "cuttlefish":
    Sequence = Cuttlefish(NUMBER_OF_LEDS)
    Sequence.setup()
elif selected_sequence == "fade":
    Sequence = Fade(NUMBER_OF_LEDS)
    colors_start = [(0,0,255)] * NUMBER_OF_LEDS
    colors_end = [(255,255,0)] * NUMBER_OF_LEDS
    Sequence.setup("hsv", 10, colors_start, colors_end)
elif selected_sequence == "fire":
    frame_delay = 1/20
    Sequence = Fire(NUMBER_OF_LEDS)
    Sequence.setup("data/fire.png")
elif selected_sequence == "off":
    dots.fill((0, 0, 0))
    dots.deinit()
    quit()
elif selected_sequence == "on":
    dot_colors = [(255, 255, 255)] * NUMBER_OF_LEDS
elif selected_sequence == "points":
    frame_delay = 1/20
    Sequence = Points(NUMBER_OF_LEDS)
    Sequence.setup(-1, 6, 5, (255, 0, 0))
elif selected_sequence == "rainbow":
    dot_colors = [(0,0,0)] * NUMBER_OF_LEDS
    colors = rainbow(1)
    for i in range(NUMBER_OF_LEDS):
        rainbow_index = math.floor((i/NUMBER_OF_LEDS) * len(colors))
        dot_colors[i] = colors[rainbow_index]
elif selected_sequence == "random":
    Sequence = Random(NUMBER_OF_LEDS)
    Sequence.setup()
elif selected_sequence == "sparkle":
    Sequence = Sparkle(NUMBER_OF_LEDS)
    Sequence.setup()
elif selected_sequence == "spectrum-fade":
    Sequence = Spectrum(NUMBER_OF_LEDS)
    Sequence.setup("sinebow", "fade", 60)
elif selected_sequence == "spectrum-slide":
    Sequence = Spectrum(NUMBER_OF_LEDS)
    Sequence.setup("sinebow", "slide", 3)
elif selected_sequence == "spectrum-wipe":
    Sequence = Spectrum(NUMBER_OF_LEDS)
    Sequence.setup("sinebow", "wipe", 3)
elif selected_sequence == "stripes":
    Sequence = Stripes(NUMBER_OF_LEDS)
    Sequence.setup(-1, 4)
elif selected_sequence == "white":
    dot_colors = [(255, 255, 255)] * NUMBER_OF_LEDS
elif selected_sequence == "wipe":
    Sequence = Wipe(NUMBER_OF_LEDS)
    hue_1 = random.random()
    # random_hue_2 = random.random()
    hue_2 = hue_1 + 0.5 % 1
    Sequence.setup(6, hue_1, hue_2, -45)

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
