#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create an animated GIF of an LED Sequence

Example usage:
    python simulate.py breathe

Author: Mark Roland
Date Created: 2020-10-31
"""

from dotenv import load_dotenv
import os
import argparse
from pathlib import Path
from PIL import Image, ImageDraw
import math

from sequence.acceleration import *
from sequence.breathe import *
from sequence.clock import *
from sequence.crossing import *
from sequence.cuttlefish import *
from sequence.fade import *
from sequence.pngFile import *
from sequence.points import *
from sequence.random import *
from sequence.sparkle import *
from sequence.spectrum import *
from sequence.stripes import *
from sequence.textFileDemo import *
# from sequence.wipe import *

load_dotenv()
NUMBER_OF_LEDS = int(os.environ.get("NUMBER_OF_LEDS"))

def sequence_setup(sequence_name):

    # Set the frame delay in seconds
    # A shorter frame delay will result in smoother, longer animations
    # Each Sequence should have a sequence_length calculated that represents
    # the full period of the sequence. Most, if not all, Sequences are calculated
    # using a real-time clock and this should be taken into account.
    frame_delay = 1/20

    # Note: sequence_length represents the number of frames in the animated GIF

    if sequence_name == "acceleration":
        Sequence = Acceleration(NUMBER_OF_LEDS)
        Sequence.setup(6)
        sequence_length = 300
    elif sequence_name == "breathe":
        Sequence = Breathe(NUMBER_OF_LEDS)
        Sequence.setup(0.3, 0.8)
        sequence_length = math.floor(4 / frame_delay)
    elif sequence_name == "clock":
        frame_delay = 1/4
        Sequence = Clock(NUMBER_OF_LEDS)
        display_rotation = math.floor(NUMBER_OF_LEDS * 0.25)
        # print(f"Display rotation: {display_rotation}")
        Sequence.setup(display_rotation)
        sequence_length = 120
    elif sequence_name == "cuttlefish":
        Sequence = Cuttlefish(NUMBER_OF_LEDS)
        Sequence.setup()
        sequence_length = 200
    elif sequence_name == "crossing":
        Sequence = Crossing(NUMBER_OF_LEDS)
        Sequence.setup(0.1, 0.5, 30, 40)
        sequence_length = 200
    elif sequence_name == "csv":
        frame_delay = 1/2
        Sequence = TextFileDemo(NUMBER_OF_LEDS)
        Sequence.setup("data/blink-magenta.csv")
        sequence_length = 2
    elif selected_sequence == "fade":
        Sequence = Fade(NUMBER_OF_LEDS)
        colors_start = [(0,0,255)] * NUMBER_OF_LEDS
        colors_end = [(255,255,0)] * NUMBER_OF_LEDS
        Sequence.setup("hsv", 10, colors_start, colors_end)
        sequence_length = round(10 / frame_delay)
    elif selected_sequence == "fire":
        frame_delay = 1/200
        Sequence = PngFile(NUMBER_OF_LEDS)
        Sequence.setup("data/fire.png")
        height = 500
        sequence_length = height
    elif selected_sequence == "points":
        Sequence = Points(NUMBER_OF_LEDS)
        Sequence.setup(-1, 6, 5, (255, 0, 0))
        sequence_length = 24 # math.floor(NUMBER_OF_LEDS / 5)
    elif selected_sequence == "random":
        frame_delay = 1/10
        Sequence = Random(NUMBER_OF_LEDS)
        Sequence.setup()
        sequence_length = 60
    elif selected_sequence == "sparkle":
        frame_delay = 1/40
        Sequence = Sparkle(NUMBER_OF_LEDS)
        Sequence.setup()
        sequence_length = 200
    elif selected_sequence == "spectrum-fade":
        Sequence = Spectrum(NUMBER_OF_LEDS)
        Sequence.setup("sinebow", "fade", 10)
        # Tje subtracted value is an experimentally determined value to try to make the animation loop seamlessly
        sequence_length = round(10 / frame_delay) - 10
    elif selected_sequence == "spectrum-slide":
        Sequence = Spectrum(NUMBER_OF_LEDS)
        Sequence.setup("sinebow", "slide", 3)
        sequence_length = NUMBER_OF_LEDS
    elif selected_sequence == "spectrum-wipe":
        Sequence = Spectrum(NUMBER_OF_LEDS)
        Sequence.setup("sinebow", "wipe", 3)
        sequence_length = NUMBER_OF_LEDS
    elif selected_sequence == "stripes":
        Sequence = Stripes(NUMBER_OF_LEDS)
        num_stripes = 4
        Sequence.setup(-1, num_stripes)
        sequence_length = math.floor(NUMBER_OF_LEDS / num_stripes) * 2 + 1
    elif selected_sequence == "sunrise":
        Sequence = PngFile(NUMBER_OF_LEDS)
        Sequence.setup("data/sunrise.png")
        height = 500
        sequence_length = height
    else:
        print("Invalid sequence name")
        return None, None # or raise an exception

    return Sequence, sequence_length, frame_delay

# Example: If reading from an image, the sequence length is the height of the image
# sequence_length = source_image.size[1]

# Parse input
supported_sequences = [
    "acceleration",
    "breathe",
    "csv",
    "clock",
    "crossing",
    "cuttlefish",
    "fade",
    "fire",
    "points",
    "random",
    "sparkle",
    "spectrum-fade",
    "spectrum-slide",
    "spectrum-wipe",
    "stripes",
    "sunrise"
    # "wipe"
]
parser = argparse.ArgumentParser()
parser.add_argument("sequence", nargs='?', type=str, choices=supported_sequences,
    help="Specify the sequence to play"
)
args = parser.parse_args()

if args.sequence is None:

    print('Please select a sequence number')
    for i in range(len(supported_sequences)):
        print((i+1), ") ", supported_sequences[i], sep='')

    x = input('Selection: ')

    selected_sequence = supported_sequences[int(x) - 1]

else:

    selected_sequence = args.sequence

Sequence, sequence_length, frame_delay = sequence_setup(selected_sequence)

output_filepath = Path(__file__).parent / "demo" / f"{selected_sequence}.gif"

# A list of images to compose the animation
images = []

# Create empty black canvas
WIDTH = 256
HEIGHT = 256

ANGLE_OFFSET = ((1/NUMBER_OF_LEDS) / 2) * (2 * math.pi)
RADIUS = (WIDTH * 0.9) / 2

for y in range(sequence_length):

    print(f"Frame {y+1} of {sequence_length}")

    dot_colors = Sequence.update()

    im = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(im)

    # Loop through pixels
    for x in range(len(dot_colors)):

        # Set Color
        color = dot_colors[x]

        # Define shape
        angle = math.sin(x/NUMBER_OF_LEDS * 2 * math.pi)
        p1_x = (WIDTH/2) + RADIUS * math.cos(x/NUMBER_OF_LEDS * 2 * math.pi - ANGLE_OFFSET)
        p1_y = (HEIGHT/2) + RADIUS * math.sin(x/NUMBER_OF_LEDS * 2 * math.pi - ANGLE_OFFSET)
        p2_x = (WIDTH/2) + RADIUS * math.cos(x/NUMBER_OF_LEDS * 2 * math.pi + ANGLE_OFFSET)
        p2_y = (HEIGHT/2) + RADIUS * math.sin(x/NUMBER_OF_LEDS * 2 * math.pi + ANGLE_OFFSET)
        p3_x = (WIDTH/2) + 0.9 * RADIUS * math.cos(x/NUMBER_OF_LEDS * 2 * math.pi + ANGLE_OFFSET)
        p3_y = (HEIGHT/2) + 0.9 * RADIUS * math.sin(x/NUMBER_OF_LEDS * 2 * math.pi + ANGLE_OFFSET)
        p4_x = (WIDTH/2) + 0.9 * RADIUS * math.cos(x/NUMBER_OF_LEDS * 2 * math.pi - ANGLE_OFFSET)
        p4_y = (HEIGHT/2) + 0.9 * RADIUS * math.sin(x/NUMBER_OF_LEDS * 2 * math.pi - ANGLE_OFFSET)

        # Draw shape
        draw.polygon([(p1_x, p1_y), (p2_x, p2_y), (p3_x, p3_y), (p4_x, p4_y)], fill = color)

    # Add image to animation
    images.append(im)

    time.sleep(frame_delay)

# Save animated gif
images[0].save(
    output_filepath,
    save_all=True,
    append_images=images[1:],
    optimize=False,
    duration=(frame_delay) * 1000,
    loop=0
)

print(f"Image saved to {output_filepath}")