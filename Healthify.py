from ssd1306 import SSD1306_I2C
from os import listdir
from time import sleep
import ssd1306
import time
import urequests as requests
import network
from machine import ADC, Pin, I2C
from fifo import Fifo  # module for data storage
from piotimer import Piotimer  # module for hardware timer

button1 = Pin(8, Pin.IN, Pin.PULL_UP)

# Set the width and height of the OLED display
width = 128
height = 64

# Set initial values for menu display
line = 0
highlight = 1
shift = 0
list_length = 1
total_lines = 2

# Initialize I2C connection to OLED display
oled_dcl = machine.I2C(1, scl=machine.Pin("GP15"), sda=machine.Pin("GP14"))
oled = SSD1306_I2C(128, 64, oled_dcl)

# Define pins for rotary encoder
button_pin = Pin(12, Pin.IN, Pin.PULL_UP)
direction_pin = Pin(11, Pin.IN, Pin.PULL_UP)
step_pin = Pin(10, Pin.IN, Pin.PULL_UP)

emergency = Pin("GP12", mode=Pin.IN, pull=Pin.PULL_UP)

previous_value = True
button_down = False

ssid = "KME661Group5"
password = '735Q4FhHM6daMWz'
url = 'http://194.110.231.243:8000'


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')


APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a"
CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"
LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login"
TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token"
REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login"

connect()
intervals = []


def show_menu(menu):
    # global değişkenleri getiriyoruz.
    global line, highlight, shift, list_length

    # menü değişkenleri
    item = 1
    line = 1
    line_height = 10

    # ekranı temizle
    oled.fill_rect(0, 0, width, height, 0)

    # Shift the list of files so that it shows on the display
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


def test():
    if len(intervals) < 21:
        oled.fill(0)
        oled.text(f'No Data', 34, 30)
        oled.show()
    else:
        oled.fill(0)
        oled.text(f'Getting data..', 12, 30)
        oled.show()
        data_set = {'type': 'RRI',
                    'data': intervals,
                    'analysis': {
                        'type': 'readiness'
                    }
                    }

        response = requests.post(
            url=TOKEN_URL,
            data='grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            auth=(CLIENT_ID, CLIENT_SECRET))

        response = response.json()

        access_token = response["access_token"]

        response = requests.post(
            url="https://analysis.kubioscloud.com/v2/analytics/analyze",
            headers={"Authorization": "Bearer {}".format(access_token),
                     "X-Api-Key": APIKEY},
            json=data_set)

        response = response.json()

        if response['status'] == 'ok':
            oled.fill(0)
            sns = response['analysis']['sns_index']
            oled.text(f'SNS_Index:', 23, 5)
            oled.text(f'{sns}', 23, 15)
            pns = response['analysis']['pns_index']
            oled.text(f'PNS_Index:', 23, 35)
            oled.text(f'{pns}', 23, 45)
            oled.show()


def heart():
    # define the HeartRateMonitor class
    class HeartRateMonitor:

        # initialize the class with required parameters
        def __init__(self):
            self.analog_in = ADC(26)  # initialize an analog input on pin 26
            self.data_fifo = Fifo(750)  # initialize a FIFO buffer with a capacity of 900
            self.sensor_timer = Piotimer(mode=Piotimer.PERIODIC, freq=250,
                                         callback=self.read_sensor)  # initialize a hardware timer with a frequency of 250 Hz, in periodic mode, and assign the read_sensor() method as its callback function
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
        def monitor(self):
            testi = True

            oled.fill(0)
            oled.text(f'Measuring...', 15, 30)
            oled.show()

            moving_average = 0

            while testi:
                if button1.value() == 0:
                    break
                if not self.data_fifo.empty():  # check if the FIFO buffer is not empty
                    sensor_value = self.data_fifo.get()  # get the latest sensor reading from the FIFO buffer
                    self.sensor_values.append(sensor_value)  # add the latest sensor reading to the sensor_values list

                    if len(self.sensor_values) >= self.window_size:  # check if there are enough readings in the sensor_values list to calculate the average
                        window = self.sensor_values[-self.window_size:]  # get the latest window of sensor readings

                        window_average = round(
                            sum(window) / self.window_size)  # calculate the average of the latest window of sensor readings

                        moving_average = (moving_average * (
                                    self.window_size - 1) + sensor_value) / self.window_size  # update the moving average

                        if self.min_limit <= window_average <= self.max_limit:  # check if the average sensor reading is within the peak range
                            self.peak_times.append(time.ticks_ms())  # add the current time stamp to the peak_times list

                            if len(self.peak_times) == 2:  # check if there are two time stamps in the peak_times list
                                time_diff_ms = self.peak_times[1] - self.peak_times[
                                    0]  # calculate the time difference between the two time stamps

                                if time_diff_ms > 500:  # check if the time difference is greater than 500 ms
                                    heart_rate = round(
                                        60000 / time_diff_ms)  # calculate the heart rate in beats per minute

                                    if heart_rate > 130 or heart_rate < 40:  # check if heart rate is too high or too low
                                        self.peak_times.pop(0)
                                        self.peak_times = []
                                        continue

                                    oled.fill(0)
                                    oled.text("Heart rate", 25, 10)
                                    oled.text(str(heart_rate) + " BPM", 40, 30)
                                    oled.show()
                                    print("Heart rate:", heart_rate)
                                    intervals.append(int(60000 / heart_rate))

                                self.peak_times.pop(0)  # remove the first time stamp from the peak_times list
                                self.peak_times = []  # empty the peak_times list

                        self.sensor_values = self.sensor_values[
                                             -self.window_size:]  # only keep the latest window_size number of sensor readings in the sensor_values list

    heart_rate_monitor = HeartRateMonitor()
    heart_rate_monitor.monitor()


# Menüde gösterilecek seçenekler.
file_list = ["Heart Rate", "Kubios Cloud"]
show_menu(file_list)

while True:
    if previous_value != step_pin.value():
        if step_pin.value() == False:

            # Rotary sola dönerse
            if direction_pin.value() == False:
                if highlight > 1:
                    highlight -= 1
                else:
                    if shift > 0:
                        shift -= 1

                        # Sağa dönerse
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
        heart()
    elif highlight == 2 and button_pin.value() == False and not button_down:
        button_down = True
        test()

    # Tuşu debounce etmek için
    if button1.value() == 0:
        button_down = False
        show_menu(file_list)
