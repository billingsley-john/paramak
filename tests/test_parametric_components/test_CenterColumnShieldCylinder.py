
import os
import unittest
from pathlib import Path

import paramak
import pytest


class test_CenterColumnShieldCylinder(unittest.TestCase):
    def test_CenterColumnShieldCylinder_creation(self):
        """Creates a center column shield using the CenterColumnShieldCylinder
        parametric component and checks that a cadquery solid is created."""

        test_shape = paramak.CenterColumnShieldCylinder(
            height=600, inner_radius=100, outer_radius=200
        )

        assert test_shape.solid is not None
        assert test_shape.volume > 1000

    def test_volume_CenterColumnShieldCylinder(self):
        """Creates a CenterColumnShieldCylinder shape and checks that the
        volume is correct."""

        test_shape = paramak.CenterColumnShieldCylinder(
            rotation_angle=360,
            height=15,
            inner_radius=5,
            outer_radius=10,
            azimuth_placement_angle=0,
        )

        assert test_shape.volume == pytest.approx(3534.29)

        test_shape = paramak.CenterColumnShieldCylinder(
            rotation_angle=180,
            height=15,
            inner_radius=5,
            outer_radius=10,
            azimuth_placement_angle=95,
        )

        assert test_shape.volume == pytest.approx(3534.29 / 2.0)

    def test_export_stp_CenterColumnShieldCylinder(self):
        """Creates a CenterColumnShieldCylinder shape and checks that a stp
        file of the shape can be exported using the export_stp method."""

        test_shape = paramak.CenterColumnShieldCylinder(
            rotation_angle=360,
            height=15,
            inner_radius=5,
            outer_radius=10,
            azimuth_placement_angle=0,
        )

        os.system("rm center_column_shield.stp")

        test_shape.export_stp("center_column_shield.stp")

        assert Path("center_column_shield.stp").exists()

        os.system("rm center_column_shield.stp")

    def test_parametric_component_hash_value(self):
        """Creates a parametric component and checks that a cadquery solid with
        a unique hash value is created when .solid is called. Checks that the
        same cadquery solid with the same unique hash value is returned when
        shape.solid is called again after no changes have been made to the
        parametric component. Checks that a new cadquery solid with a new
        unique hash value is constructed when shape.solid is called after
        changes to the parametric component have been made. Checks that the
        hash_value of a parametric component is not updated until a new
        cadquery solid has been created."""

        test_shape = paramak.CenterColumnShieldCylinder(
            height=100,
            inner_radius=20,
            outer_radius=40
        )

        assert test_shape.hash_value is None
        assert test_shape.solid is not None
        assert test_shape.hash_value is not None
        initial_hash_value = test_shape.hash_value
        assert test_shape.solid is not None
        assert initial_hash_value == test_shape.hash_value
        test_shape.height = 120
        assert initial_hash_value == test_shape.hash_value
        assert test_shape.solid is not None
        assert initial_hash_value != test_shape.hash_value
