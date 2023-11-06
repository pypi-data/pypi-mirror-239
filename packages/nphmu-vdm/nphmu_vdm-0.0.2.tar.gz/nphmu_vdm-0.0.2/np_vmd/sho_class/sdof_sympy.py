#%% [markdown]
# # Mark
#%%

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy.printing.ccode import print_ccode

from sympy.abc import t as sp_t

#%%
class TimeFactory():
    def __init__(self, tmax, dt):
        self.tmax = tmax
        self.dt = dt
        self.nt = int(tmax/dt) # Number of steps
        self.ti = np.linspace(0., self.nt * dt, self.nt)
        
#%%
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



# %%

def solve_sdof_sympy2( m=1,c=0,k=1, x0=1, v0=1, ft=0):
    ''' solving using sp.Fuction

    '''
    from sympy.abc import t
    fx = sp.Function('fx') # disposable variable to contain data
    df2 = fx(t).diff(t,t)
    df = fx(t).diff(t)
    res = sp.dsolve(m*df2 + c*df +k*fx(t)- ft ,fx(t),ics={fx(0): x0, fx(t).diff(t).subs(t, 0): v0})
    resf = sp.lambdify(t,res.rhs)
    return resf


# %% as script
# https://mungoengineering.files.wordpress.com/2018/03/sympy_ode_example_12.pdf
def solve_sdof_sympy3( m=1,c=0,k=1, x0=1, v0=1, ft=0):
    ''' solving using sp.Fuction and sp.solve
    # mimics the solution in:
    # https://mungoengineering.files.wordpress.com/2018/03/sympy_ode_example_12.pdf

    '''
    from sympy.abc import t
    y = sp.symbols('y', cls=sp.Function)

    y1 = sp.dsolve(m*y(t).diff(t,t)+ c*y(t).diff(t)+ k*y(t)- ft)
    C = sp.solve([y1.rhs.subs(t,0)-x0, y1.rhs.diff(t).subs(t,0)-v0] )
    # print(C)
    y1=y1.subs(C)
    y1l=sp.lambdify(t,y1.rhs, 'numpy')
    return y1l

#%%
if __name__=="__main__":
    m = 1
    c = 0.1
    k = 1
    x0=-1
    v0=-1
    # External Excitaion
    ft=0                    # zero excitation

    ft= sp.sin(sp_t)    # sine  excitation
    tf= TimeFactory(10, dt=0.01)
#%%
    y1s = solve_sdof_sympy( m=m,c=c,k=k, x0=x0, v0 = v0, ft= ft)
    # # sin(t) example
    # y1s = solve_sdof_sympy( m=1,c=0.2,k=5, x0=1, v0 = 1, ft= sp.sin(sp.abc.t))
    # # piecewise function (step function simulation)
    # y1s = solve_sdof_sympy( m=1,c=0.2,k=5, x0=1, v0 = 1, ft=  sp.Piecewise((0, sp.abc.t< 5), (10, True)))
    plt.plot(tf.ti, y1s(tf.ti), label='v1')
    
#%%
    y2f = solve_sdof_sympy2(m=m,c=c,k=k, x0=x0, v0 = v0, ft= ft)
    plt.plot(tf.ti, y2f(tf.ti), '.', label='v2')
#%% use of solve_sdof_sympy3 
    y3 = solve_sdof_sympy3( m=m,c=c,k=k, x0=x0, v0 = v0, ft= ft)
    plt.plot(tf.ti, y3(tf.ti), label='v3')
    # %%
    plt.legend()
    plt.show()

