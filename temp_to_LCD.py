import RPi.GPIO as GPIO
from RPLCD import i2c
import time
import pandas as pd
import FTTRv4_temp as tmp

auto = 0

degree_sign = u'\N{DEGREE SIGN}'
 


GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)



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



def auto_mode():
    with open ('pid.conf', 'r+') as g:
        conf = g.readline().split(',')
        SP = str(conf[0])
    temp0 = tmp.read_temp0()
    temp0 = str(temp0)
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("SP: " + SP + " " + degree_sign + "C")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("PV: " + temp0 + " " + degree_sign + "C")
    time.sleep(0.5)

    
def man_mode():
    temp0 = tmp.read_temp0()
    temp0 = str(temp0)
    with open ('pid.conf', 'r+') as g:
        conf = g.readline().split(',')
        man = str(conf[5])
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("ManVal: " + man)
    lcd.cursor_pos = (1, 0)
    lcd.write_string("PV: " + temp0 + " " + degree_sign + "C")
    time.sleep(0.5)

    
try:
    lcd.clear()
    lcd.write_string("Welcome!")
    time.sleep(2)
    while True:
        with open ('pid.conf', 'r+') as g:
            conf = g.readline().split(',')
            auto = int(conf[4])
        button_state = GPIO.input(23)
        if(button_state == False and auto == 1): 
            button_state = True
            GPIO.output(17, True)
            GPIO.output(27, False)
            button_state = True
            auto_mode()
            
        else:
            button_state = False
            GPIO.output(27, True)
            GPIO.output(17, False)
            button_state = False
            man_mode()

            
except KeyboardInterrupt:
    lcd.clear()
#   loop_string(long_string, lcd, framebuffer, 1, 16)
    lcd.write_string("Goodbye")
    time.sleep(2)
    lcd.close(clear = True)
    GPIO.cleanup()
