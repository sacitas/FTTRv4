from PIL import ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np
import time


#-----Plot data------
def plot_data():
    global cond



#------Main GUI code-----
root = tk.Tk()
root.title('Real Time Plot')
root.configure(background = 'light grey')
root.geometry("900x600") # Window size

#------Create Plot object on GUI------
# Add figure canvas
fig = Figure()
ax = fig.add_subplot(111)

ax.set_title('FTTRv4 test')
ax.set_xlabel('Time')
ax.set_ylabel('Temperature C')
ax.set_xlim(0, 100)
ax.set_ylim(0, 150)
ax.grid()
lines = ax.plot([],[])[0]


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x = 10, y = 10, width = 600, height = 400)
canvas.draw()

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