import PID_FTTR_V4_FINAL as PID
import temp_gen_digi as temp

def main():
    # default mode    
    Auto = 0

    # User input
    user_input = int(input("Enter Auto (1) or Manual (0): "))

    if user_input == 1:
        Auto = 1
    else:
        Auto = 0

    PID.createConfig()
    PID.setup()
    try:
        while True:
            if Auto == 1:
                PID.PID_loop()
            elif Auto == 0:
                PID.ManVal_loop()
    except KeyboardInterrupt:
        destroy()

main()
