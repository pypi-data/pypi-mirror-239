# this py file showcases the SHOClass
# it creates a comparison between the numerical solution and the analytic solution (Free_generic)

from np_vmd.sho_class.SHO_sdof_class import SHO_sdof_solver
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

#%% simple animation of a mass. 

plt.rcParams["font.size"] = "15"


def Free_Generic(t,  zeta=1, wn=1, x0 =1, xdot0=0):
    if zeta<1:
        wd = wn*np.sqrt(1-zeta**2)
        A = np.sqrt(x0**2 + ((xdot0+zeta*wd*x0)/(wd))**2)
        phid= np.arctan2(x0*wd,(xdot0+zeta*wd*x0))
        x =  A * np.exp(-zeta*wn*t)*np.sin(wd*t+phid)
    if zeta==1:
        x =   np.exp(-wn*t) * (x0 + (xdot0+ wn*x0)*t )
    if zeta>1:
        z2m1 = np.sqrt(zeta**2-1)
        x= np.exp(-zeta*wn*t)/(2*z2m1)*((xdot0/wn + x0*(zeta+z2m1))*np.exp(z2m1*wn*t) -(xdot0/wn +x0*(zeta-z2m1))*np.exp(-z2m1*wn*t))
    return x


def solve_sdof_sympy(m:float=1,c:float=0,k:float=1, x0:float=1, v0:float=1, ft=0):
    """ this solves the SDOF Harmonic Oscillator 

    uses dsolve with the ics argument

    Args:
        m (int, optional): [description]. Defaults to 1.
        c (int, optional): [description]. Defaults to 0.
        k (int, optional): [description]. Defaults to 1.
        x0 (int, optional): [description]. Defaults to 1.
        v0 (int, optional): [description]. Defaults to 1.
        ft (int, optional): [description]. Defaults to 0.

    Returns:
        [lambdified sp function]: [description]
    """    
    from sympy.abc import t
    y = sp.symbols('y', cls=sp.Function)
    y1 = sp.dsolve(m*y(t).diff(t,t)+ c*y(t).diff(t)+ k*y(t) - ft, ics={y(0): x0, y(t).diff(t).subs(t, 0): v0})

    # print(y1)
    y1=sp.lambdify(t,y1.rhs, 'numpy')
    return y1



#%%
if __name__ == "__main__":
    # system definition
    m1= 1
    c1 = 2
    k = 1

    sho = SHO_sdof_solver(m=m1, c=c1, k=k)
#%%
    # set time
    niter = 1001
    t = np.linspace(0,10,niter)

#%%
    # Initial Conditions
    x1_0 = 0
    v1_0 = -1
    y0 =[x1_0, v1_0]

    # Force excitation
    F2 = np.ones(len(t))*0.0
    F2[:] = 0
    sho1_res = sho.perform_simulation(t, y0=y0, Fs=F2, desc="Full")
    # sho1_res.plot_results()
#%% sympy analytical example
    ft = 0
    y1s = solve_sdof_sympy(m=m1,c=c1,k=k, x0=x1_0, v0=v1_0, ft=0)
    


#%%    #   
    wn = np.sqrt(k/m1)
    zeta = c1/(2*m1*wn)

    plt.figure()
    plt.plot(t,sho1_res.xs,'.-', label= 'numer.')
    plt.plot(t, Free_Generic(t,  zeta=zeta, wn=wn, x0 =x1_0, xdot0=v1_0), label= 'Analytic')
    plt.plot(t, y1s(t), label= 'sympy')
    plt.legend()

    plt.show()
# %%
