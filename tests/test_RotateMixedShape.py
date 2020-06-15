"""
This file is part of PARAMAK which is a design tool capable
of creating 3D CAD models compatible with automated neutronics
analysis.

PARAMAK is released under GNU General Public License v3.0.
Go to https://github.com/Shimwell/paramak/blob/master/LICENSE
for full license details.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Copyright (C) 2019  UKAEA

THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
"""

import unittest

import pytest

from paramak import RotateMixedShape


class test_object_properties(unittest.TestCase):
    def test_absolute_shape_volume(self):
        """creates a rotated shape using straight and spline connections and \
                checks the volume is correct"""

        test_shape = RotateMixedShape(
            points=[
                (0, 0, "straight"),
                (0, 20, "spline"),
                (20, 20, "spline"),
                (20, 0, "spline")
            ]
        )

        test_shape.rotation_angle = 360
        test_shape.create_solid()

        assert test_shape.solid is not None
        assert test_shape.volume > 100

        test_shape2 = RotateMixedShape(
            points=[
                (0, 0, "straight"),
                (0, 20, "spline"),
                (20, 20, "spline"),
                (20, 0, "spline")
            ]
        )

        test_shape2.rotation_angle = 180
        test_shape2.create_solid()

        assert test_shape2.solid is not None
        assert 2 * test_shape2.volume == test_shape.volume

    def test_shape_volume_with_multiple_azimuth_placement_angles(self):
        """creates rotated shapes with multiple placement angles using straight and \
                spline connections and checks volumes are correct"""

        test_shape = RotateMixedShape(
            points=[
                (1, 1, "straight"),
                (1, 20, "spline"),
                (20, 20, "spline"),
                (20, 1, "spline")
            ]
        )

        test_shape.rotation_angle = 10
        test_shape.azimuth_placement_angle = [0, 90, 180, 270]
        test_shape.create_solid()

        assert test_shape.solid is not None
        assert test_shape.volume > 100

        test_shape2 = RotateMixedShape(
            points=[
                (1, 1, "straight"),
                (1, 20, "spline"),
                (20, 20, "spline"),
                (20, 1, "spline")
            ]
        )

        test_shape2.rotation_angle = 5
        test_shape2.azimuth_placement_angle = [0, 90, 180, 270]
        test_shape2.create_solid()

        assert test_shape2.solid is not None
        assert 2 * test_shape2.volume == pytest.approx(test_shape.volume)

        test_shape3 = RotateMixedShape(
            points=[
                (1, 1, "straight"),
                (1, 20, "spline"),
                (20, 20, "spline"),
                (20, 1, "spline")
            ]
        )

        test_shape3.rotation_angle = 20
        test_shape3.azimuth_placement_angle = [0, 180]
        test_shape3.create_solid()

        assert test_shape3.solid is not None
        assert test_shape3.volume == pytest.approx(test_shape.volume)

    def test_incorrect_connections(self):
        def incorrect_string_for_connection_type():
            """checks that a ValueError is raised when the an invalid connection \
                        type is specified"""

            test_shape = RotateMixedShape(
                points=[
                    (0, 0, "straight"),
                    (0, 20, "spline"),
                    (20, 20, "spline"),
                    (20, 0, "not_a_valid_entry")
                ]
            )

        self.assertRaises(ValueError, incorrect_string_for_connection_type)

        def incorrect_number_of_connections_function():
            """checks that a ValueError is raised when an incorrect \
                           number of connections are specified. There are 4 \
                           points set, so only 4 connections are needed"""
            test_shape = RotateMixedShape(
                points=[
                    (0, 200, "straight"),
                    (200, 100, "spline"),
                    (0, 0, "spline"),
                    (0, 200),
                ]
            )

            test_shape.create_solid()

        self.assertRaises(ValueError, incorrect_number_of_connections_function)

    def test_cut_volume(self):
        """creates a rotated shape using straight and spline connections with another \
                shape cut out and checks the volume is correct"""

        inner_shape = RotateMixedShape(
            points=[
                (5, 5, "straight"),
                (5, 10, "spline"),
                (10, 10, "spline"),
                (10, 5, "spline")
            ],
            rotation_angle=180,
        )

        outer_shape = RotateMixedShape(
            points=[
                (3, 3, "straight"),
                (3, 12, "spline"),
                (12, 12, "spline"),
                (12, 3, "spline")
            ],
            rotation_angle=180,
        )

        outer_shape_cut = RotateMixedShape(
            points=[
                (3, 3, "straight"),
                (3, 12, "spline"),
                (12, 12, "spline"),
                (12, 3, "spline")
            ],
            cut=inner_shape,
            rotation_angle=180,
        )

        assert inner_shape.volume == pytest.approx(862.5354)
        assert outer_shape.volume == pytest.approx(2854.5969)
        assert outer_shape_cut.volume == pytest.approx(2854.5969 - 862.5354)


if __name__ == "__main__":
    unittest.main()
