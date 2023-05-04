from piotimer import Piotimer  # module for hardware timer
from machine import ADC, Pin  # module for analog input and pin
from fifo import Fifo  # module for data storage
import time  # module for time management
from ssd1306 import SSD1306_I2C

oled_dcl = machine.I2C(1, scl=machine.Pin("GP15"), sda=machine.Pin("GP14"))
oled = SSD1306_I2C(128, 64, oled_dcl)
oled.fill(0)
oled.text("EXPLORE UR HEART",0,25)
oled.text("press sensor",20,45)
oled.show()
time.sleep(1)

# define the HeartRateMonitor class
class HeartRateMonitor:

    # initialize the class with required parameters
    def __init__(self):
        self.analog_in = ADC(26)  # initialize an analog input on pin 26
        self.data_fifo = Fifo(900)  # initialize a FIFO buffer with a capacity of 900
        self.sensor_timer = Piotimer(mode=Piotimer.PERIODIC, freq=250, callback=self.read_sensor)  # initialize a hardware timer with a frequency of 250 Hz, in periodic mode, and assign the read_sensor() method as its callback function
        self.window_size = 10  # set the window size to 10
        self.min_limit = 36000  # set the minimum value for the average sensor reading to be considered a peak
        self.max_limit = 37000  # set the maximum value for the average sensor reading to be considered a peak
        self.sensor_values = []  # create an empty list to store the sensor readings
        self.heart_rate = 0  # initialize the heart rate to 0
        self.peak_times = []  # create an empty list to store the time stamps of the detected peaks

    # define the read_sensor method that will be called by the hardware timer
    def read_sensor(self, timer_id):
        self.data_fifo.put(self.analog_in.read_u16())  # read the sensor value and put it in the FIFO buffer

    # define the monitor method that will continuously monitor the sensor readings
    # define the monitor method that will continuously monitor the sensor readings
    def monitor(self):
        moving_average = 0  # initialize the moving average to 0
        while True:  # loop indefinitely
            if not self.data_fifo.empty():  # check if the FIFO buffer is not empty
                sensor_value = self.data_fifo.get()  # get the latest sensor reading from the FIFO buffer
                self.sensor_values.append(sensor_value)  # add the latest sensor reading to the sensor_values list

                if len(self.sensor_values) >= self.window_size:  # check if there are enough readings in the sensor_values list to calculate the average
                    window = self.sensor_values[-self.window_size:]  # get the latest window of sensor readings

                    window_average = round(sum(window) / self.window_size)  # calculate the average of the latest window of sensor readings

                    moving_average = (moving_average * (self.window_size - 1) + sensor_value) / self.window_size  # update the moving average

                    if self.min_limit <= window_average <= self.max_limit:  # check if the average sensor reading is within the peak range
                        self.peak_times.append(time.ticks_ms())

                        if len(self.peak_times) == 2:  # check if there are two time stamps in the peak_times list
                            time_diff_ms = self.peak_times[1] - self.peak_times[0]  # calculate the time difference between the two time stamps

                            if time_diff_ms > 500:
                                heart_rate = round(60000 / time_diff_ms)  # the heart rate in beats per minute

                                if heart_rate > 130 or heart_rate < 40:  # check if heart rate is too high or too low
                                    self.peak_times.pop(0)
                                    self.peak_times = []
                                    continue

                                oled.fill(0)
                                oled.text("Heart rate", 25, 20)
                                oled.text(str(heart_rate) + " BPM", 40, 40)
                                oled.show()
                                print("Heart rate:", heart_rate)

                            self.peak_times.pop(0)  # remove the first time stamp from the peak_times list
                            self.peak_times = []  # empty the peak_times list

                    self.sensor_values = self.sensor_values[-self.window_size:]  # only keep the latest window_size number of sensor readings in the sensor_values list

heart_rate_monitor = HeartRateMonitor()
heart_rate_monitor.monitor()

