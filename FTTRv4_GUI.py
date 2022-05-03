from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import datetime as dt
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import csv
import os
import FTTRv4_temp as tmp
import FTTRv4_PID as PID
#import Adafruit_ADS1x15
import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1115 import Mode
import time

#adc = Adafruit_ADS1x15.ADS1115()

#GAIN = 1

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)

ads.mode = Mode.CONTINUOUS

degree_sign = u'\N{DEGREE SIGN}'

#---Initial values---
sp = 0
kp = 0
ti = 0
td = 0
auto = 0
man = 0
is_on = True


plot_folder = "plot/"
plot_filename = ""
plot_filepath = ""


#------Main GUI code-----
root = tk.Tk()
root.title("Real Time Plot")
root.configure(background = 'light grey')
root.geometry("1150x700") # Window size

plt.style.use('fivethirtyeight')


def init_time_plot():
    global ref_time  
    global plot_folder
    global plot_filename
    global plot_filepath
    
    now = dt.datetime.now()
    t = now.strftime("%H:%M:%S")
    (h, m, s) = t.split(':')
    ref_time = int(h) * 3600 + int(m) * 60 + int(s)
    
    plot_filename = now.strftime("%m_%d_%Y-%H:%M")
    plot_filepath = plot_folder + plot_filename
    
    S['text'] = 'Plot saved!'


#--------Save plot function--------
def savePlot():
    init_time_plot()
    plt.savefig(f'{plot_filepath}.png')
    saved = tk.Label(root, text='/home/pi/Orbit-NTNU', font = ('calibre', 10))
    saved.place(x=730, y=620)
    open(f'{plot_filepath}.png')

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
    
    plt.plot(x, dtemp0, linewidth = 1.5, label='Sensor d0', color = '#4876FF')
    plt.plot(x, dtemp1, linewidth = 1.5, label='Sensor d1', color = '#EE0000')
    plt.plot(x, dtemp2, linewidth = 1.5, label='Sensor d2', color = 'orange')
    plt.plot(x, dtemp3, linewidth = 1.5, label='Sensor d3', color = '#008B45')
    plt.plot(x, dtemp4, linewidth = 1.5, label='Sensor d4', color = '#708090')    
    
    plt.ylim([0, 150])
    plt.xlabel("Time [hh:mm:ss]", fontsize=10)
    plt.ylabel("Temperature " + "[" + degree_sign + "C]", fontsize=10)
    plt.xticks(rotation=90, ha='right', fontsize=8)
    plt.xticks(np.arange(0, len(x)+1, 70))
    plt.yticks(fontsize=10)
    plt.tight_layout()
    
    
    chan0 = AnalogIn(ads, ADS.P0)
    chan1 = AnalogIn(ads, ADS.P1)
    S1 = chan0.value
    V1 = chan0.voltage
    atemp0 = V1 / (11/1000)
    atemp0 = float(round(atemp0, 1))
    S2 = chan1.value
    V2 = chan1.voltage
    atemp1 = V2 / (11/1000)
    atemp1 = float(round(atemp1, 1))
    
    #S1 = adc.read_adc(0, gain = GAIN)
    #V1 = S1*(5.0/65535)
    #atemp0 = V1 / (7/1000)
    #atemp0 = str(round(atemp0, 2))
    #S2 = adc.read_adc(1, gain = GAIN)
    #V2 = S2*(5.0/65535)
    #atemp1 = V2 / (7/1000)
    #atemp1 = str(round(atemp1, 2))
    
    
    root.update()
    temp0 = tmp.read_temp0()
    temp0 = str(round(temp0, 2))
    temp = tk.Entry(root, width = 7)
    temp.insert(0, temp0)
    temp.config(state='readonly')
    temp.place(x = 970, y = 415)
    
    control = tk.Entry(root, width = 7)
    control.insert(0, 'U_total')
    control.config(state='readonly')
    control.place(x = 970, y = 455)
    
    root.update()
    A0 = tk.Entry(root, width = 7)
    A0.insert(0, atemp0)
    A0.config(state='readonly')
    A0.place(x = 970, y = 535)
    
    root.update()
    A1 = tk.Entry(root, width = 7)
    A1.insert(0, atemp1)
    A1.config(state='readonly')
    A1.place(x = 970, y = 575)
    

#----------------Plot window in GUI----------------
canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas.get_tk_widget().place(x = 10, y = 10, width = 840, height = 555)
canvas.draw()

#------------------Animate function------------------
ani = FuncAnimation(plt.gcf(), animate, interval=1000)


def switch():
    global sp, kp, ti, td, auto, man, is_on
    if is_on:
        auto = 0
        MA.config(image = off)
        SP_ent.config(state='readonly')
        kp_ent.config(state='readonly')
        ti_ent.config(state='readonly')
        td_ent.config(state='readonly')
        man_ent.config(state='normal')
        modeA_ = tk.Entry(root, width=8)
        modeA_.insert(0, "Manual")
        modeA_.config(state='readonly')
        modeA_.place(x = 940, y = 10)
        
        is_on = False
    else:
        auto = 1
        MA.config(image = on)
        SP_ent.config(state='normal')
        kp_ent.config(state='normal')
        ti_ent.config(state='normal')
        td_ent.config(state='normal')
        man_ent.config(state='readonly')
        modeM_ = tk.Entry(root, width=8)
        modeM_.insert(0, "Auto")
        modeM_.config(state='readonly')
        modeM_.place(x = 940, y = 10)
        
        is_on = True
        

    #-----Gets values from input fields-----
    sp = SP_ent.get()
    sp = float(sp)
    kp = kp_ent.get()
    kp = float(kp)
    ti = ti_ent.get()
    ti = float(ti)
    td = td_ent.get()
    td = float(td)
    
    #-----Gets value from input field-----
    man = man_ent.get()
    man = float(man)
    
