# Adafruit Dotstar RGB LED Strip
#
# Cycle through many sequence patterns

# Import required libraries
import sys
import board
import adafruit_dotstar as dotstar
import time
from sequences import *

# Write a List of colors to the Dotstar object and then Show them
def render(colors):

    # Assign pattern colors to Dotstar object
    for i in range(number_of_leds):
        dots[i] = colors[i]

    # Render LEDs
    dots.show()

# Move the start of the input List to a new position and wrap remaining
# values to the beginning of the list
def wrap_list(dot_colors, position):
    return dot_colors[position:] + dot_colors[:position]

# Set Brightness
brightness = 0.5

# Set time delay between frames
frame_delay = 1/60;

# Specify number of pixels
number_of_leds = 119;

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, number_of_leds, brightness=brightness, auto_write=False)

# Initialize timing
time_0 = time.time()
time_now = time_0

# Sequence
duration = 10
position_0 = 0
position = 0
velocity_0 = 0
velocity = velocity_0
acceleration = 30

dot_colors = stripes((200, 0, 0), (0,128,255), number_of_leds, 6)

print('Accelerating')
while (time_now - time_0) < duration:

    time_now = time.time()

    new_dot_colors = dot_colors

    # Calculate the new angular position
    position = velocity_0 * (time_now - time_0) + 0.5 * acceleration * pow(time_now - time_0, 2)
    position = int(round(position % number_of_leds))

    # Apply the transformation
    new_dot_colors = wrap_list(new_dot_colors, position)

    # Render to LED Strip
    render(new_dot_colors)

    # Delay before iterating through loop
    time.sleep(frame_delay)

# Steady
print('Steady')
velocity_0 = acceleration * (time_now - time_0)
time_0 = time_now
acceleration = 0
while (time_now - time_0) < duration:

    time_now = time.time()

    # TODO: This glitches location
    new_dot_colors = dot_colors

    # Calculate the new angular position
    position = velocity_0 * (time_now - time_0) + 0.5 * acceleration * pow(time_now - time_0, 2)
    position = int(round(position % number_of_leds))

    # Apply the transformation
    new_dot_colors = wrap_list(new_dot_colors, position)

    # Render to LED Strip
    render(new_dot_colors)

    # Delay before iterating through loop
    time.sleep(frame_delay)


# Decelerate
print('Decelerating')
# velocity_0 = acceleration * (time_now - time_0)
time_0 = time_now
acceleration = -1.05 * 10
while (time_now - time_0) < duration:

    time_now = time.time()

    # TODO: This glitches location
    new_dot_colors = dot_colors

    # Calculate the new angular position
    position = velocity_0 * (time_now - time_0) + 0.5 * acceleration * pow(time_now - time_0, 2)
    position = int(round(position % number_of_leds))

    # Apply the transformation
    new_dot_colors = wrap_list(new_dot_colors, position)

    # Render to LED Strip
    render(new_dot_colors)

    # Delay before iterating through loop
    time.sleep(frame_delay)

# Turn Off Sequence
brightness_start = brightness
fade_off_frames = 20
for i in range(fade_off_frames):
    dots.brightness = brightness - (brightness_start * (i/fade_off_frames))
    dots.show()
    time.sleep(frame_delay)
dots.deinit()
quit()
