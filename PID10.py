#PID Controller

#Import necessary packages
import time
import threading

#Definition of variables
#SP      - Setpoint 
#PV      - Process value
#Kp      - Proportional gain
#Ki      - Integral gain
#Kd      - Derivative gain
#Td      - Derivative time 
#N       - Filter coefficient
#dt      - Sampling time
#Beta    - Beta?
#e       - error value
#PV_prev - Process value value previous

#Startup parameters
SP = 120
Kp = 1
Ki = 0
Kd = 0
dt = 1

#Startup parameters for Beta
Td = 0
N = 10

#Process value readings
PV = 6

class PID(): 
    def __init__(self, SP, Kp, Ki, Kd, dt, Td, N): 
        #Setpoint
        self.SP = SP
    
        #Gain parameters for proportional, integral and derivative
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        
        #Sampling time
        self.dt = dt
        
        #Beta???
        self.Td = Td
        self.N = N
        
        if (self.Td + self.dt * self.N) > 0:
            self.Beta = self.Td/(self.Td + self.dt * self.N)
        else:
            self.Beta = 0
            
        #Limits for saturation and output
        self.max_windup = 100
        self.min_windup = 0
        self.max_output = 100
        self.min_output = 0
    
        #Initial condition 
        self.e = 0
        self.e_prev = 0
        self.PV_prev = 0
        self.P = 0
        self.I = 0
        self.D = 0
        
        #Startup flag to stop/pause or continue the controller
        self.stop = False
        
    def Compute(self, PV): 
        if self.stop == False:
            #Error term
            self.e = self.SP - PV
            
            #Proportional term
            self.P = self.Kp * self.e
                
            #Integral term
            self.I += self.Ki * self.e * self.dt
        
            #Saturation Integral term
            if self.I >= self.max_windup:
                self.I = self.max_windup
            elif self.I <= self.min_windup:
                self.I = self.min_windup
            
            #Derivative term and Beta
            if (self.Td + self.dt * self.N) > 0:
                self.Beta = self.Td/(self.Td + self.dt * self.N)
            else:
                self.Beta = 0
                
            self.D = self.Beta * self.D - self.Kd/dt * (1 - self.Beta)*(PV - self.PV_prev)
            
            #update stored data for next calculation
            self.PV_prev = PV
                
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
        
    def setKp(self, Proportional_gain):
        self.Kp = Proportional_gain
        
    def setKi(self, Integral_gain):
        self.Ki = Integral_gain
 
    def setKd(self, Derivative_gain):
        self.Kd = Derivative_gain
        
    def setTd(self, Td):
        self.Td = Td
        
    def setN(self, N):
        self.N = N
       
    def setdt(self, Sampling_time):
        self.dt = Sampling_time
        
    def setstop(self, stop):
        self.stop = stop

#Call the class to start the PID controller            
PID = PID(SP, Kp, Ki, Kd, dt, Td, N)

def run():
    while True:
        if PID.Compute(PV) == None:
            pass
         
        elif PID.Compute(PV) != None:
            print('\nPID output value is: ', PID.Compute(PV))
            time.sleep(PID.dt)  
 
#Thread the function over to let it run in the background
thread_PID = threading.Thread(target=run)
thread_PID.start()