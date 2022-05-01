from RPLCD import i2c
import time
import Adafruit_ADS1x15
import pandas as pd

adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1



# constants to initialise the LCD
lcdmode = 'i2c'
cols = 20
rows = 4
charmap = 'A02'
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
#   data = pd.read_csv('temp_read.csv')
#   dtemp0 = data["dtemp0"]
#   dtemp0 = str(dtemp0)
    lcd.clear()
    lcd.write_string("SP: " + SP)
#   lcd.write_string("Temp: " + dtemp0)
#   lcd.cursor_pos(1, 0)
    time.sleep(0.5)

def man_mode():
#   data = pd.read_csv('temp_read.csv')
#   dtemp0 = data["dtemp0"]
#   dtemp0 = str(dtemp0)
    with open ('pid.conf', 'r+') as g:
        conf = g.readline().split(',')
        man = conf[5]
        man = str(man)
    lcd.clear()
#   lcd.write_string("Temp: " + dtemp0)
#   lcd.cursor_pos(0, 0)
    lcd.write_string("ManVal: " + man)
#   lcd.cursor_pos(1, 0)

    time.sleep(0.5)



try:
    lcd.clear()
    lcd.write_string("Welcome!")
    time.sleep(3)
    while True:

        with open ('pid.conf', 'r+') as g:
            conf = g.readline().split(',')
            auto = conf[4]
        if (auto == 0):
            auto_mode()
        else:
            man_mode()
            
except KeyboardInterrupt:
    lcd.close(clear = True)




#while True:
#    S1 = adc.read_adc(0, gain = GAIN)
#    V1 = S1*(5.0/65535)
#    temp1 = V1 / (8/1000)
#    temp1 = str(round(temp1, 1))
#    S2 = adc.read_adc(1, gain = GAIN)
#    V2 = S2*(5.0/65535)
#    temp2 = V2 / (8/1000)
#    temp2 = str(round(temp2, 1))
#    lcd.cursor_pos = (0, 0)
#    lcd.write_string("S1 Temp: " + temp1)
#    lcd.cursor_pos = (1, 0)
#    lcd.write_string("S2 Temp: " + temp2)

#    time.sleep(0.5)
