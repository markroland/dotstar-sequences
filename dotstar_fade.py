# Adafruit Dotstar RGB LED Strip Fade
#
# Fade all pixels from one color to another

# Import required libraries
import board
import adafruit_dotstar
import time

# Specify number of pixels
number_of_leds = 119;

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = adafruit_dotstar.DotStar(board.SCK, board.MOSI, number_of_leds, brightness=0.5, auto_write=False)

# Frame period in seconds
frame_delay = 0.03

# Number of steps between 2 colors
steps = 50

color_1 = (255, 0, 0)
color_2 = (64, 128, 84)

# Initialize array
dot_colors = [color_1] * number_of_leds

# Set brightness
dots.brightness = 0.5

def fade_component(start, finish, step, steps):
    if (start > finish):
        value = start - ((start - finish) * (step / (steps-1)))
    else:
        value = start + ((finish - start) * (step / (steps-1)))
    return value

# Loop through steps
for x in range(0, steps):

    # Calculate color components
    r = fade_component(color_1[0], color_2[0], x, steps)
    g = fade_component(color_1[1], color_2[1], x, steps)
    b = fade_component(color_1[2], color_2[2], x, steps)

    # Assign RGB to all LEDs
    dot_colors = [(int(r), int(g), int(b))] * number_of_leds

    # Debugging
    # print(color_1[1], color_2[1], sep="\t")
    # print(dot_colors[0][0], dot_colors[0][1], dot_colors[0][2], sep="\t")

    # Assign colors to Dotstar object
    for i in range(number_of_leds):
        dots[i] = dot_colors[i]

    # Render LEDs
    dots.show()

    # Delay before iterating through loop
    time.sleep(frame_delay)
