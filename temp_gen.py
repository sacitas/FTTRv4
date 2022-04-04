import csv
import time
import datetime as dt
import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1115 import Mode

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)

ads.mode = Mode.CONTINUOUS

x = dt.datetime.now().strftime('%H:%M:%S')
temp1 = 21
temp2 = 21

fieldnames = ["x", "temp1", "temp2"]

with open('temp_data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
    
    with open('temp_data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "x": x,
            "temp1": temp1,
            "temp2": temp2
        }

        csv_writer.writerow(info)
        print(x, temp1, temp2)


        x = dt.datetime.now().strftime('%H:%M:%S')
        
        chan0 = AnalogIn(ads, ADS.P0)
        chan1 = AnalogIn(ads, ADS.P1)
        S1 = chan0.value
        V1 = chan0.voltage
        temp1 = V1 / (11/1000)
        temp1 = float(round(temp1, 1))
        S2 = chan1.value
        V2 = chan1.voltage
        temp2 = V2 / (11/1000)
        temp2 = float(round(temp2, 1))
        
    time.sleep(1)
