import time
import colorsys

class Crossing:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds

    def rotate_list(self, my_list, position):
        return my_list[position:] + my_list[:position]

    # Add the RGB components of 2 colors
    def colors_add(self, colors_1, colors_2):

        colors = [(0,0,0)] * self.number_of_leds

        # Initialize array
        for i in range(self.number_of_leds):
            # Calculate color components
            r = min(colors_1[i][0] + colors_2[i][0], 255)
            g = min(colors_1[i][1] + colors_2[i][1], 255)
            b = min(colors_1[i][2] + colors_2[i][2], 255)

            # Assign RGB to all LEDs
            colors[i] = (int(r), int(g), int(b))

        return colors

    def setup(self, hue_1, hue_2, length_1, length_2):
        self.random_hue_1 = hue_1
        self.random_hue_2 = hue_2
        self.length = length_1
        self.length_2 = length_2
        self.time_0 = time.time()

        return

    def update(self):

        # Update time
        self.time = time.time() - self.time_0

        # Change offset (every 1/10 of a second for example)
        # Increase the last number (denominator) makes the animation faster
        offset = int(((self.time) * 1000) / 30)
        offset = offset % self.number_of_leds

        # Color 1
        colors_1 = [(4,4,4)] * self.number_of_leds
        for i in range(0,self.length):
            intensity = 1 - (i/self.length)
            color_1_hsv = colorsys.hsv_to_rgb(self.random_hue_1, 1.0, intensity)
            colors_1[i] = (int(color_1_hsv[0] * 255), int(color_1_hsv[1] * 255), int(color_1_hsv[2] * 255))
        colors_1 = self.rotate_list(colors_1, offset)

        # Color 2 - on "opposite" side of strip going the opposite direction
        offset_2 = int(((self.time) * 1000) / 40)
        offset_2 = offset_2 % self.number_of_leds

        colors_2 = [(4,4,4)] * self.number_of_leds
        for i in range(0,self.length_2):
            intensity = 1 - (i/self.length_2)
            color_2_hsv = colorsys.hsv_to_rgb(self.random_hue_2, 1.0, intensity)
            colors_2[i] = (int(color_2_hsv[0] * 255), int(color_2_hsv[1] * 255), int(color_2_hsv[2] * 255))
        colors_2.reverse()
        colors_2 = self.rotate_list(colors_2, -offset_2)

        # Add colors
        leds = self.colors_add(colors_1, colors_2)

        return leds
