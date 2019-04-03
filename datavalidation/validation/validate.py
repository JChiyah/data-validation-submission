#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
validate
----------------------------------

Module with the main functionality of the validation process. It validates BikeGeometries and GeometryParameters, and
calculates the GeometryParameters missing if possible.

Author: Javier Chiyah, Heriot-Watt University, 2019
"""


import logging

from ..core import BikeGeometry, GeometryParameter
from .equations import get_equations, solve_equation
from .constraints import check_parameter_constraints, get_parameter_deviation


def validate_bike_geometry(bike_geometry: BikeGeometry):
	"""
	Validates a BikeGeometry. Be careful as it modifies the BikeGeometry in place!

	After calling this function, the BikeGeometry has been modified in the following way:

	- The GeometryParameters from inside the BikeGeometry that could be validated now have confidence values.
	- Some GeometryParameters may be deemed invalid due to low confidence values.
	- Some GeometryParameters may have new calculated values, even if the previous values were valid.
	- Some GeometryParameters without a value may have a new value calculated by deriving it from others.
	- The BikeGeometry can now be queried for a confidence value (get_confidence_score()).

	:param bike_geometry: BikeGeometry object to validate
	:return: None
	"""
	change_flag = True

	# loop as long as the list of parameters is increasing (they are being calculated)
	while change_flag:
		missing_len = len(bike_geometry.get_missing_parameter_list())

		calculate_missing_parameters(bike_geometry)

		# set change_flag to False if the list of parameters didn't increase
		change_flag = missing_len != len(bike_geometry.get_missing_parameter_list())

	# note that this loop can be executed in parallel and it is likely to be the most expensive loop of the package
	for param in bike_geometry.get_parameter_list():
		validate_geometry_parameter(param, bike_geometry)

	# calculate parameters again to give values to invalid parameters
	# no need to do this anymore as validate will add the parameter's calculated values by default now
	# calculate_missing_parameters(bike_geometry)

	logging.info("BikeGeometry validated")


def validate_geometry_parameter(parameter: GeometryParameter, bike_geometry: BikeGeometry):
	"""
	Validates a GeometryParameter of the BikeGeometry. It modifies the GeometryParameter but not the BikeGeometry.

	After calling this function in a GeometryParameter, it will:

	- Have a confidence value if we were able to validate it.
	- Have a new calculated value if we were able to validate it.

	:param parameter: GeometryParameter inside the BikeGeometry
	:param bike_geometry: the BikeGeometry
	:return: None
	"""
	if not parameter.is_number() or parameter.calculated_value is not None:
		# either not a number or it already has a calculated value
		# if the parameter reached this with a calculated value, it is skipped, as we do not validate those parameters
		# calculated by the `calculate_missing_parameters()` function
		return None

	equation_list = get_equations(parameter.name, bike_geometry.get_parameter_list())

	if len(equation_list) > 0:
		for formula in equation_list:
			new_values = solve_equation(formula, parameter.name, bike_geometry)

			if len(new_values) > 0:
				if parameter.value is None:
					# parameter has no value, this should never happen, but left here for legacy purposes
					logging.error("GeometryParameter('{}') has reached a deprecated code section in "
									"validate.validate_geometry_parameter".format(parameter.name))
					parameter.set_calculated_value(new_values)

				elif parameter.calculated_value is None:
					# only valid branch at this point as the rest are deprecated
					param_values = parameter.normalised_value

					if not isinstance(param_values, list):
						param_values = [param_values]

					# keep a list with similarity
					similarity_list = []
					for param_val in param_values:
						similarity_list.extend([(get_value_similarity(param_val, new_val), new_val) for new_val in new_values])

					if len(similarity_list) > 0:
						best_case = max(similarity_list, key=lambda l: l[0])

						# adjust confidence from the average of the list calculated earlier
						parameter.set_confidence(sum(map(lambda l: l[0], similarity_list)) / len(similarity_list))

						# set the calculated value to be the best value found
						parameter.set_calculated_value(best_case[1], change_confidence=False)

			else:
				# it should never reach this code either
				_set_confidence_from_deviation(parameter)
	else:
		# parameter could not be validated using maths, so use deviation from average statistics instead
		# note how invert is True, so we are getting (1 - deviation) for confidence
		_set_confidence_from_deviation(parameter)


def calculate_missing_parameters(bike_geometry: BikeGeometry, include_invalid: bool = True):
	"""
	Calculates missing GeometryParameters of a BikeGeometry if possible. It modifies the BikeGeometry in place!

	Missing parameters are defined in the function BikeGeometry.get_missing_parameter_list().
	It also includes invalid parameters, from the function get_invalid_parameters().

	:param bike_geometry: the BikeGeometry
	:param include_invalid: if it should calculate invalid parameters too, default is True
	:return: None
	"""
	# get a list with all the missing or invalid parameters (only the names)
	parameter_list = bike_geometry.get_missing_parameter_list()
	if include_invalid:
		parameter_list.extend(get_invalid_parameters(bike_geometry))

	# this loop can be executed in parallel if needed as it only modifies the parameter given in the arguments
	for param in parameter_list:
		calculate_parameter(param, bike_geometry)


def calculate_parameter(parameter_name: str, bike_geometry: BikeGeometry):
	"""
	Calculates the value of a parameter and sets it confidence value if it can derived from the geometry statistics.
	It modifies the GeometryParameter given in the BikeGeometry (or creates one if it does not exists).

	:param parameter_name: name of the GeometryParameter
	:param bike_geometry: the BikeGeometry
	:return: None
	"""
	parameter = bike_geometry.get_parameter(parameter_name)

	# check if parameter exists
	if parameter is None:
		parameter = GeometryParameter(parameter_name, None)
		bike_geometry.set_parameter(parameter)

	# check if it has already been calculated (e.g. in a previous iteration)
	elif parameter.calculated_value is not None:
		# skip this iteration
		return

	# set confidence from deviation first to save previous confidence (if it can be calculated)
	_set_confidence_from_deviation(parameter)

	equation_list = get_equations(parameter.name, bike_geometry.get_parameter_list())

	for formula in equation_list:
		new_values = solve_equation(formula, parameter.name, bike_geometry)

		if len(new_values) > 0:
			parameter.set_calculated_value(new_values, change_confidence=True)


def get_invalid_parameters(bike_geometry: BikeGeometry) -> list:
	"""
	Gets a list with the names of invalid GeometryParameters of a BikeGeometry that are numbers (that can be calculated).
	An invalid parameters is defined by the function is_parameter_invalid().

	Note: this function should be inside BikeGeometry, but is_parameter_invalid() uses the geometry constraints, thus
	it is best to keep the core of the datavalidation module (BikeGeometry) separated from the constraints module.

	:param bike_geometry: the BikeGeometry
	:return: list of invalid parameters (list of str)
	"""
	invalid_params = []

	for param in bike_geometry.get_parameter_list():
		if param.is_number() and is_parameter_invalid(param, bike_geometry):
			# this means that the parameter is likely wrong
			invalid_params.append(param.name)

	return invalid_params


def get_value_similarity(value1, value2) -> float:
	"""
	Gets the similarity between two values.
	The similarity is a number between 0 and 1 as a percentage where 1 means that the values are the same and 0
	means that the values are completely different.
	This function is duplicated in the constraints module. A common utility file could improve this...

	:param value1: value
	:param value2: value
	:return: (0 to 1) percentage float of how close value1 is to value2
	"""
	if isinstance(value2, list):
		# if value2 is a list, then return the one with least similarity from the whole similarity list
		val_list = [get_value_similarity(value1, x) for x in value2]
		return min(val_list)

	return float(min([value1, value2])) / float(max([value1, value2]))


def is_parameter_invalid(parameter: GeometryParameter, bike_geometry: BikeGeometry) -> bool:
	"""
	Checks if a GeometryParameter is invalid.

	A GeometryParameter is invalid if:

	- The parameter has very low confidence.
	- The parameter does not satisfy geometry constraints.
	- The parameter is too deviated from normal constraints.

	Note: this function should be inside BikeGeometry, but it uses the geometry constraints, thus
	it is best to keep the core of the datavalidation module (BikeGeometry) separated from the constraints module.

	:param parameter: GeometryParameter to check
	:param bike_geometry: BikeGeometry to make the comparison
	:return: bool, True if the parameter IS invalid
	"""
	# TODO: change the access to private member _PARAMETER_THRESHOLD
	return not check_parameter_constraints(parameter.name, bike_geometry) or (
		parameter.confidence is not None and parameter.confidence < bike_geometry._PARAMETER_THRESHOLD)


def _set_confidence_from_deviation(parameter: GeometryParameter):
	"""
	Sets the confidence value of the parameter based on its deviation from the normal geometry statistics.
	It is safe to call even when the deviation cannot be calculated.

	:param parameter: GeometryParameter to set confidence
	:return: None
	"""
	deviation = get_parameter_deviation(parameter, invert=True)
	if deviation is not None:
		parameter.set_confidence(deviation)
