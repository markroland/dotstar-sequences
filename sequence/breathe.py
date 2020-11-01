import time
import math
import colorsys

class Breathe:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds

    def setup(self, min_b, max_b):
        self.time_0 = time.time()
        self.time = time.time() - self.time_0
        self.min_brightness = min_b
        self.max_brightness = max_b
        self.period = 4
        return

    # Fade lights on and off, like breathing
    # Human breathing is between 12-25 breathes/minute
    # 15 breaths/minute is 1 breathe every 4 seconds
    # With 129 LEDs a delay of 0.3 seconds (4/129) will accurately represent breathing
    def update(self):

        self.time = time.time() - self.time_0

        # Calculate brightness
        normal_brightness = 0.5 + (0.5 * math.sin( self.time * (1/self.period) * 2 * math.pi))
        scaled_brightness = self.max_brightness * (normal_brightness * (self.max_brightness - self.min_brightness) + self.min_brightness)

        # Convert to RGB pixels
        hsv_color = colorsys.hsv_to_rgb(0, 0.0, scaled_brightness)
        r = int(hsv_color[0] * 255)
        g = int(hsv_color[1] * 255)
        b = int(hsv_color[2] * 255)
        leds = [(r, g, b)] * self.number_of_leds

        return leds
