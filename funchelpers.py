#!/usr/bin/env python

def recApply(f, x, n, args=(), kwargs={}):
    for i in range(n):
        x = f(x, *args, **kwargs)
    return(x)

class TextProgress(object):
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
        self._count = 0
        self._iter = iter(self._iterable)
        return(self)

    def __next__(self):
        self._count += 1
        print("\r{}/{}".format(self._count,self._len), end="")
        try:    
            return(next(self._iter))
        except StopIteration:
            print()
            raise

