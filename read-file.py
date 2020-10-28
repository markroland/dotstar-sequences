# Adafruit Dotstar RGB LED Strip
#
# Read a sequence from a text file

# Import required libraries
import board
import adafruit_dotstar as dotstar
import time
import csv

def render(colors):

    # Assign pattern colors to Dotstar object
    for i in range(number_of_leds):
        dots[i] = colors[i]

    # Render LEDs
    dots.show()

# From https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# Set Brightness
brightness = 0.5

# Set time delay between frames
frame_delay = 1;

# Specify number of pixels
number_of_leds = 119;

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, number_of_leds, brightness=brightness, auto_write=False)

# Initial LED list
dot_colors = [(64, 64, 64)] * number_of_leds

# Initialize sequence
sequence = []

# Read in file
with open('./data/sequence-1.csv', newline='') as csvfile:
    file = csv.reader(csvfile, delimiter=',', quotechar='"')
    for line in file:
        sequence.append(line)

# Loop forever
while True:

    # Loop through lines of file, and columns in line, assign to Dots, and render
    for line in range(len(sequence)):
        for i in range(len(sequence[line])):
            dot_colors[i] = hex_to_rgb(sequence[line][i])

        # Render to LED strip
        render(dot_colors)

        # Delay before iterating through loop
        time.sleep(frame_delay)
