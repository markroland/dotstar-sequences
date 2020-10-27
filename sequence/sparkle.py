import math
import random
import colorsys

class Led:
  def __init__(self, color, period, phase):
    self.color = color
    self.period = period
    self.phase = phase

class Sparkle:

    def __init__(self, number_of_leds):
        self.number_of_leds = number_of_leds
        self.Leds = []
        # self.Led = Led()

    def setup(self):

        # Generate random "gold" colors
        for i in range(self.number_of_leds):
            hsv_color = colorsys.hsv_to_rgb(random.randrange(10, 60) / 360.0, 1.0, random.randrange(60, 95) / 100)
            r = int(hsv_color[0] * 255)
            g = int(hsv_color[1] * 255)
            b = int(hsv_color[2] * 255)
            period = random.randrange(10, 50) / 10
            phase = 2 * math.pi * random.random()
            self.Leds.append(Led((r,g,b), period, phase))

    def update(self, time):

        leds = [(20, 10, 0)] * self.number_of_leds

        twinkle_led = random.randrange(0, self.number_of_leds-1)

        # Decay
        # twinkle_brightness = (0.5 * math.exp(-1/2 * time)) + 0.5
        # print(twinkle_brightness)

        # Growth
        # twinkle_brightness = 1 - math.exp(-1/5 * time)

        # Gaussian
        # https://people.richland.edu/james/lecture/m116/logs/models.html
        # twinkle_brightness = a * math.exp (-(time-c) / b)2

        # if (twinkle_brightness < 0.5):
        #     twinkle_brightness = 0.5

        # for i in range(self.number_of_leds):
        #     hsv_color = colorsys.rgb_to_hsv(leds[i][0], leds[i][1], leds[i][2])
        #     # if (i == 0):
        #         # print((hsv_color[2] / 255) * twinkle_brightness)
        #     rgb_color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], twinkle_brightness)
        #     # rgb_color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], (hsv_color[2] / 255) * twinkle_brightness)
        #     r = int(rgb_color[0] * 255)
        #     g = int(rgb_color[1] * 255)
        #     b = int(rgb_color[2] * 255)
        #     leds[i] = (r, g, b)

        for i in range(self.number_of_leds):
            if (i % 4 != 0):
                continue
            hsv_color = colorsys.rgb_to_hsv(self.Leds[i].color[0], self.Leds[i].color[1], self.Leds[i].color[2])
            led_brightness = 0.5 + 0.4 * math.sin( 2 * math.pi * (1/self.Leds[i].period) * time + self.Leds[i].phase)
            # print(led_brightness)
            rgb_color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], led_brightness)
            r = int(rgb_color[0] * 255)
            g = int(rgb_color[1] * 255)
            b = int(rgb_color[2] * 255)
            leds[i] = (r, g, b)
            # leds[i] = (self.Leds[i].color[0], self.Leds[i].color[1], self.Leds[i].color[2])

        return leds
