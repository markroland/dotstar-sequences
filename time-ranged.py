# Adafruit Dotstar RGB LED Strip
#
# Run a squence for a set period of time

# Import required libraries
import board
import adafruit_dotstar as dotstar
import time
from datetime import datetime
from sequences import *

# Write a List of colors to the Dotstar object and then Show them
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

# Instantiate a DotStar LED Strip
dots = dotstar.DotStar(board.SCK, board.MOSI, number_of_leds, brightness=brightness, auto_write=False)

# Load color sequence
spectrum_colors = get_sinebow_colors()

# Define running time (7am - 10pm)
today = datetime.now()
time_start = datetime.timestamp(datetime(today.year, today.month, today.day, 7, 0, 0))
time_end = datetime.timestamp(datetime(today.year, today.month, today.day, 22, 0, 0))
time_now = today.timestamp() # time.time() can also be used

# Loop
while time_now < time_end:

    # Update time
    time_now = time.time()

    # Calculate offset as a function of time
    offset = int((len(spectrum_colors)-1) * min((time_now - time_start)/(time_end - time_start), 1.0))

    # Set the colors
    dot_colors = [spectrum_colors[offset]] * number_of_leds

    # Render the colors
    render(dot_colors)

    # Delay before iterating through loop
    time.sleep(frame_delay)

# Fade Off Sequence
brightness_start = brightness
fade_off_frames = 20
for i in range(fade_off_frames):
    dots.brightness = brightness - (brightness_start * (i/fade_off_frames))
    dots.show()
    time.sleep(frame_delay)
dots.deinit()
