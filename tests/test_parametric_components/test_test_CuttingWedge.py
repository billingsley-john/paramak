
import math
import random
import unittest

import paramak
import pytest


class test_CuttingWedge(unittest.TestCase):
    def test_volume_of_CuttingWedge_for_5_random_dimentions(self):
        for test_number in range(5):
            height = random.uniform(1., 2000.)
            radius = random.uniform(1., 1000)
            rotation_angle = random.uniform(1., 360.)
            azimuth_placement_angle = random.uniform(1., 360.)

            test_shape = paramak.CuttingWedge(
                height=height,
                radius=radius,
                rotation_angle=rotation_angle,
                azimuth_placement_angle=azimuth_placement_angle
            )
            angle_fraction = 360 / rotation_angle
            correct_volume = (math.pi * radius ** 2 * height) / angle_fraction
            assert test_shape.volume == pytest.approx(correct_volume)
