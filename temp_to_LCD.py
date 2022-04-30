from RPLCD import i2c
import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

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


lcd.write_string("Welcome!")
lcd.cursor_pos = (0, 0)
time.sleep(1000)

while True:
  
    lcd.write_string("Modes: ")
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Auto/Manual")
    lcd.cursor_pos = (1, 0)
    
    time.sleep(0.5)


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
