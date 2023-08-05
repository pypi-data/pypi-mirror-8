# -*- coding: utf-8 -*-
"""Provides functions for creating and manipulating 3D vectors.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
from .utils import parameters_as_numpy_arrays

# import common vector operations
from .vector import *


def create(x=0., y=0., z=0., dtype=None):
    return np.array([x,y,z], dtype=dtype)

def create_unit_length_x(dtype=None):
    return np.array([1.0, 0.0, 0.0], dtype=dtype)

def create_unit_length_y(dtype=None):
    return np.array([0.0, 1.0, 0.0], dtype=dtype)

def create_unit_length_z(dtype=None):
    return np.array([0.0, 0.0, 1.0], dtype=dtype)

@parameters_as_numpy_arrays('vector')
def create_from_vector4(vector, dtype=None):
    dtype = dtype or vector.dtype
    return np.array(vector[:3], dtype=dtype)

def create_from_matrix44_translation(mat):
    return mat[3, :3].copy()


class index:
    #: The index of the X value within the vector
    x = 0

    #: The index of the Y value within the vector
    y = 1

    #: The index of the Z value within the vector
    z = 2


class unit:
    #: A vector of unit length in the X-axis. (1.0, 0.0, 0.0)
    x = create_unit_length_x()

    #: A vector of unit length in the Y-axis. (0.0, 1.0, 0.0)
    y = create_unit_length_y()

    #: A vector of unit length in the Z-axis. (0.0, 0.0, 1.0)
    z = create_unit_length_z()
