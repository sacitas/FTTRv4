import os
import csv
import glob
from time import sleep
import datetime as dt


#---Setup DS18B20 sensors---
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#---Directory for temp-sensors---
base_dir = '/sys/bus/w1/devices/'

#--Temperature data file location--
temp_folder = "temp/"
temp_filename = ""
temp_filepath = ""


fieldnames = ["x", "dtemp0", "dtemp1", "dtemp2", "dtemp3", "dtemp4"]

#---Function for temp filelocation---
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
    
    
#---Reads raw temperature data---
def read_temp_raw(n):
    device_folder = glob.glob(base_dir + '28*')[n]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#---Converts temp to Celsius---
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

#---Reads temperature functions---
def read_temp():
    temps = []

    for i in range (0, 5):
        temp = convert_temp(i)
        temps.append(temp)

    return temps

def read_temp0():
    temps0 = read_temp()

    return temps0[0]

#---Creating temperature files for plotting---
def create_tmpFile_live():
    with open('temp_read.csv', 'w') as live_csv:
        csv_writer = csv.DictWriter(live_csv, fieldnames=fieldnames)
        csv_writer.writeheader()

def create_tmpFile():
    with open(f'{temp_filepath}.csv', 'w') as data_csv:
        csv_writer = csv.DictWriter(data_csv, fieldnames=fieldnames)
        csv_writer.writeheader()
     
#---Writes to temperature files---
def write_tmp():
    x = dt.datetime.now().strftime('%H:%M:%S')
  
    temps = read_temp()

    with open(f'{temp_filepath}.csv', 'a') as data_csv:
        csv_writer = csv.DictWriter(data_csv, fieldnames=fieldnames)
        
        info = {
            "x": x,
            "dtemp0": temps[0],
            "dtemp1": temps[1],
            "dtemp2": temps[2],
            "dtemp3": temps[3],
            "dtemp4": temps[4]
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
            "dtemp4": temps[4]
        }
        csv_writer.writerow(info)
        data_csv.close()
        
        x = dt.datetime.now().strftime('%H:%M:%S')
   

    sleep(0.1)
