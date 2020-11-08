# Adafruit Dotstar RGB LED Strip
#
# Run a squence for a set period of time

# Import required libraries
import board
import adafruit_dotstar as dotstar
import time
import math
import random
from datetime import datetime
from sequences import *
from sequence.crossing import Crossing
from sequence.sparkle import Sparkle
from sequence.spectrum import *
from sequence.wipe import *

# Write a List of colors to the Dotstar object and then Show them
def render(colors):

    # Assign pattern colors to Dotstar object
    for i in range(number_of_leds):
        dots[i] = colors[i]

    # Render LEDs
    dots.show()

def fade_brightness(start, end, duration):
    brightness_start = brightness
    fade_on_frames = round(duration * (1/frame_delay))
    for i in range(fade_on_frames):
        dots.brightness = brightness * (i/fade_on_frames)
        dots.show()
        time.sleep(frame_delay)
    dots.brightness = brightness

# Set Brightness
brightness = 0.5

# Set time delay between frames (Refresh rate)
frame_delay = 1/60;

# Specify number of pixels
number_of_leds = 119;

# Set start and end hours of the day (i.e. 7am - 10pm)
start_hour = 6
end_hour = 22

# Load color sequence
spectrum_colors = spectrum("sinebow")

# Loop forever
while True:

    # Define now
    today = datetime.now()
    time_now = today.timestamp() # time.time() can also be used
    day_of_week = datetime.now().weekday()

    # Define running time
    time_start = datetime.timestamp(datetime(today.year, today.month, today.day, start_hour, 0, 0))
    time_end = datetime.timestamp(datetime(today.year, today.month, today.day, end_hour, 0, 0))

    # Run this pattern on Friday (day 4 of week)
    if time_now > time_start and time_now < time_end:

        # Instantiate a DotStar LED Strip
        dots = dotstar.DotStar(board.SCK, board.MOSI, number_of_leds, brightness=brightness, auto_write=False)

        if day_of_week == 0:

            # Two colors back and forth

            Sequence = Wipe(number_of_leds)
            hue_1 = random.random()
            hue_2 = hue_1 + 0.5 % 1
            Sequence.setup(6, hue_1, hue_2, -45)

            while time_now < time_end:

                dot_colors = Sequence.update()

                # Render to LED strip
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(frame_delay)

                # Update time
                time_now = time.time()

            # Fade Off
            fade_brightness(brightness, 0, 0.33)

        elif day_of_week == 1:

            # Transition through full spectrum during full run time

            # Fade On
            dot_colors = [spectrum_colors[0]] * number_of_leds
            fade_brightness(0, brightness, 0.33)

            Sequence = Spectrum(number_of_leds)
            Sequence.setup("sinebow", "fade", time_end - time_start)

            while time_now < time_end:

                time_now = time.time()

                dot_colors = Sequence.update()

                # Render to LED strip
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(frame_delay)

            # Fade Off
            fade_brightness(brightness, 0, 0.33)

        elif day_of_week == 2:

            Sequence = Spectrum(NUMBER_OF_LEDS)
            Sequence.setup("sinebow", "wipe", 3)

            # Loop
            while time_now < time_end:

                # Set colors
                dot_colors = Sequence.update()

                # Render the colors
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(frame_delay)

                # Update time
                time_now = time.time()

        elif day_of_week == 3:

            Sequence = Spectrum(NUMBER_OF_LEDS)
            Sequence.setup("sinebow", "slide", 3)

            # Loop
            while time_now < time_end:

                # Set colors
                dot_colors = Sequence.update()

                # Render the colors
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(frame_delay)

                # Update time
                time_now = time.time()

        elif day_of_week == 4:

            # Crossing bands

            Sequence = Crossing(number_of_leds)
            hue_1 = random.random()
            # random_hue_2 = random.random()
            hue_2 = hue_1 + 0.5 % 1
            length_1 = int(number_of_leds * 0.33)
            length_2 = int(number_of_leds * 0.2)
            Sequence.setup(hue_1, hue_2, length_1, length_2)

            while time_now < time_end:

                time_now = time.time()

                dot_colors = Sequence.update()

                # Render to LED strip
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(frame_delay)

        elif day_of_week == 5:

            # Cuttlefish

            # Create and setup a Loop module
            Sequence = Cuttlefish(number_of_leds)
            dot_colors = Sequence.setup()

            while time_now < time_end:

                dot_colors = Sequence.update()

                # Render to LED strip
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(frame_delay)

                time_now = time.time()

        elif day_of_week == 6:

            # Create and setup a Loop module
            sp = Sparkle(number_of_leds)
            dot_colors = sp.setup()

            # Initialize timing
            time_0 = time.time()
            time_now = time_0

            while time_now < time_end:

                time_now = time.time()

                dot_colors = sp.update()

                # Render to LED strip
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(frame_delay)

        # Disable LEDs at end of active time
        dots.deinit()
