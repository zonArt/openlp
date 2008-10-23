"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

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
