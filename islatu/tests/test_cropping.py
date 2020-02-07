"""
Tests for cropping module

Copyright (c) Andrew R. McCluskey

Distributed under the terms of the MIT License

@author: Andrew R. McCluskey
"""

# pylint: disable=R0201

import unittest
import numpy as np
from numpy.testing import assert_almost_equal
from islatu import cropping


class TestCropping(unittest.TestCase):
    """
    Unit tests for cropping module
    """

    def test_crop_2d_a(self):
        """
        Test crop_2d.
        """
        initial_array = np.ones((50, 50))
        expected_array = np.ones((20, 20))
        result = cropping.crop_2d(initial_array, 20, 40, 10, 30)
        assert_almost_equal(result, expected_array)

    def test_crop_2d_b(self):
        """
        Test crop_2d.
        """
        initial_array = np.ones((50, 50))
        expected_array = np.ones((20, 10))
        result = cropping.crop_2d(initial_array, 20, 40, 10, 20)
        assert_almost_equal(result, expected_array)

    def test_crop_around_peak_2d_a(self):
        """
        Test crop_around_peak_2d with defaults.
        """
        initial_array = np.ones((50, 50))
        initial_array[25, 25] = 100
        expected_array = np.ones((20, 20))
        expected_array[10, 10] = 100
        result = cropping.crop_around_peak_2d(initial_array)
        assert_almost_equal(result, expected_array)

    def test_crop_around_peak_2d_b(self):
        """
        Test crop_around_peak_2d with custom.
        """
        initial_array = np.ones((50, 50))
        initial_array[25, 25] = 100
        expected_array = np.ones((10, 10))
        expected_array[5, 5] = 100
        result = cropping.crop_around_peak_2d(initial_array, 10, 10)
        assert_almost_equal(result, expected_array)

    def test_crop_around_peak_2d_c(self):
        """
        Test crop_around_peak_2d with asymmetry.
        """
        initial_array = np.ones((50, 50))
        initial_array[25, 25] = 100
        expected_array = np.ones((10, 20))
        expected_array[5, 10] = 100
        result = cropping.crop_around_peak_2d(initial_array, 10, 20)
        assert_almost_equal(result, expected_array)
