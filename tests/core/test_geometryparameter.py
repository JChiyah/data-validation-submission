#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `geometryparameter` module

Author: Javier Chiyah
		Heriot-Watt University
"""


from datavalidation.core import GeometryParameter


json_dict = {
	"p": "head_tube",
	"v": "190",
	"id": "random_id"
}

empty_dict = {
	"p": "head_tube",
	"v": "",
	"id": "random_id"
}


def test_geometry_parameter():
	parameter1 = GeometryParameter("head_tube", "190")

	assert parameter1.name == "head_tube"
	assert parameter1.value == 190
	assert parameter1.original_value == "190"
	assert parameter1.type == float

	parameter2 = GeometryParameter("slug", "190")

	assert parameter2.name == "slug"
	assert parameter2.value == "190"
	assert parameter2.original_value == "190"
	assert parameter2.type == str

	assert parameter1.value != parameter2.value

	# make sure no crashes happen when a new GeometryParameter is initialised with None
	parameter3 = GeometryParameter("head_tube", None)

	assert parameter3.value is None


def test_geometry_parameter_from_json():
	parameter = GeometryParameter.from_dict(json_dict)

	assert parameter.to_dict() == json_dict

	assert parameter.name == json_dict['p']
	assert parameter.value == 190
	assert parameter.original_value == json_dict['v']
	assert parameter.type == float

	parameter = GeometryParameter.from_dict(empty_dict)
	assert parameter.to_dict() == empty_dict


def test_geometry_parameter_not_normalised():
	json_par = {
		"p": "head_tube",
		"v": "A 190aa$",
		"id": "random_id"
	}

	parameter = GeometryParameter.from_dict(json_par)

	assert parameter.value == json_par['v']

	parameter.set_normalised_value("190")

	assert parameter.value == 190

	parameter.set_normalised_value([190, 170])

	assert parameter.value == [190, 170]
