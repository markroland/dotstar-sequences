import time
import math

class Points:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds

    def rotate_list(self, my_list, position):
        return my_list[position:] + my_list[:position]

    def setup(self, direction, period_seconds, quantity, dot_color):
        self.time_0 = time.time()
        self.direction = direction
        self.period_seconds = period_seconds
        self.quantity = quantity
        self.dot_color = dot_color
        self.iteration = 0
        return

    def update(self):

        self.time = time.time() - self.time_0

        # Initialize LED values
        leds = [(0, 0, 0)] * self.number_of_leds

        # Calculate which LEDs should be lit
        if self.quantity == 1:
            leds[0] = self.dot_color
        elif self.quantity < self.number_of_leds:
            for i in range(len(leds)):

                # math.ceil() is used here instead of floor or round in order
                # to prevent additional dots toward the maximum range
                if i % math.ceil(self.number_of_leds/self.quantity) == 0:
                    leds[i] = self.dot_color

        # Option 1: Calculate position based on iteration
        # This prevents "jumps" in dots due to rounding
        led_position = self.iteration

        # Option 2: Calculate position based on time
        # offset = self.time
        # if self.time > self.period_seconds:
            # offset = (self.time % self.period_seconds)
        # led_position = round((offset / self.period_seconds) * (self.number_of_leds-1))

        # Rotate the list
        leds = self.rotate_list(leds, self.direction * led_position)

        # Increment iteration counter
        self.iteration = (self.iteration + 1) % self.number_of_leds

        return leds
