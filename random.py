#!/usr/bin/env python3

import numpy as np
import ghalton as gh
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

def rejection_sample(func, samples, xbounds, ybounds=None, seed=None
					,return_rejects=False, return_exact=True):
    xrange = np.asarray(xbounds)
    if seed is None:
        seed = np.random.randint(1,10000)
    if ybounds is None:
        yrange = np.asarray((minimize_scalar(func, bounds=xrange,  method='bounded').fun
                            ,-1*minimize_scalar(lambda x: -1*func(x), bounds=xrange,  method='bounded').fun))
    else:
        yrange = np.asarray(ybounds)
    integ,err = quad(func, xrange.min(), xrange.max())
    coverage = integ/ (np.diff(xrange)*np.diff(yrange))
    halton = gh.GeneralizedHalton(2,seed)
    
    accept = np.empty(0)
    sample_mult = 1.05
    while accept.size < samples:
        if accept.size > 0:
            sample_mult += 0.5
            print("Developer Warning, had to loop...")
            print("{} samples requested, found {}".format(samples, accept.size))
        sample = np.asarray(halton.get(int(sample_mult*samples/coverage))).T
        sample[0] = sample[0] * xrange.max() - xrange.min()
        sample[1] = sample[1] * yrange.max() - yrange.min()
    
        rej_mask = sample[1] > func(sample[0])
        accept = sample[0,np.where(np.invert(rej_mask))]
        
    if return_exact:
        accept = np.reshape(accept[:samples], -1)
    if return_rejects:
        reject = np.reshape(sample[0,np.where(rej_mask)], -1)
        return(accept,reject)
    return(accept) 
