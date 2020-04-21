"""
Reflectometry data must be corrected as a part of reduction. 
These functions facilitate this, including the footprint and DCD q-variance corrections.
"""

# Copyright (c) Andrew R. McCluskey
# Distributed under the terms of the MIT License
# author: Andrew R. McCluskey (andrew.mccluskey@diamond.ac.uk)

import numpy as np
from scipy.stats import norm
from uncertainties import unumpy as unp
from islatu.io import i07_dat_parser
from scipy.interpolate import splrep


def footprint_correction(beam_width, sample_size, theta):
    """
    The factor by which the intensity should be multiplied to account for the
    scattering geometry, where the beam is Gaussian in shape.

    Args:
        beam_width (float): Width of incident beam, in metres.
        sample_size (uncertainties.core.Variable): Width of sample in the
            dimension of the beam, in metres.
        theta (float): Incident angle, in degrees.

    Returns:
        (uncertainties.core.Variable): Correction factor.
    """
    beam_sd = beam_width / 2 / np.sqrt(2 * np.log(2))
    length = sample_size * unp.sin(unp.radians(theta))
    mid = unp.nominal_values(length) / 2.0 / beam_sd
    upper = (unp.nominal_values(length) + unp.std_devs(length)) / 2.0 / beam_sd
    lower = (unp.nominal_values(length) - unp.std_devs(length)) / 2.0 / beam_sd
    probability = 2.0 * (
        unp.uarray(norm.cdf(mid), (norm.cdf(upper) - norm.cdf(lower)) / 2)
        - 0.5
    )
    return probability


def get_interpolator(file_path, parser, q_flag='qdcd_', intensity_flag='adc2'):
    """
    Get an interpolator object from scipy, this is useful for the DCD q-normalisation step.

    Args:
        file_path (str): File path to the normalisation file.
        parser (callable): Parser function for the normalisation file.
        q_flag (str, optional): Label for the q-value in the normalisation file. Defaults to ``'qdcd_'``.
        intensity_flag (str, optional): Label for the intensity in the normalisation file. Defaults to ``'adc2'``.

    Returns:
        (scipy.interpolator): Interpolation object. 
    """
    normalisation_data = parser(file_path)[1]
    return splrep(normalisation_data[q_flag], normalisation_data[intensity_flag])