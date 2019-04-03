#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
equations
----------------------------------

File containing different formulae and equations to validate bike geometries.

Author: Javier Chiyah, Heriot-Watt University, 2019
"""


# The core of the mathematical model of bikes.
# Some notes:
#   - all equations must be equalled to 0 (e.g. equation = 0)
#   - equations are automatically reordered to solve different parameters
#   - if you want to add more equations, do not reorder or derive from those already here, as each equation increases
#   considerably the execution time of the validation step
#   - be careful when adding trigonometry such as inverse sine or cosine operations, as they may lead to unsolvable
#   equations. It is sometimes best to strive for tangents (or inverse tangents) if possible, and use ATAN2 instead
VALIDATION_FORMULAE = [
	{
		"equation": "{top_tube} - {stack} * TAN((90 - {seat_angle}) / 180 * PI) - {reach}",
		"parameters": [
			"reach",
			"stack",
			"seat_angle",
			"top_tube"
		]
	},
	{
		"equation": "SQRT( {bb_drop}^2 + ({wheelbase} - SQRT( {front_centre}^2 - {bb_drop}^2 ))^2 ) - {chainstay}",
		# "equation": "SQRT( ({wheelbase} - ( SQRT( {front_centre}^2 - {bb_drop}^2 )) )^2 + {bb_drop}^2 ) - {chainstay}",
		"parameters": [
			"bb_drop",
			"chainstay",
			"wheelbase",
			"front_centre"
		]
	},
	{
		"equation": "SQRT({seat_tube_length_eff}^2 - {stack}^2) + {reach} - {top_tube}",
		"parameters": [
			"stack",
			"reach",
			"top_tube",
			"seat_tube_length_eff"
		]
	},
	{
		"equation": "SIN({head_angle} / 180 * PI) * ({head_tube} + {fork_length} - {fork_rake} * COS({head_angle} / 180 * PI)) + {bb_drop} - {stack}",
		"parameters": [
			"stack",
			"bb_drop",
			"head_tube",
			"fork_rake",
			"head_angle",
			"fork_length"
		]
	},
	{
		"equation": "{stack} / COS((90 - {seat_angle}) / 180 * PI) - {seat_tube_length_eff}",
		"parameters": [
			"stack",
			"seat_angle",
			"seat_tube_length_eff"
		]
	},
	{
		# be careful with the comma in the middle of the equation so we can use ATAN2
		"equation": "(ATAN2( ( {stack} - {bb_drop} ) , ( SQRT( {front_centre}^2 - {bb_drop}^2 ) - {reach} - {fork_rake} ) ) * 180 / PI) - {head_angle}",
		"parameters": [
			"stack",
			"reach",
			"bb_drop",
			"fork_rake",
			"head_angle",
			"front_centre"
		]
	}

]


# dictionary with things to substitute in the equations above. It goes in order when substituting.
SUBS_DICT = {
	"PI": "sympy.pi",
	"SIN": "sympy.sin",
	"COS": "sympy.cos",
	"ATAN2": "sympy.atan2",
	"TAN": "sympy.tan",
	"SQRT": "sympy.sqrt",
	"^": "**"
}
