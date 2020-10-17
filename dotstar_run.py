# Adafruit Dotstar RGB LED Strip
#
# Run a squence for a set period of time

# Import required libraries
import board
import adafruit_dotstar as dotstar
import time
import random
from datetime import datetime
from sequences import *

# Write a List of colors to the Dotstar object and then Show them
def render(colors):

    # Assign pattern colors to Dotstar object
    for i in range(number_of_leds):
        dots[i] = colors[i]

    # Render LEDs
    dots.show()

# Add the RGB components of 2 colors
def colors_add(colors_1, colors_2):

    colors = [(0,0,0)] * number_of_leds

    # Initialize array
    for i in range(number_of_leds):
        # Calculate color components
        r = min(colors_1[i][0] + colors_2[i][0], 255)
        g = min(colors_1[i][1] + colors_2[i][1], 255)
        b = min(colors_1[i][2] + colors_2[i][2], 255)

        # Assign RGB to all LEDs
        colors[i] = (int(r), int(g), int(b))

    return colors

# Set Brightness
brightness = 0.5

# Set time delay between frames (Refresh rate)
frame_delay = 1/60;

# Specify number of pixels
number_of_leds = 119;

# Set start and end hours of the day (i.e. 7am - 10pm)
start_hour = 7
end_hour = 22

# Load color sequence
spectrum_colors = get_sinebow_colors()

