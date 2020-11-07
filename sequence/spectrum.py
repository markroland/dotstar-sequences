import time
from pattern.spectrum import *

class Spectrum:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds

    def setup(self, spectrum_type, sequence_type, period):
        self.sequence_type = sequence_type
        self.period = period
        self.spectrum = spectrum(spectrum_type)
        self.time_0 = time.time()
        self.iteration = 0

    def update(self):

        leds = [(255,255,255)] * self.number_of_leds

        if self.sequence_type == "fade":

            # Option 1: Timed iteration
            self.time = time.time() - self.time_0
            self.iteration = round((self.time / self.period) * (len(self.spectrum) - 1)) % (len(self.spectrum) - 1)

            # Option 2: Numeric iteration
            # self.iteration = (self.iteration + 1) % len(self.spectrum)

            leds = [self.spectrum[self.iteration]] * self.number_of_leds

        return leds
