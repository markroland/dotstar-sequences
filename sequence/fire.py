from PIL import Image
from pathlib import Path

class Fire:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds

        # Calculate gamma correction table, makes mid-range colors look "correct"
        self.GAMMA = bytearray(256)
        for i in range(256):
            self.GAMMA[i] = int(pow(float(i) / 255.0, 2.7) * 255.0 + 0.5)

        self.iteration = 0

    def setup(self, input_file):

        # Load image in RGB format and get dimensions:
        file_source = Path(__file__).parent / "../" / f"{input_file}"
        IMG = Image.open(file_source).convert("RGB")
        self.PIXELS = IMG.load()
        self.WIDTH = IMG.size[0]
        self.HEIGHT = IMG.size[1]

        # Ignore pixels in image that won't map to the LED Strip
        if self.WIDTH > self.number_of_leds:
            self.WIDTH = self.number_of_leds

        return

    def update(self):

        # Initialize LED values
        leds = [(0, 0, 0)] * self.number_of_leds

        # Set Y-position of image
        y = self.iteration

        # Loop through columns of row
        for x in range(self.WIDTH):

            # Read pixel in image
            rgb_pixel = self.PIXELS[x, y]

            # Set value with Gamma correction
            leds[x] = (self.GAMMA[rgb_pixel[0]], self.GAMMA[rgb_pixel[1]], self.GAMMA[rgb_pixel[2]])

        # Increment iteration counter.
        # Reset once it exceeds image height
        self.iteration += 1
        if self.iteration >= self.HEIGHT:
            self.iteration = 0

        return leds
