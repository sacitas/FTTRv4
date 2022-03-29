# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 09:06:18 2022

@author: Martin
"""

# load the necessary packages
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# TVC model
def TVC_nonlinear(y, t):

    # parameters
    A_1 = 0.02 # Area of Aluminium plate
    A_k = 0.009 # Area of component
    eps_1 = 0.11 # Emmisitivity of Aluminium plate
    eps_k = 0.8 # Emisitivty of component
    sigma = 5.67e-8 # Stefan-Boltzman constant
    C_pcb = 396 # heat capacity of component
    m_pcb = 0.18 # mass of component 
    C_al = 921 # heat capacity of Aluminium plate
    m_al = 0.50 # mass of Aluminium plate
    d = 0.01 # thickness
    k = 239 # thermal conductivity of aluminium
    VF = 0.85 # view factor
    
    # get the individual variables - for readability
    yTemp_comp = y[0]
    yTemp_al = y[1]

    # controller    
    e_nl = setpoint - yTemp_comp
    
    u_p_nl = k_p * e_nl
    
    if (u_p_nl > 60):
        u_p_nl = 60
    elif (u_p_nl < 0):
        u_p_nl = 0
    
    P_nl = u_p_nl 
        
    TaK_nl = 273.15 + 22 + 2.6*38 # temperature from heat pad 
    
    # individual derivatives
    # Radiation ODE
    num = sigma*((yTemp_al)**4-yTemp_comp**4)
    det = ((1-eps_1)/(A_1*eps_1)+1/(A_1*VF)+(1-eps_k)/(A_k*eps_k))*(C_pcb*m_pcb)
    dyTemp_compdt = 2*num/det # two plates
    
    # Conduction ODE
    num = k*A_1*(TaK_nl-yTemp_al)
    det = d*(C_al*m_al)
    dyTemp_aldt = num/det
    
    return [ dyTemp_compdt, dyTemp_aldt ]

def TVC_linear(z, t):
    #
    # parameters
    A_1 = 0.02 # Area of Aluminium plate
    A_k = 0.009 # Area of component
    eps_1 = 0.11 # Emmisitivity of Aluminium plate
    eps_k = 0.8 # Emisitivty of component
    sigma = 5.67e-8 # Stefan-Boltzman constant
    C_pcb = 396 # heat capacity of component
    m_pcb = 0.18 # mass of component 
    C_al = 921 # heat capacity of Aluminium plate
    m_al = 0.50 # mass of Aluminium plate
    d = 0.01 # thickness
    k = 239 # thermal conductivity of aluminium
    VF = 0.85 # view factor
    
    # get the individual variables - for readability
    zTemp_comp = z[0]
    zTemp_al = z[1]
    
    # controller    
    e_l = setpoint - zTemp_comp
    u_p_l = k_p * e_l
    
    if (u_p_l > 60):
        u_p_l = 60
    elif (u_p_l < 0):
        u_p_l = 0
    
    P_l = u_p_l 
    
    TaK_l = 273.15 + 22 + (2.6*P_l) # temperature from heat pad add 1. order lowpass
    
    # individual derivatives
    # linearzied
    # Radiation ODE
    num = (4*sigma*(zTemp_al)**3)*(zTemp_al-393.15)-(4*sigma*(zTemp_comp)**3)*(zTemp_comp-393.15)
    det = ((1-eps_1)/(A_1*eps_1)+1/(A_1*VF)+(1-eps_k)/(A_k*eps_k))*(C_pcb*m_pcb)
    dzTemp_compdt = 2*(num/det) # two plates
    
    # Conduction ODE
    num = k*A_1*(TaK_l-393.15)-k*A_1*(zTemp_al-393.15)
    det = d*(C_al*m_al)
    dzTemp_aldt = num/det
    #
    return [ dzTemp_compdt, dzTemp_aldt ]

# define the initial condition
y0 = [ 22 + 273.15, 22 + 273.15 ]
z0 = [ 22 + 273.15, 22 + 273.15 ]

# define the time points where the solution is computed
n    = 50
tmax = 10000
t    = np.linspace(0, tmax, n)

# controller initialize
setpoint = 273 + 120
k_p = 4
e_nl = 0
e_l = 0

# solve the ODE
y = odeint(TVC_nonlinear, y0, t)
z = odeint(TVC_linear, z0, t)

# get the individual variables
yTemp_comp = y[:,0] - 273.15
yTemp_al = y[:,1] - 273.15
zTemp_comp = z[:,0] - 273.15
zTemp_al = z[:,1] - 273.15

# plot the time evolution
plt.subplot(1,2,1)
plt.plot(t, yTemp_comp, label='temp component nl', linewidth=1)
plt.plot(t, yTemp_al, label='temp aluminium nl', linewidth=1)
plt.grid()
plt.legend(loc = 'upper right')
plt.xlabel('time evolution')

plt.subplot(1,2,2)
plt.plot(t, zTemp_comp, label='temp component l', linewidth=1)
plt.plot(t, zTemp_al, label='temp aluminium l', linewidth=1)
plt.grid()
plt.legend(loc = 'upper right')
plt.xlabel('time evolution')