import time
import math
import colorsys

class Wipe:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds

    def rotate_list(self, my_list, position):
        return my_list[position:] + my_list[:position]

    def setup(self, period, hue_1, hue_2, orientation):

        self.hue_1 = hue_1
        self.hue_2 = hue_2
        self.degrees_rotation = orientation
        self.period = period

        # Define Color 1
        color_1_hsv = colorsys.hsv_to_rgb(self.hue_1, 1.0, 1.0)
        self.color_1 = (int(color_1_hsv[0] * 255), int(color_1_hsv[1] * 255), int(color_1_hsv[2] * 255))

        # Define Color 2
        color_2_hsv = colorsys.hsv_to_rgb(self.hue_2, 1.0, 1.0)
        self.color_2 = (int(color_2_hsv[0] * 255), int(color_2_hsv[1] * 255), int(color_2_hsv[2] * 255))

        self.time_0 = time.time()

        return

    def update(self):

        # Set all LEDs
        dot_colors = [self.color_1] * self.number_of_leds

        # Calculate wipe position
        elapsed_time = time.time() - self.time_0
        position = math.sin((2*math.pi) * (elapsed_time / self.period))

        # 0 to 1/2 of number_of_leds
        i_position = math.floor(position * (self.number_of_leds / 4) + (self.number_of_leds / 4))

        # Top Half
        for i in range(i_position):
            dot_colors[i] = self.color_2

        # Bottom Half
        for i in range((self.number_of_leds-1) - i_position, self.number_of_leds-1, 1):
            dot_colors[i] = self.color_2

        # Optional: Change orientation for table
        dot_colors = self.rotate_list(dot_colors, math.floor((self.degrees_rotation/360) * self.number_of_leds))

        return dot_colors
