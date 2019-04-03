#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
measure
----------------------------------

Module that contains functions to normalise GeometryParameters with measures (angles, metres, millimetres, etc.).

Author: Javier Chiyah, Heriot-Watt University, 2019
"""


import math

from ..core import GeometryParameter
# from ..core.constants import GEOMETRY_MEASURES


INCHES_TO_MM = 25.4


def normalise_measure(parameter: GeometryParameter):
	"""
	NOT IMPLEMENTED
	Normalises a number parameter that is a metric of some sort

	:param parameter: GeometryParameter to normalise
	:return: None
	"""
	# not implemented
	pass


def normalise_range_measure(parameter: GeometryParameter):
	"""
	Normalises range parameters that may be the same value in different metrics.

	This checks for things like [1, 25.4], where the first is the second one in millimetres or vice-versa.
	Note that this only works with lists of length 2.

	:param parameter: GeometryParameter to normalise
	:return: None
	"""
	# check if first value is in inches
	if math.isclose(parameter.value[0] * INCHES_TO_MM, parameter.value[1], abs_tol=1):
		# delete first one
		parameter.set_normalised_value(parameter.value[1])

	elif math.isclose(parameter.value[1] * INCHES_TO_MM, parameter.value[0], abs_tol=1):
		# delete second one
		parameter.set_normalised_value(parameter.value[0])
