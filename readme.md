# Adafruit Dotstar Sequence Scripts

This project contains scripts that perform lighting effect sequences for Adafruit Dotstar LED strips.

## "Cuttlefish" Sequence Video

![Demo Video](demo/cuttlefish-video.gif)

## "Cuttlefish" Sequence Simulation

![Demo Video](demo/cuttlefish.gif)



## Hardware Recommendations

 - [Raspberry Pi 3](https://www.adafruit.com/category/105)
 - [Adafruit Dotstar LED Strip](https://learn.adafruit.com/adafruit-dotstar-leds)
 - [Breadboard](https://www.adafruit.com/product/239)
 - [Jumber Wires](https://www.adafruit.com/category/306)
 - [Power Supply](https://www.adafruit.com/product/1466)


## Software Recommendations

 - Python 3.5+
 - [Adafruit CircuitPython](https://github.com/adafruit/circuitpython)


## Circuit

```
TBD
```


## Usage

```
python3 play.py cuttlefish
```


## Folder Descriptions

##### data

Contains static data to be read in for rendering a sequence

##### demo

Contains project documentation resources

##### pattern

Python modules for static lighting patterns

##### sequence

Python modules for animated lighting sequences

##### server

A web server for controller lighting sequences remotely

```
python3 ./server/index.py
```


## Script Descriptions

##### crossfade.py

Test script for a smooth cross-fade transition between two sequences.

##### dotstar_basic.py

Fill the LEDs with a solid color.

##### dotstar_fade.py

Fade from one color to another. RGB and HSV fade modes are supported.

##### dotstar_off.py

Turn off the Dotstar strip. This is useful if the strip is left lit by a previously run script.

##### dotstar_rainbow.py

Render the full color spectrum across the strip and slowly translate their position over time.

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



## Resources

- [Adafruit DotStar LEDs](https://learn.adafruit.com/adafruit-dotstar-leds/overview)
- [CircuitPython DotStar](https://learn.adafruit.com/circuitpython-essentials/circuitpython-dotstar)
- [Blinka Test Script](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)

## License

[![Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://i.creativecommons.org/l/by-nd/2.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

This work is licensed under a [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) License.

This work makes use of the [Adafruit CircuitPython DotStar](https://github.com/adafruit/Adafruit_CircuitPython_DotStar) library.

