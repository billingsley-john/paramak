
import paramak
import numpy as np
import cadquery as cq


class SegmentedBlanketBallReactor(paramak.BallReactor):
    """Creates geometry for a single ball reactor with a single divertor
    including a plasma, cylindrical center column shielding, square toroidal
    field coils. There is no inboard breeder blanket on this ball reactor like
    most spherical reactors.

    Arguments:
        inner_bore_radial_thickness (float): the radial thickness of the
            inner bore (cm)
        inboard_tf_leg_radial_thickness (float): the radial thickness of the
            inner leg of the toroidal field coils (cm)
        center_column_shield_radial_thickness (float): the radial thickness of
            the center column shield (cm)
        divertor_radial_thickness (float): the radial thickness of the divertor
            (cm), this fills the gap between the center column shield and
            blanket
        inner_plasma_gap_radial_thickness (float): the radial thickness of the
            inboard gap between the plasma and the center column shield (cm)
        plasma_radial_thickness (float): the radial thickness of the plasma
        outer_plasma_gap_radial_thickness (float): the radial thickness of the
            outboard gap between the plasma and firstwall (cm)
        firstwall_radial_thickness (float): the radial thickness of the first
            wall (cm)
        blanket_radial_thickness (float): the radial thickness of the blanket
            (cm)
        blanket_rear_wall_radial_thickness (float): the radial thickness of the
            rear wall of the blanket (cm)
        gap_between_blankets (float): the distance between adjacent blanket
            segments,
        number_of_blanket_segments (int): the number of segments to divide the
            blanket up into. This for a full 360 degrees rotation
        elongation (float): the elongation of the plasma
        triangularity (float): the triangularity of the plasma
        number_of_tf_coils (int): the number of tf coils
    """

    def __init__(
        self,
        inner_bore_radial_thickness,
        inboard_tf_leg_radial_thickness,
        center_column_shield_radial_thickness,
        divertor_radial_thickness,
        inner_plasma_gap_radial_thickness,
        plasma_radial_thickness,
        outer_plasma_gap_radial_thickness,
        firstwall_radial_thickness,
        blanket_radial_thickness,
        blanket_rear_wall_radial_thickness,
        elongation,
        triangularity,
        number_of_tf_coils,
        gap_between_blankets,
        number_of_blanket_segments,
        blanket_fillet_radius=10,
        **kwargs
    ):

        self.gap_between_blankets = gap_between_blankets
        self.number_of_blanket_segments = number_of_blanket_segments
        self.blanket_fillet_radius = blanket_fillet_radius

        super().__init__(
            inner_bore_radial_thickness=inner_bore_radial_thickness,
            inboard_tf_leg_radial_thickness=inboard_tf_leg_radial_thickness,
            center_column_shield_radial_thickness=center_column_shield_radial_thickness,
            divertor_radial_thickness=divertor_radial_thickness,
            inner_plasma_gap_radial_thickness=inner_plasma_gap_radial_thickness,
            plasma_radial_thickness=plasma_radial_thickness,
            outer_plasma_gap_radial_thickness=outer_plasma_gap_radial_thickness,
            firstwall_radial_thickness=firstwall_radial_thickness,
            blanket_radial_thickness=blanket_radial_thickness,
            blanket_rear_wall_radial_thickness=blanket_rear_wall_radial_thickness,
            elongation=elongation,
            triangularity=triangularity,
            number_of_tf_coils=number_of_tf_coils,
            **kwargs)

        self.shapes_and_components = []

        self.create_solids()

    @property
    def gap_between_blankets(self):
        return self._gap_between_blankets

    @gap_between_blankets.setter
    def gap_between_blankets(self, value):
        """Sets the SegmentedBlanketBallReactor.gap_between_blankets
        attribute which controls the horitzonal distance between blanket
        segments."""
        if isinstance(value, (float, int)) and value > 0:
            self._gap_between_blankets = float(value)
        else:
            raise ValueError(
                "gap_between_blankets but be a positive value float")

    @property
    def number_of_blanket_segments(self):
        """Sets the SegmentedBlanketBallReactor.number_of_blanket_segments
        attribute which controls the number of blanket segments."""
        return self._number_of_blanket_segments

    @number_of_blanket_segments.setter
    def number_of_blanket_segments(self, value):
        if isinstance(value, int) and value > 2:
            self._number_of_blanket_segments = value
        else:
            raise ValueError(
                "number_of_blanket_segments but be an int greater than 2")

    def _make_blankets_layers(self):

        center_column_cutter = paramak.CenterColumnShieldCylinder(
            height=self._center_column_shield_height * 1.5,  # extra 0.5 to ensure overlap,
            inner_radius=0,
            outer_radius=self._center_column_shield_end_radius,
            rotation_angle=360
        )

        thin_cutter = paramak.BlanketCutterStar(
            distance=self.gap_between_blankets,
            azimuth_placement_angle=np.linspace(
                0, 360, self.number_of_blanket_segments, endpoint=False))

        self._blanket_envelope = paramak.BlanketFP(
            plasma=self._plasma,
            thickness=self.firstwall_radial_thickness +
            self.blanket_radial_thickness,
            offset_from_plasma=[
                self.inner_plasma_gap_radial_thickness,
                self.plasma_gap_vertical_thickness,
                self.outer_plasma_gap_radial_thickness,
                self.plasma_gap_vertical_thickness,
                self.inner_plasma_gap_radial_thickness],
            start_angle=-179,
            stop_angle=179,
            rotation_angle=self.rotation_angle,
            material_tag="firstwall_mat",
            stp_filename="firstwall.stp",
            cut=[
                center_column_cutter,
                thin_cutter])

        # makes a thicker star shaped cutting tool
        thick_cutter = paramak.BlanketCutterStar(
            distance=self.gap_between_blankets +
            2 *
            self.firstwall_radial_thickness,
            azimuth_placement_angle=np.linspace(
                0,
                360,
                self.number_of_blanket_segments,
                endpoint=False))

        self._blanket = paramak.BlanketFP(
            plasma=self._plasma,
            thickness=self.blanket_radial_thickness,
            offset_from_plasma=[
                self.inner_plasma_gap_radial_thickness +
                self.firstwall_radial_thickness,
                self.plasma_gap_vertical_thickness +
                self.firstwall_radial_thickness,
                self.outer_plasma_gap_radial_thickness +
                self.firstwall_radial_thickness,
                self.plasma_gap_vertical_thickness +
                self.firstwall_radial_thickness,
                self.inner_plasma_gap_radial_thickness +
                self.firstwall_radial_thickness],
            start_angle=-179,
            stop_angle=179,
            rotation_angle=self.rotation_angle,
            material_tag="blanket_mat",
            stp_filename="blanket.stp",
            cut=[center_column_cutter, thick_cutter])

        if self.blanket_fillet_radius != 0:
            x = self.major_radius+1 # tried firstwall start radius here already
            front_face_b = self._blanket.solid.faces(cq.NearestToPointSelector((0, x, 0)))
            front_edge_b = front_face_b.edges(cq.NearestToPointSelector((0, x, 0)))
            front_edge_length_b = front_edge_b.val().Length()
            self._blanket.solid = self._blanket.solid.edges(
                paramak.EdgeLengthSelector(front_edge_length_b)).fillet(self.blanket_fillet_radius)
        
        # TODO this segfaults at the moment but works as an opperation on the
        # reactor after construction in jupyter
        # tried different x values and (0, x, 0)
        # noticed that it much quicker as a post process so perhaps some unwanted looping is happening
        # if self.blanket_fillet_radius != 0:
        #     x = self.major_radius # tried firstwall start radius here already
        #     front_face = self._blanket_envelope.solid.faces(cq.NearestToPointSelector((x, 0, 0)))
        #     print('found front face')
        #     front_edge = front_face.edges(cq.NearestToPointSelector((x, 0, 0)))
        #     print('found front edge')
        #     front_edge_length = front_edge.val().Length()
        #     print('found front edge length', front_edge_length)
        #     self._blanket_envelope.solid = self._blanket_envelope.solid.edges(
        #         paramak.EdgeLengthSelector(front_edge_length)).fillet(self.blanket_fillet_radius)
        # print('finished')

        self._blanket_envelope.solid = self._blanket_envelope.solid.cut(
            self._blanket.solid)

        self._firstwall = self._blanket_envelope
        

        self._blanket_rear_wall = paramak.BlanketFP(
            plasma=self._plasma,
            thickness=self.blanket_rear_wall_radial_thickness,
            offset_from_plasma=[
                self.inner_plasma_gap_radial_thickness +
                self.firstwall_radial_thickness +
                self.blanket_radial_thickness,
                self.plasma_gap_vertical_thickness +
                self.firstwall_radial_thickness +
                self.blanket_radial_thickness,
                self.outer_plasma_gap_radial_thickness +
                self.firstwall_radial_thickness +
                self.blanket_radial_thickness,
                self.plasma_gap_vertical_thickness +
                self.firstwall_radial_thickness +
                self.blanket_radial_thickness,
                self.inner_plasma_gap_radial_thickness +
                self.firstwall_radial_thickness +
                self.blanket_radial_thickness],
            start_angle=-
            179,
            stop_angle=179,
            rotation_angle=self.rotation_angle,
            material_tag="blanket_rear_wall_mat",
            stp_filename="blanket_rear_wall.stp",
            cut=center_column_cutter)
