import csv
import os.path

class TextFileDemo:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds
        self.iteration = 0
        self.sequence = []

    # From https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def setup(self, input_file):

        # Define path (for Python 3.5)
        my_path = os.path.abspath(os.path.dirname(__file__))
        file_source = os.path.join(my_path, "../" f"{input_file}")

        # Load image in RGB format and get dimensions:
        with open(file_source, newline='') as csvfile:
            file = csv.reader(csvfile, delimiter=',', quotechar='"')
            for line in file:
                self.sequence.append(line)

        return

    def update(self):

        # Initialize LED values
        leds = [(0, 0, 0)] * self.number_of_leds

        line_number = self.iteration

        # Loop through data from file
        for i in range(len(self.sequence[line_number])):
            leds[i] = self.hex_to_rgb(self.sequence[line_number][i])

        # Increment iteration counter.
        # Reset once it exceeds image height
        self.iteration += 1
        if self.iteration >= len(self.sequence):
            self.iteration = 0

        return leds
