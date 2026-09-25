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

        # Amplifies the sine position before clamping to [-1, 1] so it pins at the
        # extremes instead of just touching them; must be > 1 to hold fully open/closed
        # for any length of time (at 1.0 it's back to an instantaneous touch).
        self.dwell_factor = 1.0

        # Define Color 1
        color_1_hsv = colorsys.hsv_to_rgb(self.hue_1, 1.0, 1.0)
        self.color_1 = (int(color_1_hsv[0] * 255), int(color_1_hsv[1] * 255), int(color_1_hsv[2] * 255))

        # Define Color 2
        color_2_hsv = colorsys.hsv_to_rgb(self.hue_2, 1.0, 1.0)
        self.color_2 = (int(color_2_hsv[0] * 255), int(color_2_hsv[1] * 255), int(color_2_hsv[2] * 255))

        self.time_0 = time.time()

        return

    def update(self):

        # Set all LEDs to the background color
        dot_colors = [self.color_1] * self.number_of_leds

        # Calculate wipe position (-1 fully open ... +1 fully closed). Amplifying the
        # sine before clamping makes it dwell at -1/+1 for a visible portion of the
        # cycle instead of only touching them for an instant.
        elapsed_time = time.time() - self.time_0
        raw_position = math.sin((2*math.pi) * (elapsed_time / self.period))
        position = max(-1.0, min(1.0, raw_position * self.dwell_factor))
        fraction = (position + 1) / 2  # 0 = fully open, 1 = fully closed

        # Two arms grow from the two ends toward the middle. Sizing them ceil/floor of
        # N/2 (instead of both from one shared, floor-capped position) means they sum
        # to exactly number_of_leds at fraction=1, so every LED gets covered at full
        # close, regardless of whether number_of_leds is odd or even.
        low_arm_max = math.ceil(self.number_of_leds / 2)
        high_arm_max = self.number_of_leds - low_arm_max
        low_size = round(fraction * low_arm_max)
        high_size = round(fraction * high_arm_max)

        # Arm growing from the start of the strip
        for i in range(low_size):
            dot_colors[i] = self.color_2

        # Arm growing from the end of the strip
        for i in range(self.number_of_leds - high_size, self.number_of_leds):
            dot_colors[i] = self.color_2

        # Optional: Change orientation for table
        dot_colors = self.rotate_list(dot_colors, math.floor((self.degrees_rotation/360) * self.number_of_leds))

        return dot_colors