#-----------Writes the regulator values to file-------------
    with open ('pid.conf', 'w') as f:
        f.write('%s,%s,%s,%s,%s,%s'%(sp,kp,ti,td,auto,man))
 

on = tk.PhotoImage(file = "on.png")
off = tk.PhotoImage(file = "off.png")

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
    
    #-----Gets value from input field-----
    man = man_ent.get()
    man = float(man)
    
#-----------Writes the regulator values to file-------------
    with open ('pid.conf', 'w') as f:
        f.write('%s,%s,%s,%s,%s,%s'%(sp,kp,ti,td,auto,man))
        
    S_P_ = tk.Entry(root, width=7)
    S_P_.insert(0, sp)
    S_P_.config(state='readonly')
    S_P_.place(x = 970, y = 495)

    
with open ('pid.conf', 'r+') as g:
    conf = g.readline().split(',')
    SP = float(conf[0])
    KP = float(conf[1])
    TI = float(conf[2])
    TD = float(conf[3])


root.update()
MA = tk.Button(root, image = off, bd = 0, command = lambda: switch())
MA.place(x = 930, y = 30)
#mode_label = tk.Label(root, text = 'Auto on/off', font = ('calibre', 10))
#mode_label.place(x = 900, y = 10)


#-------Creates button-------
root.update()
S = tk.Button(root, text = "Save plot", font = ('calibri', 12), command = lambda: savePlot())
S.place(x = 730, y = 590, width=120, heigh=31)


frame1 = tk.Frame(root, width=230, height=290, highlightbackground='grey', highlightthickness=1)
frame1.place(x=860, y=80)


frame2 = tk.Frame(root, width=230, height=220, highlightbackground='grey', highlightthickness=1)
frame2.place(x=860, y=400)

#-------Create input fields--------
root.update()
SP_label = tk.Label(root, text = 'Setpoint:', font = ('calibre', 10))
SP_label.place(x = 890, y = 90)
SP_ent = tk.Entry(root, width=7)
SP_ent.insert(0, SP)
SP_ent.place(x = 970, y = 90)

root.update()
kp_label = tk.Label(root, text = 'Proportional\n            gain:', font = ('calibre', 10))
kp_label.place(x = 870, y = 130)
kp_ent = tk.Entry(root, width=7)
kp_ent.insert(0, KP)
kp_ent.place(x = 970, y = 140)

root.update()
ti_label = tk.Label(root, text = 'Integral\n     time:', font = ('calibre', 10))
ti_label.place(x = 895, y = 180)
ti_ent = tk.Entry(root, width=7)
ti_ent.insert(0, TI)
ti_ent.place(x = 970, y = 190)

root.update()
td_label = tk.Label(root, text = 'Derivative\n        time:', font = ('calibre', 10))
td_label.place(x = 885, y = 230)
td_ent = tk.Entry(root, width=7)
td_ent.insert(0, TD)
td_ent.place(x = 970, y = 240)

root.update()
man_label = tk.Label(root, text = 'Manual\n   value:', font = ('calibre', 10))
man_label.place(x = 900, y = 280)
man_ent = tk.Entry(root, width=7)
man_ent.insert(0, "0")
man_ent.place(x = 970, y = 290)

#-------Creates button-------
root.update()
SV = tk.Button(root, text = "APPLY", font = ('calibri', 12), command = lambda: SetRegVals())
SV.place(x = 970, y = 330, width=70, height=30)

#-------Labels--------
temp_label = tk.Label(root, text = 'Process\n     value: ', font = ('calibre', 10))
temp_label.place(x = 888, y = 405)

control_label = tk.Label(root, text = 'Control\n     value: ', font = ('calibre', 10))
control_label.place(x = 888, y = 445)

root.update()
S_P_label = tk.Label(root, text = 'Setpoint:', font = ('calibre', 10))
S_P_label.place(x = 893, y = 495)
S_P_ = tk.Entry(root, width=7)
S_P_.insert(0, SP)
S_P_.config(state='readonly')
S_P_.place(x = 970, y = 495)

root.update()
A0_label = tk.Label(root, text = 'Analog\nsensor 0: ', font = ('calibre', 10))
A0_label.place(x = 890, y = 525)

root.update()
A1_label = tk.Label(root, text = 'Analog\nsensor 1: ', font = ('calibre', 10))
A1_label.place(x = 890, y = 565)

sensord0_c = tk.Label(root, text = 'Sensor d0', font = ('calibre', 10, 'bold'), fg = '#4876FF')
sensord0_c.place(x = 20, y = 580)
sensord1_c = tk.Label(root, text = 'Sensor d1', font = ('calibre', 10, 'bold'), fg = '#EE0000')
sensord1_c.place(x = 120, y = 580)
sensord2_c = tk.Label(root, text = 'Sensor d2', font = ('calibre', 10, 'bold'), fg = 'orange')
sensord2_c.place(x = 220, y = 580)
sensord3_c = tk.Label(root, text = 'Sensor d3', font = ('calibre', 10, 'bold'), fg = '#008B45')
sensord3_c.place(x = 320, y = 580)
sensord4_c = tk.Label(root, text = 'Sensor d4', font = ('calibre', 10, 'bold'), fg = '#708090')
sensord4_c.place(x = 420, y = 580)
root.mainloop()
