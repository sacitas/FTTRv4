# Import LCD library
from RPLCD import i2c

# Import sleep library
import time

import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1115 import Mode

I2C = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(I2C)
#ads.mode = Mode.CONTINUOUS

# constants to initialise the LCD
lcdmode = 'i2c'
cols = 16
rows = 4
charmap = 'A02'
i2c_expander = 'PCF8574'

# Generally 27 is the address;Find yours using: i2cdetect -y 1 
address = 0x27 
port = 1 # 0 on an older Raspberry Pi



# Initialise the LCD
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap,
                  cols=cols, rows=rows)

try:
    lcd.clear()
    lcd.write_string("Welcome!")
    time.sleep(2)
    while True:
        chan0 = AnalogIn(ads, ADS.P2)
        V1 = chan0.voltage
        man = (V1*100)/3.3
        man = str(round(man, 0))
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("ManVal: " + man + "%")
    
        time.sleep(0.5)
except KeyboardInterrupt:
    lcd.clear()
    lcd.write_string("Goodbye!")
    time.sleep(2)
    lcd.close(clear = True)
