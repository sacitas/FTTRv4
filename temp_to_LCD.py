import RPi.GPIO as GPIO
from RPLCD import i2c
import time
import pandas as pd
import FTTRv4_temp as tmp

import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1115 import Mode


I2C = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(I2C)
ads.mode = Mode.CONTINUOUS

SP = 0
Kp = 0
Ti = 0
Td = 0
auto = 0
man = 0
ManVal = 0

degree_sign = u'\N{DEGREE SIGN}'
 

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(23, GPIO.RISING, bouncetime=150)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(24, GPIO.RISING, bouncetime=150)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

# constants to initialise the LCD
lcdmode = 'i2c'
cols = 20
rows = 4
charmap = 'A00'
i2c_expander = 'PCF8574'

# Generally 27 is the address;Find yours using: i2cdetect -y 1 
address = 0x27 
port = 1 # 0 on an older Raspberry Pi


# Initialise the LCD
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap,
                  cols=cols, rows=rows)

framebuffer = [
    'Orbit NTNU',
    '',
]

def write_to_lcd(lcd, framebuffer, num_cols):
    lcd.home()
    for row in framebuffer:
        lcd.write_string(row.ljust(num_cols)[:num_cols])
        lcd.write_string('\r\n')


def loop_string(string, lcd, framebuffer, row, num_cols, delay=0.1):
    padding = ' ' * num_cols
    s = padding + string + padding
    for i in range(len(s)- num_cols + 1):
        framebuffer[row] = s[i:i+num_cols]
        write_to_lcd(lcd, framebuffer, num_cols)
        time.sleep(delay)

long_string = 'Like and subscribe or I will delete your Minecraft account'


def readConfig():
    global SP, Kp, Ti, Td, auto, man
    with open ('pid.conf', 'r+') as g:
        conf = g.readline().split(',')
        SP = float(conf[0])
        Kp = float(conf[1])
        Ti = float(conf[2])
        Td = float(conf[3])
        auto = int(conf[4])
        man = float(conf[5])
        

def auto_mode():
    global SP, Kp, Ti, Td, auto, man
    isPressed1 = False
    isPressed2 = False
    while(isPressed1 == False):
        chan1 = AnalogIn(ads, ADS.P1)
        V1 = chan1.voltage
        sp = (V1*121)/3.3
        sp = str(round(sp, 0))
        lcd.clear()
        lcd.write_string("SP: " + sp + " " + degree_sign + "C")
        time.sleep(0.1)
        if(GPIO.event_detected(24)):
            isPressed1 = True
            GPIO.output(17, False)
            time.sleep(0.2)
            GPIO.output(17, True)
            time.sleep(0.2)
            GPIO.output(17, False)
            time.sleep(0.2)
            GPIO.output(17, True)
            time.sleep(0.2)
            GPIO.output(17, False)
            time.sleep(0.2)
            readConfig()
            with open ('pid.conf', 'w') as f:
                f.write('%s,%s,%s,%s,%s,%s'%(sp,Kp,Ti,Td,auto,man))
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("SP set")
            time.sleep(0.5)
            showAll_A()
        
        else:
            isPressed1 = False
    
        if(GPIO.event_detected(23)):
            isPressed2 = True
            GPIO.output(17, False)
            time.sleep(0.1)
            GPIO.output(17, True)
            time.sleep(0.1)
            GPIO.output(17, False)
            readConfig()
            auto = 0
            with open ('pid.conf', 'w') as f:
                f.write('%s,%s,%s,%s,%s,%s'%(SP,Kp,Ti,Td,auto,man))
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Manual mode set")
            time.sleep(0.5)
        else:
            isPressed2 = False 

def showAll_A():
    global SP, Kp, Ti, Td, auto, man
    readConfig()
    isPressed3 = False
    while (isPressed3 == False):
        readConfig()
        GPIO.output(17, True)
        GPIO.output(27, False)
        temp0 = tmp.read_temp0()
        temp0 = str(temp0)
        SP = str(SP)
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("SP: " + SP + " " + degree_sign + "C")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("PV: " + temp0 + " " + degree_sign + "C")
        time.sleep(0.5)
        
        if(GPIO.event_detected(23)):
            isPressed3 = True
            time.sleep(0.5)
            auto_mode()
        else:
            isPressed3 = False
      
def man_mode():
    global SP, Kp, Ti, Td, auto, man
    isPressed1 = False
    isPressed2 = False
    while(isPressed1 == False):
        chan1 = AnalogIn(ads, ADS.P1)
        V1 = chan1.voltage
        ManVal = (V1*100.5)/3.3
        ManVal = str(round(ManVal, 0))
        lcd.clear()
        lcd.write_string("ManVal: " + ManVal + "%")
        time.sleep(0.1)
        if(GPIO.event_detected(24)):
            isPressed1 = True
            GPIO.output(27, False)
            time.sleep(0.1)
            GPIO.output(27, True)
            time.sleep(0.1)
            GPIO.output(27, False)
            time.sleep(0.1)
            GPIO.output(27, True)
            time.sleep(0.1)
            GPIO.output(27, False)
            readConfig()
            with open ('pid.conf', 'w') as f:
                f.write('%s,%s,%s,%s,%s,%s'%(SP,Kp,Ti,Td,auto,ManVal))
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Manual value set")
            time.sleep(0.5)
            showAll_M()
        else:
            isPressed1 = False
    
        if(GPIO.event_detected(23)):
            isPressed2 = True
            GPIO.output(27, False)
            time.sleep(0.2)
            GPIO.output(27, True)
            time.sleep(0.2)
            GPIO.output(27, False)
            readConfig()
            auto = 1
            with open ('pid.conf', 'w') as f:
                f.write('%s,%s,%s,%s,%s,%s'%(SP,Kp,Ti,Td,auto,man))
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Auto mode set")
            time.sleep(0.5)
        else:
            isPressed2 = False

def showAll_M():
    global SP, Kp, Ti, Td, auto, man
    isPressed4 = False
    while isPressed4 == False:
        readConfig()
        GPIO.output(27, True)
        GPIO.output(17, False)
        temp0 = tmp.read_temp0()
        temp0 = str(temp0)
        man = str(man)
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("ManVal: " + man + "%")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("PV: " + temp0 + " " + degree_sign + "C")
        time.sleep(0.5)
        
        if(GPIO.event_detected(23)):
            isPressed4 = True
            time.sleep(0.5)
            man_mode()
        else:
            isPressed4 = False  
          
try:
    lcd.clear()
    lcd.write_string("Welcome!")
    time.sleep(2)
    lcd.clear()
    while True:
        readConfig()
        if(auto == 1): 
            GPIO.output(17, True)
            GPIO.output(27, False)
            showAll_A()
            
        elif(auto == 0):
            GPIO.output(27, True)
            GPIO.output(17, False)  
            showAll_M()

            
except KeyboardInterrupt:
    lcd.clear()
#   loop_string(long_string, lcd, framebuffer, 1, 16)
    lcd.write_string("Goodbye")
    time.sleep(2)
    lcd.close(clear = True)
    GPIO.cleanup()
