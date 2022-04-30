import os
import glob
from time import sleep
import csv
import datetime as dt
import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1115 import Mode

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.mode = Mode.CONTINUOUS


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'

temp_folder = "temp/"
temp_filename = ""
temp_filepath = ""


fieldnames = ["x", "dtemp0", "dtemp1", "dtemp2", "dtemp3", "dtemp4", "atemp0", "atemp1"]


def init_time():
    global ref_time
    global temp_filename
    global temp_folder
    global temp_filepath


    now = dt.datetime.now()
    t = now.strftime("%H:%M:%S")
    (h, m, s) = t.split(':')
    ref_time = int(h) * 3600 + int(m) * 60 + int(s)

    temp_filename = now.strftime("%m_%d_%Y-%H:%M")
    temp_filepath = temp_folder + temp_filename
    
    

def read_temp_raw(n):
    device_folder = glob.glob(base_dir + '28*')[n]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def convert_temp(n):
    lines = read_temp_raw(n)

    while lines[0].strip()[-3:] != 'YES':
        lines = read_temp_raw(n)

    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0

        if temp_c > 2048:
            temp_c = temp_c - 4096

        return temp_c


def read_temp():
    temps = []

    for i in range (0, 5):
        temp = convert_temp(i)
        temps.append(temp)

    return temps

def read_temp0():
    temps0 = []

    for i in range (0, 1):
        temp0 = convert_temp(i)
        temps0.append(temp0)

    return temps0[0]


def create_tmpFile_live():
    with open('temp_read.csv', 'w') as live_csv:
        csv_writer = csv.DictWriter(live_csv, fieldnames=fieldnames)
        csv_writer.writeheader()

def create_tmpFile():
    with open(f'{temp_filepath}.csv', 'w') as data_csv:
        csv_writer = csv.DictWriter(data_csv, fieldnames=fieldnames)
        csv_writer.writeheader()

def write_tmp():
    x = dt.datetime.now().strftime('%H:%M:%S')

    chan0 = AnalogIn(ads, ADS.P0)
    chan1 = AnalogIn(ads, ADS.P1)
    S1 = chan0.value
    V1 = chan0.voltage
    atemp0 = V1 / (11/1000)
    atemp0 = float(round(atemp0, 1))
    S2 = chan1.value
    V2 = chan1.voltage
    atemp1 = V2 / (11/1000)
    atemp1 = float(round(atemp1, 1))
  
    temps = read_temp()

    with open(f'{temp_filepath}.csv', 'a') as data_csv:
        csv_writer = csv.DictWriter(data_csv, fieldnames=fieldnames)
        
        info = {
            "x": x,
            "dtemp0": temps[0],
            "dtemp1": temps[1],
            "dtemp2": temps[2],
            "dtemp3": temps[3],
            "dtemp4": temps[4],
            "atemp0": atemp0,
            "atemp1": atemp1
        }
        csv_writer.writerow(info)
        data_csv.close()
        
        x = dt.datetime.now().strftime('%H:%M:%S')
        
    with open('temp_read.csv', 'a') as live_csv:
        csv_writer = csv.DictWriter(live_csv, fieldnames=fieldnames)
        
        info = {
            "x": x,
            "dtemp0": temps[0],
            "dtemp1": temps[1],
            "dtemp2": temps[2],
            "dtemp3": temps[3],
            "dtemp4": temps[4],
            "atemp0": atemp0,
            "atemp1": atemp1
        }
        csv_writer.writerow(info)
        data_csv.close()
        
        x = dt.datetime.now().strftime('%H:%M:%S')
   

    sleep(0.1)
