#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
constraints
----------------------------------

Module containing functions that check the constraints of GeometryParameters and the BikeGeometry in general

Author: Javier Chiyah, Heriot-Watt University, 2019
"""


import logging
# keep this import as it is used indirectly below through an eval()
import operator

from datavalidation.core import BikeGeometry, GeometryParameter
from datavalidation.core.constants import GEOMETRY_CONSTRAINTS, OPERATORS, GEOMETRY_STATISTICS


def filter_by_constraints(value_list: list, parameter_name: str, bike_geometry: BikeGeometry) -> list:
	"""
	Filters a list of values depending on the BikeGeometry constraints and the GeometryParameter they belong to.
	It returns the filtered list, which can be empty if no values passed the checks.

	This is used to, for instance, filter the solutions to the equations to only those that are possible.

	:param value_list: list of possible values
	:param parameter_name: name of the GeometryParameter to which the values would apply to
	:param bike_geometry: the BikeGeometry
	:return: filtered list of values, it can be empty []
	"""
	filtered_result = []

	# check if the parameter has any constraints
	if parameter_name in GEOMETRY_CONSTRAINTS:
		# for each value in value_list
		for value in value_list:
			# check that the value makes the constraints true
			if _check_constraint_list(value, GEOMETRY_CONSTRAINTS[parameter_name], bike_geometry):
				filtered_result.append(value)

		logging.debug("GeometryParameter('{}') - list of values {} filtered to {} with geometry constraints".format(
			parameter_name, value_list, filtered_result))
		return filtered_result

	else:
		return value_list


def check_parameter_constraints(parameter_name: str, bike_geometry: BikeGeometry) -> bool:
	"""
	Checks that the GeometryParameter satisfies all the geometry constraints.
	It also checks the geometry statistics, so even if the parameter does NOT satisfy the geometry constraints,
	this function may return True when the issue is likely to be from another parameter of the bike geometry.

	:param parameter_name: name of the GeometryParameter
	:param bike_geometry: BikeGeometry
	:return: bool, True if the GeometryParameter satisfies constraints (or the issue is with another parameter)
	"""
	if parameter_name in GEOMETRY_CONSTRAINTS:
		parameter_value = bike_geometry.get_parameter_value(parameter_name)

		if not isinstance(parameter_value, list):
			parameter_value = [parameter_value]

		result = []
		# for each value in parameter_value list
		for value in parameter_value:
			# check that the value makes the constraints true
			if _check_constraint_list(value, GEOMETRY_CONSTRAINTS[parameter_name], bike_geometry) or \
				_check_constraint_statistics(parameter_name, value, bike_geometry):
				result.append(value)

		bool_constraints = result == parameter_value
		logging.debug("GeometryParameter('{}') {} the geometry constraints".format(
			parameter_name, "satisfies" if bool_constraints else "does NOT satisfy"))

		return bool_constraints
	else:
		return True


def get_parameter_deviation(parameter: GeometryParameter, invert: bool = False):
	"""
	Gets the parameter deviation from the normal geometry statistics.
	Deviation is in the range of 0 to 1.

	:param parameter: GeometryParameter
	:param invert: bool, give True to calculate the inverted deviation (1 - dev) when dev is not None. False by default
	:return: float or None
	"""
	if parameter.name in GEOMETRY_CONSTRAINTS:
		dev = _get_deviation(parameter.name, parameter.value)

		if dev is not None:
			logging.debug("GeometryParameter('{}') has a deviation of {} from statistics (0 - 1)".format(parameter.name, dev))

		if invert and dev is not None:
			return 1 - dev
		else:
			return dev
	else:
		return None


def _check_constraint_list(value: float, constraint_list: list, bike_geometry: BikeGeometry) -> bool:
	"""
	Checks if the value satisfies a list of constraints.

	:param value: value to check
	:param constraint_list: list of constraints
	:param bike_geometry: the BikeGeometry
	:return: bool, True if it checks all the constraints
	"""
	# check that it fulfills all its constraints
	for constraint in constraint_list:
		if not _check_constraint(value, constraint, bike_geometry):
			return False

	return True


def _check_constraint(value: float, constraint: tuple, bike_geometry: BikeGeometry) -> bool:
	"""
	Checks if the value satisfies a geometry constraint.

	:param value: value to check
	:param constraint: geometry constraint tuple
	:param bike_geometry: BikeGeometry
	:return: bool, True if the parameter satisfies the constraint
	"""
	bike_param = bike_geometry.get_parameter_value(constraint[1])

	if bike_param is None or bike_param == "":
		return True

	if not isinstance(bike_param, list):
		bike_param = [bike_param]

	for param in bike_param:
		if not OPERATORS[constraint[0]](value, param):
			# logging.debug("solution discarded < (p=" + str(param) + "): " + str(solution))
			return False
		# else raise ValueError("Constraint operator not recognised: {} in tuple {}".format(constraint[0], constraint))

	return True


def _check_constraint_statistics(parameter_name: str, value: float, bike_geometry: BikeGeometry) -> bool:
	"""
	Checks that the parameter satisfies the geometry statistics.
	This is, that the parameter is not further from the normal values than other parameters involved in its
	geometry constraints.

	Note that this function should only be called when the _check_constraint_list() function returns False, as it may
	provide odd results otherwise.

	:param parameter_name: name of the GeometryParameter
	:param value: value of the parameter
	:param bike_geometry: BikeGeometry
	:return: True if the GeometryParameter is closer to the normal statistics than the other GeometryParameters involved
	"""
	# first check how far this constraint is from the normal statistics
	deviation = _get_deviation(parameter_name, value)

	# now get deviation for the other parameters involved
	other_deviations = []
	# note that other_deviations is a list of tuples like ("chainstay", 0.8), although the first value is not used

	for constraint in GEOMETRY_CONSTRAINTS[parameter_name]:
		other_deviations.append(
			(constraint[1], _get_deviation(constraint[1], bike_geometry.get_parameter_value(constraint[1])))
		)

	# filter those with None as deviation
	other_deviations = [x for x in other_deviations if x[1] is not None]

	return max(other_deviations, key=lambda l: l[1])[1] > deviation


def _get_deviation(parameter_name: str, value: float):
	"""
	Gets the deviation of a parameter from the normal statistics.
	This is a number from 0 to 1 where 1 represents that the value is exactly right and 0 where the value
	is very off from the normal statistics (e.g. a wheelbase of 1150 would give something close to 1, but
	a wheelbase of 10 would give a deviation close to 0).
	It averages the similarity of the value to its mean and to its median.

	:param parameter_name: name of the GeometryParameter
	:param value: value for the GeometryParameter
	:return: float or None (if value is None only)
	"""
	if value is None:
		return None
	return 1 - (_get_value_similarity(GEOMETRY_STATISTICS[parameter_name]['mean'], value) +
		_get_value_similarity(GEOMETRY_STATISTICS[parameter_name]['median'], value)) / 2


def _get_value_similarity(value1, value2) -> float:
	"""
	Gets the similarity between two values.
	The similarity is a number between 0 and 1 as a percentage where 1 means that the values are the same and 0
	means that the values are completely different.
	This function is duplicated in the validate module. A common utility file could improve this...

	:param value1: value
	:param value2: value
	:return: (0 to 1) percentage float of how close value1 is to value2
	"""
	if isinstance(value2, list):
		# if value2 is a list, then return the one with least similarity from the whole similarity list
		val_list = [_get_value_similarity(value1, x) for x in value2]
		return sum(val_list) / len(val_list)

	return float(min([value1, value2])) / float(max([value1, value2]))
