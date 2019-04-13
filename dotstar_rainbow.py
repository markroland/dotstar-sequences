# Adafruit Dotstar RGB LED Strip
#
# Display a rainbow spectrum across the range of all LEDs

# Import required libraries
import board
import adafruit_dotstar as dotstar
import math

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, 120, brightness=0.2)

# Option 2: Using a DotStar Digital LED Strip with LEDs connected to digital pins
# dots = dotstar.DotStar(board.D6, board.D5, 120)

# Initialize RGB values
r = 0
g = 0
b = 0

# Count number of LEDs
n_dots = len(dots)

# Loop through full spectrum one time
for i in range(n_dots):

    # Divide the spectrum into 6 segments (Red, Yellow, Green, Cyan, Blue, Magenta)
    spectrum_band = math.floor(i/(n_dots/6))
    if spectrum_band == 0:
        r = 255
        g = 255 * (i - (0/6.0) * n_dots) / (n_dots/6.0) # ramp up
        b = 0
    elif spectrum_band == 1:
        r = 255 - 255 * (i - (1/6.0) * n_dots) / (n_dots/6.0) # ramp down
        g = 255
        b = 0
    elif spectrum_band == 2:
        r = 0
        g = 255
        b = 255 * (i - (2/6.0) * n_dots) / (n_dots/6.0) # ramp up
    elif spectrum_band == 3:
        r = 0
        g = 255 - 255 * (i - (3/6.0)*n_dots) / (n_dots/6.0) # ramp down
        b = 255
    elif spectrum_band == 4:
        r = 255 * (i - ((4/6.0)*n_dots)) / (n_dots/6.0) # ramp up
        g = 0
        b = 255
    elif spectrum_band == 5:
        r = 255
        g = 0
        b = 255 - 255 * (i - (5/6.0)*n_dots) / (n_dots/6.0) # ramp down

    # Set pixel color
    dots[i] = (int(r), int(g), int(b))
