from RPLCD import i2c
import time
import Adafruit_ADS1x15
import pandas as pd
import FTTRv4_temp as tmp

adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

auto = 0

degree_sign = u'\N{DEGREE SIGN}'

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


def auto_mode():
    with open ('pid.conf', 'r+') as g:
        conf = g.readline().split(',')
        SP = str(conf[0])
    temp0 = tmp.read_temp0()
    temp0 = str(round(temp0, 1))
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("SP: " + SP + degree_sign + "C")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("PV: " + temp0 + degree_sign + "C")
    time.sleep(0.5)

    
def man_mode():
    temp0 = tmp.read_temp0()
    temp0 = str(round(temp0, 1))
    with open ('pid.conf', 'r+') as g:
        conf = g.readline().split(',')
        man = conf[5]
        man = str(man)
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("ManVal: " + man)
    lcd.cursor_pos = (1, 0)
    lcd.write_string("PV: " + temp0 + degree_sign + "C")
    time.sleep(0.5)



try:
    lcd.clear()
    lcd.write_string("Welcome!")
    time.sleep(3)
    while True:

        with open ('pid.conf', 'r+') as g:
            conf = g.readline().split(',')
            auto = float(conf[4])
        if (auto == 1):
            auto_mode()
        else:
            man_mode()
            
except KeyboardInterrupt:
    lcd.close(clear = True)
