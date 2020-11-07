import time
from pattern.spectrum import *

class Spectrum:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds

    def rotate_list(self, my_list, position):
        return my_list[position:] + my_list[:position]

    def setup(self, spectrum_type, sequence_type, period):
        self.sequence_type = sequence_type
        self.period = period
        if sequence_type == "fade":
            self.spectrum = spectrum(spectrum_type)
        else:
            self.spectrum = spectrum(spectrum_type, self.number_of_leds)
        self.time_0 = time.time()
        self.iteration = 0
        self.revolutions = 0

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

        elif self.sequence_type == "wipe":

            # Fill dots object with values from "spectrum".
            # "dots" can't be assigned directly because it's a "dostar" object, not an array
            for i in range(self.number_of_leds):
                if i < self.number_of_leds/2:
                    index = (self.iteration + i) % len(self.spectrum)
                else:
                    index = (self.iteration + (self.number_of_leds - i)) % len(self.spectrum)
                leds[i] = self.spectrum[index]

            # Optional: Rotate starting point
            leds = self.rotate_list(leds, self.revolutions % math.floor(self.number_of_leds/2))

            if (self.iteration + 1) == self.number_of_leds:
                self.revolutions += 1

            self.iteration = (self.iteration + 1) % self.number_of_leds

        return leds
