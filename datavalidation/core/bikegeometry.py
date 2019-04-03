#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BikeGeometry
----------------------------------

Main object of the datavalidation package.
It holds information about a bike geometry, including its parameters and certain config options.
It also provides logic to work with bike geometries and to convert from/to JSON representation.

Author: Javier Chiyah, Heriot-Watt University, 2019
"""


import logging

from .geometryparameter import GeometryParameter
from .constants import GEOMETRY_PARAMETERS, VALIDATABLE_PARAMETER_LIST, TOTAL_VALIDATABLE_PARAMETERS


class BikeGeometry:
	"""
	A BikeGeometry can be initialised with a JSON-like dict with a list of parameters.

	If the dict given contains more elements than those needed by the BikeGeometry itself, it will save
	and output them when the BikeGeometry is converted back to a dict.
	For instance, giving a field "id" would return the same field with the values at the end.

	Example valid dict::

		{
			"parameter_list": [
				{
					"p": "reach",
					"v": "371",
					"id": "**any-value**"
				},
				{
					"p": "stack",
					"v": "533",
					"id": "**any-value**"
				}
			}
		}

	There is a @classmethod available if you need to create a BikeGeometry from a dict of parameters instead.

	:param json_dict: dict with the bike geometry information
	"""

	# config values
	# thresholds - it will mark geometries or parameters as invalid if confidence is below this threshold
	_GEOMETRY_THRESHOLD = 0.7
	_PARAMETER_THRESHOLD = 0.7

	_OPTIMISTIC_VALIDATION = False
	_COUNT_CALCULATED_PARAMETERS = False

	_extra_values = {}

	_validated_params = 0
	_calculated_params = 0

	_parameters = {
		"slug": None,
		"alt_size": None,
		"axle_spacing": None,
		"axle_to_crown": None,
		"bb_drop": None,
		"bb_height": None,
		"bb_type": None,
		"bike_slug": None,
		"chainstay": None,
		"crank_length": None,
		"fork_length": None,
		"fork_rake": None,
		"front_centre": None,
		"front_sus_travel": None,
		"handlebar_drop": None,
		"handlebar_reach": None,
		"handlebar_width": None,
		"head_angle": None,
		"head_tube": None,
		"pad_reach": None,
		"pad_stack": None,
		"reach": None,
		"rear_sus_travel": None,
		"saddle_height": None,
		"seat_angle": None,
		"seat_clamp_size": None,
		"seat_tube_length": None,
		"seat_tube_length_cc": None,
		"seat_tube_length_eff": None,
		"seatpost_diameter": None,
		"seatpost_length": None,
		"seatpost_offset": None,
		"shock_size": None,
		"size": None,
		"stack": None,
		"standover": None,
		"stem_angle": None,
		"stem_length": None,
		"top_tube": None,
		"top_tube_actual": None,
		"trail": None,
		"type": None,
		"tyre_width": None,
		"wheel_size": None,
		"wheelbase": None,
		"year": None
	}

	def __init__(self, json_dict: dict):
		# this makes sure that the parameters are None to start with, to avoid Python messing with the objects at run-time
		for key in self._parameters.keys():
			self._parameters[key] = None

		self._from_json(json_dict)

	@classmethod
	def from_parameter_dict(cls, json_dict: dict):
		"""
		Creates a new BikeGeometry from a dictionary of parameters. This is used mostly in testing.
		Example dict::

			{
				"parameter1": "value1",
				"parameter2": "value2"
			}

		:param json_dict: dict of parameters
		:return: BikeGeometry
		"""
		result = []
		for key, val in json_dict.items():
			result.append({
				"p": key,
				"v": val
			})

		return cls({"parameter_list": result})

	def get_parameter(self, parameter_name: str):
		"""
		Gets a GeometryParameter of this BikeGeometry.
		It returns None if the parameter has not been initialised or does not exists.

		Example usage::

			>> bike.get_parameter("slug")
			GeometryParameter()

		:param parameter_name: name of the parameter
		:return: GeometryParameter or None
		"""
		return self._parameters[parameter_name]

	def get_parameter_value(self, parameter_name: str):
		"""
		Gets the value of a GeometryParameter of this BikeGeometry.
		It returns None if the parameter is missing, does not exists or if its value is None.

		Example usage::

			>> bike.get_parameter_value("slug")
			"bike_slug_name"
			# this is also equivalent
			>> bike.get_parameter("slug").value
			"bike_slug_name"

		:param parameter_name: name of the parameter
		:return: the value of the parameter, which can be str, int, float (or None if it does not exists)
		"""
		try:
			return (self._parameters[parameter_name]).value

		except KeyError:
			logging.warning("Trying to retrieve missing GeometryParameter('{}'), defaulting to None".format(parameter_name))
			return None

		except AttributeError:
			logging.debug("GeometryParameter('{}') empty, defaulting to None".format(parameter_name))
			return None

	def get_parameter_list(self, filter_empty: bool = True) -> list:
		"""
		Gets a list with all the parameters from the BikeGeometry. It filters empty/invalid parameters by default.

		:param filter_empty: whether to filter empty parameters (those that are None or their value is empty), True by default
		:return: list of GeometryParameter
		"""
		if not filter_empty:
			return [val for key, val in self._parameters.items()]

		return [val for key, val in self._parameters.items() if not self._is_parameter_empty(key)]

	def get_missing_parameter_list(self) -> list:
		"""
		Gets a list of all the parameters that are missing (e.g. None value, "" value, etc).
		It only returns those parameters that can be calculated based on constants.VALIDATABLE_PARAMETERS_LIST

		:return: list of parameter names (list of str)
		"""
		return [key for key in self._parameters.keys()
			if self._is_parameter_empty(key) and key in VALIDATABLE_PARAMETER_LIST]

	def get_confidence_score(self):
		"""
		Gets the confidence score of this BikeGeometry. It is None if no validation has been performed on this
		BikeGeometry.

		The confidence score is how confident we are that the parameters of this BikeGeometry fit together. The score is
		calculated only when this function is called, without updating parameters confidences when these change.
		Therefore, it is safe for parallel execution, but it is best not to call this function too often as it may
		take some time to calculate.

		:return: float from 0 to 1, or None if no validation has been performed
		"""
		validated_param_list = [(param.name, param.confidence) for param in self.get_parameter_list()
			if param.confidence is not None and param.is_number() and param.normalised_value is not None]

		if len(validated_param_list) > 0:
			confidence = 0

			if self._OPTIMISTIC_VALIDATION:
				# optimistic validation
				confidence = sum(map(lambda l: l[1], validated_param_list)) / len(validated_param_list)

			elif self._COUNT_CALCULATED_PARAMETERS:
				# pessimist validation that takes all the possible validatable parameters into account
				total_validated_calculated_params = len([(param.name, param.confidence) for param in self.get_parameter_list()
					if param.confidence is not None and param.is_number()])
				confidence = sum(map(lambda l: l[1], validated_param_list)) / total_validated_calculated_params

			else:
				# very pessimistic validation
				confidence = sum(map(lambda l: l[1], validated_param_list)) / TOTAL_VALIDATABLE_PARAMETERS

			self._validated_params = len(validated_param_list)
			logging.info("BikeGeometry confidence score = {} (validated params = {}/{})".format(
				confidence, self._validated_params, TOTAL_VALIDATABLE_PARAMETERS))

			validated_names_list = [x[0] for x in validated_param_list]
			logging.debug("GeometryParameters validated: {}".format(validated_names_list))

			logging.debug("GeometryParameters not validated: {}".format(
				[x for x in VALIDATABLE_PARAMETER_LIST if x not in validated_names_list]))
			return confidence

		else:
			return None

	def set_parameter(self, parameter: GeometryParameter):
		"""
		Sets a parameter of the BikeGeometry. This is used to set the parameters of the BikeGeometry when they
		were missing from the initialisation dict.
		Note that it substitutes the value, overriding whatever was before!

		:param parameter: GeometryParameter
		:return: None
		"""
		self._parameters[parameter.name] = parameter

	def to_dict(self, string_values=True) -> dict:
		"""
		Returns the value as a dict type so it can be serialised in a JSON response.

		:param string_values: whether to return the values in string format or not. Default is True, so everything is
			returned as string
		:return: dict object similar to that given in the __init__ function
		"""
		parameter_list = []
		for param_name, param_value in self._parameters.items():
			if param_value is not None:
				param_dict = param_value.to_dict(string_values)
				# add invalid True or False depending on threshold
				if "confidence" in param_dict:
					param_dict['invalid'] = param_dict['confidence'] < self._PARAMETER_THRESHOLD

				parameter_list.append(param_dict)

		geometry_dict = {
			"parameter_list": parameter_list,
			"geometry_threshold": self._GEOMETRY_THRESHOLD,
			"parameter_threshold": self._PARAMETER_THRESHOLD,
			"optimistic_validation": self._OPTIMISTIC_VALIDATION,
			"count_calculated_params": self._COUNT_CALCULATED_PARAMETERS,
			**self._extra_values
		}

		confidence = self.get_confidence_score()
		if confidence is not None:
			geometry_dict['confidence'] = confidence
			geometry_dict['invalid'] = confidence < self._GEOMETRY_THRESHOLD
			geometry_dict['validated_parameters'] = self._validated_params
			geometry_dict['validatable_parameters'] = TOTAL_VALIDATABLE_PARAMETERS

		return geometry_dict

	def _from_json(self, json_dict: dict):
		"""
		Initialises the several class members of the BikeGeometry from a dict. See __init__ for more information.

		:param json_dict: dict object
		:return: None
		"""
		for key, value in json_dict.items():
			if key == "parameter_list":
				self._set_parameters(value)

			elif key == "geometry_threshold":
				try:
					self._GEOMETRY_THRESHOLD = float(value)
				except ValueError:
					logging.warning("Value in 'geometry_threshold' not valid, it must be between 0 and 1. Defaulting to {}".format(self._GEOMETRY_THRESHOLD))

			elif key == "parameter_threshold":
				try:
					self._PARAMETER_THRESHOLD = float(value)
				except ValueError:
					logging.warning("Value in 'parameter_threshold' not valid, it must be between 0 and 1. Defaulting to {}".format(self._PARAMETER_THRESHOLD))

			elif key == "optimistic_validation":
				self._OPTIMISTIC_VALIDATION = bool(value)

			elif key == "count_calculated_params":
				self._COUNT_CALCULATED_PARAMETERS = bool(value)

			else:
				# setattr(self, "_" + key, value)
				self._extra_values[key] = value

	def _set_parameters(self, parameter_list: list):
		"""
		Initialises the GeometryParameters of the BikeGeometry from a list of parameters.

		:param parameter_list: list of parameter objects
		:return: None
		"""
		for parameter in parameter_list:
			try:
				self._parameters[parameter['p']] = GeometryParameter.from_dict(parameter)
			except KeyError:
				logging.warning("Unknown GeometryParameter('{}'), ignoring it".format(str(parameter)))

	def _is_parameter_empty(self, parameter_name: str) -> bool:
		"""
		Checks if a GeometryParameter is empty. In other words, if the parameter is None or
		its value is None or the empty string.

		:return: bool, True if parameter is empty
		"""
		return parameter_name in self._parameters \
				and (self._parameters[parameter_name] is None
				or self._parameters[parameter_name].value is None
				or self._parameters[parameter_name].value == "")
