  
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import numpy as np
import sys

# the maximum time of virus in days
maxtime = 365
# people in Idaho
N = 1754000 # Population of Idaho according to U.S. Census
def kinetics(k1, k2, h_0, i_0, r_0):   #Units of k1 
    def abc(t, y):
        ''' System of differential equations: y(t) = [H(t),I(t),R(t)]
            returns:
                A list containing [dH/dt, dI/dt, dR/dt]
        '''
        H,I,R = y
	#H = the number of healthy people who have never contracted the virus.
        #I = the number of people who have become infected due to the virus.
	#R = the number of people who have recoverd from the virus.
	
	return [-k1*H*I/(H+I+R), k1*H*I/(H+I+R)-k2*I, k2*I] #The equation for Dead will just be (k3*I) where k3 is the death rate, we will have to add (-k3*I) to the infected part of the graph.
    return solve_ivp(abc, [0, maxtime], [h_0,i_0,r_0], t_eval=np.arange(0, maxtime, 1),method='Radau')
# Original k1 is 0.1
filename = sys.argv[1]
population_infected = np.loadtxt(filename, skiprows = 3, delimiter = ',', usecols = (2))
time = np.loadtxt(filename, skiprows = 3, delimiter = ',', usecols =(0))

time = np.loadtxt(filename, skiprows = 8, delimiter = ',', usecols = (0))
infected = np.loadtxt(filename, skiprows = 8, delimiter = ',', usecols = (2))
dead = np.loadtxt(filename, skiprows = 8, delimiter = ',', usecols = (4))
recovered = np.loadtxt(filename, skiprows = 8,  delimiter = ',', usecols = (6))
solution = kinetics(0.5,0.02, N-1,1,0) #ONE infected person on day0

plt.plot(time, dead, label='Real Dead', color = 'k')
plt.plot(time,infected, label='Real Infections')
plt.plot(time,recovered, label='Real Recovered', color = 'm')
plt.plot(solution.t,solution.y[0],label='Model Uninfected')
plt.plot(solution.t,solution.y[1],label='Model Infected',linestyle='dashed')
plt.plot(solution.t,solution.y[2],label='Model Recovered',linestyle='dotted')

plt.xlabel('Time [days]')
plt.ylabel('Population infected')
plt.grid() 
plt.legend(loc='best')
plt.show()
