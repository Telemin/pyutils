import numpy as np

def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.
	Originally from http://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()


def interp_nans(y, x=None):
    nans, idx = nan_helper(y)
    if x is None:
        y[nans] = np.interp(idx(nans), idx(~nans), y[~nans])
    else:
        y[nans] = np.interp(x[nans], x[~nans], y[~nans])

    return(y)
