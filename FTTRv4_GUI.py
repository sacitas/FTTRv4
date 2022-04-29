from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import tkinter as tk
import pandas as pd
import numpy as np
import csv
import os
import FTTRv4_temp as tmp

#---Initial values---
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
root.geometry("1000x700") # Window size

plt.style.use('fivethirtyeight')


#--------Save plot function--------
def savePlot():
    plt.savefig("sacitErKjekk.png")
    
#-------Plot function to animate--------
def animate(i):
    
    #-----Reads csv file & collecting data-----
    data = pd.read_csv('temp_read.csv')
    x = data["x"]
    dtemp0 = data["dtemp0"]
    dtemp1 = data["dtemp1"]
    dtemp2 = data["dtemp2"]
    dtemp3 = data["dtemp3"]
    dtemp4 = data["dtemp4"]

    plt.cla()
    
    plt.plot(x, dtemp0, linewidth = 1.5, label='Sensor d0')
    plt.plot(x, dtemp1, linewidth = 1.5, label='Sensor d1')
    plt.plot(x, dtemp2, linewidth = 1.5, label='Sensor d2')
    plt.plot(x, dtemp3, linewidth = 1.5, label='Sensor d3')
    plt.plot(x, dtemp4, linewidth = 1.5, label='Sensor d4')    
    
    plt.ylim([0, 200])
    plt.xticks(rotation=90, ha='right', fontsize=8)
    plt.xticks(np.arange(0, len(x)+1, 30))
    plt.legend(loc='upper left', prop={'size':10})
    plt.tight_layout()
    

#----------------Plot window in GUI----------------
canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas.get_tk_widget().place(x = 10, y = 10, width = 820, height = 550)
canvas.draw()

#------------------Animate function------------------
ani = FuncAnimation(plt.gcf(), animate, interval=500)

#-------Setting regulator values-------
def SetRegVals():  
    
    global sp, kp, ti, td, auto, man
    #-----Gets values from input fields-----
    sp = SP_ent.get()
    sp = float(sp)
    kp = kp_ent.get()
    kp = float(kp)
    ti = ti_ent.get()
    ti = float(ti)
    td = td_ent.get()
    td = float(td)
    
#-----Sets auto/manual mode from checkbox-----
    if (var0.get() == 1):
        auto = 1
    else:
        auto = 0
    #-----Gets value from input field-----
    man = man_ent.get()
    man = float(man)
    
#-----------Writes the regulator values to file-------------
    with open ('pid.conf', 'w') as f:
        f.write('%s,%s,%s,%s,%s,%s'%(sp,kp,ti,td,auto,man))
        
    S_P_label = tk.Label(root, text = 'Setpoint:', font = ('calibre', 10))
    S_P_label.place(x = 10, y = 600)
    S_P = tk.Label(root, text = sp, font = ('calibre', 10))
    S_P.place(x = 100, y = 600)

    
with open ('pid.conf', 'r+') as g:
    conf = g.readline().split(',')
    SP = float(conf[0])
    KP = float(conf[1])
    TI = float(conf[2])
    TD = float(conf[3])


#-------Creates checkbutton-------
root.update()
var0 = tk.IntVar()
MA = tk.Checkbutton(root, text='AUTO', variable=var0, onvalue=1, offvalue=0)
MA.place(x = 870, y = 30)

#-------Creates button-------
root.update()
S = tk.Button(root, text = "Save plot", font = ('calibri', 12), command = lambda: savePlot())
S.place(x = 730, y = 570)

#-------Create input fields--------
root.update()
SP_label = tk.Label(root, text = 'SP:', font = ('calibre', 10))
SP_label.place(x = 870, y = 100)
SP_ent = tk.Entry(root, width=7)
if (var0.get() == 0):
    SP_ent.config(state='disabled')
SP_ent.insert(0, SP)
SP_ent.place(x = 900, y = 100)

root.update()
kp_label = tk.Label(root, text = 'Kp:', font = ('calibre', 10))
kp_label.place(x = 870, y = SP_label.winfo_y()+SP_label.winfo_reqwidth() + 30)
kp_ent = tk.Entry(root, width=7)
kp_ent.insert(0, KP)
kp_ent.place(x = 900, y = SP_label.winfo_y()+SP_label.winfo_reqwidth() + 30)

root.update()
ti_label = tk.Label(root, text = 'Ti:', font = ('calibre', 10))
ti_label.place(x = 870, y = kp_label.winfo_y()+kp_label.winfo_reqwidth() + 30)
ti_ent = tk.Entry(root, width=7)
ti_ent.insert(0, TI)
ti_ent.place(x = 900, y = kp_label.winfo_y()+kp_label.winfo_reqwidth() + 30)

root.update()
td_label = tk.Label(root, text = 'Td:', font = ('calibre', 10))
td_label.place(x = 870, y = ti_label.winfo_y()+ti_label.winfo_reqwidth() + 30)
td_ent = tk.Entry(root, width=7)
td_ent.insert(0, TD)
td_ent.place(x = 900, y = ti_label.winfo_y()+ti_label.winfo_reqwidth() + 30)

root.update()
man_label = tk.Label(root, text = 'Manual\nvalue:', font = ('calibre', 10))
man_label.place(x = 845, y = td_label.winfo_y()+td_label.winfo_reqwidth() + 20)
man_ent = tk.Entry(root, width=7)
man_ent.insert(0, "0")
man_ent.place(x = 900, y = td_label.winfo_y()+td_label.winfo_reqwidth() + 30)

#-------Creates button-------
root.update()
SV = tk.Button(root, text = "SET", font = ('calibri', 12), command = lambda: SetRegVals())
SV.place(x = 900, y = 360)


root.update()
temp_label = tk.Label(root, text = 'RegTemp: ', font = ('calibre', 10))
temp_label.place(x = 10, y = 570)
temp = tk.Label(root, text = 'dtemp0', font = ('calibre', 10))
temp.place(x = 100, y = 570)

root.update()
S_P_label = tk.Label(root, text = 'Setpoint:', font = ('calibre', 10))
S_P_label.place(x = 10, y = 600)
S_P = tk.Label(root, text = SP, font = ('calibre', 10))
S_P.place(x = 100, y = 600)

root.update()
A0_label = tk.Label(root, text = 'A0: ', font = ('calibre', 10))
A0_label.place(x = 10, y = 630)
A0 = tk.Label(root, text = '150', font = ('calibre', 10))
A0.place(x = 100, y = 630)

root.update()
A1_label = tk.Label(root, text = 'A1: ', font = ('calibre', 10))
A1_label.place(x = 10, y = 660)
A1 = tk.Label(root, text = '150', font = ('calibre', 10))
A1.place(x = 100, y = 660)
   
root.mainloop()
