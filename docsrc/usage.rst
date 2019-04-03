=====
Usage
=====

To use Data Validation in a project::


    import datavalidation.datavalidation as dv

    request = { ... } # your bike request, possibly from a HTTP request, see below

    validated_bike_response = dv.request_validate_bike_geometry(request)

    # OR to validate multiple geometries without request

    bike_geometry_list = [
        { ... } # bike geometry
    ]

    validated_bike_geometry_list = dv.validate_bike_geometry_list(bike_geometry_list)

    # OR to validate only one geometry

    single_bike_geometry = {
        "parameter_list": [
            {
                "p": "wheelbase",
                "v": "1024"
            }
            # ... more parameters as needed
        ]
    }

    validated_bike_geometry = dv.validate_bike_geometry(single_bike_geometry)





Example Bike Request
--------------------

A request to validate bike geometries can have multiple bike geometries at the same time and these bike geometries do not need to have all the parameters in them.

An example valid request would look like this::

    # valid bike request
    {
        "geometries": [
            {
                "geometry_threshold": 0.7,
                "parameter_threshold": 0.7,
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
                    },
                    {
                        "p": "top_tube",
                        "v": "534",
                        "id": "**any-value**"
                    },
                    {
                        "p": "seat_tube_length",
                        "v": "",
                        "id": "**any-value**"
                    },
                    {
                        "p": "seat_tube_length_cc",
                        "v": "",
                        "id": "**any-value**"
                    },
                    {
                        "p": "seat_tube_length_eff",
                        "v": "",
                        "id": "**any-value**"
                    },
                    {
                        "p": "head_angle",
                        "v": "71",
                        "id": "**any-value**"
                    },
                    {
                        "p": "seat_angle",
                        "v": "73",
                        "id": "**any-value**"
                    },
                    {
                        "p": "head_tube",
                        "v": "107",
                        "id": "**any-value**"
                    },
                    {
                        "p": "chainstay",
                        "v": "430",
                        "id": "**any-value**"
                    },
                    {
                        "p": "wheelbase",
                        "v": "1014",
                        "id": "**any-value**"
                    },
                    {
                        "p": "front_centre",
                        "v": "",
                        "id": "**any-value**"
                    },
                    {
                        "p": "bb_drop",
                        "v": "57.5",
                        "id": "**any-value**"
                    }
                ]
            }
        ]
    }




Example Response
----------------


An example response of validated bike geometries would look like this::

    {
        "geometries": [
            {
                "geometry_threshold": 0.7,
                "parameter_threshold": 0.7,
                "optimistic_validation": False,
                "count_calculated_params": False,
                "confidence": 0.5999918164974749,
                "invalid": True,
                "validated_parameters": 9,
                "validatable_parameters": 15,
                "parameter_list": [
                    {
                        "p": "axle_spacing",
                        "v": "",
                        "original_v": None
                    },
                    {
                        "p": "bb_drop",
                        "id": "**any-value**",
                        "v": "57.5",
                        "original_v": "57.5",
                        "calculated_v": "57.49999999999998",
                        "confidence": 0.9999999999999997,
                        "invalid": False
                    },
                    {
                        "p": "bb_height",
                        "v": "",
                        "original_v": None
                    },
                    {
                        "p": "chainstay",
                        "id": "**any-value**",
                        "v": "430",
                        "calculated_v": "430",
                        "confidence": 1.0,
                        "invalid": False
                    },
                    {
                        "p": "crank_length",
                        "v": "",
                        "original_v": None
                    },
                    {
                        "p": "fork_length",
                        "v": "413.197384616416",
                        "original_v": None,
                        "calculated_v": "413.197384616416",
                        "confidence": 0.75,
                        "invalid": False
                    },
                    {
                        "p": "fork_rake",
                        "v": "53.13403806646118",
                        "original_v": None,
                        "calculated_v": "53.13403806646118",
                        "confidence": 0.75,
                        "invalid": False
                    },
                    {
                        "p": "front_centre",
                        "id": "**any-value**",
                        "v": "590.6672221146129",
                        "original_v": "",
                        "calculated_v": "590.6672221146129",
                        "confidence": 0.75,
                        "invalid": False
                    },
                    {
                        "p": "handlebar_drop",
                        "v": "",
                        "original_v": None
                    },
                    {
                        "p": "handlebar_width",
                        "v": "",
                        "original_v": None
                    },
                    {
                        "p": "head_angle",
                        "id": "**any-value**",
                        "v": "71",
                        "original_v": "71",
                        "calculated_v": "70.9999999999999",
                        "confidence": 0.9999999999999986,
                        "invalid": False
                    },
                    {
                        "p": "head_tube",
                        "id": "**any-value**",
                        "v": "107",
                        "original_v": "107",
                        "calculated_v": "107.00000000000028",
                        "confidence": 0.9999999999999973,
                        "invalid": False
                    },
                    {
                        "p": "reach",
                        "id": "**any-value**",
                        "v": "371",
                        "original_v": "371",
                        "calculated_v": "371.045546782534",
                        "confidence": 0.999877247462127,
                        "invalid": False
                    },
                    {
                        "p": "saddle_height",
                        "v": "",
                        "original_v": None
                    },
                    {
                        "p": "seat_angle",
                        "id": "**any-value**",
                        "v": "73",
                        "calculated_v": "73",
                        "confidence": 1.0,
                        "invalid": False
                    },
                    {
                        "p": "seat_tube_length",
                        "id": "**any-value**",
                        "v": ""
                    },
                    {
                        "p": "seat_tube_length_cc",
                        "id": "**any-value**",
                        "v": ""
                    },
                    {
                        "p": "seat_tube_length_eff",
                        "id": "**any-value**",
                        "v": "557.3537062076499",
                        "original_v": "",
                        "calculated_v": "557.3537062076499",
                        "confidence": 0.75,
                        "invalid": False
                    },
                    {
                        "p": "seatpost_diameter",
                        "v": "",
                        "original_v": None
                    },
                    {
                        "p": "seatpost_length",
                        "v": "",
                        "original_v": None
                    },
                    {
                        "p": "stack",
                        "id": "**any-value**",
                        "v": "533",
                        "original_v": "533",
                        "calculated_v": "533.0000000000001",
                        "confidence": 0.9999999999999998,
                        "invalid": False
                    },
                    {
                        "p": "standover",
                        "v": "",
                        "original_v": None
                    },
                    {
                        "p": "stem_length",
                        "v": "",
                        "original_v": None
                    },
                    {
                        "p": "top_tube",
                        "id": "**any-value**",
                        "v": "534",
                        "original_v": "534",
                        "calculated_v": "534",
                        "confidence": 1.0,
                        "invalid": False
                    },
                    {
                        "p": "top_tube_actual",
                        "v": "",
                        "original_v": None
                    },
                    {
                        "p": "trail",
                        "v": "",
                        "original_v": None
                    },
                    {
                        "p": "tyre_width",
                        "v": "",
                        "original_v": None
                    },
                    {
                        "p": "wheelbase",
                        "id": "**any-value**",
                        "v": "1014",
                        "calculated_v": "1014",
                        "confidence": 1.0,
                        "invalid": False
                    }
                ]
            }
        ]
    }


This response was filled with the additional parameters missing from the previous request.
