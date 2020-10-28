# Adafruit Dotstar RGB LED Strip
#
# Read a sequence from an image file
#
# Inspired by https://github.com/adafruit/Adafruit_CircuitPython_DotStar/blob/master/examples/dotstar_image_paint.py

# Import required libraries
import board
import adafruit_dotstar as dotstar
import time
from PIL import Image

def render(colors):

    # Assign pattern colors to Dotstar object
    for i in range(number_of_leds):
        dots[i] = colors[i]

    # Render LEDs
    dots.show()

# Set Brightness
brightness = 0.5

# Set time delay between frames
frame_delay = 1/60;

# Specify number of pixels
number_of_leds = 119;

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, number_of_leds, brightness=brightness, auto_write=False)

# Load image in RGB format and get dimensions:
file_source = "data/test.png"
IMG = Image.open(file_source).convert("RGB")
PIXELS = IMG.load()
WIDTH = IMG.size[0]
HEIGHT = IMG.size[1]

# Ignore pixels in image that won't map to the LED Strip
if WIDTH > number_of_leds:
    WIDTH = number_of_leds

# Calculate gamma correction table, makes mid-range colors look "correct"
GAMMA = bytearray(256)
for i in range(256):
    GAMMA[i] = int(pow(float(i) / 255.0, 2.7) * 255.0 + 0.5)

# Loop forever
while True:

    # Loop through rows of image
    for y in range(HEIGHT):

        # Initialize LED list
        dot_colors = [(64, 64, 64)] * number_of_leds

        # Loop through columns of row
        for x in range(WIDTH):

            # Read pixel in image
            value = PIXELS[x, y]

            # Set value with Gamma correction
            dot_colors[x] = (GAMMA[value[0]], GAMMA[value[1]], GAMMA[value[2]])

        # Render to LED strip
        render(dot_colors)

        # Delay before iterating through loop
        time.sleep(frame_delay)
