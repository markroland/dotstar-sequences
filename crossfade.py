# Adafruit Dotstar RGB LED Strip
#
# Cycle through many sequence patterns

# Import required libraries
import sys
import board
import adafruit_dotstar as dotstar
import time
from sequences import *
from pattern.stripes import *

# Write a List of colors to the Dotstar object and then Show them
def render(colors):

    # Assign pattern colors to Dotstar object
    for i in range(number_of_leds):
        dots[i] = colors[i]

    # Render LEDs
    dots.show()

def colors_add(colors_1, colors_2):

    colors = [(0,0,0)] * number_of_leds

    # Initialize array
    for i in range(number_of_leds):
        # Calculate color components
        r = min(colors_1[i][0] + colors_2[i][0], 255)
        g = min(colors_1[i][1] + colors_2[i][1], 255)
        b = min(colors_1[i][2] + colors_2[i][2], 255)

        # Assign RGB to all LEDs
        colors[i] = (int(r), int(g), int(b))

    return colors

# Fade
def fade(led_strip, percent):
    faded_colors = [(0,0,0)] * len(led_strip)
    for i in range(len(led_strip)):
        faded_colors[i] = (int(led_strip[i][0] * percent), int(led_strip[i][1] * percent), int(led_strip[i][2] * percent))
    return faded_colors

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
duration = 3
position_0 = 0
position = 0
velocity_0 = 0
velocity = velocity_0
acceleration = 10

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
duration = 10
fade_out = 5
fade_start = duration - fade_out
while (time_now - time_0) < duration:

    time_now = time.time()

    # TODO: This glitches location
    new_dot_colors = dot_colors

    # Calculate the new angular position
    position = velocity_0 * (time_now - time_0) + 0.5 * acceleration * pow(time_now - time_0, 2)
    position = int(round(position % number_of_leds))

    # Apply the transformation
    new_dot_colors = wrap_list(new_dot_colors, position)

    if (time_now - time_0) > fade_start:

        next_dot_colors = [(128,128,0)] * number_of_leds

        next_dot_colors = fade(next_dot_colors, ((time_now - time_0) - fade_start) / fade_out)

        new_dot_colors = fade(new_dot_colors, 1 - (((time_now - time_0) - fade_start) / fade_out))

        new_dot_colors = colors_add(next_dot_colors, new_dot_colors)

    # Render to LED Strip
    render(new_dot_colors)

    # Delay before iterating through loop
    time.sleep(frame_delay)

time.sleep(2)

# Crossfade

# Turn Off Sequence
brightness_start = brightness
fade_off_frames = 20
for i in range(fade_off_frames):
    dots.brightness = brightness - (brightness_start * (i/fade_off_frames))
    dots.show()
    time.sleep(frame_delay)
dots.deinit()
quit()
