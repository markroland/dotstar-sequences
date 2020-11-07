import time
from pattern.stripes import *

class Acceleration:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds

        self.time_0 = 0
        self.time = self.time_0

        self.position_0 = 0
        self.position = self.position_0

        self.velocity_0 = 0
        self.velocity = self.velocity_0

    # Move the start of the input List to a new position and wrap remaining
    # values to the beginning of the list
    def wrap_list(self, dot_colors, position):
        return dot_colors[position:] + dot_colors[:position]

    def setup(self, num_stripes):
        self.num_stripes = num_stripes
        self.time_0 = time.time()
        self.time = time.time() - self.time_0
        self.leds = stripes((200, 0, 0), (0,128,255), self.number_of_leds, self.num_stripes)
        return

    def update(self):

        # Update time
        self.time = time.time() - self.time_0

        # Acceleration sequence
        # TODO: This glitches location at changes
        segment_time = self.time
        if self.time < 10:
            acceleration = 10
            self.velocity = acceleration * self.time
        elif self.time < 20:
            segment_time = self.time - 10
            self.velocity_0 = self.velocity
            acceleration = 0
        else:
            segment_time = self.time - 20
            acceleration = -10

        # Calculate the position
        position = self.velocity_0 * segment_time + 0.5 * acceleration * pow(segment_time, 2)
        position = int(round(position % self.number_of_leds))

        # Apply the transformation
        leds = self.wrap_list(self.leds, position)

        return leds
