# Adafruit Dotstar RGB LED Strip
#
# Disable all LEDs

# Import required libraries
import board
import adafruit_dotstar

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = adafruit_dotstar.DotStar(board.SCK, board.MOSI, 120)

# Option 2: Using a DotStar Digital LED Strip with LEDs connected to digital pins
# dots = adafruit_dotstar.DotStar(board.D6, board.D5, 120)

# Turn off all pixels
dots.deinit();
