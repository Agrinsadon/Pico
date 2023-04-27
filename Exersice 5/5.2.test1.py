import ssd1306
from machine import Pin
import machine
import math

oled_dcl = machine.I2C(1, scl=machine.Pin("GP15"), sda=machine.Pin("GP14"))
oled = ssd1306.SSD1306_I2C(128, 64, oled_dcl)

ppi = [1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100]

# Mean PPI
mean_ppi = sum(ppi) / len(ppi)

# Mean HR
mean_hr = 60000 / mean_ppi

# Standard deviation of PPI (SDNN)
sdnn = math.sqrt(sum([(x - mean_ppi) ** 2 for x in ppi]) / (len(ppi) - 1.5))

# Root mean square of successive differences (RMSSD)
squared_diffs = [(ppi[i+1] - ppi[i]) ** 2 for i in range(len(ppi)-1)]
rmssd = math.sqrt(sum(squared_diffs) / (len(ppi) - 1))

# Display results Shell
print("Mean PPI: {:.0f} ms".format(mean_ppi))
print("Mean HR: {:.0f} bpm".format(mean_hr))
print("SDNN: {:.0f} ms".format(sdnn))
print("RMSSD: {:.0f} ms".format(rmssd))

# Display results Oled
oled.fill(0)
oled.text("Mean PPI:{:.0f} ms".format(mean_ppi), 0, 0)
oled.text("Mean HR:{:.0f} bpm".format(mean_hr), 0, 15)
oled.text("SDNN:{:.0f} ms".format(sdnn), 0, 30)
oled.text("RMSSD:{:.0f} ms".format(rmssd), 0, 45)
oled.show()
