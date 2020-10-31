# Simulate a sequence as an animated GIF

from pathlib import Path
from PIL import Image, ImageDraw
import math
from sequence.fire import *
from sequence.cuttlefish import *

NUMBER_OF_LEDS = 119

# Set Sequence
frame_delay = 1/20
Sequence = Cuttlefish(NUMBER_OF_LEDS)
Sequence.setup()
sequence_length = 200

# Define where to save the image
output_filepath = Path(__file__).parent / "demo/cuttlefish.gif"

# A list of images to compose the animation
images = []

# Create empty black canvas
WIDTH = 256
HEIGHT = 256

ANGLE_OFFSET = ((1/NUMBER_OF_LEDS) / 2) * (2 * math.pi)
RADIUS = (WIDTH * 0.9) / 2

# for y in range(source_image.size[1]):
for y in range(sequence_length):

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

# Save animated gif
images[0].save(
    output_filepath,
    save_all=True,
    append_images=images[1:],
    optimize=False,
    duration=(frame_delay) * 1000,
    loop=0
)
