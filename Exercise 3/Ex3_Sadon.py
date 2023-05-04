from piotimer import Piotimer
from machine import ADC, Pin
from fifo import Fifo
import time
from ssd1306 import SSD1306_I2C

oled_dcl = machine.I2C(1, scl=machine.Pin("GP15"), sda=machine.Pin("GP14"))
oled = SSD1306_I2C(128, 64, oled_dcl)
oled.fill(0)
oled.text("EXPLORE UR HEART",0,25)
oled.text("press sensor",20,45)
oled.show()
time.sleep(1)

class HeartRateMonitor:

    def __init__(self):
        self.analog_in = ADC(26)
        self.data_fifo = Fifo(900)
        self.sensor_timer = Piotimer(mode=Piotimer.PERIODIC, freq=250, callback=self.read_sensor)
        self.window_size = 10
        self.min_limit = 36000  # minimum value for the average sensor reading to be considered a peak
        self.max_limit = 37000  # maximum value for the average sensor reading to be considered a peak
        self.sensor_values = []
        self.heart_rate = 0
        self.peak_times = []

    def read_sensor(self, timer_id):
        self.data_fifo.put(self.analog_in.read_u16())

    def monitor(self):
        moving_average = 0
        while True:
            if not self.data_fifo.empty():
                sensor_value = self.data_fifo.get()
                self.sensor_values.append(sensor_value)

                if len(self.sensor_values) >= self.window_size:
                    window = self.sensor_values[-self.window_size:]  # getting the latest window of sensor readings

                    window_average = round(sum(window) / self.window_size)

                    moving_average = (moving_average * (self.window_size - 1) + sensor_value) / self.window_size  # update the moving average

                    if self.min_limit <= window_average <= self.max_limit:
                        self.peak_times.append(time.ticks_ms())

                        if len(self.peak_times) == 2:
                            time_diff_ms = self.peak_times[1] - self.peak_times[0]  # the time difference between the two time stamps

                            if time_diff_ms > 500:
                                heart_rate = round(60000 / time_diff_ms)  # heart rate in beats per minute

                                if heart_rate > 130 or heart_rate < 40:  # check if heart rate is too high or too low
                                    self.peak_times.pop(0)
                                    self.peak_times = []
                                    continue

                                oled.fill(0)
                                oled.text("Heart rate", 25, 20)
                                oled.text(str(heart_rate) + " BPM", 40, 40)
                                oled.show()
                                print("Heart rate:", heart_rate)

                            self.peak_times.pop(0)
                            self.peak_times = []

                    self.sensor_values = self.sensor_values[-self.window_size:]

heart_rate_monitor = HeartRateMonitor()
heart_rate_monitor.monitor()