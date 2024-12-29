# Adafruit Dotstar RGB LED Strip
#
# Display a rainbow spectrum across the range of all LEDs

# Import required libraries
import os
from dotenv import load_dotenv
from pathlib import Path
# import board
# import adafruit_dotstar as dotstar
import math
import time
from PIL import Image
import csv

load_dotenv()
NUMBER_OF_LEDS = int(os.environ.get("NUMBER_OF_LEDS"))

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
# dots = dotstar.DotStar(board.SCK, board.MOSI, NUMBER_OF_LEDS, brightness=0.8, auto_write=False)

# Option 2: Using a DotStar Digital LED Strip with LEDs connected to digital pins
# dots = dotstar.DotStar(board.D6, board.D5, NUMBER_OF_LEDS)

# Function to map the full spectrum of colors across a set number of steps
# Very similar to the Adafruit "Wheel" method
# https://learn.adafruit.com/hacking-ikea-lamps-with-circuit-playground-express/generate-your-colors#wheel-explained
def get_spectrum_color(total_steps, step):

    # Divide the spectrum into 6 segments (Red, Yellow, Green, Cyan, Blue, Magenta)
    spectrum_band = math.floor(step/(total_steps/6))
    if spectrum_band == 0:
        r = 255
        g = 255 * (step - (0/6) * total_steps) / (total_steps/6) # ramp up
        b = 0
    elif spectrum_band == 1:
        r = 255 - 255 * (step - (1/6) * total_steps) / (total_steps/6) # ramp down
        g = 255
        b = 0
    elif spectrum_band == 2:
        r = 0
        g = 255
        b = 255 * (step - (2/6) * total_steps) / (total_steps/6) # ramp up
    elif spectrum_band == 3:
        r = 0
        g = 255 - 255 * (step - (3/6)*total_steps) / (total_steps/6) # ramp down
        b = 255
    elif spectrum_band == 4:
        r = 255 * (step - ((4/6)*total_steps)) / (total_steps/6) # ramp up
        g = 0
        b = 255
    elif spectrum_band == 5:
        r = 255
        g = 0
        b = 255 - 255 * (step - (5/6)*total_steps) / (total_steps/6) # ramp down

    return int(r), int(g), int(b)

def shift(l, n):
    return l[n:] + l[:n]

# Initialization. Fill an array of length "n_dots" with zeros
spectrum = [0] * NUMBER_OF_LEDS

# fill "spectrum" with calculated RGB tuples
for i in range(NUMBER_OF_LEDS):
    spectrum[i] = get_spectrum_color(NUMBER_OF_LEDS, i)

# Intialize counter
offset = 0

# Open Image file for writing
output_filepath = Path(__file__).parent / "data/rainbow.png"
img = Image.new('RGB', (NUMBER_OF_LEDS, NUMBER_OF_LEDS))

# Initialize array to hold RGB tuples
img_dots = []

# Loop through sequence
for t in range(NUMBER_OF_LEDS):

    # Shift spectrum
    # offset = ((offset + 1) % NUMBER_OF_LEDS)

    # Fill dots object with values from "spectrum".
    # "dots" can't be assigned directly because it's a "dotstar" object, not an array
    spectrum = shift(spectrum, 1)
    for i in range(NUMBER_OF_LEDS):
        # dots[i] = spectrum[i]
        img_dots.append(spectrum[i])

    # Render to LED strip
    # dots.show()

    # Delay before iterating through loop
    # time.sleep(1/60)

img.putdata(img_dots)
img.save(output_filepath)

print(f"Image saved to {output_filepath}")

# --- Create a CSV file of HEX values for each frame

# Open CSV file for writing
csv_filepath = Path(__file__).parent / "data/rainbow.csv"
with open(csv_filepath, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Loop through sequence
    for t in range(NUMBER_OF_LEDS):

        # Fill dots object with values from "spectrum".
        spectrum = shift(spectrum, 1)

        # Convert RGB tuples to hex strings
        hex_spectrum = ['#' + '%02x%02x%02x' % rgb for rgb in spectrum]

        # Write current frame to CSV
        # writer.writerow(spectrum)
        writer.writerow(hex_spectrum)

print(f"CSV data saved to {csv_filepath}")