import random

class Random:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds

    # A random color 32 -> 224
    def random_color(self):
        return random.randrange(1, 7) * 32

    def setup(self):
        return

    def update(self):

        leds = [(0, 0, 0)] * self.number_of_leds

        for i in range(self.number_of_leds):
            leds[i] = (self.random_color(), self.random_color(), self.random_color())

        return leds
