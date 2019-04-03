#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GeometryParameter
----------------------------------

Object that holds information about a parameter of a BikeGeometry. It contains several utility functions
to retrieve the parameter value, its confidence, calculated value, etc.

It also provides logic to convert from/to JSON representation.

Author: Javier Chiyah, Heriot-Watt University, 2019
"""


import logging

from .constants import GEOMETRY_PARAMETERS


class GeometryParameter:
	"""
	A GeometryParameter can be initialised with its name and value. The value can be None if it is used as a
	placeholder for a future value.

	Example initialisation::

		>> GeometryParamter("head_angle", 73)
		GeometryParameter() object
		# or
		>> GeometryParamter("head_angle", "73") # here "73" is casted to float without having to normalise
		GeometryParameter() object
		# or
		>> GeometryParamter("head_angle", None)
		GeometryParameter() object

	Normalising or validating the parameter changes the object in place and expand the available functionality with
	additional class member variables such as calculated_value.

	:param name: name of the parameter
	:param value: value of the parameter, either as string or the correct value
	:param extra_values: if there is anything else to store in the parameter, but not used (e.g. "id" field)
	"""

	_name = None
	_value = None
	_original_value = None
	_calculated_value = None
	_type = str
	_confidence = None
	_extra_values = {}

	def __init__(self, name: str, value, extra_values: dict = None):
		self._name = name
		self._original_value = value
		self._extra_values = extra_values if extra_values is not None else {}
		self._resolve_type()

		# try to set the value to the correct type directly
		try:
			self.set_normalised_value(value)

		except (ValueError, TypeError):
			if value is not None and value != "":
				logging.debug("GeometryParameter('{}') needs normalisation (v: '{}', {})".format(
					self.name, self.original_value, self.type
				))

	@classmethod
	def from_dict(cls, json_dict: dict):
		"""
		Creates a new GeometryParameter from a dictionary.

		Example dict::

			{
				"p": "parameter_name",
				"v": "parameter_value",
				"id": "optional additional field",
				...
			}

		:param json_dict: dict of the parameter (aka JSON)
		:return: GeometryParameter
		"""
		pname = json_dict['p']
		pvalue = json_dict['v']

		new_dict = dict(json_dict)
		del new_dict['p']
		del new_dict['v']

		return cls(
			name=pname,
			value=pvalue,
			extra_values=new_dict
		)

	@property
	def name(self) -> str:
		"""
		Gets the name of the parameter.

		:return: string name
		"""
		return self._name

	@property
	def value(self):
		"""
		Gets the most up to date value of the parameter (it can be the normalised value, the calculated value or
		the original value if none of those is available).
		It will return the value in the correct type (e.g. integers will return as int) and it will not produce
		exceptions if there is something wrong with the GeometryParameter value.

		In order, it provides:
		- the calculated value if such exists
		- the normalised value if the parameter has been normalised
		- the original value in the correct type (if it can cast it, e.g. "17" can be easily casted to float)
		- the original value as a string if all above fails

		You should check other functions if you require one of these values in particular instead.

		:return: [int|float|str] value
		"""
		if self._calculated_value:
			return self.calculated_value
		elif self._value is None and self._original_value:
			return str(self._original_value)
		else:
			return self._value

	@property
	def normalised_value(self):
		"""
		Gets the normalised value of the parameter, without taking the calculated value into account.
		It will return the value in the correct type (e.g. integers will return as int).

		If the GeometryParameter has not been normalised, it will return the original parameter instead.

		:return: [int|float|str] value
		"""
		if self._value is None and self._original_value:
			return str(self._original_value)
		else:
			return self._value

	@property
	def original_value(self) -> str:
		"""
		Gets the original value of the GeometryParameter as a string, regardless of its true type.

		:return: string value
		"""
		return self._original_value

	@property
	def calculated_value(self):
		"""
		Gets the calculated value of the parameter if one exists.
		It will return the value in the correct type (e.g. integers will return as int).

		:return: [int|float|str] value or None
		"""
		return self._calculated_value

	@property
	def type(self):
		"""
		Gets the type of the GeometryParameter.

		:return: type
		"""
		return self._type

	@property
	def confidence(self) -> float:
		"""
		Gets the confidence score of the GeometryParameter.

		:return: float confidence score
		"""
		return self._confidence

	def set_normalised_value(self, new_value):
		"""
		Sets the value of the GeometryParameter after normalising its value.

		It will raise an exception if the new value is not a valid type.

		It gets the new value (e.g., a str) and casts it to the correct type (e.g., float) to make sure it does not
		violate any constraints of normalised parameters.
		It can also accept a list, which means a range of values (e.g., [190, 170]).

		:param new_value: normalised value
		:return: None
		:raise ValueError: raised if the new value cannot be casted into the correct type
		:raise TypeError: raised if the new value is None or the empty string
		"""
		if isinstance(new_value, list):
			# handle ranges
			self._value = [self.type(x) for x in new_value]

		else:
			self._value = self.type(new_value)

		# logging.debug("GeometryParameter('{}') has a new normalised value: '{}'".format(self.name, self._value))

	def set_calculated_value(self, new_value, change_confidence: bool = True):
		"""
		Sets the calculated value of the GeometryParameter.

		It will raise an exception if the new value is not a valid type.

		:param new_value: calculated value
		:param change_confidence: if True, it will change confidence, default is False
		:return: None
		:raise ValueError: raised if the new value cannot be casted into the correct type
		:raise TypeError: raised if the new value is None or the empty string
		"""
		if self._calculated_value is None:
			if isinstance(new_value, list):
				if len(new_value) == 1:
					self._calculated_value = self.type(new_value[0])
				else:
					self._calculated_value = [self.type(x) for x in new_value]
			else:
				self._calculated_value = self.type(new_value)

			if self._value is None:
				logging.info("GeometryParameter('{}') has a new calculated value: {}".format(self.name, self.value))

			if change_confidence and self._confidence is None:
				self.set_confidence(0.75)

		else:
			# do not change the calculated value
			logging.warning("GeometryParameter('{}') already has a calculated value (current={}, new={})".format(
				self.name, self._calculated_value, new_value
			))

	def set_confidence(self, confidence: float, force: bool = False):
		"""
		Sets the confidence score of the GeometryParameter.
		Note that it will average the current confidence value with the one given to smooth differences in precision of
		the equations. It also rounds the confidence to be within the range of 0 to 1 (inclusive)

		:param confidence: new confidence value
		:param force: if True, it will force the confidence change. Otherwise, it chooses the highest (default is False)
		:return: None
		"""
		if self._confidence is None or force or self.calculated_value is None:
			if self._confidence is None:
				self._confidence = confidence

			else:
				self._confidence = (self._confidence + confidence) / 2
				if self.confidence < 0 or self.confidence > 1:
					logging.warning("GeometryParameter('{}') has confidence value of '{}' (outside the 0-1 range)".format(
						self.name, self.confidence))
					self._confidence = 0 if self.confidence < 0 else 1

	def is_number(self) -> bool:
		"""
		Checks if the GeometryParameter is a number type (float or int, but not a string or unknown).
		It is used to check if the GeometryParameter needs to be normalised or validated.

		:return: bool, True if the GeometryParameter is a float or an int
		"""
		return self.type is not str

	def to_dict(self, string_values: bool = True) -> dict:
		"""
		Returns the GeometryParameter as a dictionary ready to be serialised into a JSON response. It packs all the
		information currently contained in the GeometryParameter.

		:param string_values: whether to return the values in string format or not, default is True
		:return: dict
		"""
		json_dict = {
			"p": self.name,
			**self._extra_values
		}

		if self.value is not None:
			json_dict['v'] = self._format_parameter_value(self.value) if string_values else self.value
		else:
			json_dict['v'] = ""

		if self.original_value != json_dict['v']:
			json_dict['original_v'] = self.original_value

		if self.calculated_value is not None:
			json_dict['v'] = self._value if self._value is not None else self.calculated_value
			json_dict['v'] = self._format_parameter_value(json_dict['v']) if string_values else json_dict['v']
			json_dict['calculated_v'] = self._format_parameter_value(self.calculated_value) \
				if string_values else self.calculated_value

		if self.confidence is not None:
			json_dict['confidence'] = self.confidence

		return json_dict

	def _resolve_type(self):
		"""
		Resolves the type of the GeometryParameter from the list of names.

		:return: None
		"""
		try:
			self._type = GEOMETRY_PARAMETERS[self.name]
		except KeyError:
			logging.warning("Unknown GeometryParameter name '{}', defaulting to type str".format(self.name))

	@staticmethod
	def _format_parameter_value(value) -> str:
		"""
		Formats a value to a string, taking the final 0s if the value is a float.

		E.g. "1.000000" becomes "1"

		:param value: value to convert to string
		:return: string
		"""
		if "." in str(value):
			return str(value).rstrip("0").rstrip(".")
		else:
			return str(value)
