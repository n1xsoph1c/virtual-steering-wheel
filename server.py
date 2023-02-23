from flask import Flask, render_template, request
from flask_socketio import SocketIO
from engineio.payload import Payload

import vgamepad as vg
import time
import logging

logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)

app = Flask(__name__,  static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'

Payload.max_decode_packets = 1000
socketio = SocketIO(app,  async_mode='threading', logging=False)
gamepad = vg.VX360Gamepad()



@app.route('/', methods=['GET', 'POST'])
def home():
   return render_template('index.html')


BUTTON_LIST = {
    'dU': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    'dD': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    'dL': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    'dR': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    'start': vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
    'back': vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
    'LT': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
    'RT': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
    'LS': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    'RS': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    'G': vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,
    'A': vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    'B': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    'X': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    'Y': vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
}


@app.route("/buttonPress", methods=['POST'])
def buttonPress():
    button = request.get_json()
    gamepad.press_button(button=BUTTON_LIST[button])
    gamepad.update()
    time.sleep(0.5)
    gamepad.reset()
    gamepad.update()
    return '200'

@app.route("/buttonTouchStart", methods=['POST'])
def buttonTouchStart():
    button = request.get_json()
    if button == "RT" :
        gamepad.right_trigger_float(1)

    if button == "LT":
        gamepad.left_trigger_float(1)
    
    if button != "RT" and button != "LT":
        gamepad.press_button(button=BUTTON_LIST[button])

    gamepad.update()
    return '200'

@app.route("/buttonTouchEnd", methods=['POST'])
def buttonTouchEnd():
    button = request.get_json()

    if button == "RT" :
        gamepad.right_trigger_float(0)

    if button == "LT":
        gamepad.left_trigger_float(0)
    
    if button != "RT" and button != "LT":
        gamepad.release_button(button=BUTTON_LIST[button])
        
    gamepad.update()
    return '200'

@socketio.on('gyro')
def gyro(data):
    global OLD_STEERING

    DEADZONE = 0.25
    STEERING = data['steering']
    MAX_STEERING = 65

    if STEERING > MAX_STEERING: STEERING = MAX_STEERING
    if STEERING < -MAX_STEERING: STEERING = -MAX_STEERING

    TRIGGER = float("{:.4f}".format((STEERING * (100/ MAX_STEERING) / 100)))
    gamepad.left_joystick_float(x_value_float=TRIGGER, y_value_float=0)
    # gamepad.right_trigger_float(value_float=data['thrust'] / 75)
    # time.sleep(DEADZONE)
    gamepad.update()

    print(f'\nTRIGGER: {TRIGGER} | STEERING: {STEERING} \n')

 
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", ssl_context=("cert.pem", "key.pem"))