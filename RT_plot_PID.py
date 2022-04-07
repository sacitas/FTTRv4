from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import tkinter as tk
import pandas as pd
import numpy as np


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
    
    f = pd.read_csv('pid_conf.csv')
    for i in range(4):
        f.readline()
    SP_read = f.readline().split(':')
    SP = float(SP_read[1])
    
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
auto = tk.Button(root, text = "Start", font = ('calibri', 12), command = lambda: start())
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



root.mainloop()
