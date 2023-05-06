import machine
import utime as time
import micropython
from machine import Pin, PWM
from time import sleep
import time
from ssd1306 import SSD1306_I2C

i2c_1 = machine.I2C(1, scl=machine.Pin("GP15"), sda=machine.Pin("GP14"))
oled = SSD1306_I2C(128, 64, i2c_1)

button1 = Pin(8, Pin.IN, Pin.PULL_UP)

pwm = PWM(Pin(20))


class Rotary:
    ROT_CW = 1
    ROT_CCW = 2
    SW_PRESS = 4
    SW_RELEASE = 8

    def _init_(self, dt, clk, sw):
        self.dt_pin = Pin(dt, Pin.IN, Pin.PULL_DOWN)
        self.clk_pin = Pin(clk, Pin.IN, Pin.PULL_DOWN)
        self.sw_pin = Pin(sw, Pin.IN, Pin.PULL_DOWN)
        self.last_status = (self.dt_pin.value() << 1) | self.clk_pin.value()
        self.dt_pin.irq(handler=self.rotary_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self.clk_pin.irq(handler=self.rotary_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self.sw_pin.irq(handler=self.switch_detect, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)
        self.handlers = []
        self.last_button_status = self.sw_pin.value()

    def rotary_change(self, pin):
        new_status = (self.dt_pin.value() << 1) | self.clk_pin.value()
        if new_status == self.last_status:
            return
        transition = (self.last_status << 2) | new_status
        if transition == 0b1110:
            micropython.schedule(self.call_handlers, Rotary.ROT_CW)
        elif transition == 0b1101:
            micropython.schedule(self.call_handlers, Rotary.ROT_CCW)
        self.last_status = new_status

    def switch_detect(self, pin):
        if self.last_button_status == self.sw_pin.value():
            return
        self.last_button_status = self.sw_pin.value()
        if self.sw_pin.value():
            micropython.schedule(self.call_handlers, Rotary.SW_RELEASE)
        else:
            micropython.schedule(self.call_handlers, Rotary.SW_PRESS)

    def add_handler(self, handler):
        self.handlers.append(handler)

    def call_handlers(self, type):
        for handler in self.handlers:
            handler(type)


rotary = Rotary(11, 10, 12)
val = 0
pwm.freq(1000)

width = 128
height = 64

line = 1
highlight = 1
shift = 0
list_length = 0
total_lines = 3

i2c_1 = machine.I2C(1, scl=machine.Pin("GP15"), sda=machine.Pin("GP14"))
oled = SSD1306_I2C(128, 64, i2c_1)

button_pin = Pin(12, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(11, Pin.IN, Pin.PULL_UP)
step_pin = Pin(10, Pin.IN, Pin.PULL_UP)

previous_value = True
button_down = False


def leds(number, pwm):
    oled.fill(0)
    oled.text(f"Rotate", 37, 22)
    oled.text(f"Clockwise", 25, 38)
    oled.show()
    pwm = PWM(Pin(int(pwm)))

    def brightness(duty):
        value = duty * 100
        pwm.duty_u16(value)
        print(value)

    def oledtest(luku):
        oled.fill(0)
        oled.text(f"LED {number}", 48, 10)
        oled.hline(15, 30, luku, 1)
        oled.text(f"{luku}%", 50, 40)
        oled.show()
        brightness(luku)

    def rotary_changed(change):
        global val
        duty = 1
        if change == Rotary.ROT_CW and val < 10:
            val = val + 1
            print(val)
            valed = val * 10
            duty = duty * 100
            oledtest(valed)
        elif change == Rotary.ROT_CCW and val > 0:
            val = val - 1
            valed = val * 10
            print(val)
            oledtest(valed)
        elif change == Rotary.SW_PRESS:
            return
        elif change == Rotary.SW_RELEASE:
            return

    rotary.add_handler(rotary_changed)

    while True:
        time.sleep(0.1)


def show_menu(menu):
    global line, highlight, shift, list_length

    item = 1
    line = 1
    line_height = 10

    oled.fill_rect(0, 0, width, height, 0)

    list_length = len(menu)
    short_list = menu[shift:shift + total_lines]

    for item in short_list:
        if highlight == line:
            oled.fill_rect(0, (line - 1) * line_height, width, line_height, 1)
            oled.text(">", 0, (line - 1) * line_height, 0)
            oled.text(item, 10, (line - 1) * line_height, 0)
            oled.show()
        else:
            oled.text(item, 10, (line - 1) * line_height, 1)
            oled.show()
        line += 1
    oled.show()


file_list = ["Led 1", "Led 2", "Led 3"]
show_menu(file_list)

while True:
    if previous_value != step_pin.value():
        if step_pin.value() == False:

            if direction_pin.value() == False:
                if highlight > 1:
                    highlight -= 1
                else:
                    if shift > 0:
                        shift -= 1
            else:
                if highlight < total_lines:
                    highlight += 1
                else:
                    if shift + total_lines < list_length:
                        shift += 1

            show_menu(file_list)
        previous_value = step_pin.value()

    time.sleep(.1)
    if highlight == 1 and button_pin.value() == False and not button_down:
        button_down = True
        oled.fill(0)
        oled.show()
        leds(1, 20)
    elif highlight == 2 and button_pin.value() == False and not button_down:
        button_down = True
        oled.fill(0)
        oled.show()
        leds(2, 21)
    elif highlight == 3 and button_pin.value() == False and not button_down:
        button_down = True
        oled.fill(0)
        oled.show()
        leds(3, 22)

    if button1.value() == 0:
        button_down = False
        print("Hello")
        show_menu(file_list)

    if button_pin.value() == False and not button_down:
        button_down = True


def back():
    if button_pin.value() == True and button_down:
        button_down = False
