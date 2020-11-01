# Adafruit Dotstar Sequence Scripts

This project contains scripts that perform lighting effect sequences for Adafruit Dotstar LED strips.

## "Cuttlefish" Sequence Video

![Demo Video](demo/cuttlefish-video.gif)

## "Cuttlefish" Sequence Simulation

![Demo Video](demo/cuttlefish.gif)



## Folder Descriptions

##### data

Contains static data to be read in for rendering a sequence

##### demo

Contains project documentation resources

##### pattern

Python modules for static lighting patterns

##### sequence

Python modules for animated lighting sequences



## Script Descriptions

##### crossfade.py

Test script for a smooth cross-fade transition between two sequences.

##### dotstar_basic.py

Fill the LEDs with a solid color.

##### dotstar_clock.py

Render a clock face with hour indicators, and hands for the hour, minute and second.

##### dotstar_fade.py

Fade from one color to another. RGB and HSV fade modes are supported.

##### dotstar_off.py

Turn off the Dotstar strip. This is useful if the strip is left lit by a previously run script.

##### dotstar_rainbow.py

Render the full color spectrum across the strip and slowly translate their position over time.

##### dotstar_rgb_input.py

Set all LEDs to a single color defined by command-line arguments.

##### dotstar_run.py

Run a show continuously

##### dotstar_sequences.py

This is a CLI for selecting and running a sequence.

##### dotstar_show.py

This is a test script for cycling through multiple sequences and making a smooth transition between them.

##### dotstar_spectrum.py

Loop through each color in the spectrum as a solid fill.

##### sequences.py

This is a function library of color patterns and sequences.

##### simulate.py

Render a Sequence to an animated GIF image.

##### time-ranged.py

This is a test script for rendering a sequence for a set period of time, for example from 7am to 10pm.

## Resources

- [Adafruit DotStar LEDs](https://learn.adafruit.com/adafruit-dotstar-leds/overview)
- [CircuitPython DotStar](https://learn.adafruit.com/circuitpython-essentials/circuitpython-dotstar)
- [Blinka Test Script](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)
