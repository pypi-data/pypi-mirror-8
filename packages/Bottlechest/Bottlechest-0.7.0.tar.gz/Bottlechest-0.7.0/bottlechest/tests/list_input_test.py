"Test list input."

# For support of python 2.5
from __future__ import with_statement

import numpy as np
from numpy.testing import (assert_equal, assert_array_equal, assert_raises,
                           assert_array_almost_equal, assert_almost_equal)
import bottlechest as bn

# ---------------------------------------------------------------------------
# Check that functions can handle list input

def lists():
    "Iterator that yields lists to use for unit testing."
    ss = {}
    ss[1] = {'size':  4, 'shapes': [(4,)]}
    ss[2] = {'size':  6, 'shapes': [(1,6), (2,3)]}
    ss[3] = {'size':  6, 'shapes': [(1,2,3)]}
    ss[4] = {'size': 24, 'shapes': [(1,2,3,4)]}  # Unaccelerated
    for ndim in ss:
        size = ss[ndim]['size']
        shapes = ss[ndim]['shapes']
        a = np.arange(size)
        for shape in shapes:
            a = a.reshape(shape)
            yield a.tolist()

def unit_maker(func, func0, args=tuple()):
    "Test that bn.xxx gives the same output as bn.slow.xxx for list input."
    msg = '\nfunc %s | input %s | shape %s\n'
    msg += '\nInput array:\n%s\n'
    for i, arr in enumerate(lists()):
        argsi = tuple([list(arr)] + list(args))
        actual = func(*argsi)
        desired = func0(*argsi)
        tup = (func.__name__, 'a'+str(i), str(np.array(arr).shape), arr)
        err_msg = msg % tup
        assert_array_almost_equal(actual, desired, err_msg=err_msg)

def test_nansum():
    "Test nansum."
    yield unit_maker, bn.nansum, bn.slow.nansum

def test_nanmax():
    "Test nanmax."
    yield unit_maker, bn.nanmax, bn.slow.nanmax

def test_nanargmin():
    "Test nanargmin."
    yield unit_maker, bn.nanargmin, bn.slow.nanargmin

def test_nanargmax():
    "Test nanargmax."
    yield unit_maker, bn.nanargmax, bn.slow.nanargmax

def test_nanmin():
    "Test nanmin."
    yield unit_maker, bn.nanmin, bn.slow.nanmin

def test_nanmean():
    "Test nanmean."
    yield unit_maker, bn.nanmean, bn.slow.nanmean

def test_nanstd():
    "Test nanstd."
    yield unit_maker, bn.nanstd, bn.slow.nanstd

def test_nanvar():
    "Test nanvar."
    yield unit_maker, bn.nanvar, bn.slow.nanvar

def test_median():
    "Test median."
    yield unit_maker, bn.median, bn.slow.median

def test_nanmedian():
    "Test nanmedian."
    yield unit_maker, bn.nanmedian, bn.slow.nanmedian
   
def test_rankdata():
    "Test rankdata."
    yield unit_maker, bn.rankdata, bn.slow.rankdata

def test_nanrankdata():
    "Test nanrankdata."
    yield unit_maker, bn.nanrankdata, bn.slow.nanrankdata

def test_ss():
    "Test ss."
    yield unit_maker, bn.ss, bn.slow.ss

def test_nn():
    "Test nn."
    a = [[1, 2], [3, 4]]
    a0 = [1, 2]
    assert_equal(bn.nn(a, a0), bn.slow.nn(a, a0))

def test_anynan():
    "Test anynan."
    yield unit_maker, bn.anynan, bn.slow.anynan

def test_allnan():
    "Test allnan."
    yield unit_maker, bn.allnan, bn.slow.allnan

