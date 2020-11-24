
import math
import unittest

import paramak
import pytest


class test_PoloidalFieldCoilCase(unittest.TestCase):

    def setUp(self):
        self.test_shape = paramak.PoloidalFieldCoilCase(
            casing_thickness=5,
            coil_height=50,
            coil_width=50,
            center_point=(1000, 500)
        )

    def test_default_parameters(self):
        """Checks that the default parameters of a PoloidalFieldCoilCase are correct."""

        assert self.test_shape.rotation_angle == 360
        assert self.test_shape.stp_filename == "PoloidalFieldCoilCase.stp"
        assert self.test_shape.stl_filename == "PoloidalFieldCoilCase.stl"
        assert self.test_shape.material_tag == "pf_coil_case_mat"
    
    def test_PoloidalFieldCoilCase_creation(self):
        """Creates a pf coil case using the PoloidalFieldCoilCase parametric
        component and checks that a cadquery solid is created."""

        assert self.test_shape.solid is not None
        assert self.test_shape.volume > 1000

    def test_PoloidalFieldCoilCase_absolute_volume(self):
        """Creates a pf coil case using the PoloidalFieldCoilCase parametric
        component and checks that its volume is correct."""

        assert self.test_shape.volume == pytest.approx(
            (math.pi * 2 * 1000) * ((60 * 5 * 2) + (50 * 5 * 2)))

    def test_PoloidalFieldCoilCase_absolute_areas(self):
        """Creates a pf coil case using the PoloidalFieldCoilCase parametric
        component and checks that the areas of its faces are correct."""

        assert len(self.test_shape.areas) == 8
        assert len(set([round(i) for i in self.test_shape.areas])) == 6
        assert self.test_shape.areas.count(
            pytest.approx(50 * math.pi * 2 * 1000)) == 2
        assert self.test_shape.areas.count(
            pytest.approx(60 * math.pi * 2 * 1000)) == 2
        assert self.test_shape.areas.count(
            pytest.approx(50 * math.pi * 2 * 1025)) == 1
        assert self.test_shape.areas.count(
            pytest.approx(50 * math.pi * 2 * 975)) == 1
        assert self.test_shape.areas.count(
            pytest.approx(60 * math.pi * 2 * 1030)) == 1
        assert self.test_shape.areas.count(
            pytest.approx(60 * math.pi * 2 * 970)) == 1
