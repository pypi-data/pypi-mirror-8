import numpy as np
from numpy.testing import assert_allclose

from ..util import fast_limits


def test_fast_limits_nans():
    x = np.zeros((10, 10)) * np.nan
    assert_allclose(fast_limits(x, 0, 1), [0, 1])


def test_single_value():
    x = np.array([1])
    assert_allclose(fast_limits(x, 5., 95.), [1, 1])
