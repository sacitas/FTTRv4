import FTTRv4_PID as PID
import FTTRv4_temp as tmp
import FTTRv4_GUI as GUI

def main():
    
    tmp.init_time()
    GUI.init_time_plot()
    PID.PID_main()

main()
