# Adafruit Dotstar RGB LED Strip
#
# Fill all LEDs with the same color. Cycle through the spectrum of Red, Yellow, Green, Cyan, Blue, Magenta
#
# Related: https://learn.adafruit.com/circuitpython-essentials/circuitpython-internal-rgb-led

# Import required libraries
import board
import adafruit_dotstar as dotstar
import time
from pattern.spectrum import *

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, 120, brightness=0.2)

# Option 2: Using a DotStar Digital LED Strip with LEDs connected to digital pins
# dots = dotstar.DotStar(board.D6, board.D5, 120)

# MAIN LOOP
step = 0;
n_dots = len(dots)

# Load an array(?) of RGB colors for every possible color
spectrum_colors = spectrum("linear")

# Loop forever
while True:

    # Set each pixel color
    dots.fill(spectrum_colors[step])

    # Increment step counter
    step = (step + 1) % (255 * 6)

    # Delay before iterating through loop
    time.sleep(0.020)
