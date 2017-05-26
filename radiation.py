#/usr/bin/env python3

import numpy as np
from scipy.special import jn
import scipy.constants as sc


## Shared Helper Functions

def beta_from_gamma(gamma):
    return(np.sqrt(1-np.power(gamma,-2)))

def k_beta_(gamma_0, k_p):
    return(k_p/np.sqrt(2*gamma_0))

def r_beta_(a_beta, gamma_0, k_beta):
    return(a_beta/gamma_0/k_beta)

def alpha_0(a_beta, gamma_0, theta):
    return(1 - np.cos(theta)*beta_from_gamma(gamma_0)*(1 - np.power(a_beta/gamma_0/2,2)))

def alpha_x(k, r_beta, theta, phi):
    return(k*r_beta*np.sin(theta)*np.cos(phi))

def alpha_z(k, k_beta, r_beta, beta_z, theta):
    return(np.cos(theta)*beta_z*k*k_beta*r_beta*r_beta/8)


### Esarey approximate calculation

def calculate_psd_esarey(k, N_beta, a_beta, gamma_0, k_p, theta, phi):
    if theta != 0:
        raise NotImplementedError("Off axis radiation not yet implemented.")
    if phi != 0:
        raise NotImplementedError("Off axis radiation not yet implemented.")
 
    k_beta = k_beta_(gamma_0, k_p)
    r_beta = r_beta_(a_beta, gamma_0, k_beta)

    k_min = np.min(np.asarray(k))
    k_max = np.max(np.asarray(k))

    n_min = 1
    n_max = np.ceil( np.max(np.asarray( alpha_0(a_beta, gamma_0, theta)
                                        *k_max/k_beta)))
    n_range = np.arange(n_min, n_max+1, 2)

    n = np.outer(np.ones(k.shape), n_range)
    k = np.outer(k, np.ones(n_range.shape))

    k_n = n*k_beta/alpha_0(a_beta, gamma_0, theta)

    alpha = np.power(a_beta,2)*np.power(8*k_beta*np.power(gamma_0,2),-1)
    Fn = n*alpha*k*np.power(jn((n-1)/2,alpha*k) + jn((n+1)/2, alpha*k),2)
    Rn = np.power(np.sinc(n*N_beta* (k/k_n -1)),2)
    pref = np.power(2*sc.e*gamma_0*N_beta,2)*k/(sc.c*k_n*(1 + 0.5*a_beta**2))
   
    return(np.sum(pref * Rn * Fn, -1))

### Full Calculation including crossterms

def Ixn(k, n, N_beta, a_beta, gamma_0, k_p, theta, phi):
    beta_z = beta_from_gamma(gamma_0)
    k_beta = k_beta_(gamma_0, k_p)
    r_beta = r_beta_(a_beta, gamma_0, k_beta)

    sinc_term = np.sinc(N_beta*( alpha_0(a_beta, gamma_0, theta)*k/k_beta - n))
    if theta == 0:
        if n/2 == int(n/2):
            sum_term = 0 #even harmonics don't contribute on axis
        else:
            sum_term = jn((n-1)/2, alpha_z(k, k_beta, r_beta, beta_z, theta)) + jn((n+1)/2, alpha_z(k, k_beta, r_beta, beta_z, theta))
    else:
        raise NotImplementedError("Off axis radiation not yet implemented.")
        
    return(sinc_term * sum_term)


def calculate_psd_full(k, N_beta, a_beta, gamma_0, k_p, theta, phi, sinc_overlap_periods=5, mtol=0.1):
    if theta != 0:
        raise NotImplementedError("Off axis radiation not yet implemented.")
    if phi != 0:
        raise NotImplementedError("Off axis radiation not yet implemented.")
    
    k_min = np.min(np.asarray(k))
    k_max = np.max(np.asarray(k))
    
    k_beta = k_beta_(gamma_0, k_p)
    r_beta = r_beta_(a_beta, gamma_0, k_beta)
    
    n_min = np.floor(np.min(np.asarray(alpha_0(a_beta, gamma_0, theta)))*k_min/k_beta) - np.ceil(sinc_overlap_periods/N_beta)
    n_max = np.ceil(np.max(np.asarray(alpha_0(a_beta, gamma_0, theta)))*k_max/k_beta) + np.ceil(sinc_overlap_periods/N_beta)
    n_range = np.arange(n_min,n_max+1,1)
    
    I_xn = np.empty(n_range.shape + k.shape)
    for i,n in enumerate(n_range):
        I_xn[i] = Ixn(k, n, N_beta, a_beta, gamma_0, k_p, theta, phi)
    
    I_x = np.pi*N_beta * r_beta* np.sum(I_xn,0)
    
    return( 0.25*np.power(sc.e * k / np.pi,2)/sc.c * np.power(I_x,2))
        
        
