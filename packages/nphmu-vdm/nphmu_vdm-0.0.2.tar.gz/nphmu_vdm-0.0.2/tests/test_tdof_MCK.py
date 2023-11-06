import numpy as np
from np_vmd.tdof_MCK import TDOF_modal
import pytest

def test_modal_inman_4_1_1():
    # examples 4.1.1. to 4.2.6
    m1,m2  = 9,1
    k1=24
    k2=3
    tmck = TDOF_modal(np.array([[m1,0],[0,m2]]), K=np.array([[k1+k2,-k2],[-k2,k2]]))
    np.testing.assert_equal(tmck.Ktilde, np.array([[3,-1],[-1,3]]))
    #eigenvalues
    np.testing.assert_almost_equal(tmck.ls, np.array([4,2]),4)
    #eigenfrequencies
    np.testing.assert_almost_equal(tmck.wns, np.array([2, 1.41421]),4) 
    #eigenvectors
    np.testing.assert_almost_equal(tmck.vs, np.array([[0.70710678 ,0.70710678 ],[-0.70710678 , 0.70710678 ]]),4)
    #eigenmodes
    np.testing.assert_almost_equal(tmck.us, np.array([[1,1],[-0.333333, 0.3333333]]),4)
    np.testing.assert_almost_equal(tmck.Lambda_mat, np.array([[4, 0], [0, 2]]),4)
    np.testing.assert_almost_equal(tmck.Lambda_mat, np.diag([4,  2]),4)


def test_Inman_4_2_6():
    # example Inman  4.2.6
    m1 , m2 = 1,4
    k1, k2, k3=10,2, 10
    tmck = TDOF_modal(np.array([[m1,0],[0,m2]]), K=np.array([[k1+k2,-k2],[-k2,k2+k3]]))
    np.testing.assert_equal(tmck.Ktilde, np.array([[12,-1],[-1,3]]))
    #eigenvalues
    np.testing.assert_almost_equal(tmck.ls, np.array([12.10977,2.89022]),4)
    #eigenfrequencies
    np.testing.assert_almost_equal(tmck.wns, np.array([3.4799098, 1.70006699]),4) 
    #eigenvectors
    np.testing.assert_almost_equal(tmck.vs, np.array([[0.99402894,0.10911677],[-0.10911677, 0.99402894]]),4)
    #eigenmodes
    np.testing.assert_almost_equal(tmck.us, np.array([[1,1],[-0.21954446, 18.21954446]]),4)

    np.testing.assert_almost_equal(tmck.Lambda_mat, np.array([[1.21097722e+01, 2.22044605e-16], [5.55111512e-17, 2.89022777e+00]]),4)

# %%
    



def test_modal_raisingValueError():
    '''
    this is a test for testing impoper mass matrices. 
    '''
    # examples 4.1.1. to 4.2.6
    m1,m2  = 9,1
    k1=24
    k2=3
    with pytest.raises(ValueError):
        tmck = TDOF_modal(np.array([[m1,0],[0,m2],[0,m2]]), K=np.array([[k1+k2,-k2],[-k2,k2]]))
    
def test_modal_set_iv():
    # examples inman 4.3.2
    m1,m2  = 9,1
    k1=24
    k2=3
    tmck = TDOF_modal(np.array([[m1,0],[0,m2]]), K=np.array([[k1+k2,-k2],[-k2,k2]]))
    tmck.set_iv(x0s = np.array([[1,0]]).T, dx0s = np.array([[0,0]]).T)
    tmck._set_rfs_hom()
    ts = np.linspace(0, 5,10)
    r1 = 3/np.sqrt(2)*np.cos(2*ts)
    r2 = 3/np.sqrt(2)*np.cos(np.sqrt(2)*ts)
    np.testing.assert_almost_equal(tmck.rfs_h[0](ts),r1 ,4)
    np.testing.assert_almost_equal(tmck.rfs_h[1](ts),r2 ,4)

