#PID Controller

#Import necessary packages
import RPi.GPIO as GPIO
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

#### Startup parameters ####
SP = 100 #Setpoint
Kp = 1   #Proportional gain
Ti = 0   #Integral time
Td = 0   #Derivative time  
N = 10   #filter coefficient
dt = 5  #Sampling time
PV = 0   #Process value readings


PWM_pin = 33 # PWM pin on Raspberry Pi

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PWM_pin, GPIO.OUT)
pwm = GPIO.PWM(PWM_pin, 1000) # Set Frequency to 1 KHz
pwm.start(0) # Set the starting Duty Cycle
            
class PID(): 
    def __init__(self, SP, Kp, Ti, Td, N, dt): 
        #Setpoint
        self.SP = SP
    
        #Gain parameters for proportional, integral and derivative 
        self.Kp = Kp
        
        self.Ti = Ti
        if self.Ti == 0:
            self.Ki = 0
        else:
            self.Ki = self.Kp / self.Ti
          
        self.Td = Td
        self.Kd = self.Kp * self.Td
    
        #Filter coefficient
        self.N = N
        
        #Sampling time
        self.dt = dt
        
        #Beta
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
            if self.Ti == 0:
                 self.Ki = 0
                 self.I = 0
            else:
                self.Ki = self.Kp / self.Ti
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
            pass
    
    def setstop(self, stop):
        self.stop = stop

    def setSP(self, Setpoint):
        self.SP = Setpoint
        
    def setKp(self, Kp):
        self.Kp = Kp
        
    def setTi(self, Ti):
        self.Ti = Ti
 
    def setTd(self, Td):
        self.Td = Td
        
    def setN(self, N):
        self.N = N
       
    def setdt(self, dt):
        self.dt = dt
        
#Call the class to start the PID controller            
PID = PID(SP, Kp, Ti, Td, N, dt)



def main():   
    while True:              
        try: 
            pwm.ChangeDutyCycle(PID.Compute(PV)) 
        except KeyboardInterrupt:
            pwm.stop()
            GPIO.cleanup() # cleanup all GPIO 
    
#Thread the function over to let it run in the background
threading.Thread(target = main).start()   
              
