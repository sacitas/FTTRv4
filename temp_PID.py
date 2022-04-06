import os
import glob
from time import sleep
import csv
import datetime as dt


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'

x = dt.datetime.now().strftime('%H:%M:%S')

fieldnames = ["x", "temp0", "temp1", "temp2"]
 
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

    for i in range (0, 1):
        temp = convert_temp(i)
        temps.append(temp)
#       print("Temp_sensor{} = {}*C.".format(i, temp))

    return temps[0]

