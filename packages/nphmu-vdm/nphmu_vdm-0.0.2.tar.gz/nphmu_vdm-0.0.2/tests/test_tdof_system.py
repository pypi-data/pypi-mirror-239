# in order to run this in Vscode, a good work around is to 
# use 
#   python setup.py develop

import pytest
from np_vmd import tdof_system

def test_one():
    pass

def test_tdofparams():
    tdp = tdof_system.Tdof_params()
    assert(tdp.c1,0)