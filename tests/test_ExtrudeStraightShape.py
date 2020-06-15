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

from paramak import ExtrudeStraightShape


class test_object_properties(unittest.TestCase):
    def test_absolute_shape_volume(self):
        """creates an extruded shape with one placement angle using straight \
                connections and checks the volume is correct"""

        test_shape = ExtrudeStraightShape(
            points=[(0, 0), (0, 20), (20, 20), (20, 0), (0, 0)], distance=30
        )

        test_shape.create_solid()

        assert test_shape.solid is not None
        assert test_shape.volume == 20 * 20 * 30

    def test_extruded_shape_volume(self):
        """creates an extruded shape with multiple placement angles using straight \
                connections and checks the volume is correct"""

        test_shape = ExtrudeStraightShape(
            points=[(5, 0), (5, 20), (15, 20), (15, 0), (5, 0)], distance=10
        )

        test_shape.azimuth_placement_angle = 0

        assert test_shape.volume == pytest.approx(10 * 20 * 10 * 1)

        test_shape.azimuth_placement_angle = [0, 90, 180, 270]

        assert test_shape.volume == pytest.approx(10 * 20 * 10 * 4)

    def test_extruded_shape_with_overlap_volume(self):
        """creates an extruded shape with multiple placement angles with overlap \
                using straight connections and checks the volume is correct"""

        test_shape = ExtrudeStraightShape(
            points=[(0, 0), (0, 20), (10, 20), (10, 0), (0, 0)], distance=10
        )

        test_shape.azimuth_placement_angle = [0, 90, 180, 270]

        assert test_shape.volume == pytest.approx((10 * 20 * 10 * 4) - (5 * 20 * 5 * 4))

    def test_cut_volume(self):
        """creates an extruded shape with one placement angle using straight \
                connections with another shape cut out and checks the volume \
                is correct"""

        inner_shape = ExtrudeStraightShape(
            points=[(5, 5), (5, 10), (10, 10), (10, 5), (5, 5)], distance=30
        )

        outer_shape = ExtrudeStraightShape(
            points=[(3, 3), (3, 12), (12, 12), (12, 3), (3, 3)], distance=30
        )

        outer_shape_with_cut = ExtrudeStraightShape(
            points=[(3, 3), (3, 12), (12, 12), (12, 3), (3, 3)],
            cut=inner_shape,
            distance=30,
        )

        assert inner_shape.volume == 5 * 5 * 30
        assert outer_shape.volume == 9 * 9 * 30
        assert outer_shape_with_cut.volume == pytest.approx(
            (9 * 9 * 30) - (5 * 5 * 30), abs=0.1
        )


if __name__ == "__main__":
    unittest.main()
