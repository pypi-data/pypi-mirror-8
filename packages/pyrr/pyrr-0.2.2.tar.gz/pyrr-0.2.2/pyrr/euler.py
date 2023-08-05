# -*- coding: utf-8 -*-
"""Provide functions for the creation and manipulation of Euler angles.

Eulers represent 3 rotations: Pitch, Roll and Yaw.

Eulers are represented using a numpy.array of shape (3,).
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np


class index:
    #: The index of the pitch value within the euler
    pitch = 0

    #: The index of the roll value within the euler
    roll = 1

    #: The index of the yaw value within the euler
    yaw = 2


def create(pitch=0., roll=0., yaw=0., dtype=None):
    """Creates an array storing the specified euler angles.

    Input values are in radians.

    :param float pitch: The pitch in radians.
    :param float roll: The roll in radians.
    :param float yaw: The yaw in radians.
    :rtype: numpy.array
    """
    return np.array([pitch, roll, yaw], dtype=dtype)

def pitch(eulers):
    """Extracts the pitch value from the euler.

    :rtype: float.
    """
    return eulers[0]

def roll( eulers ):
    """Extracts the roll value from the euler.

    :rtype: float.
    """
    return eulers[1]

def yaw(eulers):
    """Extracts the yaw value from the euler.

    :rtype: float.
    """
    return eulers[2]
