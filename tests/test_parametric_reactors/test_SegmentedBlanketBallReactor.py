
import unittest

import paramak


class test_SegmentedBlanketBallReactor(unittest.TestCase):

    def test_gap_between_blankets_impacts_volume(
            self):
        """creates a SegmentedBlanketBallReactor with different
        gap_between_blankets and checks the volume of the blankes and the
        firstwall changes."""

        reactor = paramak.SegmentedBlanketBallReactor(
            inner_bore_radial_thickness=10,
            inboard_tf_leg_radial_thickness=30,
            center_column_shield_radial_thickness=60,
            divertor_radial_thickness=150,
            inner_plasma_gap_radial_thickness=30,
            plasma_radial_thickness=300,
            outer_plasma_gap_radial_thickness=30,
            firstwall_radial_thickness=20,
            blanket_radial_thickness=50,
            blanket_rear_wall_radial_thickness=30,
            elongation=2,
            triangularity=0.55,
            number_of_tf_coils=16,
            rotation_angle=180,
            pf_coil_radial_thicknesses=[50, 50, 50, 50],
            pf_coil_vertical_thicknesses=[50, 50, 50, 50],
            pf_coil_to_rear_blanket_radial_gap=50,
            pf_coil_to_tf_coil_radial_gap=50,
            outboard_tf_coil_radial_thickness=100,
            outboard_tf_coil_poloidal_thickness=50,
            gap_between_blankets=30,
            number_of_blanket_segments=4,
        )
        reactor.create_solids()
        small_gap_blanket = reactor._blanket.volume
        small_gap_fw = reactor._firstwall.volume

        reactor.gap_between_blankets = 60
        reactor.create_solids()
        large_gap_blanket = reactor._blanket.volume
        large_gap_fw = reactor._firstwall.volume

        assert small_gap_blanket > large_gap_blanket
        assert small_gap_fw > large_gap_fw

    def test_number_of_blanket_segments_impacts_volume(self):
        """creates a SegmentedBlanketBallReactor with different
        number_of_blanket_segments and checks the volume of the blanket and
        firstwall changes"""

        reactor = paramak.SegmentedBlanketBallReactor(
            inner_bore_radial_thickness=10,
            inboard_tf_leg_radial_thickness=30,
            center_column_shield_radial_thickness=60,
            divertor_radial_thickness=150,
            inner_plasma_gap_radial_thickness=30,
            plasma_radial_thickness=300,
            outer_plasma_gap_radial_thickness=30,
            firstwall_radial_thickness=20,
            blanket_radial_thickness=50,
            blanket_rear_wall_radial_thickness=30,
            elongation=2,
            triangularity=0.55,
            number_of_tf_coils=16,
            rotation_angle=180,
            pf_coil_radial_thicknesses=[50, 50, 50, 50],
            pf_coil_vertical_thicknesses=[50, 50, 50, 50],
            pf_coil_to_rear_blanket_radial_gap=50,
            pf_coil_to_tf_coil_radial_gap=50,
            outboard_tf_coil_radial_thickness=100,
            outboard_tf_coil_poloidal_thickness=50,
            gap_between_blankets=30,
            blanket_fillet_radius=0,
            number_of_blanket_segments=4,
        )
        reactor.create_solids()
        blanket_few_segments = reactor._blanket.volume
        fw_few_segments = reactor._firstwall.volume

        reactor.number_of_blanket_segments = 6
        reactor.create_solids()
        blanket_many_segments = reactor._blanket.volume
        fw_many_segments = reactor._firstwall.volume

        assert blanket_many_segments < blanket_few_segments
        assert fw_many_segments > fw_few_segments