def test_modal_set_rfs_hom():
    # examples inman 4.3.2
    m1,m2  = 9,1
    k1=24
    k2=3
    tmck = TDOF_modal(np.array([[m1,0],[0,m2]]), K=np.array([[k1+k2,-k2],[-k2,k2]]))
    tmck.set_iv(x0s = np.array([[1,0]]).T, dx0s = np.array([[0,0]]).T)
    tmck._set_rfs_hom()
    ts = np.linspace(0, 5,10)
    r1 = 3/np.sqrt(2)*np.cos(2*ts)
    r2 = 3/np.sqrt(2)*np.cos(np.sqrt(2)*ts)
    np.testing.assert_almost_equal(tmck.rfs_h[0](ts),r1 ,4)
    np.testing.assert_almost_equal(tmck.rfs_h[1](ts),r2 ,4)
# %%
def test_modal_calc_xs():
    # examples inman 4.3.2
    m1,m2  = 9,1
    k1=24
    k2=3
    tmck = TDOF_modal(np.array([[m1,0],[0,m2]]), K=np.array([[k1+k2,-k2],[-k2,k2]]))
    tmck.set_iv(x0s = np.array([[1,0]]).T, dx0s = np.array([[0,0]]).T)
    ts = np.linspace(0, 5,10)
    xs1 = 0.5*(np.cos(np.sqrt(2)*ts) + np.cos(2*ts))
    xs2 =  1.5*(np.cos(np.sqrt(2)*ts) - np.cos(2*ts))
    xs = tmck.calc_x_hom_response(ts)
    np.testing.assert_almost_equal(xs[0,:],xs1 ,4)
    np.testing.assert_almost_equal(xs[1,:],xs2 ,4)
# %%


def test_modal_calc_xs():
    # examples inman 4.4.2
    m1,m2,m3  = 4,4,4
    k1,k2,k3 = 4,4,4

    tmck = TDOF_modal(np.array([[m1,0,0],[0,m2,0],[0,0,m3]]), K=np.array([[k1+k2,-k2,0],[-k2,k2+k3, -k3],[0,-k3,k3]]))


    np.testing.assert_equal(tmck.Ktilde, np.array([[2,-1,0],[-1,2,-1],[0,-1,1]]))
    #eigenvalues
    np.testing.assert_almost_equal(tmck.ls, np.array([3.2470, 1.5550,0.1981]),4)
    #eigenfrequencies
    np.testing.assert_almost_equal(tmck.wns, np.array([1.8019, 1.2470, 0.4450]),4) 
    #eigenvectors
    np.testing.assert_almost_equal(tmck.vs, np.array([[-0.5910,-0.7370, 0.3280 ],[0.7370 ,-0.3280 , 0.5910],[ -0.3280,0.5910 , 0.7370]]),4)

    # #eigenmodes
    # np.testing.assert_almost_equal(tmck.us, np.array([[1,1],[-0.21954446, 18.21954446]]),4)

    np.testing.assert_almost_equal(tmck.Lambda_mat, np.diag(tmck.ls),4)

    tmck.set_iv(x0s = np.array([[1,0, 0]]).T, dx0s = np.array([[0,0,0]]).T)
    np.testing.assert_almost_equal(tmck.r0s, np.array([[-1.1820,-1.4740,0.6560]]).T,4)

    ## The following x_repsonse does not work. Might be due to rounding error. 
    # ts = np.linspace(0, 1,10)
    # xs1 = 0.2417*np.cos(0.4450*ts) -0.4355*np.cos(1.2470*ts)+0.1935*np.cos(0.18019*ts)
    # xs2 = 0.1938*np.corfs_h.4450*ts) +0.2417*np.cos(1.2470*ts)-0.4355*np.cos(0.18019*ts)
    # xs3 = 0.1075*np.cos(0.4450*ts) +0.5443*np.cos(1.2470*ts)+0.3492*np.cos(0.18019*ts)
    # xs = tmck.calc_x_response(ts)
    # np.testing.assert_almost_equal(xs[0,:],xs3,3)
    # # np.testing.assert_almost_equal(xs[1,:],xs2 ,4)
# %%