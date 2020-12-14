# -*- coding: utf-8 -*-
# Finite Element Simulation of the KPZ model using the Moveing Mesh method, v 0.9                                                *
# Date: 03.09.1399  
#                                                   
# Copyleft 2020 H. Derakhshan All left reserved!
# The real-time graphic function "xxxx" was taken from M. D. Niry                                                     
#                                                                              
# Licensed under The GNU General Public License v3.0                
# --------------------------------------------------------------------------------

# General Modules
import numpy as np               # Numeric Python
import matplotlib.pyplot as plt  # Plot package
# Constants
L  = 64                          # Size of the lattice
g  = 1/8                         # Coupling constant g
dx = 1/4                         # primary  Δx 
dt = 1/1024                      # Δt

# Header
print("Finite Element Simulation of the KPZ model using the Moveing Mesh method, v 0.9 ")
print("Date: 03.09.1399")
print("Parameters:")
print("L  = %4d  \t g  = %.4f" %(L, g))
print("Δx = %.4f \t Δt = %.4f" %(dx, dt), "\n")


# KPZ class
class KPZClass:
    def __init__(self):
        self.t     = 0
        self.x     = np.linspace(0, L*dx, L) # Array of discrete points
        self.u     = np.zeros(L)             # Array of speed of mesh points
        self.__u   = np.empty(L)             # Temporary array of last time step speed of mesh points
        self.h     = np.zeros(L)             # Array of heights
        self.__xi  = np.empty(L)             # Array of the ξ noise
        self.__eta = np.empty(L)             # Array of the ƞ noise

    def __noise(self, x, xi, eta):
        import math                          # For math functions
        N    = len(x)                        # total descret pionts of the lattice
        beta = 0 * 0.5                       #Beta 0 White nose, 1 Purple noise, 2 Brownian motion
        Phi  = np.random.rand(int(N/2))*2*math.pi #Array of the φ_n uniformly disriuted random number
        for n in range(N):
            k    = 1
            xi_n  = 0                                  #ξ_n noise
            eta_n = 0                                  #ƞ_n noise derivative of ξ_n            
            while k <= (N/2):
                w     = (2 * math.pi * x[n] * k / N) + Phi[k-1]
                xi_n  += k**(-beta) * math.cos(w)
                eta_n += k**(1-beta) * math.sin(w) 
                k    += 1
            xi[n]     = xi_n
            eta[n]    = (4 * math.pi / N) * eta_n    
            
    
    def __speed(self, u0, u1, x, eta):
        # The interior part of the lattice
        uf       = u0[2:]             # forward u  
        ub       = u0[:-2]            # backward u
        uc       = u0[1:-1]           # center u
        xf       = x[2:]              # forward x  
        xb       = x[:-2]             # backward x
        xc       = x[1:-1]            # center x
        u1[1:-1] = uc + \
            (2 * g * dt) * ((uf - uc) / ((xf - xc) * (xf - xb))) + \
            (2 * g * dt) * ((ub - uc) / ((xc - xb) * (xf - xb))) + \
            (dt) * eta[1:-1]
        # The periodic boundary condition applied on edges of the lattice
        #((L+1)*dx)+ is the correction of bundry condition 
        u1[0]    = u0[0] + \
            (2 * g * dt) * ((u0[1] - u0[0]) / ((x[1] - x[0]) * (((L+1)*dx)+x[1] - x[-1]))) + \
            (2 * g * dt) * ((u0[-1] - u0[0]) / ((((L+1)*dx)+x[0] - x[-1]) * (((L+1)*dx)+x[1] - x[-1]))) + \
            (dt) * eta[0]
        u1[-1]    = u0[-1] + \
            (2 * g * dt) * ((u0[0] - u0[-1]) / ((((L+1)*dx)+x[0] - x[-1]) * (((L+1)*dx)+x[0] - x[-2]))) + \
            (2 * g * dt) * ((u0[-2] - u0[-1]) / ((x[-1] - x[-2]) * (((L+1)*dx)+x[0] - x[-2]))) + \
            (dt) * eta[-1]

    def __mesh(self, x, u):
        x = x + (u * dt) #x is the array of x's

    # The following private constatnts are used in the __next()
    __c1 = g*dt/2
    __c2 = dt/4
    __c3 = dt
    def __next(self, h, u, x, xi):          # h0(t) ---> h1(t + Δt)
        # The interior part of the lattice
        hc       = h[1:-1]            # center h
        xf       = x[2:]              # forward x  
        xb       = x[:-2]             # backward x
        xc       = x[1:-1]            # center x
        uf       = u[2:]              # forward u  
        ub       = u[:-2]             # backward u
        uc       = u[1:-1]            # center u
        h[1:-1] = hc - \
                   self.__c1 * (uf - uc ) * (xc - xb) / ((xf - xc)*(xf - xb)) + \
                   self.__c1 * (ub - uc ) * (xf - xc) / ((xc - xb)*(xf - xb)) + \
                   self.__c2 * uc**2 + \
                   self.__c3 * xi[1:-1]
        # The periodic boundary condition applied on edges of the lattice
        h[0]    = h[0] - \
                   self.__c1 * (u[1] - u[0] ) * (((L+1)*dx)+x[0] - x[-1]) / ((x[1] - x[0])*(((L+1)*dx)+x[1] - x[-1])) + \
                   self.__c1 * (u[-1] - u[0] ) * (x[1] - x[0]) / ((((L+1)*dx)+x[0] - x[-1])*(((L+1)*dx)+x[1] - x[-1])) + \
                   self.__c2 * u[0]**2 + \
                   self.__c3 * xi[0]
        h[-1]   = h[-1] - \
                   self.__c1 * (u[0] - u[-1] ) * (x[-1] - x[-2]) / ((((L+1)*dx)+x[0] - x[-1])*(((L+1)*dx)+x[0] - x[-2])) + \
                   self.__c1 * (u[-2] - u[-1] ) * (((L+1)*dx)+x[0] - x[-1]) / ((x[-1] - x[-2])*(((L+1)*dx)+x[0] - x[-2])) + \
                   self.__c2 * u[-1]**2 + \
                   self.__c3 * xi[-1]
        self.t  += dt

    def next(self, n=1):               # Next n KPZ steps (t ---> t+2nΔt)
        for x in range(n):
            print(x)
            self.__noise(self.x, self.__xi, self.__eta)
            self.__next(self.h, self.u, self.x, self.__xi)
            self.__speed(self.u, self.__u, self.x, self.__eta)
            self.__mesh(self.x, self.__u)
            self.__noise(self.x, self.__xi, self.__eta)
            self.__next(self.h, self.__u, self.x, self.__xi)
            self.__speed(self.__u, self.u, self.x, self.__eta)
            self.__mesh(self.x, self.u)

