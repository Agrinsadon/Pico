from machine import Pin
import time
import ssd1306

reset = Pin("GP12", mode=Pin.IN, pull=Pin.PULL_UP)

Oled_dcl = machine.I2C(1, scl=machine.Pin("GP15"), sda=machine.Pin("GP14"))
Oled = ssd1306.SSD1306_I2C(128, 64, Oled_dcl)

B1 = Pin(9, mode=Pin.IN, pull=Pin.PULL_UP)
B2 = Pin(8, mode=Pin.IN, pull=Pin.PULL_UP)
B3 = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP)

D1 = machine.Pin(22, Pin.OUT)
D2 = machine.Pin(21, Pin.OUT)
D3 = machine.Pin(20, Pin.OUT)


def reset_button(buttons):
    D1.off()
    D2.off()
    D3.off()


reset.irq(handler=reset_button, trigger=Pin.IRQ_FALLING)


def Oled_screen():
    Oled.fill(0)
    Oled.text("LED_1: " + ("on" if D1.value() else "off"), 25, 15)
    Oled.text("LED_2: " + ("on" if D2.value() else "off"), 25, 30)
    Oled.text("LED_3: " + ("on" if D3.value() else "off"), 25, 45)
    Oled.show()


while True:
    Oled_screen()
    if B1.value() == 0:
        D1.toggle()
        while B1.value() == 0:
            pass

    if B2.value() == 0:
        D2.toggle()
        while B2.value() == 0:
            pass

    if B3.value() == 0:
        D3.toggle()
        while B3.value() == 0:
            pass
