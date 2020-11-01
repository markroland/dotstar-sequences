from datetime import datetime
import time

class Clock:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds

    # Rotate array values
    def rotate_list(self, my_list, position):
        return my_list[position:] + my_list[:position]

    def setup(self, rotation):
        self.rotation = rotation
        return

    def update(self):

        # Get clock hand positions
        second_index = round((float(datetime.now().strftime('%S.%f')) / 60) * self.number_of_leds)
        if second_index >= self.number_of_leds:
            second_index = 0

        minute_index = round((int(datetime.now().strftime('%M')) / 60) * self.number_of_leds)
        if minute_index >= self.number_of_leds:
            minute_index = 0

        hour_index = round(((int(datetime.now().strftime('%H')) % 12) / 12) * self.number_of_leds);
        hour_index += round(
            ((int(datetime.now().strftime('%M')) / 60) / 12) * self.number_of_leds
        )
        if hour_index >= self.number_of_leds:
            hour_index = 0

        # Initialization. Fill an array of length "self.number_of_leds" with zeros
        dot_colors = [(0,0,0)] * self.number_of_leds

        # Solid fill to hours
        dot_colors[hour_index] = (255, 0, 0)
        for j in range(self.number_of_leds):
            if j < hour_index:
                dot_colors[j] = (8, 0, 0)

        # Set 12 points of clockface
        dot_colors[0] = (0, 64, 0)
        for i in range(1, 12):
            index = round((i/12) * self.number_of_leds)
            dot_colors[index] = (0, 4, 0)

        # Minute and Second hands
        dot_colors[second_index] = (64, 64, 64)
        dot_colors[minute_index] = (0, 0, 255)

        # Rotate clockface for the orientation of the viewer
        dot_colors = self.rotate_list(dot_colors, self.rotation)

        return dot_colors
