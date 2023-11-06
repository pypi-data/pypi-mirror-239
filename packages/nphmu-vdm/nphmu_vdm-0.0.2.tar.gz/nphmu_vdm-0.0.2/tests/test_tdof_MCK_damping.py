#%%
import numpy as np
from np_vmd.tdof_MCK import TDOF_modal
import pytest

def test_modal_inman_4_5_1():
    # examples 4.5.1.
    ''' With damping and forced
    '''
    m1,m2  = 9,1
    k1=24
    k2=3
    c1 = 2.4
    c2 = 0.3 
    F0=3
    w0=2
    tmck = TDOF_modal(np.array([[m1,0],[0,m2]]), K=np.array([[k1+k2,-k2],[-k2,k2]]), C= np.array([[c1+c2,-c2],[-c2,c2]]))
    np.testing.assert_equal(tmck.Ktilde, np.array([[3,-1],[-1,3]]))
    np.testing.assert_almost_equal(tmck.Ctilde, np.array([[0.3,-.1],[-.1,.3]]), 4)
    #eigenvalues
    np.testing.assert_almost_equal(tmck.ls, np.array([4,2]),4)
    #eigenfrequencies
    np.testing.assert_almost_equal(tmck.wns, np.array([2, 1.41421]),4) 
    # calculate decoupled cs
    np.testing.assert_almost_equal(tmck._calc_C_princ_coord(), np.array([[0.4,0],[0,0.2]]), 4)
    # calculate decoupled damping factors
    np.testing.assert_almost_equal(np.diag(tmck._calc_C_princ_coord())/(2*tmck.wns), np.array([0.1,0.0707]), 4)

    tmck.update_damping(  np.array([0.1, 0.05]))
    np.testing.assert_almost_equal(tmck.zs, np.array([0.1,0.05]), 4)
    np.testing.assert_almost_equal(tmck.wds, np.array([1.9900,1.4124]), 3)

    #eigenvectors
    np.testing.assert_almost_equal(tmck.vs, np.array([[0.70710678 ,0.70710678 ],[-0.70710678 , 0.70710678 ]]),4)
    #eigenmodes
    np.testing.assert_almost_equal(tmck.us, np.array([[1,1],[-0.333333, 0.3333333]]),4)
    np.testing.assert_almost_equal(tmck.Lambda_mat, np.array([[4, 0], [0, 2]]),4)
    np.testing.assert_almost_equal(tmck.Lambda_mat, np.diag([4,  2]),4)
    



def test_modal_inman_4_5_1_calc_xs():
    '''This is for the calculation of the xs values

    This continues from where the previous test left of
    '''
    m1,m2  = 9,1
    k1=24
    k2=3
    c1 = 0
    c2 = 0 
    F0=3
    w0=2
    tmck = TDOF_modal(np.array([[m1,0],[0,m2]]), K=np.array([[k1+k2,-k2],[-k2,k2]]), C= np.array([[c1+c2,-c2],[-c2,c2]]))

    tmck.update_damping(  np.array([0.1, 0.05]))
    tmck.set_iv(x0s = np.array([[1, 0]]).T, dx0s = np.array([[0,0]]).T)
    np.testing.assert_almost_equal(tmck.r0s, 3/np.sqrt(2)*np.array([[1,1]]).T,4)

    # The following x_repsonse does not work. Might be due to rounding error. 
    ts = np.linspace(0, 1,10)
    rs1 = 2.1320*np.exp(-0.2*ts)*np.sin(1.9900*ts+1.47) # r2p in the book
    rs2 = 2.1240*np.exp(-0.0706*ts)*np.sin(1.4124*ts+1.52) # r1p in the book
    # # homogeneous (transient) solutions
    xhs1 = 0.5006*np.exp(-0.0706*ts)*np.sin(1.4124*ts+1.52) + \
            0.5025*np.exp(-0.2*ts)*np.sin(1.9900*ts+1.47)
    xhs2 =  1.5019*np.exp(-0.0706*ts)*np.sin(1.4124*ts+1.52) - \
            1.5076*np.exp(-0.2*ts)*np.sin(1.9900*ts+1.47)

    xs = tmck.calc_x_hom_response(ts)
    np.testing.assert_almost_equal(xs[0,:],xhs1, 3)
    np.testing.assert_almost_equal(xs[1,:],xhs2, 3)




def test_modal_inman_4_5_1_calc_xs_alternative():
    '''This test the validity of the calculation for TDOF_modal.calc_C_from_Z()

    This continues from where the previous test left of
    '''
    m1,m2  = 9,1
    k1=24
    k2=3
    F0=3
    w0=2
    tmck = TDOF_modal(np.array([[m1,0],[0,m2]]), K=np.array([[k1+k2,-k2],[-k2,k2]]), C= np.zeros((2,2)))
    tmck.update_damping(  np.array([0.1, 0.05]))
    tmckn = tmck.calc_C_from_Z(tmck.zs)
    np.testing.assert_almost_equal(tmckn.zs, np.array([0.1, 0.05]),4)
    

    # tmck.update_damping(  np.array([0.1, 0.05]))
    tmckn.set_iv(x0s = np.array([[1, 0]]).T, dx0s = np.array([[0,0]]).T)
    np.testing.assert_almost_equal(tmckn.r0s, 3/np.sqrt(2)*np.array([[1,1]]).T,4)
    # The following x_repsonse does not work. Might be due to rounding error. 
    ts = np.linspace(0, 1,10)
    rs1 = 2.1320*np.exp(-0.2*ts)*np.sin(1.9900*ts+1.47) # r2p in the book
    rs2 = 2.1240*np.exp(-0.0706*ts)*np.sin(1.4124*ts+1.52) # r1p in the book
    # # homogeneous (transient) solutions
    xhs1 = 0.5006*np.exp(-0.0706*ts)*np.sin(1.4124*ts+1.52) + \
            0.5025*np.exp(-0.2*ts)*np.sin(1.9900*ts+1.47)
    xhs2 =  1.5019*np.exp(-0.0706*ts)*np.sin(1.4124*ts+1.52) - \
            1.5076*np.exp(-0.2*ts)*np.sin(1.9900*ts+1.47)

    xs = tmckn.calc_x_hom_response(ts)
    np.testing.assert_almost_equal(xs[0,:],xhs1, 3)
    np.testing.assert_almost_equal(xs[1,:],xhs2, 3)

def test_calc_C_from_Z():
    m1,m2  = 9,1
    k1=24
    k2=3
    c1 = 2.4
    c2 = 0.3
    C = np.array([[c1+c2,-c2],[-c2,c2]])
    tmck = TDOF_modal(np.array([[m1,0],[0,m2]]), K=np.array([[k1+k2,-k2],[-k2,k2]]), C= C)
    
    np.testing.assert_almost_equal(C,tmck.calc_C_from_Z(tmck.zs).mC, 3)
    np.testing.assert_almost_equal(C,tmck.calc_C_from_Z(np.diag(tmck.zs)).mC, 3)

    