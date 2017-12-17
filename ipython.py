#!/usr/bin/env python3

import signal
from ipywidgets import FloatProgress
from IPython.display import display

class ProgressBar(object):
    def __init__(self, iterable, length=None):
        if not hasattr(iterable, '__iter__'):
            raise AttributeError("Passed non iterable type {}".format(type(iterable)))
        self._iterable = iterable
        if hasattr(length,'__int__'):
            self._len = int(length)
        else:
            try:
                self._len = self._iterable.__len__()
            except:
                raise TypeError("No length given and iterable does not have a"
                                "__len__ method.")

    def __iter__(self):
        self._pbar = FloatProgress(min=0,max=self._len)
        display(self._pbar)             
        self._pbar.value = -1
        self._iter = iter(self._iterable)
        return(self)

    def __next__(self):
        self._pbar.value += 1
        try:    
            return(next(self._iter))
        except StopIteration:
            self._pbar.value += 1
            self._pbar.close()
            raise

