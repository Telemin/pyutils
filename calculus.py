#!/usr/bin/env python3

import numpy as np

def NonUniformForwardDifference(y,x,pad=True):
    d = np.diff(y)/np.diff(x)
    if pad is True:
        d = np.append(d,d[-1])
    return(d)

def NonUniformCentralDifference(y,x,pad=True):
    if pad is True:
        x0 = np.append(x[0],x[:-1])
        x1 = np.append(x[1:],x[-1])
        y0 = np.append(y[0],y[:-1])
        y1 = np.append(y[1:],y[-1])
    else:
        x0 = x[:-1]
        x1 = x[1:]
        y0 = y[:-1]
        y1 = y[-1]

    
    return(x0 + (x1-x0)/2), (y1 - y0)/(x1-x0)
