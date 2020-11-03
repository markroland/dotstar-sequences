import math
import colorsys
import time
from pattern.spectrum import *

def darken(color, darken):

    h = colorsys.rgb_to_hsv(color[0], color[1], color[2])[0]
    s = colorsys.rgb_to_hsv(color[0], color[1], color[2])[1]
    v = colorsys.rgb_to_hsv(color[0], color[1], color[2])[2] * darken

    # new_color = colorsys.hsv_to_rgb(h,s,v)
    new_color = colorsys.hsv_to_rgb(h,s,v)

    return (int(new_color[0]), int(new_color[1]), int(new_color[2]))

class Cuttlefish:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds
        self.spectrum_colors = spectrum("sinebow", self.number_of_leds)
        self.spectrum_offset = 0
        self.brightness_offset = 0
        self.time_0 = 0
        self.time = 0

    def setup(self):
        self.time = time.time() - self.time_0
        return

    def update(self):

        leds = [self.spectrum_colors[self.spectrum_offset]] * self.number_of_leds
        self.spectrum_offset = (self.spectrum_offset + 1) % len(self.spectrum_colors)

        # Modulate HSV lightness value

        # This needs to be a function of Pi so there are no discontinuous jumps
        self.brightness_offset = (math.pi / 12) * self.spectrum_offset
        waves = 12

        # Method 1: pulses moving in circle
        # for i in range(len(leds)):
        #     lightness_coefficient = 0.6 + (0.4 * math.cos((i/(self.number_of_leds/waves)) * 2 * math.pi + self.brightness_offset))
        #     leds[i] = darken(leds[i], lightness_coefficient)

        # Method 2: Two halves of pulses moving in opposite directions
        for i in range(self.number_of_leds):
            if i < self.number_of_leds/2:
                lightness_coefficient = 0.6 + (0.4 * math.cos((i/(self.number_of_leds/waves)) * 2 * math.pi + self.brightness_offset))
                leds[i] = darken(leds[i], lightness_coefficient)
            else:
                lightness_coefficient = 0.6 + (0.4 * math.cos((i/(self.number_of_leds/waves)) * 2 * math.pi - self.brightness_offset))
                leds[i] = darken(leds[i], lightness_coefficient)

        return leds
