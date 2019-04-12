# Adafruit Dotstar RGB LED Strip
#
# Accept 4 values from the command line to set the LED's RGB values (0-255) and Intensity (0.0-1.0)
#
# Example: Run "python3 dotstar_rgb_input.py 255 255 0 0.5" for yellow at half-intensity

# Import required libraries
import sys
import board
import adafruit_dotstar

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = adafruit_dotstar.DotStar(board.SCK, board.MOSI, 120)

# Option 2: Using a DotStar Digital LED Strip with LEDs connected to digital pins
# dots = adafruit_dotstar.DotStar(board.D6, board.D5, 120)

# Set brightness
dots.brightness = float(sys.argv[4])

# Set each pixel color
dots.fill((int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])))
