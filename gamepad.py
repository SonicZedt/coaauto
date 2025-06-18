import vgamepad as vg
import random
import time

class Gamepad:
    def __init__(self):
        self.gamepad = vg.VX360Gamepad()
    
    def press_button(self, btn: vg.XUSB_BUTTON, press_delay: float = None):
        self.gamepad.press_button(button=btn)
        self.gamepad.update()

        if press_delay:
            time.sleep(press_delay)
        else:
            self.delay()

        self.gamepad.release_button(button=btn)
        self.gamepad.update()
        self.delay()

    def hold_button(self, btn: vg.XUSB_BUTTON, update = True):
        self.gamepad.press_button(button=btn)

        if update:
            self.gamepad.update()

        self.delay()

    def release_button(self, btn: vg.XUSB_BUTTON, update = True):
        self.gamepad.release_button(btn)

        if update:
            self.gamepad.update()

        self.delay()

    def left_analog(self, x: float, y: float, delay: float = 0):
        self.gamepad.left_joystick_float(x_value_float=x, y_value_float=y)
        self.gamepad.update()

        if delay == 0:
            self.delay()
        else:
            time.sleep(delay)

    def left_analog_reset(self):
        self.gamepad.left_joystick_float(x_value_float=0, y_value_float=0)
        self.gamepad.update()
        self.delay()

    def right_analog(self, x: float, y: float):
        self.gamepad.right_joystick_float(x_value_float=x, y_value_float=y)
        self.gamepad.update()
        self.delay()

    def right_analog_reset(self):
        self.gamepad.right_joystick_float(x_value_float=0, y_value_float=0)
        self.gamepad.update()
        self.delay()

    def delay(self):
        time.sleep(random.uniform(0.1, 0.5))
    