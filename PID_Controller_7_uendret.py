#PID Controller
import time
import threading


#Definitions
#e      - error
#e_prev - error previous
#SP     - Setpoint 
#PV     - Process sensor value
#dt sampling


#Global parameters
SP = 120
PV = 0
Kp = 1
Ki = 0
Kd = 0
dt = 2
max_windup = 100
min_windup = 0
max_output = 100
min_output = 0


class PID(): 
    def __init__(self, SP, PV, Kp, Ki, Kd, dt, max_windup, min_windup, max_output, min_output):   
        #Setpoint
        self.SP = SP
        
        #Process value
        self.PV = PV
     
        #Controller parameters
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        
        #Sampling time
        self.dt = dt
        
        #Saturation parameters
        self.max_windup = max_windup
        self.min_windup = min_windup
        
        
        self.max_output = max_output
        self.min_output = min_output
        
        
        
        #Initial condition parameters
        self.e = 0
        self.e_prev = 0
        self.P = 0
        self.I = 0
        self.D = 0
     
    def Compute(self):  
        #Error term
        self.e = self.SP - self.PV
        
        #Proportional term
        self.P = self.Kp * self.e
            
        #Integral term
        self.I += self.Ki * self.e * self.dt
          
        #Saturation Integral term
        if self.I >= self.max_windup:
            self.I = self.max_windup
        elif self.I <= self.min_windup:
            self.I = self.min_windup
        
        #Derivative term
        dedt = (self.e - self.e_prev)/self.dt
        self.D = self.Kd * dedt
        
        #Update stored data for next calculation
        self.e_prev = self.e
            
        #Computed value
        self.output = self.P + self.I + self.D
        
        #Saturation output term
        if self.output >= self.max_output:
            self.output = self.max_output
        elif self.output <= self.min_output:
            self.output = self.min_output
           
        return self.output
    
    def setSP(self, Setpoint):
        self.SP = Setpoint
        
    def setPV(self, Process_value):
        self.PV = Process_value
        
    def setKp(self, proportional_gain):
        self.Kp = proportional_gain
        
    def setKi(self, integral_gain):
        self.Ki = integral_gain
 
    def setKd(self, derivative_gain):
        self.Kd = derivative_gain
     
    def setdt(self, sampling_time):
        self.dt = sampling_time
         
    def setmax_windup(self, max_saturation):
        self.max_windup = max_saturation
        
    def setmin_windup(self, min_saturation):
        self.min_windup = min_saturation
                
    def setmax_output(self, max_output):
        self.max_output = max_output
        
    def setmin_output(self, min_output):
        self.min_output = min_output


PID = PID(SP, PV, Kp, Ki, Kd, dt, max_windup, min_windup, max_output, min_output)


def PID_output():
    while True:
        print('\nPID output value is: ', PID.Compute())
        time.sleep(PID.dt)   

thread_PID = threading.Thread(target=PID_output)
thread_PID.start()
   

    