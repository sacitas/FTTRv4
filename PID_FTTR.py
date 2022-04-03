# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 09:13:05 2022

@author: Martin
"""
#import RPi.GPIO as GPIO
import RPi.GPIO as GPIO
import time
import os.path

# Parameters
Ts = float(input("Enter a samplingtime: "))
SP = float(input("Enter a setpoint: "))
K_p = float(input("Enter a K_p value: "))
T_i = float(input("Enter a T_i value: "))
T_d = float(input("Enter a T_d value: "))
N = float(input("Enter a filter (N) value: "))
T_t = 0
Tr_gain = 0
U_total = 0
PV = [0,0]
e = [0, 0]
U_i = [0, 0]
U_d = [0, 0]

PWM_pin = 33 # PWM pin on Raspberry Pi
 
# Setup of the PWM pin on the Raspberry Pi
def setup(PWM_pin):
    global pwm
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PWM_pin, GPIO.OUT)
    pwm = GPIO.PWM(PWM_pin, 1000) # Set Frequency to 1 KHz
    pwm.start(0) # Set the starting Duty Cycle
        
# Destroy PWM pin
def destroy():
    pwm.stop()
    GPIO.cleanup()

# Output value from PID into PWM signal
def FTTR_PID_output(U_total):
    Output_PID = U_total
    pwm.ChangeDutyCycle(Output_PID)
    
def createConfig():
    os.remove("pid.conf")
    with open ('pid.conf', 'w') as f:
        f.write('%s,%s,%s,%s,%s'%(SP,K_p,T_i,T_d,Auto))
            
def readConfig():
    global SP, K_p, T_i, T_d, Auto
    with open ('pid.conf', 'r+') as f:
        config = f.readline().split(',')
        SP = float(config[0])
        K_p = float(config[1])
        T_i = float(config[2])
        T_d = float(config[3])
        Auto = int(config[4])

# PID-controller
def FTTR_PID(Ts, SP, PV, K_p, T_i, T_d, T_t, Tr_gain, U_total):
    # Check for zero division
    if(T_i > 0):
        alpha = Ts/T_i
    else:
        alpha = 0
        
    if(T_t > 0):
        gamma = Ts/T_t
    else:
        gamma = 0
        
    if((T_d + Ts*N)>0):
        beta = T_d/(T_d+Ts*N)
    else:
        beta = 0
    
    # Calculate error from setpoint
    e[0] = SP - PV[0]
    
    # Proportional control
    U_p = K_p * e[0]
    
    # Clamp P-term
    if(U_p>100):
        U_p = 100
    elif(U_p<0):
        U_p = 0
    
    # Integral control with anti-windup (back calculation)
    U_i[0] = U_i[1] + (K_p * alpha * e[0]) + gamma*(Tr_gain - U_total)
    
    # Clamp I-term
    if(U_i[0]>100):
        U_i[0] = 100
    elif(U_i[0]<0):
        U_i[0] = 0
        
    # Derivative control 
    U_d[0] = beta*U_d[1] - K_p*(T_d/Ts)*(1-beta)*(PV[0]-PV[1])
    
    # Clamp D-term
    if(U_d[0]>100):
        U_d[0] = 100
    elif(U_d[0]<0):
        U_d[0] = 0
    
    # Total control
    U_total = U_p + U_i[0] + U_d[0]
    
    # Clamp total control
    if(U_total>100):
        U_total = 100
    elif(U_total<0):
        U_total = 0
    
    # Update values
    e[1] = e[0]
    PV[1] = PV[0]
    U_i[1] = U_i[0]
    U_d[1] = U_d[0]
    
    print(U_total)
    
    # Samplingtime 
    time.sleep(Ts)
    
# default mode    
Auto = 0

# User input
user_input = int(input("Enter Auto (1) or Manual (0): "))

if user_input == 1:
    Auto = 1
    createConfig()
    setup(PWM_pin)
else:
    Auto = 0
    
try:
    while Auto == 1:
        readConfig()
        FTTR_PID(Ts, SP, PV, K_p, T_i, T_d, T_t, Tr_gain, U_total)
        FTTR_PID_output(U_total)
    print("done!")

except:
    KeyboardInterrupt
    destroy()
