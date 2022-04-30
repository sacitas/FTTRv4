import FTTRv4_PID as PID
import FTTRv4_temp as tmp

def main():
    
    tmp.init_time()
    tmp.init_time_plot()
    PID.PID_main()

main()
