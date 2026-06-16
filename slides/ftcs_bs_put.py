import numpy as np
from scipy.stats import norm
from Gaussian import gaussian_cf, sin_coeff


S0= 3
sigma = 0.3
r = 0.03
T = 1
K = 4



# exact price - Black-Scholes formula
d1 = ( np.log(S0/K) + (r + 0.5*sigma**2) * T ) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)
bs_put = -1 * norm.cdf(-d1)*S0 + norm.cdf(-d2)*K*np.exp(-r*T)


# forward finite difference 
L = 10
Nx = 50
Nt = 50
h = L/Nx
k = T/Nt

T1  = np.diag([1]* (Nx-2), 1) - np.diag([1] * (Nx-2), -1)
T2  = -2 * np.diag([1] * (Nx-1)) + np.diag([1]* (Nx-2), 1) + np.diag([1] * (Nx-2), -1)

F = (1 - r*k) * np.diag([1] * (Nx-1))  + 0.5 *k * (sigma**2) /(h**2) * T2 +  k * (r-0.5*(sigma**2))/(2*h) * T1

mvec = np.linspace(start = -L/2 + h, stop = L/2-h, num=Nx-1)
U = np.zeros((Nx-1, Nt+1))
U[:, 0] = np.maximum(K - np.exp(mvec), 0)

for i in range(Nt):
    time2mat = i*k
    p = np.zeros(Nx-1)
    p[0] = ( 0.5 *k * (sigma**2) /(h**2) - k * (r-0.5*(sigma**2))/(2*h) ) * K* np.exp(-r*time2mat)
    U[:, i+1] = np.dot(F, U[:, i]) + p
    
ftcs_price = np.interp(np.log(S0), mvec, U[:, Nt])

print(f'forward finite difference price is {ftcs_price}')

