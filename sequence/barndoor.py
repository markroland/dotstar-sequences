import time
import math
import colorsys

class Barndoor:

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

        # Define Color 1 (background)
        color_1_hsv = colorsys.hsv_to_rgb(self.hue_1, 1.0, 1.0)
        self.color_1 = (int(color_1_hsv[0] * 255), int(color_1_hsv[1] * 255), int(color_1_hsv[2] * 255))

        # Define Color 2 (doors)
        color_2_hsv = colorsys.hsv_to_rgb(self.hue_2, 1.0, 1.0)
        self.color_2 = (int(color_2_hsv[0] * 255), int(color_2_hsv[1] * 255), int(color_2_hsv[2] * 255))

        self.time_0 = time.time()

        return

    def update(self):

        # Set all LEDs to the background color
        dot_colors = [self.color_1] * self.number_of_leds

        # Calculate door position (-1 fully open ... +1 fully closed). Phase-shifted
        # (a negative cosine instead of a sine) so the sequence starts fully open at
        # elapsed_time = 0, rather than mid-swing. Amplifying it before clamping makes
        # it dwell at -1/+1 for a visible portion of the cycle instead of only
        # touching them for an instant.
        elapsed_time = time.time() - self.time_0
        raw_position = -math.cos((2*math.pi) * (elapsed_time / self.period))
        position = max(-1.0, min(1.0, raw_position * self.dwell_factor))
        fraction = (position + 1) / 2  # 0 = fully open (doors at their sides), 1 = fully closed (doors meet)

        # The ring is split into two halves, each with its own pair of doors. Every
        # door is anchored to an end of its half (the "sides") and grows toward the
        # midpoint of that half (where it meets its partner), instead of one door
        # sweeping across the entire strip like Wipe does. That keeps the two meeting
        # points on opposite sides of the circle, so it reads as doors sliding closed
        # rather than a single wipe travelling all the way around.
        half_boundaries = [0, math.ceil(self.number_of_leds / 2), self.number_of_leds]

        for h in range(2):
            half_start = half_boundaries[h]
            half_end = half_boundaries[h + 1]
            half_length = half_end - half_start

            low_max = math.ceil(half_length / 2)
            high_max = half_length - low_max
            low_size = round(fraction * low_max)
            high_size = round(fraction * high_max)

            # Door sliding in from the start of this half
            for i in range(half_start, half_start + low_size):
                dot_colors[i] = self.color_2

            # Door sliding in from the end of this half
            for i in range(half_end - high_size, half_end):
                dot_colors[i] = self.color_2

        # Optional: Change orientation for table
        dot_colors = self.rotate_list(dot_colors, math.floor((self.degrees_rotation/360) * self.number_of_leds))

        return dot_colors
