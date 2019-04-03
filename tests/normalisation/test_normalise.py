#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `normalise` module

Author: Javier Chiyah
		Heriot-Watt University
"""


from datavalidation.core import BikeGeometry, GeometryParameter
from datavalidation.normalisation.normalise import normalise_bike_geometry, normalise_parameter


# this parameter should be normalised to [135, 110]
axle_spacing_param = {
	"p": "axle_spacing",
	"v": "135/110"
}

# this parameter does not need normalisation
head_angle_param = {
	"p": "head_angle",
	"v": "70"
}

# this parameter should be normalised to 190
head_tube_param = {
	"p": "head_tube",
	"v": "A 190aa$"
}

# this parameter should not be normalised
slug_param = {
	"p": "slug",
	"v": "random_slug_value"
}

# this parameter should not crash (empty value)
bb_height_param = {
	"p": "bb_height",
	"v": ""
}

# this parameter tests the measure checks
wheelbase_param = {
	"p": "wheelbase",
	"v": "39.92 / 1014"
}

geometry_dict = {
	"parameter_list":
		[axle_spacing_param, head_angle_param, head_tube_param, slug_param, bb_height_param, wheelbase_param]
}


def test_normalise_bike_geometry():
	bike = BikeGeometry(geometry_dict)

	assert bike.get_parameter_value("axle_spacing") == axle_spacing_param['v']

	normalise_bike_geometry(bike)

	assert all(x is not None for x in bike.get_parameter_list())

	test_param = bike.get_parameter_value("axle_spacing")
	assert isinstance(test_param, list)
	assert len(test_param) == 2
	assert test_param[0] == 135 and test_param[1] == 110

	test_param = bike.get_parameter_value("head_tube")
	assert test_param == 190

	test_param = bike.get_parameter_value("head_angle")
	assert test_param == 70

	test_param = bike.get_parameter_value("slug")
	assert test_param == slug_param['v']

	test_param = bike.get_parameter_value("wheelbase")
	assert test_param == 1014
