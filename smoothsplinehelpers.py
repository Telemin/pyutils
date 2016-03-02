#!/usr/bin/env python3

import numpy as np
import scipy.interpolate as si

class SBoundedSpline:
    
    def __init__(self,xdata=None,ydata=None,k=3,s=None):
        if xdata is None or ydata is None:
            self._interpobject = None
        else:
            self._xdata = xdata
            self._interpobject = si.UnivariateSpline(xdata,ydata,ext='zeros',k=k, s=s)
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
        newspline = SBoundedSpline()
        newspline._interpobject = self._interpobject.derivative()
        newspline._min = self._min
        newspline._max = self._max
        newspline._xdata = self._xdata
        return(newspline)

class STrajectory1D:
    
    def __init__(self,xdata,tdata,k=3,s=None):
        self.xdata = xdata
        self.tdata = tdata
        self.XofT = SBoundedSpline(tdata,xdata,k=k,s=s)
        self.TofX = SBoundedSpline(xdata,tdata,k=k,s=s)
        self.VofT = self.XofT.derivative()
        self.BofT = SBoundedSpline(tdata,xdata/299792458,k=k,s=s).derivative()
    
    def lsx(self,n=100):
        return(np.linspace(min(self.xdata),max(self.xdata),n))

class STrajectory2D:
    
    def __init__(self,xdata,ydata,tdata,k=3,s=None):
        self.xdata = xdata
        self.ydata = ydata
        self.tdata = tdata
        self.XofT = SBoundedSpline(tdata,xdata,k=k,s=s)
        self.YofT = SBoundedSpline(tdata,ydata,k=k,s=s)
        self.TofX = SBoundedSpline(xdata,tdata,k=k,s=s)
        self.TofY = SBoundedSpline(ydata,tdata,k=k,s=s)
        self.VxofT = self.XofT.derivative()
        self.VyofT = self.YofT.derivative()
        self.BxofT = SBoundedSpline(tdata,xdata/299792458,k=k,s=s).derivative()  
        self.ByofT = SBoundedSpline(tdata,ydata/299792458,k=k,s=s).derivative()  

    def lst(self,n=100):
        return(np.linspace(min(self.xdata),max(self.xdata),n))

    def lsx(self,n=100):
        return(np.linspace(min(self.xdata),max(self.xdata),n))

    def lsy(self,n=100):
        return(np.linspace(min(self.ydata),max(self.ydata),n))
