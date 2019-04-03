#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `geometryparameter` module

Author: Javier Chiyah
		Heriot-Watt University
"""


from datavalidation.core import GeometryParameter
from datavalidation.normalisation.number import normalise_range
from datavalidation.normalisation.measure import normalise_range_measure


# this parameter tests the measure checks
wheelbase_param = {
	"p": "wheelbase",
	"v": "39.92 / 1014"
}

stack_param = {
	"p": "stack",
	"v": "20.98 / 533"
}

# normalisation should NOT affect this parameter
axle_spacing_param = {
	"p": "axle_spacing",
	"v": "135/110"
}


def test_normalise_range_measure():
	test_param = GeometryParameter.from_dict(wheelbase_param)

	normalise_range(test_param)
	normalise_range_measure(test_param)

	assert test_param.value == 1014

	# stack
	test_param = GeometryParameter.from_dict(stack_param)

	normalise_range(test_param)
	normalise_range_measure(test_param)

	assert test_param.value == 533

	# axle spacing
	test_param = GeometryParameter.from_dict(axle_spacing_param)

	normalise_range(test_param)
	normalise_range_measure(test_param)

	assert test_param.value == [135, 110]
