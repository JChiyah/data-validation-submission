#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
number
----------------------------------

Module with functions that normalise GeometryParameter that are numbers (integers, floats, ranges, etc.).

Author: Mario Vasilev and Javier Chiyah, Heriot-Watt University, 2019
"""


import re

from ..core import GeometryParameter
from datavalidation.normalisation.measure import normalise_range_measure


def normalise_number(parameter: GeometryParameter):
	"""
	Normalises a GeometryParameters which is a number

	:param parameter: GeometryParameter to normalise
	:return: None
	"""
	# only process if value is true
	if not parameter.value:
		return

	if is_range_parameter(parameter):
		normalise_range(parameter)
		normalise_range_measure(parameter)

	else:
		normalise_float(parameter)


def normalise_float(parameter: GeometryParameter):
	"""
	Normalises a GeometryParameter that is a float.

	Author: Mario Vasilev

	:param parameter: GeometryParameter to normalise
	:return: None
	"""
	first_fix = parameter.original_value.replace(',', '.')
	first_fix2 = first_fix.replace("'", "")
	numeric_const_pattern = r'[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
	rx = re.compile(numeric_const_pattern, re.VERBOSE)
	norm_float = rx.findall(first_fix2)

	parameter.set_normalised_value(float(norm_float[0]))


def is_range_parameter(parameter: GeometryParameter) -> bool:
	"""
	Checks if the GeometryParameter is a range (e.g. "170/180" or "170 - 180").

	:param parameter: GeometryParameter to check
	:return: bool, True if the parameter has a value that is a range
	"""
	return bool(re.search(r'[0-9]+.*[/-].*[0-9]+.*', parameter.original_value))


def normalise_range(parameter: GeometryParameter):
	"""
	Normalises a GeometryParameter that is a range, possibly composed of 1 or more floats.

	Author: Mario Vasilev

	:param parameter: GeometryParameter to normalise
	:return: None
	"""
	original_str = parameter.original_value.replace('-', '/')
	list_floats = original_str.split('/')

	list_ftrim = []

	for i in list_floats:
		list_ftrim.append(_trim_non_numeric_characters(i))

	parameter.set_normalised_value(list_ftrim)


def _trim_non_numeric_characters(string: str) -> str:
	"""
	Helper function that returns a string without non-numeric characters.

	Author: Mario Vasilev

	:param string: a string (e.g., "aa 190 A")
	:return: string without non numeric characters
	"""
	numeric_const_pattern = r'[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
	rx = re.compile(numeric_const_pattern, re.VERBOSE)
	string = rx.findall(string)
	new_str = string
	return new_str[0]
