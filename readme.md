# Adafruit Dotstar Sequence Scripts

This project contains scripts that perform lighting effect sequences for Adafruit Dotstar LED strips.

## "Cuttlefish" Sequence Video

![Demo Video](demo/cuttlefish-video.gif)

[See more video on YouTube](https://www.youtube.com/watch?v=jlwEHKuH5io)

## Sequence Simulations

### Acceleration
![Cuttlefish](demo/acceleration.gif)

### Breathe
![Cuttlefish](demo/breathe.gif)

### Clock
![Clock](demo/clock.gif)

### Crossing
![Crossing](demo/crossing.gif)

### Read from CSV file (Blink)
![CSV](demo/csv.gif)

### Cuttlefish
![Cuttlefish](demo/cuttlefish.gif)

### Fade
![Fade](demo/fade.gif)

### Read from PNG image file (Fire)
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

### Stripes
![Stripes](demo/stripes.gif)

## Hardware Recommendations

 - [Raspberry Pi 3](https://www.adafruit.com/category/105)
 - [Adafruit Dotstar LED Strip](https://learn.adafruit.com/adafruit-dotstar-leds)
 - [Breadboard](https://www.adafruit.com/product/239)
 - [Jumper Wires](https://www.adafruit.com/category/306)
 - [5V Power Supply](https://www.adafruit.com/product/1466) (2-4 Amps recommended)

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

### Install

The Python scripts will likely need packages installed using a Python package manager like [PIP](https://packaging.python.org/en/latest/guides/tool-recommendations/).

```
pip install -r requirements.txt
```

### Run

Run the sequence on an LED strip.

```
python play.py cuttlefish
```

## Folder Descriptions

##### 2d-simulator

Run a browser-based 2D simulation of the Sequence with WebGL shader

##### 3d-simulator

Run a browser-based 3D simulation of the Sequence using [Three.js](https://threejs.org)

##### data

Contains static data to be read in for rendering a sequence

##### demo

Contains project documentation resources

##### pattern

Python modules for static lighting patterns

##### renderings

Contain images created by render-sequence.py

##### sequence

Python modules for animated lighting sequences

##### server

A web server for controller lighting sequences remotely

```
python ./server/index.py
```

##### shows

Contains show definitions in JSON format. Used by schedule.py.


## Script Descriptions

##### demo.py

Run a demonstration show on the LED strip. This will go through several sequences as defined in a JSON file.

##### play.py

Run a single sequence on an LED strip.

##### render-sequence.py

Render a Sequence to a static PNG image where each line represents a frame of the Sequence, and each column
represents a single LED in the strand.

##### schedule.py

Run this script continuously with different sequences scheduled for each day. This should generally be run
as a background process.

##### simulate.py

Simulate and save a Sequence as an animated GIF (as displayed in this readme file).

## 2D Simulator (Shader)

![Browser 2D Simulator](demo/2d-simulator.png)

This code runs a local webserver that will read a Sequence represented as a PNG image and render it as
a WebGL shader.

From the `2d-simulator` directory:

### Install Once:
```
npm install
```

### Run:
```
npm run dev
```

## 3D Simulator

![Browser 3D Simulator](demo/3d-simulator.png)

This code includes a browser-based simulator to display the lighting sequences. It uses [Node](https://nodejs.org/)
and [Three.js](https://threejs.org/). This reads sequences as PNG images, where each column of the image represents
a single LED in the strand, and each row represents a frame of the animated sequence.

From the `3d-simulator` directory:

### Install Once:
```
npm install
```

### Run:
```
npm run dev
```

Running `npm run dev` will start a server using [Vite](https://vitejs.dev/) and provide a locally hosted URL to load in your browser to view the simulation.

## Resources

- [Adafruit DotStar LEDs](https://learn.adafruit.com/adafruit-dotstar-leds/overview)
- [CircuitPython DotStar](https://learn.adafruit.com/circuitpython-essentials/circuitpython-dotstar)
- [Blinka Test Script](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)
- [Gradient Generator Tool](https://learnui.design/tools/gradient-generator.html)

## License

[![Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://i.creativecommons.org/l/by-nd/2.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

This work is licensed under a [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) License.

This project makes use of the [Adafruit CircuitPython DotStar](https://github.com/adafruit/Adafruit_CircuitPython_DotStar) library, Three.js and other third party code. When using this project,
please adhere to their respective licenses as necessary.