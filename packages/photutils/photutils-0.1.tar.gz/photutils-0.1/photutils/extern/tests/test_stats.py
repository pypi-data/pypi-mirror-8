# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
from photutils.utils import check_random_state
from ..stats import mad_std, gaussian_fwhm_to_sigma, gaussian_sigma_to_fwhm
from numpy.testing import assert_allclose


def test_mad_std():
    prng = check_random_state(12345)
    data = prng.normal(5, 2, size=(100, 100))
    assert_allclose(mad_std(data), 2.0, rtol=0.05)


def test_gaussian_fwhm_to_sigma():
    fwhm = (2.0 * np.sqrt(2.0 * np.log(2.0)))
    assert_allclose(gaussian_fwhm_to_sigma * fwhm, 1.0, rtol=1.0e-6)


def test_gaussian_sigma_to_fwhm():
    sigma = 1.0 / (2.0 * np.sqrt(2.0 * np.log(2.0)))
    assert_allclose(gaussian_sigma_to_fwhm * sigma, 1.0, rtol=1.0e-6)


def test_gaussian_sigma_to_fwhm_to_sigma():
    assert_allclose(gaussian_fwhm_to_sigma * gaussian_sigma_to_fwhm, 1.0)
