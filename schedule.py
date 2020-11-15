# Adafruit Dotstar RGB LED Strip
#
# Run a squence for a set period of time

# Import required libraries
import board
import adafruit_dotstar as dotstar
from datetime import datetime
import time
import math
from pathlib import Path
from dotenv import load_dotenv
import os
import json
import importlib
import atexit

def fade_brightness(start, end, duration):
    frames = round(duration * (1/frame_delay))
    for i in range(frames):
        if (start > end):
            dots.brightness = end + ((start - end) * (1-i/frames))
        else:
            dots.brightness = start + ((start - end) * (i/frames))
        dots.show()
        time.sleep(frame_delay)

# Shutdown function to turn lights off if script exits
def shutdown():
    fade_brightness(brightness, 0, 1)
    dots.deinit()

# Register shutdown function
atexit.register(shutdown)

# Load environment settings
load_dotenv()
NUMBER_OF_LEDS = int(os.environ.get("NUMBER_OF_LEDS"))
brightness = float(os.environ.get("DEFAULT_BRIGHTNESS"))
# frame_delay = float(os.environ.get("DEFAULT_FRAME_DELAY"))
frame_delay = 1/30

# Set start and end hours of the day (i.e. 7am - 10pm)
START_HOUR = int(os.environ.get("SCHEDULE_START_HOUR"))
END_HOUR = int(os.environ.get("SCHEDULE_END_HOUR"))

# Read in show configuration from a config file
show_filepath = Path(__file__).parent / "shows/weekly.json"
with open(str(show_filepath)) as show_json:
    show_config = json.load(show_json)
    show_json.close()

# Loop forever
while True:

    # Define now
    today = datetime.now()
    time_now = today.timestamp() # time.time() can also be used
    day_of_week = datetime.now().weekday()

    # Define running time
    time_start = datetime.timestamp(datetime(today.year, today.month, today.day, START_HOUR, 0, 0))
    time_end = datetime.timestamp(datetime(today.year, today.month, today.day, END_HOUR, 0, 0))

    # Run this pattern on Friday (day 4 of week)
    if time_now > time_start and time_now < time_end:

        # Instantiate a DotStar LED Strip
        dots = dotstar.DotStar(board.SCK, board.MOSI, NUMBER_OF_LEDS, brightness=brightness, auto_write=False)

        # Load Sequence
        index = day_of_week
        my_module = importlib.import_module(show_config[index]['module'])
        class_ = getattr(my_module, show_config[index]['name'])
        Sequence = class_(NUMBER_OF_LEDS)
        Sequence.setup(*show_config[index]['parameters'])

        # Loop continuously during the time range
        while time_now < time_end:

            # Update sequence
            dot_colors = Sequence.update()

            # Assign pattern colors to Dotstar object
            for i in range(len(dot_colors)):
                dots[i] = dot_colors[i]

            # Render LEDs
            dots.show()

            # Delay before iterating through loop
            time.sleep(frame_delay)

            # Update time
            time_now = time.time()

        # Fade Off
        fade_brightness(brightness, 0, 1)
        dots.deinit()
