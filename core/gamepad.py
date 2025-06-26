import vgamepad as vg
import random
import time
from model import MatchTemplate

class Gamepad:
    def __init__(self):
        self.gamepad = vg.VX360Gamepad()

    def set_velocity(self, vx: float = None, vy: float = None):
        if vx:
            self.vx = vx
        
        if vy:
            self.vy = vy
    
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

    def left_analog(self, x: float, y: float, delay: float = None):
        self.gamepad.left_joystick_float(x_value_float=x, y_value_float=y)
        self.gamepad.update()

        if delay is None:
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
    
    def left_trigger(self, delay: float = None):
        self.gamepad.left_trigger(value=255)
        self.gamepad.update()

        if delay is None:
            self.delay()
        else:
            time.sleep(delay)

        self.gamepad.left_trigger(value=0)
        self.gamepad.update()
        self.delay()

    def right_trigger(self, delay: float = None):
        self.gamepad.right_trigger(value=255)
        self.gamepad.update()

        if delay is None:
            self.delay()
        else:
            time.sleep(delay)

        self.gamepad.right_trigger(value=0)
        self.gamepad.update()
        self.delay()

    def get_analog_direction(
            self, 
            src: MatchTemplate, 
            dst: MatchTemplate, 
            speed: float = 4) -> tuple[float, float]:        
        src_x, src_y = src.center
        dst_x, dst_y = dst.center

        # calculate distance
        # distance is relateive to screen resolution
        distance_x = dst_x - src_x
        distance_y = -(dst_y - src_y)

        limit_x = src.width
        limit_y = src.height

        # normalize the distance
        analog_x = distance_x / limit_x * speed
        analog_y = distance_y / limit_y * speed

        if abs(analog_x) > 1:
            analog_x = 1 if analog_x > 0 else -1

        if abs(analog_y) > 1:
            analog_y = 1 if analog_y > 0 else -1

        return (analog_x, analog_y)

    def delay(self):
        time.sleep(random.uniform(0.1, 0.5))    
