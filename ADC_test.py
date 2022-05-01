import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1


while True:
    S1 = adc.read_adc(0, gain = GAIN)
    V1 = S1*(5.0/65535)
    temp1 = V1 / (8/1000)
    temp1 = str(round(temp1, 1))
    S2 = adc.read_adc(1, gain = GAIN)
    V2 = S2*(5.0/65535)
    temp2 = V2 / (8/1000)
    temp2 = str(round(temp2, 1))

    print("Temp1: " + temp1)
    print("\nTemp2: " + temp2)