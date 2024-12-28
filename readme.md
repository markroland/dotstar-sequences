# Adafruit Dotstar Sequence Scripts

This project contains scripts that perform lighting effect sequences for Adafruit Dotstar LED strips.

## "Cuttlefish" Sequence Video

![Demo Video](demo/cuttlefish-video.gif)

## Sequence Simulations

### Acceleration
![Cuttlefish](demo/acceleration.gif)

### Breathe
![Cuttlefish](demo/breathe.gif)

### Clock
![Clock](demo/clock.gif)

### Crossing
![Crossing](demo/crossing.gif)

### Cuttlefish
![Cuttlefish](demo/cuttlefish.gif)

### Fade
![Fade](demo/fade.gif)

### Fire
![Fire](demo/fire.gif)

### Points
![Points](demo/points.gif)

### Random
![Random](demo/random.gif)

### Sparkle
![Sparkle](demo/sparkle.gif)

### Spectrum Fade
![Spectrum Fade](demo/spectrum-fade.gif)

### Spectrum Slide
![Spectrum Slide](demo/spectrum-slide.gif)

### Spectrum Wipe
![Spectrum Wipe](demo/spectrum-wipe.gif)

## Hardware Recommendations

 - [Raspberry Pi 3](https://www.adafruit.com/category/105)
 - [Adafruit Dotstar LED Strip](https://learn.adafruit.com/adafruit-dotstar-leds)
 - [Breadboard](https://www.adafruit.com/product/239)
 - [Jumper Wires](https://www.adafruit.com/category/306)
 - [Power Supply](https://www.adafruit.com/product/1466)

## Software Recommendations

 - Python 3.5+
 - [Adafruit CircuitPython](https://github.com/adafruit/circuitpython)


## Circuit

The Dotstar has four connections:

1) **Ground** - Connect this to the common ground for the power supply and Raspberry Pi (i.e. ground rail of a breadboard)
2) **Power** - Connect this to a +5V power supply. Make sure your supply has enough current for your LED strip.
3) **Clock Input (CI)** - Connect this to Raspberry Pi's SPI SCLK Pin
4) **Data Input (DI)** - Connect this to Raspberry Pi's SPI MOSI Pin

See [Adafruit's Power and Connections](https://learn.adafruit.com/adafruit-dotstar-leds/power-and-connections) guide for more information.

## Usage

### Setup

Copy and set the .env Environment file for your configuration

```
cp .env.example .env
```

### Run

```
python play.py cuttlefish
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
python ./server/index.py
```

## Script Descriptions

##### play.py

##### demo.py

##### schedule.py

Run this script continuously with different sequences scheduled for each day.

##### simulate.py

Render a Sequence to an animated GIF image.

## Simulator

![Browser Simulator](demo/simulator.png)

This code includes a browser-based simulator to display the lighting sequences. It uses [Node](https://nodejs.org/)
and [Three.js](https://threejs.org/). At this time only the `breathe` sequence is programmed as JavaScript.
Additional work is required to implement the other sequences.

From the simulator directory:
```
npm install
npx vite
```

Once [Vite](https://vitejs.dev/) is running you can view the simulator in your browser. Vite should tell you a URL to load, like http://localhost:5173.

## Resources

- [Adafruit DotStar LEDs](https://learn.adafruit.com/adafruit-dotstar-leds/overview)
- [CircuitPython DotStar](https://learn.adafruit.com/circuitpython-essentials/circuitpython-dotstar)
- [Blinka Test Script](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)
- [Gradient Generator Tool](https://learnui.design/tools/gradient-generator.html)

## License

[![Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://i.creativecommons.org/l/by-nd/2.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

This work is licensed under a [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) License.

This work makes use of the [Adafruit CircuitPython DotStar](https://github.com/adafruit/Adafruit_CircuitPython_DotStar) library.