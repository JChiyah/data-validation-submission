#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
normalise
----------------------------------

Module that contains functions to normalise GeometryParameters. It is the main file of the normalisation module.

Author: Javier Chiyah, Heriot-Watt University, 2019
"""


import logging

from ..core import BikeGeometry
from ..core import GeometryParameter
from .number import normalise_number


def normalise_bike_geometry(bike_geometry: BikeGeometry):
	"""
	Normalises the GeometryParameters inside a BikeGeometry.
	It modifies the BikeGeometry in place!

	:param bike_geometry: BikeGeometry
	:return: None
	"""
	# this loop can be easily executed in parallel, since there is no cross-reference of GeometryParameters
	for param in bike_geometry.get_parameter_list():
		normalise_parameter(param)

	logging.info("BikeGeometry normalised")


def normalise_parameter(parameter: GeometryParameter):
	"""
	Normalises a GeometryParameter, eliminating additional characters or recognising a range of values.
	It modifies the GeometryParameter in place.

	:param parameter: GeometryParameter
	:return: None
	"""
	if parameter.is_number():
		normalise_number(parameter)
