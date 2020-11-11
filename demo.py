# Play a Show as defined in a JSON configuration file

# Import required libraries
import board
import adafruit_dotstar as dotstar
import time
from pathlib import Path
import json
import importlib

# Add two Lists of colors
def colors_add(colors_1, colors_2):

    colors = [(0,0,0)] * len(colors_1)

    # Initialize array
    for i in range(len(colors)):
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

# Fade one List of colors out and another List of colors in over a period of time
def crossfade(colors_out, colors_in, period, time):
    colors_out_fade = fade(colors_out, 1 - time/period)
    colors_in_fade = fade(colors_in, time/period)
    return colors_add(colors_out_fade, colors_in_fade)

# Set defaults prior to input
NUMBER_OF_LEDS = 119;
brightness = 0.5
FRAME_DELAY = 1/30;
CROSSFADE_SECONDS = 3

# Read in show configuration from a config file
show_filepath = Path(__file__).parent / "shows/demo.json"
with open(str(show_filepath)) as show_json:
    show_config = json.load(show_json)
    show_json.close();

# Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, NUMBER_OF_LEDS, brightness=brightness, auto_write=False)

# Initialize sequences
Sequence = None
NextSequence = None

# Loop through all Sequences in the Show
for i in range(len(show_config)):

    # Load Sequence module
    if NextSequence is not None:
        Sequence = NextSequence
    else:
        my_module = importlib.import_module(show_config[i]['module'])
        class_ = getattr(my_module, show_config[i]['name'])
        Sequence = class_(NUMBER_OF_LEDS)
        Sequence.setup(*show_config[i]['parameters'])

    # For all but the last sequence in the playlist,
    # set up next sequence so the current and next sequences can cross-fade
    if i < len(show_config) - 1:
        next_module = importlib.import_module(show_config[i+1]['module'])
        next_class_ = getattr(next_module, show_config[i+1]['name'])
        NextSequence = next_class_(NUMBER_OF_LEDS)
        NextSequence.setup(*show_config[i+1]['parameters'])

    # Initialize timer
    time_start = time.time()
    time_now = time_start

    # Loop for duration
    duration = show_config[i]['duration']
    while (time_now - time_start) < duration:

        # Update sequence
        dot_colors = Sequence.update()

        # Crossfade when the next sequence is available
        if NextSequence is not None:
            crossfade_left = duration - (time_now - time_start)
            if crossfade_left < CROSSFADE_SECONDS:
                next_dot_colors = NextSequence.update()
                dot_colors = crossfade(dot_colors, next_dot_colors, CROSSFADE_SECONDS, CROSSFADE_SECONDS - crossfade_left)

        # Assign pattern colors to Dotstar object and Render
        for i in range(len(dot_colors)):
            dots[i] = dot_colors[i]
        dots.show()

        # Delay before iterating through loop
        time.sleep(FRAME_DELAY)

        # Update timer
        time_now = time.time()

# Disconnect from lights
brightness_start = brightness
fade_off_frames = 20
for i in range(fade_off_frames):
    dots.brightness = brightness - (brightness_start * (i/fade_off_frames))
    dots.show()
    time.sleep(FRAME_DELAY)
dots.deinit()
