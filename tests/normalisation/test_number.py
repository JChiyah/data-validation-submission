#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `geometryparameter` module

Author: Javier Chiyah
		Heriot-Watt University
"""


from datavalidation.core import GeometryParameter
from datavalidation.normalisation.number import normalise_number, normalise_float, normalise_range, is_range_parameter


# this parameter should be normalised to [135, 110]
axle_spacing_param1 = {
	"p": "axle_spacing",
	"v": "135/110"
}

axle_spacing_param2 = {
	"p": "axle_spacing",
	"v": "135 - 110mm"
}

axle_spacing_param3 = {
	"p": "axle_spacing",
	"v": "135°-110.2m/90."
}

axle_spacing_param4 = {
	"p": "axle_spacing",
	"v": "135 mm / 110.2m "
}

# this parameter does not need normalisation
head_angle_param = {
	"p": "head_angle",
	"v": "70"
}

# this parameter should be normalised to 190.1
head_tube_param1 = {
	"p": "head_tube",
	"v": "A 190.1aa$"
}

# this parameter should be normalised to 190.1
head_tube_param2 = {
	"p": "head_tube",
	"v": "A 190,1aa$"
}

# this should not be a range
head_tube_param3 = {
	"p": "head_tube",
	"v": "A -190,1aa$"
}


def test_normalise_number():
	test_param = GeometryParameter.from_dict(head_tube_param1)
	normalise_number(test_param)

	assert test_param.value == 190.1

	test_param = GeometryParameter.from_dict(head_angle_param)
	normalise_number(test_param)

	assert test_param.to_dict() == head_angle_param

	# param 2
	test_param = GeometryParameter.from_dict(head_tube_param3)
	assert not is_range_parameter(test_param)

	normalise_number(test_param)

	assert test_param.value == -190.1


def test_normalise_float():
	test_param = GeometryParameter.from_dict(head_tube_param2)
	normalise_float(test_param)

	assert test_param.value == 190.1

	test_param = GeometryParameter.from_dict(head_angle_param)
	normalise_float(test_param)
	# print(type(70.0),'test')
	# print(type(test_param.value + 0),)
	assert test_param.value == 70


def test_normalise_range():
	# param 1
	test_param = GeometryParameter.from_dict(axle_spacing_param1)

	assert is_range_parameter(test_param)
	assert test_param.value == axle_spacing_param1['v']

	normalise_range(test_param)

	assert isinstance(test_param.value, list)
	assert len(test_param.value) == 2
	assert test_param.value[0] == 135 and test_param.value[1] == 110

	# param 2
	test_param = GeometryParameter.from_dict(axle_spacing_param2)

	assert is_range_parameter(test_param)

	normalise_range(test_param)

	assert isinstance(test_param.value, list)
	assert len(test_param.value) == 2
	assert test_param.value[0] == 135 and test_param.value[1] == 110

	# param 3
	test_param = GeometryParameter.from_dict(axle_spacing_param3)

	assert is_range_parameter(test_param)

	normalise_range(test_param)

	assert isinstance(test_param.value, list)
	assert len(test_param.value) == 3
	assert test_param.value[0] == 135 and test_param.value[1] == 110.2 and test_param.value[2] == 90

	# param 4
	test_param = GeometryParameter.from_dict(axle_spacing_param4)

	assert is_range_parameter(test_param)

	normalise_range(test_param)

	assert isinstance(test_param.value, list)
	assert len(test_param.value) == 2
	assert test_param.value[0] == 135 and test_param.value[1] == 110.2
