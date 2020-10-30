
import paramak
import pytest
import unittest


class test_ToroidalFieldCoilTripleArc(unittest.TestCase):
    def test_ToroidalFieldCoilTripleArc_creation(self):
        """Creates a ToroidalFieldCoilTripleArc object and checks a solid is
        created."""

        test_shape = paramak.ToroidalFieldCoilTripleArc(
            R1=1,
            h=1,
            radii=(1, 2),
            coverages=(10, 60),
            thickness=0.1,
            distance=0.5,
            number_of_coils=6,
            vertical_displacement=0.1)
        assert test_shape.solid is not None

    def test_ToroidalFieldCoilTripleArc_rotation_angle(self):
<<<<<<< HEAD
        """Creates a tf coil with a rotation_angle < 360 degrees and checks
        that the correct cut is performed and the volume is correct."""
=======
        """creates tf coils with rotation_angles < 360 in different workplanes and
        checks that the correct cuts are performed and their volumes are correct"""
>>>>>>> develop

        test_shape = paramak.ToroidalFieldCoilTripleArc(
            R1=150,
            h=200,
            radii=(50, 50),
            coverages=(70, 70),
            thickness=50,
            distance=50,
            number_of_coils=8,
        )

        test_shape.rotation_angle = 360
        test_shape.workplane = "XZ"
        test_volume = test_shape.volume
        test_shape.rotation_angle = 180
        assert test_shape.volume == pytest.approx(test_volume * 0.5, rel=0.01)

        test_shape.rotation_angle = 360
        test_shape.workplane = "YZ"
        test_volume = test_shape.volume
        test_shape.rotation_angle = 180
        assert test_shape.volume == pytest.approx(test_volume * 0.5, rel=0.01)

        # this test will remain commented until workplane issue #308 is resolved
        # currently causes terminal to crash due to large number of unions
        # test_shape.rotation_angle = 360
        # test_shape.workplane = "XY"
        # test_volume = test_shape.volume
        # test_shape.rotation_angle = 180
        # assert test_shape.volume == pytest.approx(test_volume * 0.5)
