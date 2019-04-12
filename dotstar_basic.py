# Adafruit Dotstar RGB LED Strip
#
# Set all pixels to a certain value

# Import required libraries
import board
import adafruit_dotstar

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = adafruit_dotstar.DotStar(board.SCK, board.MOSI, 120, brightness=0.2)

# Option 2: Using a DotStar Digital LED Strip with LEDs connected to digital pins
# dots = adafruit_dotstar.DotStar(board.D6, board.D5, 120, brightness=0.2)

# Set First (zero-index) pixel
# dots[0] = (255, 0, 0)

# Set all pixels to green
dots.fill((0, 255, 0))