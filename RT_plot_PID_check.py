from curses import window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import tkinter as tk
import pandas as pd
import numpy as np
import csv
import os

sp = 0
kp = 0
ti = 0
td = 0
auto = 0
man = 0


#------Main GUI code-----
root = tk.Tk()
root.title("Real Time Plot")
root.configure(background = 'light grey')
root.geometry("900x600") # Window size

plt.style.use('fivethirtyeight')

def animate(i):
    
    data = pd.read_csv('PID_temp.csv')
    x = data["x"]
    temp0 = data["temp0"]
    temp1 = data["temp1"]
    temp2 = data["temp2"]
    temp3 = data["temp3"]
    temp4 = data["temp4"]

    plt.cla()
    
    plt.plot(x, temp0, linewidth = 1.5, label='Sensor 0')
    plt.plot(x, temp1, linewidth = 1.5, label='Sensor 1')
    plt.plot(x, temp2, linewidth = 1.5, label='Sensor 2')
    plt.plot(x, temp3, linewidth = 1.5, label='Sensor 3')
    plt.plot(x, temp4, linewidth = 1.5, label='Sensor 4')
    
    
    plt.xticks(rotation=90, ha='right', fontsize=12)
    plt.xticks(np.arange(0, len(x)+1, 20))
    plt.legend(loc='upper left')
    plt.tight_layout()

    
canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas.get_tk_widget().place(x = 10, y = 10, width = 600, height = 400)
canvas.draw()


ani = FuncAnimation(plt.gcf(), animate, interval=500)

#------Create buttons------

var0 = tk.IntVar()
MA = tk.Checkbutton(root, text='Manual', variable=var0, onvalue=1, offvalue=0)
MA.place(x = 670, y = 50)

root.update()
S_P = tk.Button(root, text = "Save plot", font = ('calibri', 12), command = lambda: save_plot())
S_P.place(x = 670, y = 90)

root.update()
STOP = tk.Button(root, text = "STOP", font = ('calibri', 12), command = lambda: stop_plot())
STOP.place(x = S_P.winfo_x()+S_P.winfo_reqwidth() + 10, y = 90)

root.update()
SV = tk.Button(root, text = "Set", font = ('calibri', 12), command = lambda: SetRegVals())
SV.place(x = 670, y = 350)

root.update()
SP_label = tk.Label(root, text = 'SP:', font = ('calibre', 10))
SP_label.place(x = 640, y = 140)
SP_ent = tk.Entry(root)
SP_ent.insert(0, "25")
SP_ent.place(x = 670, y = 140)

root.update()
kp_label = tk.Label(root, text = 'Kp:', font = ('calibre', 10))
kp_label.place(x = 640, y = SP_label.winfo_y()+SP_label.winfo_reqwidth() + 10)
kp_ent = tk.Entry(root)
kp_ent.insert(0, "1")
kp_ent.place(x = 670, y = SP_label.winfo_y()+SP_label.winfo_reqwidth() + 10)

root.update()
ti_label = tk.Label(root, text = 'Ti:', font = ('calibre', 10))
ti_label.place(x = 640, y = kp_label.winfo_y()+kp_label.winfo_reqwidth() + 10)
ti_ent = tk.Entry(root)
ti_ent.insert(0, "0")
ti_ent.place(x = 670, y = kp_label.winfo_y()+kp_label.winfo_reqwidth() + 10)

root.update()
td_label = tk.Label(root, text = 'Td:', font = ('calibre', 10))
td_label.place(x = 640, y = ti_label.winfo_y()+ti_label.winfo_reqwidth() + 10)
td_ent = tk.Entry(root)
td_ent.insert(0, "0")
td_ent.place(x = 670, y = ti_label.winfo_y()+ti_label.winfo_reqwidth() + 10)

        
def SetRegVals():
    
    global sp, kp, ti, td, auto, man
    
    sp = SP_ent.get()
    sp = float(sp)
    kp = kp_ent.get()
    kp = float(kp)
    ti = ti_ent.get()
    ti = float(ti)
    td = td_ent.get()
    td = float(td)
    auto = auto_ent.get()
    auto = int(auto)
    
    if (var0.get() == 1):
        man = 1
    else:
        man = 0

    with open ('pid.conf', 'w') as f:
        f.write('%s,%s,%s,%s,%s,%s'%(sp,kp,ti,td,auto,man))
   
root.mainloop()
