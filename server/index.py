# Control Adafruit Dotstar LEDs using Flask Web Server
#
# Run as root
#
# Run in background:
#  nohup sudo python3 ./flask.py
#
# curl -X POST -d "intensity=0.5&red=255&green=0&blue=0" http://localhost:5007/color
#
# curl -X POST -d "intensity=0.5&red=255&green=0&blue=0" http://192.168.0.14:5007/color
#

# Include: Flask web server
from flask import Flask, request, render_template
from sequence.breathe import *
import subprocess

# Include: Adafruit Dotstar
import board
import adafruit_dotstar

# Initialize an Adafruit Dotstar object
dots = adafruit_dotstar.DotStar(board.SCK, board.MOSI, 120, brightness=0.2)

# Create new Flask app
app = Flask(__name__)

my_subprocess = None

dotstar_state = "off"

# Route: Front Controller
@app.route('/')
def index():
    return render_template('index.html')

# Route: Color
@app.route('/color', methods=['GET', 'POST'])
def color():

  global dotstar_state

  if request.method == 'POST':

    # if type(my_subprocess) is subprocess:
    if my_subprocess is not None:
    # poll = my_subprocess.poll()
    # if poll == None:
      my_subprocess.terminate()

    # TODO: determine if "off" has been called, then dots has to be re-initi
    # https://github.com/adafruit/Adafruit_CircuitPython_DotStar/blob/master/adafruit_dotstar.py

    red = request.form.get('red')
    green = request.form.get('green')
    blue = request.form.get('blue')
    intensity = request.form.get('intensity')

    dots.brightness=float(intensity)
    dots.fill((int(red), int(green), int(blue)))

    dotstar_state = "solid"

    return '''Red: {}, Green: {}, Blue: {}, Intensity: {}'''.format(red, green, blue, intensity)

  return '''<form method="POST">
      Red: <input type="text" name="red"><br>
      Green: <input type="text" name="green"><br>
      Blue: <input type="text" name="blue"><br>
      Intensity: <input type="text" name="intensity"><br>
      <input type="submit" value="Submit"><br>
    </form>'''

# Route: Sequence
@app.route('/sequence', methods=['POST'])
def sequence_request():

  global my_subprocess
  global dotstar_state

  if request.method == 'POST':

    response = ""

    # if type(my_subprocess) is subprocess:
    if my_subprocess is not None:
    # poll = my_subprocess.poll()
    # if poll == None:
      my_subprocess.terminate()
      response = "terminated"

    allowed_sequences = [
      "breathe",
      "random"
    ]

    requested_sequence = request.form.get('sequence')

    for i in allowed_sequences:
      if i == requested_sequence:
        my_subprocess = subprocess.Popen(["python3", "/home/pi/Documents/Dotstar/play.py", requested_sequence])
        dotstar_state = requested_sequence
        response = str(my_subprocess.pid)

    return response

# Route: Off
@app.route('/status', methods=['GET', 'POST'])
def off():

  global dotstar_state

  if request.method == 'POST':

    # Turn off all pixels
    dots.deinit();

    return 'Off'

  return dotstar_state

# Front Controller
if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5007)