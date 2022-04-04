from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt 
from matplotlib.animation import FuncAnimation
import tkinter as tk
import numpy as np
import datetime as dt
#import FTTR_temp as temp
import os
import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)

#if os.environ.get('DISPLAY', '')=='':
#    print('no display found. Using :0.0')
#    os.environ.__setitem__('DISPLAY', ':0.0')


#------Main GUI code-----
root = tk.Tk()
root.title("Real Time Plot")
root.configure(background = 'light grey')
root.geometry("900x600") # Window size

#plt.style.use('fivethirtyeight')

def animate(i):

    chan0 = AnalogIn(ads, ADS.P0)
    chan1 = AnalogIn(ads, ADS.P1)

    S1 = chan0.value
    V1 = chan0.voltage
    temp1 = V1 / (8/1000)
    temp1 = str(round(temp1, 1))
    S2 = chan1.value
    V2 = chan1.voltage
    temp2 = V2 / (8/1000)
    temp2 = str(round(temp2, 1))

    x = dt.datetime.now().strftime('%H:%M:%S')

    plt.cla()

    plt.plot(x, temp1, linewidth = 1.5, label='Sensor 0')
    plt.plot(x, temp2, linewidth = 1.5, label='Sensor 1')
    plt.xticks(rotation=45, ha='right')
    plt.xticks(np.arange(0, len(x)+1, 10))
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()


canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas.get_tk_widget().place(x = 10, y = 10, width = 600, height = 400)
canvas.draw()

x = dt.datetime.now().strftime('%H:%M:%S')

ani = FuncAnimation(plt.gcf(), animate, interval=1000)


#------Create buttons------
root.update()
auto = tk.Button(root, text = "Auto", font = ('calibri', 12), command = lambda: mode_auto())
auto.place(x = 650, y = 30)

root.update()
maunual = tk.Button(root, text = "Manual", font = ('calibri', 12), command = lambda: mode_manual())
maunual.place(x = auto.winfo_x()+auto.winfo_reqwidth() + 10, y = 30)

root.update()
P = tk.Button(root, text = "P", font = ('calibri', 12), command = lambda: contr_P())
P.place(x = 650, y = 90)

root.update()
PI = tk.Button(root, text = "PI", font = ('calibri', 12), command = lambda: contr_PI())
PI.place(x = P.winfo_x()+P.winfo_reqwidth() + 10, y = 90)

root.update()
PD = tk.Button(root, text = "PD", font = ('calibri', 12), command = lambda: contr_PD())
PD.place(x = PI.winfo_x()+PI.winfo_reqwidth() + 10, y = 90)

root.update()
PID = tk.Button(root, text = "PID", font = ('calibri', 12), command = lambda: contr_PID())
PID.place(x = PD.winfo_x()+PD.winfo_reqwidth() + 10, y = 90)

tk.mainloop()