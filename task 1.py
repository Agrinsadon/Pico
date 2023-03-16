#Task 1: 1-2
#1.1
from machine import Pin
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
from machine import Pin
import time
from machine import Pin
import time

while True:
    D1 = machine.Pin(22, machine.Pin.OUT)
    D2 = machine.Pin(21, machine.Pin.OUT)
    D3 = machine.Pin(20, machine.Pin.OUT)

    time.sleep(1)

    # 000
    D1.value(0)
    D2.value(0)
    D3.value(0)

    # 001
    time.sleep(1)
    D1.value(1)
    D2.value(0)
    D3.value(0)

    # 010
    time.sleep(1)
    D1.value(0)
    D2.value(1)
    D3.value(0)

    # 011
    time.sleep(1)
    D1.value(1)
    D2.value(1)
    D3.value(0)

    # 100
    time.sleep(1)
    D1.value(0)
    D2.value(0)
    D3.value(1)

    # 101
    time.sleep(1)
    D1.value(1)
    D2.value(0)
    D3.value(1)

    # 110
    time.sleep(1)
    D1.value(0)
    D2.value(1)
    D3.value(1)

    # 111
    time.sleep(1)
    D1.value(1)
    D2.value(1)
    D3.value(1)

