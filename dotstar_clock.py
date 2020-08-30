# Adafruit Dotstar RGB LED Strip
#
# Create a clockface

# Import required libraries
import sys
import board
import adafruit_dotstar as dotstar
from datetime import datetime
import time

# Specify number of pixels
number_of_leds = 119

# Initialize Dotstar object
dots = dotstar.DotStar(board.SCK, board.MOSI, number_of_leds, brightness=0.8, auto_write=False)

# Set brightness
dots.brightness = 0.5

# Rotate array values
def rotate_list(my_list, position):
    return my_list[position:] + my_list[:position]

# Loop forever
while True:

    # Get clock hand positions
    second_index = round((int(datetime.now().strftime('%S')) / 60) * number_of_leds)
    minute_index = round((int(datetime.now().strftime('%M')) / 60) * number_of_leds)
    hour_index = round(((int(datetime.now().strftime('%H')) % 12) / 12) * number_of_leds);
    hour_index += round(
        ((int(datetime.now().strftime('%M')) / 60) / 12) * number_of_leds
    )
    if hour_index > number_of_leds:
        hour_index = 0

    # Initialization. Fill an array of length "number_of_leds" with zeros
    dot_colors = [(0,0,0)] * number_of_leds

    # Solid fill to hours
    dot_colors[hour_index] = (255, 0, 0)
    for j in range(number_of_leds):
        if j < hour_index:
            dot_colors[j] = (8, 0, 0)

    # Set 12 points of clockface
    dot_colors[0] = (0, 64, 0)
    for i in range(1, 12):
        index = round((i/12) * number_of_leds)
        dot_colors[index] = (0, 4, 0)

    # Minute and Second hands
    dot_colors[second_index] = (64, 64, 64)
    dot_colors[minute_index] = (0, 0, 255)

    # Rotate clockface for the orientation of the viewer
    dot_colors = rotate_list(dot_colors, 75)

    # Assign pattern colors to Dotstar object
    for i in range(number_of_leds):
        dots[i] = dot_colors[i]

    # Render LEDs
    dots.show()

    # Delay before iterating through loop
    time.sleep(0.1)
