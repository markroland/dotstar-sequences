# Adafruit Dotstar RGB LED Strip
#
# Display a rainbow spectrum across the range of all LEDs

# Import required libraries
import board
import adafruit_dotstar as dotstar
import math
import time

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, 120, brightness=0.8, auto_write=False)

# Option 2: Using a DotStar Digital LED Strip with LEDs connected to digital pins
# dots = dotstar.DotStar(board.D6, board.D5, 120)

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

# Map spectrum across full range of LEDs
n_dots = len(dots)
spectrum = [0] * n_dots
for i in range(n_dots):
    spectrum[i] = get_spectrum_color(n_dots, i)

for i in range(n_dots):
    dots[i] = spectrum[i]

offset = 0
while True:
    dots.show()

    # Shift spectrum
    offset = ((offset + 1) % n_dots)
    spectrum = shift(spectrum, 1)
    for i in range(n_dots):
        dots[i] = spectrum[i]

    # Delay before iterating through loop
    time.sleep(0.03)
