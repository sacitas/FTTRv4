from curses import window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import tkinter as tk
import pandas as pd
import numpy as np
import csv

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

    plt.cla()

    plt.plot(x, temp0,  linewidth = 1.5, label='Sensor 0')
#   plt.plot(x, SP,  linewidth = 1.5, label='Setpoint')
    plt.xticks(rotation=90, ha='right', fontsize=12)
    plt.xticks(np.arange(0, len(x)+1, 20))
    plt.legend(loc='upper left')
    plt.tight_layout()


canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas.get_tk_widget().place(x = 10, y = 10, width = 600, height = 400)
canvas.draw()


ani = FuncAnimation(plt.gcf(), animate, interval=500)

#------Create buttons------
root.update()
A = tk.Button(root, text = "Auto", font = ('calibri', 12), command = lambda: mode_auto())
A.place(x = 650, y = 30)

root.update()
M = tk.Button(root, text = "Manual", font = ('calibri', 12), command = lambda: mode_manual())
M.place(x = A.winfo_x()+A.winfo_reqwidth() + 10, y = 30)

root.update()
S_P = tk.Button(root, text = "Save plot", font = ('calibri', 12), command = lambda: save_plot())
S_P.place(x = 650, y = 90)

root.update()
STOP = tk.Button(root, text = "STOP", font = ('calibri', 12), command = lambda: stop_plot())
STOP.place(x = S_P.winfo_x()+S_P.winfo_reqwidth() + 10, y = 90)

root.update()
SV = tk.Button(root, text = "Set", font = ('calibri', 12), command = lambda: SetRegVals())
SV.place(x = 650, y = 260)

root.update()
SP_ent = tk.Entry(root)
SP_ent.place(x = 650, y = 140)

root.update()
kp_ent = tk.Entry(root)
kp_ent.place(x = 650, y = 160)

root.update()
ti_ent = tk.Entry(root)
ti_ent.place(x = 650, y = 180)

root.update()
td_ent = tk.Entry(root)
td_ent.place(x = 650, y = 200)

root.update()
auto_ent = tk.Entry(root)
auto_ent.place(x = 650, y = 220)

root.update()
man_ent = tk.Entry(root)
man_ent.place(x = 650, y = 240)


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
    man = man_ent.get()
    man = int(man)
    
    with open ('pid.conf', 'w') as f:
        f.write('%s,%s,%s,%s,%s,%s'%(sp,kp,ti,ti,auto,man))
   
root.mainloop()
