import PLT_config as config
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

degree_sign = u'\N{DEGREE SIGN}'

plot_folder = "plot/"
plot_filename = ""
plot_filepath = ""


def init_time():
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


def plot(filename):

    path_to_file = 'temp/' + filename

    data = pd.read_csv(path_to_file)
    x = data["x"]
    temp0 = data["temp0"]
    temp1 = data["temp1"]
    temp2 = data["temp2"]
    temp3 = data["temp3"]
    temp4 = data["temp4"]

    
    plt.plot(x, temp0, label = config.sensors['sensor_0'], linewidth = 1.5, color = 'b')
    plt.plot(x, temp1, label = config.sensors['sensor_1'], linewidth = 1.5, color = 'g')
    plt.plot(x, temp2, label = config.sensors['sensor_2'], linewidth = 1.5, color = 'r')
    plt.plot(x, temp3, label = config.sensors['sensor_3'], linewidth = 1.5, color = 'c')
    plt.plot(x, temp4, label = config.sensors['sensor_4'], linewidth = 1.5, color = 'm')

    plt.xlabel('Time [hh:mm:ss]')
    plt.ylabel('Temperature' + '[' + degree_sign + 'C', fontsize=10)
    plt.title(str(x[0]), fontsize = 15)
    plt.ylim([0, 150])
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.xticks(np.arange(0, len(x), 80))
    plt.legend(loc='lower right', prop={'size':10})
    plt.grid()
    plt.tight_layout()
    plt.show()
    plt.savefig(f'{plot_filepath}.png')
    
