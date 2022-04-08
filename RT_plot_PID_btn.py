from curses import window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import tkinter as tk
import pandas as pd
import numpy as np
import csv

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

    getSP = pd.read_csv('SP_val.csv')
    SP = getSP["sp"]

    plt.cla()

    plt.plot(x, temp0,  linewidth = 1.5, label='Sensor 0')
    plt.plot(x, SP,  linewidth = 1.5, label='Setpoint')
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
SSP = tk.Button(root, text = "Set SP", font = ('calibri', 12), command = lambda: SetSP())
SSP.place(x = 650, y = 160)

root.update()
SP_ent = tk.Entry(root)
SP_ent.place(x = 650, y = 140)
kp = tk.Entry(root)
ti = tk.Entry(root)
td = tk.Entry(root)


def SetSP():

    sp = SP_ent.get()

    fieldnames = ["SP"]

    with open('pid_conf.csv', 'w') as SP_csv:
        csv_writer = csv.DictWriter(SP_csv, fieldnames=fieldnames)
        csv_writer.writeheader()
    
    with open('pid_conf.csv', 'a') as SP_csv:
        csv_writer = csv.DictWriter(SP_csv, fieldnames=fieldnames)
        info = {
            "SP": sp
        }
        csv_writer.writerow(info)
        SP_csv.close()

root.mainloop()
