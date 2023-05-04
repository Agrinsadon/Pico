import urequests as requests
import network
from time import sleep
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

def connect(ssid, pw):
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, pw)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected, IP address: {ip}')

ssid = 'KME661Group5'
password = '735Q4FhHM6daMWz'
url = 'http://194.110.231.243:8000'
oled_dcl = machine.I2C(1, scl=machine.Pin("GP15"), sda=machine.Pin("GP14"))
oled = SSD1306_I2C(128, 64, oled_dcl)

connect(ssid, password)

APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a"
CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"
LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login"
TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token"
REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login"

response = requests.post(
    url = TOKEN_URL,
    data = 'grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
    headers = {'Content-Type':'application/x-www-form-urlencoded'},
    auth = (CLIENT_ID, CLIENT_SECRET))

response = response.json()

access_token = response["access_token"]

intervals = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800]

data_set = {'type': 'RRI',
           'data': intervals,
           'analysis': {
            'type': 'readiness'
           }
        }

response = requests.post(
    url = "https://analysis.kubioscloud.com/v2/analytics/analyze",
    headers = { "Authorization": "Bearer {}".format(access_token),
    "X-Api-Key": APIKEY },
    json = data_set)

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
