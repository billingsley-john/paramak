
import unittest

import paramak
import pytest


class test_SingleNullSubmersionTokamak(unittest.TestCase):

    def setUp(self):
        self.test_reactor = paramak.SingleNullSubmersionTokamak(
            inner_bore_radial_thickness=10,
            inboard_tf_leg_radial_thickness=30,
            center_column_shield_radial_thickness=60,
            divertor_radial_thickness=50,
            inner_plasma_gap_radial_thickness=30,
            plasma_radial_thickness=300,
            outer_plasma_gap_radial_thickness=30,
            firstwall_radial_thickness=30,
            blanket_rear_wall_radial_thickness=30,
            support_radial_thickness=20,
            inboard_blanket_radial_thickness=20,
            outboard_blanket_radial_thickness=20,
            elongation=2.3,
            triangularity=0.45,
            divertor_position="upper",
            support_position="upper",
            rotation_angle=359,
        )

    def test_SingleNullSubmersionTokamak_with_pf_and_tf_coils(self):
        """Creates a SingleNullSubmersionTokamak with pf and tf coils and checks
        that the correct number of components are created."""

        self.test_reactor.pf_coil_radial_thicknesses = [50, 50, 50, 50]
        self.test_reactor.pf_coil_vertical_thicknesses = [50, 50, 50, 50]
        self.test_reactor.pf_coil_to_tf_coil_radial_gap = 50
        self.test_reactor.pf_coil_case_thickness = 10
        self.test_reactor.outboard_tf_coil_radial_thickness = 100
        self.test_reactor.outboard_tf_coil_poloidal_thickness = 50
        self.test_reactor.tf_coil_to_rear_blanket_radial_gap = 20
        self.test_reactor.number_of_tf_coils = 16

        assert len(self.test_reactor.shapes_and_components) == 11

    def test_SingleNullSubmersionTokamak_divertors_supports(self):
        """Checks that SingleNullSubmersionTokamaks with lower and upper supports
        and divertors can be created."""

        self.test_reactor.divertor_position = "lower"
        self.test_reactor.support_position = "lower"
        assert self.test_reactor.solid is not None

        self.test_reactor.divertor_position = "lower"
        self.test_reactor.support_position = "upper"
        assert self.test_reactor.solid is not None

        self.test_reactor.divertor_position = "upper"
        self.test_reactor.support_position = "lower"
        assert self.test_reactor.solid is not None

        self.test_reactor.divertor_position = "upper"
        self.test_reactor.support_position = "upper"
        assert self.test_reactor.solid is not None

    def test_SingleNullSubmersionTokamak_rotation_angle_impacts_volume(self):
        """Creates SingleNullSubmersionTokamaks with different rotation angles and
        checks that the relative volumes of the components are correct."""

        self.test_reactor.rotation_angle = 90
        test_reactor_90_components = [
            component for component in self.test_reactor.shapes_and_components]
        self.test_reactor.rotation_angle = 180
        test_reactor_180_components = [
            component for component in self.test_reactor.shapes_and_components]

        for r90, r180 in zip(test_reactor_90_components,
                             test_reactor_180_components):
            assert r90.volume == pytest.approx(r180.volume * 0.5, rel=0.1)

    def test_SubmersionTokamak_error_divertor_pos(self):
        """Creates a SingleNullSubmersionTokamak with an invalid divertor and support
        position and checks that the correct ValueError is raised."""

        def invalid_divertor_position():
            self.test_reactor.divertor_position = "coucou"

        self.assertRaises(ValueError, invalid_divertor_position)

        def invalid_support_position():
            self.test_reactor.support_position = "coucou"

        self.assertRaises(ValueError, invalid_support_position)

    def test_hash_value(self):
        """Creates a single null submersion reactor and checks that all shapes in the reactor
        are created when .shapes_and_components is first called. Checks that when
        .shapes_and_components is called again with no changes to the reactor, the shapes in
        the reactor are reconstructed and the previously constructed shapes are returned.
        Checks that when .shapes_and_components is called again with changes to the reactor,
        the shapes in the reactor are reconstructed and these new shapes are returned. Checks
        that the reactor_hash_value is only updated when the reactor is reconstructed."""

        self.test_reactor.pf_coil_radial_thicknesses = [30, 30, 30, 30]
        self.test_reactor.pf_coil_vertical_thicknesses = [30, 30, 30, 30]
        self.test_reactor.pf_coil_to_tf_coil_radial_gap = 50
        self.test_reactor.pf_coil_case_thickness = 10
        self.test_reactor.outboard_tf_coil_radial_thickness = 30
        self.test_reactor.outboard_tf_coil_poloidal_thickness = 30
        self.test_reactor.tf_coil_to_rear_blanket_radial_gap = 20
        self.test_reactor.number_of_tf_coils = 16

        assert self.test_reactor.reactor_hash_value is None
        for key in [
            "_inboard_tf_coils",
            "_center_column_shield",
            "_plasma",
            "_inboard_firstwall",
            "_inboard_blanket",
            "_firstwall",
            "_divertor",
            "_blanket",
            "_supports",
            "_outboard_rear_blanket_wall_upper",
            "_outboard_rear_blanket_wall_lower",
            "_outboard_rear_blanket_wall",
            "_tf_coil",
            "_pf_coil",
            "_pf_coils_casing"
        ]:
            assert key not in self.test_reactor.__dict__.keys()
        assert self.test_reactor.shapes_and_components is not None

        for key in [
            "_inboard_tf_coils",
            "_center_column_shield",
            "_plasma",
            "_inboard_firstwall",
            "_inboard_blanket",
            "_firstwall",
            "_divertor",
            "_blanket",
            "_supports",
            "_outboard_rear_blanket_wall_upper",
            "_outboard_rear_blanket_wall_lower",
            "_outboard_rear_blanket_wall",
            "_tf_coil",
            "_pf_coil",
            "_pf_coils_casing"
        ]:
            assert key in self.test_reactor.__dict__.keys()
        assert len(self.test_reactor.shapes_and_components) == 11
        assert self.test_reactor.reactor_hash_value is not None
        initial_hash_value = self.test_reactor.reactor_hash_value
        self.test_reactor.rotation_angle = 270
        assert self.test_reactor.reactor_hash_value == initial_hash_value
        assert self.test_reactor.shapes_and_components is not None
        assert self.test_reactor.reactor_hash_value != initial_hash_value
