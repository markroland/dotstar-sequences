# Control Adafruit Dotstar LEDs using Flask Web Server
#
# Run as root
#
# Run in background:
#  nohup sudo python3 ./dotstar_flask.py
#
# curl http://192.168.0.14:5007/job
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

@app.route('/color')
def color():
    dots.brightness=1.0
    dots.fill((255, 0, 0))
    return 'Color'

@app.route('/rainbow')
def cakes():
    return 'Rainbow'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5007)
