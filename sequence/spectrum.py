import time
from pattern.spectrum import *

class Spectrum:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds

    def setup(self, spectrum_type, sequence_type, period):
        self.sequence_type = sequence_type
        self.period = period
        if sequence_type == "slide":
            self.spectrum = spectrum(spectrum_type, self.number_of_leds)
        else:
            self.spectrum = spectrum(spectrum_type)
        self.time_0 = time.time()
        self.iteration = 0

    def update(self):

        # Initialize LED values
        leds = [(255,255,255)] * self.number_of_leds

        # Calculate time since start
        self.time = time.time() - self.time_0

        if self.sequence_type == "fade":

            # Option 1: Timed iteration
            self.iteration = round((self.time / self.period) * (len(self.spectrum) - 1)) % (len(self.spectrum) - 1)

            # Option 2: Numeric iteration
            # self.iteration = (self.iteration + 1) % len(self.spectrum)

            leds = [self.spectrum[self.iteration]] * self.number_of_leds

        elif self.sequence_type == "slide":

            for i in range(self.number_of_leds):
                index = (self.iteration + i) % len(self.spectrum)
                leds[i] = self.spectrum[index]

            self.iteration = (self.iteration + 1) % self.number_of_leds

        return leds
