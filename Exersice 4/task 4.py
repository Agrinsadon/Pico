from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from os import listdir
from time import sleep
import ssd1306

# Set the width and height of the OLED display
width = 128
height = 64

# Set initial values for menu display
line = 1
highlight = 1
shift = 0
list_length = 0
total_lines = 2

# Initialize I2C connection to OLED display
i2c_1 = machine.I2C(1, scl=machine.Pin("GP15"), sda=machine.Pin("GP14"))
oled = ssd1306.SSD1306_I2C(128, 64, i2c_1)

# Define pins for rotary encoder
button_pin = Pin(12, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(11, Pin.IN, Pin.PULL_UP)
step_pin = Pin(10, Pin.IN, Pin.PULL_UP)

# Initialize variables to track rotary encoder state
previous_value = True
button_down = False
button_press_time = 0


def show_menu(menu):
    # Bring in global variables
    global line, highlight, shift, list_length

    # Initialize variables for displaying menu
    item = 1
    line = 1
    line_height = 10

    # Clear the OLED display
    oled.fill_rect(0, 0, width, height, 0)

    # Shift the list of files so that it shows on the display
    list_length = len(menu)
    short_list = menu[shift:shift + total_lines]

    # Iterate through the list of files and display each one
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


def selection():
    button = Pin(9, Pin.IN, Pin.PULL_UP)
    button1 = Pin(8, Pin.IN, Pin.PULL_UP)
    button2 = Pin(7, Pin.IN, Pin.PULL_UP)

    led = Pin(20, Pin.OUT)
    led1 = Pin(21, Pin.OUT)
    led2 = Pin(22, Pin.OUT)

    State = 0
    State1 = 0
    State2 = 0

    emergency = Pin("GP12", mode=Pin.IN, pull=Pin.PULL_UP)
    i2c_1 = I2C(1, scl=Pin("GP15"), sda=Pin("GP14"))
    oled = ssd1306.SSD1306_I2C(128, 64, i2c_1)

    def screen():
        oled.fill(0)
        oled.text("LED:" + ("ON" if led.value() else "OFF"), 0, 10)
        oled.text("LED:" + ("ON" if led1.value() else "OFF"), 0, 20)
        oled.text("LED:" + ("ON" if led2.value() else "OFF"), 0, 30)
        oled.show()

    def emergency_handler(pin):
        led.off()
        led1.off()
        led2.off()
        screen()

    emergency.irq(handler=emergency_handler, trigger=Pin.IRQ_FALLING)

    while True:
        if button.value() == 0:
            if State == 0:
                led.value(1)
                # sleep_ms = 100
                screen()
                while button.value() == 0:
                    State = 1
            else:
                led.value(0)
                # sleep_ms = 100
                screen()
                while button.value() == 0:
                    State = 0

        elif button1.value() == 0:
            if State1 == 0:
                led1.value(1)
                # sleep_ms = 100
                screen()
                while button1.value() == 0:
                    State1 = 1
            else:
                led1.value(0)
                # sleep_ms = 100
                screen()
                while button1.value() == 0:
                    State1 = 0
        elif button2.value() == 0:
            if State2 == 0:
                led2.value(1)
                # sleep_ms = 100
                screen()
                while button2.value() == 0:
                    State2 = 1
            else:
                led2.value(0)
                # sleep_ms = 100
                screen()
                while button2.value() == 0:
                    State2 = 0


# List of files to display in the menu
file_list = ["Selection", "Brightness"]

# Main loop to check rotary encoder and button state
while True:
    if previous_value != step_pin.value():
        if step_pin.value() == False:

            # If the rotary encoder is turned left
            if direction_pin.value() == False:
                if highlight > 1:
                    highlight -= 1
                else:
                    if shift > 0:
                        shift -= 1

                        # If the rotary encoder is turned right
            else:
                if highlight < total_lines:
                    highlight += 1
                else:
                    if shift + total_lines < list_length:
                        shift += 1

            # Update the menu display
            show_menu(file_list)
        previous_value = step_pin.value()

        # If the button is pressed
    if button_pin.value() == False and not button_down:
        button_down = True
        print("Moi")
        oled.fill(0)
        selection()
        oled.show()

    # Debounce the button
    if button_pin.value() == True and button_down:
        button_down = False
        print("Hei")