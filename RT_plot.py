from PIL import ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import tkinter as tk
import pandas as pd
import numpy as np
import time


#------Main GUI code-----
root = tk.Tk()
root.title("Real Time Plot")
root.configure(background = 'light grey')
root.geometry("900x600") # Window size

plt.style.use('fivethirtyeight')

#-------Animate plot-------
def animate(i):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['total_1']
    y2 = data['total_2']

    plt.cla()

    plt.plot(x, y1,  linewidth = 1.5, label='Channel 1')
    plt.plot(x, y2, linewidth = 1.5, label='Channel 2')
    plt.xticks(rotation=45, ha='right')
    plt.xticks(np.arange(0, len(x)+1, 10))
    plt.legend(loc='upper left')
    plt.tight_layout()

#------Draw plot------
canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
canvas.get_tk_widget().place(x = 10, y = 10, width = 600, height = 400)
canvas.draw()

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



root.mainloop()