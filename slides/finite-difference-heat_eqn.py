

import numpy as np
import scipy.linalg as sc
import matplotlib.pyplot as plt
 
def ftcs(x, t, g, Nx, Nt, nu, a, b):
    
    u_1 = np.zeros(Nx+1) # u at the previous time level
    u   = np.zeros((Nt+1,Nx+1))
    
    u[:,0] = np.copy(a) # u(0,t) = a(t)
    u[:,Nx] = np.copy(b) # u(L,t) = b(t)
    
    
    for i in range(1,Nx):
        u_1[i] = g(x[i])
    
    u[0, :] = np.copy(u_1)
    for n in range(1,Nt+1):
        assert (np.abs(u_1[0]-u[n,0])<1.e-10) & (np.abs(u_1[-1]-u[n,-1])<1.e-10), "BCs not consistent"
       
        # Compute u at inner mesh points
        for i in range(1, Nx):
            u[n,i] = u_1[i] + nu*(u_1[i-1] - 2*u_1[i] + u_1[i+1])
    
        # Update u_1 before next step
        u_1[:]= u[n,:]
        
    return u

def btcs(x, t, g, Nx, Nt, nu, a, b):
    
    u_1 = np.zeros(Nx+1) # u at the previous time level
    u   = np.zeros((Nt+1,Nx+1))
    
    B = np.zeros((Nx+1, Nx+1))
    q = np.zeros(Nx+1)
    lhs = np.zeros(Nx+1)
    
    
    # construct stencil
    for i in range(1, Nx):
        B[i,i-1] = -nu
        B[i,i+1] = -nu
        B[i,i] = 1 + 2*nu
    B[0,0] = B[Nx,Nx] = 1
    
    for i in range(Nx+1):
        u_1[i] = g(x[i])
        
    u[0, :] = np.copy(u_1)
    
    for n in range(1, Nt+1):
        q[0] = nu*a[n]
        q[-1] = nu*b[n]
        
        for i in range(1, Nx):
            lhs[i] = u_1[i] + q[i]
        
        u[n,:] = sc.solve(B,lhs)
        
        u_1[:] = u[n, :]
    
    return u

def crank_nicholson(x, t, g, Nx, Nt, nu, a, b):
    u_1 = np.zeros(Nx+1) # u at the previous time level
    u   = np.zeros((Nt+1,Nx+1))
    
    B_hat = np.zeros((Nx-1, Nx-1))
    F_hat = np.zeros((Nx-1, Nx-1))
    r = np.zeros(Nx-1)
    
    # construct stencil
    for i in range(1,len(r)-1):
        B_hat[i,i-1] = -0.5*nu
        B_hat[i,i] = 1+nu
        B_hat[i,i+1] = -0.5*nu
        F_hat[i,i-1] = 0.5*nu
        F_hat[i,i] = 1-nu
        F_hat[i,i+1] = 0.5*nu
    
    B_hat[0,0] = B_hat[Nx-2,Nx-2] = 1+nu
    B_hat[0,1] = B_hat[Nx-2, Nx-3] = -0.5*nu
    F_hat[0,0] =F_hat[Nx-2, Nx-2] = 1-nu
    F_hat[0,1] = F_hat[Nx-2, Nx-3] = 0.5*nu
    
    for i in range(Nx+1):
        u_1[i] = g(x[i])
        
    u[0, :] = np.copy(u_1)
    
    for n in range(1,Nt+1):
        r[0] = 0.5*nu*(a[n-1]+a[n])
        r[Nx-2] = 0.5*nu*(b[n-1]+b[n])
        
        u[n,1:Nx] = sc.solve(B_hat, F_hat.dot(u_1[1:Nx]))
        
        u_1[:] = u[n, :]
    
    return u   
    
#%%
if __name__== "__main__":
    T = 3 # time 
    L = np.pi # length 
    Nx = 14
    Nt = 94
    kappa = 1
    g = lambda x: np.sin(x) # u(x,0) = g(x)
    a = [x*0 for x in np.arange(Nt+1)] # u(0,t) = a(t)
    b = [x*0 for x in np.arange(Nt+1)] # u(L,t) = b(t)
    
    x = np.linspace(0, L, Nx+1)  # space discretization
    t = np.linspace(0, T, Nt+1)  # time discretization
    
    h = x[1] - x[0]
    k = t[1] - t[0]
    nu = kappa*k/h**2
    
    # choose a method
    #u = ftcs(x, t, g, Nx, Nt, nu, a, b)
    #u = btcs(x, t, g, Nx, Nt, nu, a, b)
    u = crank_nicholson(x, t, g, Nx, Nt, nu, a, b)
    X, T = np.meshgrid(x,t)
    R = np.exp(-T)*np.sin(X)
    err_norm = np.max(np.abs(R-u))
    
    
    # plots
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(X,T,u, color='b', label='numerical')
    
    
    ax.plot_surface(X,T,R, color='r', label='analytical')
    ax.set_title(r'$\nu$' + f' ={nu:2f}' + '   inf_norm_error=' + f'{err_norm: 2f}')
    ax.set_xlabel('L')
    ax.set_ylabel('t')
    ax.set_zlabel('u')
    plt.show()