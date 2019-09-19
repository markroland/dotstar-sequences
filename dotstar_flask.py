# Control Adafruit Dotstar LEDs using Flask Web Server
#
# Run as root
#
# Run in background:
#  nohup sudo python3 ./dotstar_flask.py
#
# curl -X POST -d "red=255&green=0&blue=0" http://localhost:5007/color
#
# curl -X POST -d "red=255&green=0&blue=0" http://192.168.0.14:5007/color
#

# Include: Flask web server
from flask import Flask, request

# Include: Adafruit Dotstar
import board
import adafruit_dotstar

# Initialize an Adafruit Dotstar object
dots = adafruit_dotstar.DotStar(board.SCK, board.MOSI, 120, brightness=0.2)

# Create new Flask app
app = Flask(__name__)

# Route: Color
@app.route('/color', methods=['GET', 'POST'])
def color():

    if request.method == 'POST':

        # TODO: determine if "off" has been called, then dots has to be re-initi
        # https://github.com/adafruit/Adafruit_CircuitPython_DotStar/blob/master/adafruit_dotstar.py

        red = request.form.get('red')
        green = request.form.get('green')
        blue = request.form.get('blue')
        intensity = request.form.get('intensity')

        dots.brightness=float(intensity)
        dots.fill((int(red), int(green), int(blue)))

        return '''Red: {}, Green: {}, Blue: {}, Intensity: {}'''.format(red, green, blue, intensity)

    return '''<form method="POST">
              Red: <input type="text" name="red"><br>
              Green: <input type="text" name="green"><br>
              Blue: <input type="text" name="blue"><br>
              Intensity: <input type="text" name="intensity"><br>
              <input type="submit" value="Submit"><br>
          </form>'''

# Route: Off
@app.route('/off', methods=['GET', 'POST'])
def off():

    if request.method == 'POST':

        # Turn off all pixels
        dots.deinit();

        return 'Off'

    return '''<form method="POST">
              <select name="power">
                <option value="on">On</option>
                <option value="off">Off</option>
                <input type="submit" value="Submit">
              </select>
          </form>'''

# Route: Rainbow
@app.route('/rainbow')
def rainbow():
    return 'TODO: This would initiate the code in dotstar_rainbow.py'

# Front Controller
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5007)