# Loop forever
while True:

    # Define now
    today = datetime.now()
    time_now = today.timestamp() # time.time() can also be used
    day_of_week = datetime.now().weekday()

    # Define running time
    time_start = datetime.timestamp(datetime(today.year, today.month, today.day, start_hour, 0, 0))
    time_end = datetime.timestamp(datetime(today.year, today.month, today.day, end_hour, 0, 0))

    # Run this pattern on Friday (day 4 of week)
    if time_now > time_start and time_now < time_end:

        # Instantiate a DotStar LED Strip
        dots = dotstar.DotStar(board.SCK, board.MOSI, number_of_leds, brightness=brightness, auto_write=False)

        if day_of_week == 0:

            while time_now < time_end:

                # # Fill all to black (off)
                # dot_colors = [(0, 0, 0)] * number_of_leds

                # # Turn on selected LED pixel
                # dot_colors[offset] = (255,255,255)

                # # Turn on LED opposite of that one
                # opposite = (offset + int(number_of_leds/2)) % number_of_leds
                # dot_colors[opposite] = (255,255,255)

                # ----

                # Set random color on first iteration only
                try: random_hue
                except NameError: random_hue = random.random()

                # Define Color 1
                # color_1 = (0,64,64)
                color_1_hsv = colorsys.hsv_to_rgb(random_hue, 1.0, 1.0)
                color_1 = (int(color_1_hsv[0] * 255), int(color_1_hsv[1] * 255), int(color_1_hsv[2] * 255))

                # Define Color 2 as an offset from Color 1 around the Hue value of the HSV Color Wheel
                # color_2 = (0,0,64)
                color_2_hsv = colorsys.hsv_to_rgb((random_hue + (1/2)) % 1, 1.0, 1.0)
                color_2 = (int(color_2_hsv[0] * 255), int(color_2_hsv[1] * 255), int(color_2_hsv[2] * 255))

                # Set all
                dot_colors = [color_1] * number_of_leds

                time_now = time.time()

                position = math.sin((2*math.pi) * ((time_now - time_start) / 6))

                # # 0 to 59
                i_position = math.floor(position * (number_of_leds / 4) + (number_of_leds / 4))

                # Top Half
                # dot_colors[i_position] = color_2
                for i in range(i_position):
                    dot_colors[i] = color_2

                # Bottom Half
                # dot_colors[(number_of_leds-1) - i_position] = color_2
                for i in range((number_of_leds-1) - i_position, number_of_leds-1, 1):
                    dot_colors[i] = color_2

                # Optional: Change orientation for table
                degrees_rotation = -45
                dot_colors = rotate_list(dot_colors, math.floor((degrees_rotation/360) * number_of_leds))

                # Render the colors
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(frame_delay)

                # Update time
                time_now = time.time()

            # Fade Off
            brightness_start = brightness
            fade_off_frames = 300
            for i in range(fade_off_frames):
                dots.brightness = brightness - (brightness_start * (i/fade_off_frames))
                dots.show()
                time.sleep(frame_delay)

        elif day_of_week == 1:

            # Fade On
            brightness_start = brightness
            fade_on_frames = 20
            for i in range(fade_on_frames):
                dots.brightness = brightness * (i/fade_on_frames)
                dot_colors = [spectrum_colors[0]] * number_of_leds
                render(dot_colors)
                time.sleep(frame_delay)
            dots.brightness = brightness

            # Loop
            while time_now < time_end:

                # Update time
                time_now = time.time()

                # Calculate offset as a function of time
                offset = int((len(spectrum_colors)-1) * min((time_now - time_start)/(time_end - time_start), 1.0))

                # Set the colors
                dot_colors = [spectrum_colors[offset]] * number_of_leds

                # Render the colors
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(frame_delay)

            # Fade Off
            brightness_start = brightness
            fade_off_frames = 20
            for i in range(fade_off_frames):
                dots.brightness = brightness - (brightness_start * (i/fade_off_frames))
                dots.show()
                time.sleep(frame_delay)

        elif day_of_week == 2:

            # Reload the spectrum colors - one per LED
            spectrum_colors = get_sinebow_colors(number_of_leds)

            # Initialize colors
            dot_colors = [(0, 0, 0)] * number_of_leds

            # Loop
            while time_now < time_end:

                # Update time
                time_now = time.time()

                # Rotate spectrum around strip at one revolution per minute
                offset = int((int(time_now - time_start) % len(spectrum_colors)) * (number_of_leds/60))

                revolutions = int((time_now - time_start) / len(spectrum_colors))

                # Set colors
                dot_colors = spectrum_straight_across_with_rotation(number_of_leds, revolutions, offset, spectrum_colors)

                # Render the colors
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(frame_delay)

        elif day_of_week == 3:

            # Reload the spectrum colors - one per LED
            spectrum_colors = get_sinebow_colors(number_of_leds)

            # Initialize colors
            dot_colors = [(0, 0, 0)] * number_of_leds

            # Loop
            while time_now < time_end:

                # Update time
                time_now = time.time()

                # Rotate spectrum around strip at one revolution per minute
                offset = int((int(time_now - time_start) % len(spectrum_colors)) * (number_of_leds/60))

                # Set colors
                dot_colors = spectrum_slide(number_of_leds, offset, spectrum_colors)

                # Render the colors
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(frame_delay)

        elif day_of_week == 4:

            # Crossing bands

            random_hue_1 = random.random()
            # random_hue_2 = random.random()
            random_hue_2 = random_hue_1 + 0.5 % 1
            length = int(number_of_leds * 0.33)
            length_2 = int(number_of_leds * 0.2)

            # Loop
            while time_now < time_end:

                # Update time
                time_now = time.time()

                # Change offset (every 1/10 of a second for example)
                # Increase the last number (denominator) makes the animation faster
                offset = int(((time_now - time_start) * 1000) / 30)
                offset = offset % number_of_leds

                # Color 1
                colors_1 = [(4,4,4)] * number_of_leds
                for i in range(0,length):
                    intensity = 1 - (i/length)
                    color_1_hsv = colorsys.hsv_to_rgb(random_hue_1, 1.0, intensity)
                    colors_1[i] = (int(color_1_hsv[0] * 255), int(color_1_hsv[1] * 255), int(color_1_hsv[2] * 255))
                colors_1 = rotate_list(colors_1, offset)

                # Color 2 - on "opposite" side of strip going the opposite direction

                offset_2 = int(((time_now - time_start) * 1000) / 40)
                offset_2 = offset_2 % number_of_leds

                colors_2 = [(4,4,4)] * number_of_leds
                for i in range(0,length_2):
                    intensity = 1 - (i/length_2)
                    color_2_hsv = colorsys.hsv_to_rgb(random_hue_2, 1.0, intensity)
                    colors_2[i] = (int(color_2_hsv[0] * 255), int(color_2_hsv[1] * 255), int(color_2_hsv[2] * 255))
                colors_2.reverse()
                colors_2 = rotate_list(colors_2, -offset_2)

                # Add colors
                dot_colors = colors_add(colors_1, colors_2)

                # Render the colors
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(frame_delay)

        elif day_of_week == 5:

            # Solid

            # Loop
            while time_now < time_end:

                # Update time
                time_now = time.time()

                dot_colors = [(255, 0, 0)] * number_of_leds

                # Render the colors
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(60)

        elif day_of_week == 6:

            breathing_period = 4.0;
            dot_colors = [(255, 255, 255)] * number_of_leds

            # Loop
            while time_now < time_end:

                # Update time
                time_now = time.time()

                brightness = breathe(breathing_period, (time_now - time_start) % breathing_period)
                dots.brightness = brightness

                # Render the colors
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(frame_delay)

        else:

            # This should never be reached if there's a case above for every possible
            # day of the week, but hey, if it is reached, show solid red

            # Loop
            while time_now < time_end:

                # Update time
                time_now = time.time()

                dot_colors = [(255, 0, 0)] * number_of_leds

                # Render the colors
                render(dot_colors)

                # Delay before iterating through loop
                time.sleep(60)

        # Disable LEDs at end of active time
        dots.deinit()
