# useful linear interpolation routines

def interp1(val1, val2, fraction):
    """return a linear 1d interpolation between val1 and val2 by fraction
    if fraction=0.0, returns val1
    if fraction=1.0, returns val2"""
    return val1+((val2-val1)*fraction)
def interpolate(val1, val2, fraction):
    "vals can be list/tuples - if so, will return a tuple of interpolated values for each element."
    assert (fraction >= 0.0)
    assert (fraction <= 1.0)
    assert (type(val1) == type(val2))
    if (type(val1) == type(()) or
        type (val1) == type([])):
        assert(len(val1) == len(val2))
        retval=[]
        for i in range(len(val1)):
            retval.append(interp1(val1[i], val2[i], fraction))
        return tuple(retval)
    else:
        return interp1(val1, val2, fraction)
