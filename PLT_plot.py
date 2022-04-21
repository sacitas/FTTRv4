import PLT_config as config
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot(filename):

    path_to_file = '../temp/' + filename

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

    plt.xlabel('Time')
    plt.ylabel('Temperature[C]')
    plt.title(str(x[0]), fontsize = 15)
    plt.ylim([0, 200])
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.xticks(np.arange(0, len(x), 30))
    plt.legend(loc='upper left', prop={'size':12})
    plt.grid()
    plt.tight_layout()
    plt.show()