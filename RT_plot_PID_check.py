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
    
    t0, = plt.plot(x, temp0, linewidth = 1.5, label='Sensor 0')
    t1, = plt.plot(x, temp1, linewidth = 1.5, label='Sensor 1')
    t2, = plt.plot(x, temp2, linewidth = 1.5, label='Sensor 2')
    t3, = plt.plot(x, temp3, linewidth = 1.5, label='Sensor 3')
    t4, = plt.plot(x, temp4, linewidth = 1.5, label='Sensor 4')
    
    
    plt.xticks(rotation=90, ha='right', fontsize=12)
    plt.xticks(np.arange(0, len(x)+1, 20))
    
legend = plt.legend(loc='upper left')
t0_legend, t1_legend, t2_legend, t3_legend, t4_legend = legend.get_lines()
t0_legend.set_picker(True)
t0_legend.set_pickradius(10)
t1_legend.set_picker(True)
t1_legend.set_pickradius(10)
t2_legend.set_picker(True)
t2_legend.set_pickradius(10)
t3_legend.set_picker(True)
t3_legend.set_pickradius(10)
t4_legend.set_picker(True)
t4_legend.set_pickradius(10)

plt.tight_layout()

graphs = {}
graphs[t0_legend] = t0
graphs[t1_legend] = t1
graphs[t2_legend] = t2
graphs[t3_legend] = t3
graphs[t4_legend] = t4

    
def on_pick(event):
    legend = event.artist
    isVisible = legend.get_visible()
    
    graphs[legend].set_visible(not isVisible)
    legend.set_visible(not isVisible)
    
    
plt.connect('pick_event', on_pick)
    
canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas.get_tk_widget().place(x = 10, y = 10, width = 600, height = 400)
canvas.draw()


ani = FuncAnimation(plt.gcf(), animate, interval=500)

#------Create buttons------
root.update()
A = tk.Button(root, text = "Auto", font = ('calibri', 12), command = lambda: mode_auto())
A.place(x = 670, y = 30)

root.update()
M = tk.Button(root, text = "Manual", font = ('calibri', 12), command = lambda: mode_manual())
M.place(x = A.winfo_x()+A.winfo_reqwidth() + 10, y = 30)

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

root.update()
auto_label = tk.Label(root, text = 'Auto:', font = ('calibre', 10))
auto_label.place(x = 630, y = td_label.winfo_y()+td_label.winfo_reqwidth() + 10)
auto_ent = tk.Entry(root)
auto_ent.insert(0, "1")
auto_ent.place(x = 670, y = td_label.winfo_y()+td_label.winfo_reqwidth() + 10)

root.update()
man_label = tk.Label(root, text = 'Manual:', font = ('calibre', 10))
man_label.place(x = 610, y = 300)
man_ent = tk.Entry(root)
man_ent.insert(0, "0")
man_ent.place(x = 670, y = 300)


var0 = tk.IntVar()
M0 = tk.Checkbutton(root, text='Manual', variable=var0, onvalue=1, offvalue=0, command = lambda: mode_manual())
M0.place(x = 50, y = 420)



        
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
        f.write('%s,%s,%s,%s,%s,%s'%(sp,kp,ti,td,auto,man))
   
root.mainloop()
