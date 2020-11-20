
import unittest

import paramak


class test_PortCutterCircular(unittest.TestCase):
    def test_PortCutterCircular_creation(self):
        """Checks a PortCutterCircular creation."""

        test_component = paramak.PortCutterCircular(
            distance=3,
            z_pos=0.25,
            radius=0.1,
            azimuth_placement_angle=[0, 45, 90, 180]
        )

        assert test_component.solid is not None
