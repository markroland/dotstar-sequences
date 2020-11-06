from pattern.stripes import *

class Stripes:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds

    def rotate_list(self, my_list, position):
        return my_list[position:] + my_list[:position]

    def setup(self, direction, stripes):
        self.iteration = 0
        self.direction = direction
        self.stripes = stripes
        return

    def update(self):

        leds = stripes((128, 0, 128), (128, 128, 0), self.number_of_leds, self.stripes)

        # Rotate the list
        leds = self.rotate_list(leds, self.direction * self.iteration)

        # Increment iteration counter
        self.iteration = (self.iteration + 1) % self.number_of_leds

        return leds
