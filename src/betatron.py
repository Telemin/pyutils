#!/usr/bin/env python3

import os
import h5py
import subprocess
import numpy as np
import scipy.constants as sc
import uuid
import tempfile

def bfg(gamma):
    return(np.sqrt(1 - np.power(gamma,-2)))

def _x(t, a_beta, k_beta, gamma_0):
    return(a_beta/(k_beta*gamma_0) * np.sin(k_beta*sc.c*t))

def _beta_x(t, a_beta, k_beta, gamma_0):
    return((a_beta/gamma_0)*np.cos(k_beta*sc.c*t))

def _z(t, a_beta, k_beta, gamma_0):
    return( bfg(gamma_0)*(sc.c*t - 0.25*np.power(a_beta/gamma_0, 2)*(sc.c*t + (0.5/k_beta)*np.sin(2*k_beta*sc.c*t))))

def _beta_z(t, a_beta, k_beta, gamma_0):
    return( bfg(gamma_0)*(1 - 0.25*np.power(a_beta/gamma_0, 2)*(1 + np.cos(2*k_beta*sc.c*t))))

def _gamma(r, a_beta, k_beta, gamma_0):
    return( gamma_0 + 0.25*(np.power(a_beta/gamma_0,2) - np.power(k_beta*r,2)))

def _osctime(N_beta, k_beta):
    return(2*np.pi*N_beta/(sc.c*k_beta))


def open_h5file(fname, fmode='x'):
    fh = h5py.File(fname, fmode)
    return(fh)

def create_h5track(fh, N_beta, a_beta, gamma_0, k_p, steps_per_cycle=1000, groupname=None, t_offset=0):
    k_beta = k_p/np.sqrt(2*gamma_0)
    T = _osctime(N_beta, k_beta)
    t = np.linspace(0,T,steps_per_cycle*N_beta)+t_offset
    x = _x(t, a_beta, k_beta, gamma_0)
    gamma = _gamma(x, a_beta, k_beta, gamma_0)
    p_x = _beta_x(t, a_beta, k_beta, gamma_0)*gamma
    z = _z(t, a_beta, k_beta, gamma_0)
    p_z = _z(t, a_beta, k_beta, gamma_0)*gamma
    
    if groupname is None or not hasattr(groupname,"__str__"):
        groupname = uuid.uuid4()
    
    try:
        os.mkdir(os.path.dirname(fname))
    except:
        pass
    
    gh = fh.create_group(str(groupname))
    gh.create_dataset("t", data=(t)*sc.c*1e6)
    gh.create_dataset("x1", data=z*1e6)
    gh.create_dataset("x2", data=x*1e6)
    gh.create_dataset("x3", data=np.zeros(t.shape))
    gh.create_dataset("p1", data=p_z)
    gh.create_dataset("p2", data=p_x)
    gh.create_dataset("p3", data=np.zeros(t.shape))
    gh.create_dataset("q", data=np.ones(t.shape))
    gh.create_dataset("ene", data=gamma-1)
    
def close_h5file(fh):
    fh.close()


def run_radt(work_dir, config, radt_command="/home/telemin/repos/radt/radt-omp"):
    with tempfile.NamedTemporaryFile(mode='w+t', suffix=".conf", dir=work_dir, delete=False) as fh:
        config_tempfile = fh.name
        fh.write(config)
    p = subprocess.Popen((radt_command, config_tempfile), cwd=work_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    results = p.communicate()[0]
    os.remove(config_tempfile)
    return()
