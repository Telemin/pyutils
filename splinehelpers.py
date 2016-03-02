#!/usr/bin/env python3

import numpy as np
import scipy.interpolate as si

class BoundedSpline:
    
    def __init__(self,xdata=None,ydata=None,k=1):
        if xdata is None or ydata is None:
            self._interpobject = None
        else:
            self._xdata = xdata
            self._interpobject = si.InterpolatedUnivariateSpline(xdata,ydata,ext='zeros',k=k)
            self._min = xdata[0]
            self._max = xdata[-1]
        
    def __call__(self,val):
        return(self._interpobject(val))

    def fullrange(self):
        return(self.__call__(self._xdata))
   
    def fullrangeinterp(self,n=100):
        return(self.__call__(np.linspace(self._min,self._max,n)))

    def linspace(self,n):
        return(np.linspace(self._min,self._max,n))
    
    def derivative(self):
        newspline = BoundedSpline()
        newspline._interpobject = self._interpobject.derivative()
        newspline._min = self._min
        newspline._max = self._max
        newspline._xdata = self._xdata
        return(newspline)

class Trajectory1D:
    
    def __init__(self,xdata,tdata,k=1):
        self.xdata = xdata
        self.tdata = tdata
        self.XofT = BoundedSpline(tdata,xdata,k=k)
        self.TofX = BoundedSpline(xdata,tdata,k=k)
        self.VofT = self.XofT.derivative()
        self.BofT = BoundedSpline(tdata,xdata/299792458,k=k).derivative()
    
    def lsx(self,n=100):
        return(np.linspace(min(self.xdata),max(self.xdata),n))

class Trajectory2D:
    
    def __init__(self,xdata,ydata,tdata,k=1):
        self.xdata = xdata
        self.ydata = ydata
        self.tdata = tdata
        self.XofT = BoundedSpline(tdata,xdata,k=k)
        self.YofT = BoundedSpline(tdata,ydata,k=k)
        self.TofX = BoundedSpline(xdata,tdata,k=k)
        self.TofY = BoundedSpline(ydata,tdata,k=k)
        self.VxofT = self.XofT.derivative()
        self.VyofT = self.YofT.derivative()
        self.BxofT = BoundedSpline(tdata,xdata/299792458,k=k).derivative()  
        self.ByofT = BoundedSpline(tdata,ydata/299792458,k=k).derivative()  

    def lst(self,n=100):
        return(np.linspace(min(self.xdata),max(self.xdata),n))

    def lsx(self,n=100):
        return(np.linspace(min(self.xdata),max(self.xdata),n))

    def lsy(self,n=100):
        return(np.linspace(min(self.ydata),max(self.ydata),n))
