import asyncio
import socketio
import vgamepad as vg
import time 

sio = socketio.AsyncClient(ssl_verify=False)
gamepad = vg.VX360Gamepad()

LAST_UPDATE = 0  # Global timestamp tracker
UPDATE_INTERVAL = 0.01  # 10ms delay

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
    print('🔗 Connection established')
    await sio.emit('connect-device', "host")
    print("✅ Connected as HOST!")
    await sio.emit("join-room", "android")


@sio.event
async def gyro(data):
    """ Process gyroscope input with minimal latency """
    global LAST_UPDATE

    # Update only if at least 10ms have passed
    current_time = time.time()
    if current_time - LAST_UPDATE < UPDATE_INTERVAL:
        return
    LAST_UPDATE = current_time
    
    STEERING = 100
    MULTIPLIER = 1.4
    TRIGGER = (data['y'] / STEERING) * MULTIPLIER
    TRIGGER = max(min(TRIGGER, 1), -1)  # Clamp values between -1 and 1

    gamepad.left_joystick_float(x_value_float=TRIGGER, y_value_float=0)
    gamepad.update()
    
    print(f"🎮 Gyro Input: {TRIGGER:.2f}")


@sio.event
async def disconnect():
    print('❌ Disconnected from server')


@sio.event
async def buttonPress(button):
    """ Handles button press with improved responsiveness """
    gamepad.press_button(button=BUTTON_LIST[button])
    gamepad.update()
    await asyncio.sleep(0.1)  # Faster response (100ms instead of 200ms)
    gamepad.release_button(button=BUTTON_LIST[button])
    gamepad.update()


@sio.event
async def buttonTouchStart(button):
    """ Handles continuous button press without unnecessary delay """
    if button == "RT":
        gamepad.right_trigger_float(1)
    elif button == "LT":
        gamepad.left_trigger_float(1)
    else:
        gamepad.press_button(button=BUTTON_LIST[button])

    gamepad.update()


@sio.event
async def buttonTouchEnd(button):
    """ Handles releasing of button inputs """
    if button == "RT":
        gamepad.right_trigger_float(0)
    elif button == "LT":
        gamepad.left_trigger_float(0)
    else:
        gamepad.release_button(button=BUTTON_LIST[button])

    gamepad.update()


async def main():
    """ Main async loop to keep the client connected """
    while True:
        try:
            await sio.connect('https://localhost:5000', wait_timeout=5)
            print("🚀 Connected!")
            await sio.wait()
        except Exception as e:
            print(f"🔄 Reconnecting... {e}")
            await asyncio.sleep(2)  # Retry every 2 seconds


if __name__ == '__main__':
    asyncio.run(main())
