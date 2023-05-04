import network
from time import sleep
import machine
from machine import Pin
import ssd1306

ssid = 'KME661Group5'
password = '735Q4FhHM6daMWz'

def connect():
    oled_dcl = machine.I2C(1, scl=machine.Pin("GP15"), sda=machine.Pin("GP14"))
    oled = ssd1306.SSD1306_I2C(128, 64, oled_dcl)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    oled.fill(0)
    oled.text("IP Address:", 0, 0)
    oled.text(ip, 0, 10)
    oled.show()
    return ip


try:
    ip = connect()
except KeyboardInterrupt:
    machine.reset()
