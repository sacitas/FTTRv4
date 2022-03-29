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
SP = 100
PV = 60
Kp = 2
Ki = 3
Kd = 5
dt = 0.5
max_windup = 1000
min_windup = 0


class PID(): 
    def __init__(self, SP, PV, Kp, Ki, Kd, dt, max_windup, min_windup):   
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
        
        
        #Saturation output
        if self.I >= self.max_windup:
            self.I = self.max_windup
        elif self.I <= self.min_windup:
            self.I = self.min_windup
        
        #Derivative term
        dedt = (self.e - self.e_prev)/self.dt
        self.D = self.Kd * dedt
        
        #update stored data for next calculation
        self.e_prev = self.e
            
        #Computed value
        self.output = self.P + self.I + self.D
            
    
                   
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

PID = PID(SP, PV, Kp, Ki, Kd, dt, max_windup, min_windup)


def PID_output():
    while True:
        print('\nPID output value is: ', PID.Compute())
        time.sleep(PID.dt)   

thread_PID = threading.Thread(target=PID_output)
thread_PID.start()
   

    