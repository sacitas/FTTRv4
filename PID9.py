#PID Controller

#Import necessary ?
import time
import threading

#Definition of variables
#SP     - Setpoint 
#PV     - Process value
#Kp     - Proportional gain
#Ki     - Integral gain
#Kd     - Derivative gain
#dt     - Sampling time
#e      - error value
#e_prev - error value previous

#Startup parameters
SP = 100
PV = 50
Kp = 2
Ki = 3
Kd = 5
dt = 0.5
max_windup = 1000
min_windup = 0
max_output = 1000
min_output = 0

#Startup flag to stop/pause the controller
stop = False

class PID(): 
    def __init__(self, SP, PV, Kp, Ki, Kd, dt, max_windup, min_windup, max_output, min_output, stop): 
        #Setpoint
        self.SP = SP
        
        #Process value
        self.PV = PV
       
        #Gain parameters for proportional, integral and derivative
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
        
        self.stop = stop
        
    def Compute(self): 
        if self.stop == False:
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
            
            #update stored data for next calculation
            self.e_prev = self.e
                
            #Computed value
            self.output = self.P + self.I + self.D
            
            #Saturation output 
            if self.output >= self.max_output:
                self.output = self.max_output
            elif self.output <= self.min_output:
                self.output = self.min_output
                
            return self.output
    
        elif self.stop == True:
            return None
           
    def setSP(self, Setpoint):
        self.SP = Setpoint
        
    def setPV(self, Process_value):
        self.PV = Process_value
        
    def setKp(self, Proportional_gain):
        self.Kp = Proportional_gain
        
    def setKi(self, Integral_gain):
        self.Ki = Integral_gain
 
    def setKd(self, Derivative_gain):
        self.Kd = Derivative_gain
     
    def setdt(self, Sampling_time):
        self.dt = Sampling_time
         
    def setmax_windup(self, max_saturation):
        self.max_windup = max_saturation
        
    def setmin_windup(self, min_saturation):
        self.min_windup = min_saturation
               
    def setmax_output(self, max_output):
        self.max_output = max_output
        
    def setmin_output(self, min_output):
        self.min_output = min_output
        
    def setstop(self, stop):
        self.stop = stop

#Call the class to start the PID controller            
PID = PID(SP, PV, Kp, Ki, Kd, dt, max_windup, min_windup, max_output, min_output, stop)

def run():
    while True:
        if PID.Compute() == None:
            pass
         
        elif PID.Compute() != None:
            print('\nPID output value is: ', PID.Compute())
            time.sleep(PID.dt)  
 
#Thread the function over to let it run in the background
thread_PID = threading.Thread(target=run)
thread_PID.start()
