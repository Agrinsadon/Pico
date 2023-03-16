#Task 1: 1-2
from machine import Pin

#1.1
import time

while True:
    time.sleep(1)
    D1 = machine.Pin(22, machine.Pin.OUT)
    D1.value(1)
    time.sleep(1)
    D2 = machine.Pin(21, machine.Pin.OUT)
    D1.value(0)
    D2.value(1)
    time.sleep(1)
    D3 = machine.Pin(20, machine.Pin.OUT)
    D1.value(0)
    D2.value(0)
    D3.value(1)
    time.sleep(1)
    D3.value(0)

#1.2