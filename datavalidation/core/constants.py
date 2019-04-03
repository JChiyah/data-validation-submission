#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
constants
----------------------------------

Module containing different package-wide constants

Author: Javier Chiyah, Heriot-Watt University, 2019
"""

import operator


# list of all parameters with their respective type
# note that only those that have `float` here will be normalised
GEOMETRY_PARAMETERS = {

	# OMITTED DUE TO CONFIDENTIAL INFORMATION
	# It may come back in the future

}


# the geometry constraints
GEOMETRY_CONSTRAINTS = {
	"chainstay": [
		("<", "wheelbase")
	],
	"front_centre": [
		("<", "wheelbase")
	],
	"seat_tube_length": [
		(">", "seat_tube_length_cc"),
		("<", "seat_tube_length_eff")
	],
	"seat_tube_length_cc": [
		("<", "seat_tube_length"),
		("<", "seat_tube_length_eff")
	],
	"seat_tube_length_eff": [
		(">", "seat_tube_length"),
		(">", "seat_tube_length_cc")
	],
	"top_tube": [
		(">", "top_tube_actual")
	],
	"top_tube_actual": [
		("<", "top_tube")
	],
	"wheelbase": [
		(">", "chainstay"),
		(">", "front_centre")
	]
}

# operators referenced in the GEOMETRY_CONSTRAINTS dict
OPERATORS = {
	"<": operator.lt,
	"<=": operator.le,
	">": operator.gt,
	">=": operator.ge
}


# some geometry statistics
GEOMETRY_STATISTICS = {

	# OMITTED DUE TO CONFIDENTIAL INFORMATION
	# It may come back in the future

}


# these are the parameters that we can validate based on the mathematical model, equations and the geometry statistics
VALIDATABLE_PARAMETER_LIST = [
	"bb_drop", "chainstay", "front_centre", "fork_length", "fork_rake", "head_angle", "head_tube", "reach",
	"stack", "seat_angle", "seat_tube_length", "seat_tube_length_cc", "seat_tube_lenght_eff", "top_tube", "wheelbase"
]


TOTAL_VALIDATABLE_PARAMETERS = len(VALIDATABLE_PARAMETER_LIST)
