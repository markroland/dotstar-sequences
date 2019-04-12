# Adafruit Dotstar RGB LED Strip
#
# Fill all LEDs with the same color. Cycle through the spectrum of Red, Yellow, Green, Cyan, Blue, Magenta

# Import required libraries
import board
import adafruit_dotstar as dotstar
import time
import math

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, 120, brightness=0.2)

# Option 2: Using a DotStar Digital LED Strip with LEDs connected to digital pins
# dots = dotstar.DotStar(board.D6, board.D5, 120)

# MAIN LOOP
n_dots = len(dots)
while True:

    r = 0
    g = 0
    b = 0
    loop_step = 0
    spectrum_steps = 255 * 6

    # Loop through full spectrum one time
    for loop_step in range(spectrum_steps):

        # Divide the spectrum into 6 segments (Red, Yellow, Green, Cyan, Blue, Magenta)
        spectrum_band = math.floor(loop_step/(spectrum_steps/6))
        if spectrum_band == 0:
            r = 255
            g = 255 * (loop_step - (0/6.0) * spectrum_steps) / (spectrum_steps/6.0) # ramp up
            b = 0
        elif spectrum_band == 1:
            r = 255 - 255 * (loop_step - (1/6.0) * spectrum_steps) / (spectrum_steps/6.0) # ramp down
            g = 255
            b = 0
        elif spectrum_band == 2:
            r = 0
            g = 255
            b = 255 * (loop_step - (2/6.0) * spectrum_steps) / (spectrum_steps/6.0) # ramp up
        elif spectrum_band == 3:
            r = 0
            g = 255 - 255 * (loop_step - (3/6.0)*spectrum_steps) / (spectrum_steps/6.0) # ramp down
            b = 255
        elif spectrum_band == 4:
            r = 255 * (loop_step - ((4/6.0)*spectrum_steps)) / (spectrum_steps/6.0) # ramp up
            g = 0
            b = 255
        elif spectrum_band == 5:
            r = 255
            g = 0
            b = 255 - 255 * (loop_step - (5/6.0)*spectrum_steps) / (spectrum_steps/6.0) # ramp down

        # Set each pixel color
        dots.fill((int(r), int(g), int(b)))

        # Delay before iterating through loop
        time.sleep(0.020)