# Append a point (x, y) to the curve in the plot
def AppendPoint(curve, x, y):
    curve.set_xdata(np.append(curve.get_xdata(), [x]))
    curve.set_ydata(np.append(curve.get_ydata(), [y]))
    curve.axes.set_xlim([0, x])
    curve.axes.set_ylim([0, y])


# Main part of the code
import time                            # For calculating the executing time
start_time = time.process_time()       # keeps the time when the program was begined

C   = KPZClass()                       # KPZ class instance

plt.ion()
fig = plt.figure()
fig.canvas.set_window_title('Real-Time KPZ Simulation')

ax1 = fig.add_subplot(1, 2, 1)         # Left figure - h(x,t)
ax2 = fig.add_subplot(2, 2, 2)         # Top right figure - ❬h❭(t)
ax3 = fig.add_subplot(2, 2, 4)         # Bottom right - figure w(t)
fig.tight_layout(pad=2.0)
plt.show()

# plot label/title
ax1.set_xlabel('x')
ax1.set_ylabel('h(x, t)')
ax2.set_xlabel('t')
ax2.set_ylabel('❬h❭(t)')
ax3.set_xlabel('t')
ax3.set_ylabel('w(t)')
ax3.set_xscale('log')
ax3.set_yscale('log')

# create a variable for the line so we can later update it
line1, = ax1.plot(C.x, C.h)            # plot() returns multiple variables (line, ...)
line2, = ax2.plot([0], [0])


# main loop of code
k = 0
while C.t < 5:
    # Height profile
    k += 1
    if k % 100 == 0:
        line1, = ax1.plot(C.x, C.h)        
    update_step = 50       #plots will be updated after 50 steps
    C.next(update_step)
    line1.set_ydata(C.h)
    if np.min(C.h) <= line1.axes.get_ylim()[0] or np.max(C.h) >= line1.axes.get_ylim()[1]:
        line1.axes.set_ylim([min([0, np.min(C.h)-np.std(C.h)]),np.max(C.h)+np.std(C.h)])
    
    # ❬h❭(t)
    AppendPoint(line2, C.t, np.mean(C.h))
    
    # w(t)
    ax3.scatter([C.t], [np.std(C.h)], s=2, c="r")
    
    plt.pause(0.1)
    
# executing_time = 1000 * (time.process_time() - start_time)
step = update_step * k
print("\ntotal step %.1d" % step)
# print("\nfinishd in %.1f ms!" % executing_time)
