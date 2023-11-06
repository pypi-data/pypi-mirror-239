#%% [markdown]
# this is a calculation for tdof systems with matrices M, C, K 

import numpy as np

class TDOF_modal():
    
    def __init__(self, M, K, C=None):
        self.mM = M 
        self.mK = K 
        dims = self.mM.shape
        if len(set(dims))==1:
            self._n = self.mM.shape[0]
        else:
            raise ValueError('Size of matrix array not ok')
        self.mC = np.zeros((self._n,self._n)) if C is None else C 
        # set up excitation matrices
        # mB* mF   
        # mB is the generic case where a force may be shared by moe than one dof
        self.mB = np.zeros((self._n,self._n)) 
        self.mF = np.zeros((self._n,1)) 
        self.__perform_initial_setup()

    def __perform_initial_setup(self):
        self.M_1ov2 = np.linalg.cholesky(self.mM)
        self.Linv = np.linalg.inv(self.M_1ov2)
        

        self.Ktilde = self.Linv.dot(self.mK).dot(self.Linv)
        self.Ctilde = self.Linv.dot(self.mC).dot(self.Linv)
        self.ls, self.vs = np.linalg.eig(self.Ktilde)
        self.Pmat = self.vs
        self.wns = np.sqrt(self.ls)
        self.calc_eigenmodes()
        self.Lambda_mat = self.vs.T.dot(self.Ktilde).dot(self.vs)
        self.Smat  = self.Linv.dot(self.Pmat)

        # damping
        self.update_damping()

    # [staticmethod]
    # def gen_modal_eq(wn, x0, dx0):
    #     ''' this is the undamped homogeneous solution

    #     This became obsolete with gen_modal_d_eq
    #     '''
    #     A = np.sqrt(x0**2+  (dx0/wn)**2)
    #     phi = np.arctan2(wn*x0, dx0)
    #     r_t = lambda t: A *np.sin(wn*t + phi)
    #     return r_t

    [staticmethod]
    def gen_modal_d_eq(wn, z ,x0, dx0):
        ''' generic solution for the homogeneous problem for an underdamped vibration of 1 sdof

        This is used in the principal coordinates to calculate the response in principal coordinates
        '''
        wd = wn*np.sqrt(1-z**2)
        A = np.sqrt(x0**2+  ((dx0+z*wn*x0)/wd)**2)
        theta = np.arctan2(wd*x0, dx0 + z*wn*x0)
        r_t = lambda t: A *np.exp(-z*wn*t)*np.sin(wd*t + theta)
        return r_t

    def set_excitation(self, B=None, F=None):
        ''' This function sets the exciation parameters. 
        '''
        self.mB = np.eye(self._n)  if B is None else B
        self.mF = np.zeros((self._n,1))  if F is None else F
        self.B_tilde = self.Pmat.T.dot(self.Linv).dot(self.mB)
        return self.B_tilde

    def update_damping(self, zs= None):
        ''' sets zs in their **decoupled form** and recalculates the wds

        zs defaults to none which calculates based on the C matrix
        '''
        if zs is None:
            self.zs = np.diag(self._calc_C_princ_coord())/(2*self.wns)
        else:
            self.zs = zs
        self.wds = self.wns *np.sqrt(1-self.zs**2)
        
    def set_iv(self, x0s:None, dx0s=None):
        ''' This functions sets the parameters for 

        # TODO: what happens when the excitation have an offset.?  
        # In that case in the SDOF, the initial condition should be set to - F/k
        # consider what happens in the principal coordinates. 
        '''
        self.x0s=x0s        
        self.dx0s=dx0s
        self.r0s = np.linalg.inv(self.Smat).dot(self.x0s)
        self.dr0s = np.linalg.inv(self.Smat).dot(self.dx0s)
        
    def _set_rfs_hom(self):
        ''' Create response functions for the homogeneous equation
        of the MDOF
        '''
        self.rfs_h = []
        for i in range(self._n):
            x0i = self.r0s[i]
            dx0i = self.dr0s[i]
            wn = self.wns[i]
            self.rfs_h.append(
                TDOF_modal.gen_modal_d_eq(wn, z=self.zs[i],x0=x0i, dx0=dx0i)
            )

    def _calc_C_princ_coord(self):
        ''' calculate matrix $P^t \tilde{C} P$

        This is damping in the principal coordinates system

        it calculates the damping factor in the decoupled generalised coordinates. 
        '''
        return self.Pmat.T.dot(self.Ctilde).dot(self.Pmat)

    def calc_x_hom_response(self, ts):
        ''' returns the numerical values for the homogenous part of the response (transient)
        uses rfs in order to create the numerical 
        response results 
        '''

        self._set_rfs_hom()
        
        ris = []
        for i in range(self._n):
            ris.append(self.rfs_h[i](ts))
        xs = self.Smat.dot(np.array(ris))
        return xs

    def calc_x_ss_response(self, ts):
        ''' Calculates the steady state response of the system (partial solution)

        # TODO: not complete need to see how to handle convolution integral
        This is the function that creates the 
        '''


        
        # ris = []

        # for i in range(self._n):
        #     ris.append(self.rfs_ss[i](ts))
        # xs = self.Smat.dot(np.array(ris))
        # return xs
        pass

    def calc_C_from_Z(self, Z=None):
        ''' Calculates C matrix from the Z matrix of the decoupled equations

        TODO: Add test
        '''
        if Z.ndim==1:
            zn = np.diag(Z*2*self.wns)
        elif Z.ndim==2:
            zn = np.diag(np.diag(Z)*2*self.wns)
        else:
            raise Exception
        C = self.M_1ov2.dot(self.Pmat).dot(zn ).dot(self.Pmat.T).dot(self.M_1ov2)
        newsys = TDOF_modal(M=self.mM, K=self.mK , C= C)
        return newsys

    def calc_eigenmodes(self):
        ''' creates eigenmodes in columns 
        '''
        self.us_nn = np.array(self.M_1ov2.dot(self.vs))  ## not normalised
        us_a = []
        for ui in self.us_nn.T:
            # us_a.append( ui/np.sqrt(np.sum(ui*ui.T)))
            us_a.append( ui/ui[0])
        self.us = np.array(us_a).T
        return self.us_nn
    
    def print_eigvectors(self):
        n = len(self.wns)
        print('============ eigen values and eigenvectors =================')
        for i in range(n):
            print ("lambda_{}= {:10.3f}, \t eigen vector:{}".format(i+1, self.ls[i], self.vs[:,i].T))
    def print_eigenmodes(self):
        n = len(self.wns)
        print('\n============ eigen Frequencies and eigenmodes =================')
        for i in range(n):
            print ("w_{}= {:10.3f}, \t eigen vector:{}".format(i+1, self.wns[i], self.us[:,i].T))

    def print_results(self):
        print("Khat : \n {}".format(self.Ktilde))
        print("Eigenvalues (lambda) :  {}".format(self.ls))
        print("Eigenfrequencies (omega) :  {}".format(self.wns))
        self.print_eigvectors()
        # print("EigenVectors (v) : \n {}".format(self.vs))
        self.print_eigenmodes()
        # print("EigenModes (u) : \n {}".format(self.us))
        print("\n","*"*50,"\nSpectral matrix $Lambda$: \n {}".format(self.Lambda_mat))


