import FTTRv4_PID as PID
import FTTRv4_temp as tmp

def main():
    
    tmp.init_time()
    PID.PID_main()

main()
