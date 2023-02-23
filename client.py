import asyncio
import socketio
import vgamepad as vg

sio = socketio.AsyncClient(ssl_verify=False)
gamepad = vg.VX360Gamepad()

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

@sio.event
async def connect():
    print('connection established')
    await sio.emit('connect-device', "host")
    print("connected as HOST!")
    await sio.emit("join-room", "android")


@sio.event
async def gyro(data):
    STEERING = 100
    MULTIPLIER = 1.4
    TRIGGER = (data['y'] / STEERING) * MULTIPLIER
    if TRIGGER > 1: TRIGGER = 1
    if TRIGGER < -1: TRIGGER = -1
    print(TRIGGER)              
    # if TRIGGER > 0.2: TRIGGER += 0.4
    # if TRIGGER < 0.2: TRIGGER -= 0.4  
    # if TRIGGER < -1: TRIGGER = -1
    # if TRIGGER > 1: TRIGGER = 1            
    # print(TRIGGER, AXIS)
    gamepad.left_joystick_float(x_value_float=TRIGGER, y_value_float=0)
    gamepad.update()

@sio.event
async def disconnect():
    print('disconnected from server')

@sio.event
async def buttonPress(button):
    gamepad.press_button(button=BUTTON_LIST[button])
    gamepad.update()
    await asyncio.sleep(0.5)
    gamepad.reset()
    gamepad.update()

@sio.event
async def buttonTouchStart(button):

    if button == "RT" :
        gamepad.right_trigger_float(1)

    if button == "LT":
        gamepad.left_trigger_float(1)
    
    if button != "RT" and button != "LT":
        gamepad.press_button(button=BUTTON_LIST[button])

    gamepad.update()

@sio.event
async def buttonTouchEnd(button):
    if button == "RT" :
        gamepad.right_trigger_float(0)

    if button == "LT":
        gamepad.left_trigger_float(0)
    
    if button != "RT" and button != "LT":
        gamepad.release_button(button=BUTTON_LIST[button])
        
    gamepad.update()


async def main():
    await sio.connect('https://localhost:3000')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())