if __name__=="__main__":
    pass
    import matplotlib.pyplot as plt
    # examples 4.1.1. to 4.2.6
    m1,m2  = 9,1
    k1=24
    k2=3
    tmck = TDOF_modal(np.array([[m1,0],[0,m2]]), K=np.array([[k1+k2,-k2],[-k2,k2]]))
    tmck.print_results()
    tmck.set_iv(x0s = np.array([[1,0]]).T, dx0s = np.array([[0,0]]).T)
    print(tmck.Smat)
    print(tmck.r0s)
    print(tmck.dr0s)
    # ts = np.linspace(0, 5, 1000)
    # plt.plot(tmck.calc_x_response(ts).T , label ='tmck')
    # plt.plot(0.5*(np.cos(np.sqrt(2)*ts) + np.cos(2*ts)) , '.', label ='r1')
    # plt.plot(1.5*(np.cos(np.sqrt(2)*ts) - np.cos(2*ts)) , '.', label ='f2')
    # plt.legend()
# %%    
    # example Inman  4.2.6
    k1=10
    k3=10
    k2=2
    tmck = TDOF_modal(np.array([[1,0],[0,4]]), K=np.array([[k1+k2,-k2],[-k2,k2+k3]]))
    tmck.print_results()    
    # tmck.cholesky()
    # tmck.calc_Khat()
    # tmck.calc_eigenvalues()
    # tmck.calc_eigenfrequencies()
    # tmck.calc_eigenvectors()
    # tmck.calc_eigenmodes()
    # tmck.calc_spectralMatrix()
# %%
    # examples 4.1.1. to 4.2.6
    m1,m2  = 9,1
    k1=24
    k2=3
    tmck = TDOF_modal(np.array([[m1,0],[0,m2]]), K=np.array([[k1+k2,-k2],[-k2,k2]]))
    tmck.print_results()
# %%
    tmck.print_eigvectors()
    tmck.print_eigenmodes()
# %%

# %%
    # examples 4.3.2
    k1=10
    k3=10
    k2=2
    tmck = TDOF_modal(np.array([[1,0],[0,4]]), K=np.array([[k1+k2,-k2],[-k2,k2+k3]]))
    tmck.print_results()
    tmck.set_iv(x0s = np.array([[1,1]]).T, dx0s = np.array([[0,0]]).T)
    print(tmck.Smat)
    print(tmck.r0s)
    print(tmck.dr0s)
    ts = np.linspace(0, 5, 1000)
    plt.plot(tmck.calc_x_hom_response(ts).T , label ='tmck')
    plt.legend()
# %%
    # this is an example for an  MDOF (n=3). The TDOF file works just fine. 
    m1,m2,m3  = 4,4,4
    k1,k2,k3 = 4,4,4

    tmck = TDOF_modal(np.array([[m1,0,0],[0,m2,0],[0,0,m3]]), K=np.array([[k1+k2,-k2,0],[-k2,k2+k3, -k3],[0,-k3,k3]]))
    tmck.set_iv(x0s = np.array([[1,0, 0]]).T, dx0s = np.array([[0,0,0]]).T)
    ts = np.linspace(0, 5, 1000)
    plt.plot(tmck.calc_x_hom_response(ts).T , label ='tmck')
    plt.legend()
    plt.show()
# %%
    tmck.print_results()
# %%
