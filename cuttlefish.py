# Adafruit Dotstar RGB LED Strip
#
# Cycle through many sequence patterns

# Import required libraries
import board
import adafruit_dotstar as dotstar
import time
from sequence.cuttlefish import Cuttlefish

# Set Brightness
brightness = 0.5

# Set time delay between frames
FRAME_DELAY = 1/60;

# Specify number of pixels
NUMBER_OF_LEDS = 119;

# Option 1: Using a DotStar Digital LED Strip with LEDs connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, NUMBER_OF_LEDS, brightness=brightness, auto_write=False)

# Initialize sequence
Sequence = Cuttlefish(NUMBER_OF_LEDS)
dot_colors = Sequence.setup()

# Loop Forever
while True:

    # Update sequence
    dot_colors = Sequence.update()

    # Assign pattern colors to Dotstar object and Render
    for i in range(len(colors)):
        dots[i] = colors[i]
    dots.show()

    # Delay before iterating through loop
    time.sleep(FRAME_DELAY)
