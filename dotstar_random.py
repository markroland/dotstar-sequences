import time
import random
import board
import adafruit_dotstar as dotstar

# Using a DotStar Digital LED Strip with 120 LEDs connected to hardware SPI
dots = dotstar.DotStar(board.SCK, board.MOSI, 120, brightness=0.2)

# Using a DotStar Digital LED Strip with 120 LEDs connected to digital pins
# dots = dotstar.DotStar(board.D6, board.D5, 120, brightness=0.2)

# HELPERS
# a random color 32 -> 224
def random_color():
    return random.randrange(1, 7) * 32


# MAIN LOOP
n_dots = len(dots)
while True:
    # Fill each dot with a random color
    for dot in range(n_dots):
        dots[dot] = (random_color(), random_color(), random_color())
        time.sleep(0.01)