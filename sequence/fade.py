import time
import colorsys

class Fade:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds

    def fade_component(self, start, finish, step, steps):
        if (start > finish):
            # value = start - ((start - finish) * (step / (steps-1)))
            value = start - ((start - finish) * (step/steps))
        else:
            # value = start + ((finish - start) * (step / (steps-1)))
            value = start + ((finish - start) * (step/steps))
        return value

    def setup(self, fade_type, time_period_seconds, colors_start, colors_end):
        self.time_period = time_period_seconds
        self.fade_type = fade_type
        self.colors_start = colors_start
        self.colors_end = colors_end
        self.time_0 = time.time()
        self.time = time.time() - self.time_0
        return

    def update(self):

        self.time = time.time() - self.time_0

        if (self.time >= self.time_period):
            return self.colors_end

        leds = [(0, 0, 0)] * self.number_of_leds

        # Initialize array
        for i in range(self.number_of_leds):

            r = 0
            g = 0
            b = 0

            # Method 1: RGB component fade - goes through white
            if self.fade_type == "rgb":
                r = self.fade_component(self.colors_start[i][0], self.colors_end[i][0], self.time, self.time_period)
                g = self.fade_component(self.colors_start[i][1], self.colors_end[i][1], self.time, self.time_period)
                b = self.fade_component(self.colors_start[i][2], self.colors_end[i][2], self.time, self.time_period)

            # Method 2: HSV hue vade - goes around color wheel
            elif self.fade_type == "hsv":
                h = self.fade_component(colorsys.rgb_to_hsv(self.colors_start[i][0],self.colors_start[i][1],self.colors_start[i][2])[0], colorsys.rgb_to_hsv(self.colors_end[i][0], self.colors_end[i][1], self.colors_end[i][2])[0], self.time, self.time_period)
                s = self.fade_component(colorsys.rgb_to_hsv(self.colors_start[i][0],self.colors_start[i][1],self.colors_start[i][2])[1], colorsys.rgb_to_hsv(self.colors_end[i][0], self.colors_end[i][1], self.colors_end[i][2])[1], self.time, self.time_period)
                v = self.fade_component(colorsys.rgb_to_hsv(self.colors_start[i][0],self.colors_start[i][1],self.colors_start[i][2])[2], colorsys.rgb_to_hsv(self.colors_end[i][0], self.colors_end[i][1], self.colors_end[i][2])[2], self.time, self.time_period)
                new_color = colorsys.hsv_to_rgb(h,s,v)
                r = new_color[0]
                g = new_color[1]
                b = new_color[2]

            # Assign RGB to all LEDs
            leds[i] = (int(r), int(g), int(b))

        return leds
