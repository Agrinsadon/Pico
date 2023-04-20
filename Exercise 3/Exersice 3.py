from piotimer import Piotimer
from fifo import Fifo
from machine import ADC
import utime

adc = ADC(26)
samples = Fifo(50)
average_window = 10
average_fifo = Fifo(average_window)

def read_sample(tid):
    samples.put(adc.read_u16())

timer = Piotimer(mode = Piotimer.PERIODIC, freq = 250, callback = read_sample)
utime.sleep(1)

while True:
    if not samples.empty():
        value = samples.get()
        average_fifo.put(value)
        average = int(sum(average_fifo.data)/average_window)
        average_fifo.get()
        print(average)