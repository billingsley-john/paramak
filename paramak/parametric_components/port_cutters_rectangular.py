
from paramak import ExtrudeStraightShape


class PortCutterRectangular(ExtrudeStraightShape):
    """Creates an extruded shape with a rectangular section that is used to cut
    other components (eg. blanket, vessel,..) in order to create ports.

    Args:
        center_point: Center point of the port cutter. Defaults to (0, 0).
        height: height (cm) of the port cutter.
        width: width (cm) of the port cutter.
        distance: extruded distance (cm) of the port cutter.
        fillet_radius (float, optional): If not None, radius (cm) of fillets
            added to edges orthogonal to the Z direction. Defaults to None.
        stp_filename (str, optional): defaults to "PortCutterRectangular.stp".
        stl_filename (str, optional): defaults to "PortCutterRectangular.stl".
        name (str, optional): defaults to "rectangular_port_cutter".
        material_tag (str, optional): defaults to
            "rectangular_port_cutter_mat".
        extrusion_start_offset (float, optional): the distance between 0 and
            the start of the extrusion. Defaults to 1..
    """

    def __init__(
        self,
        height,
        width,
        distance,
        center_point=(0, 0),
        workplane="ZY",
        rotation_axis="Z",
        extrusion_start_offset=1.,
        fillet_radius=None,
        stp_filename="PortCutterRectangular.stp",
        stl_filename="PortCutterRectangular.stl",
        name="rectangular_port_cutter",
        material_tag="rectangular_port_cutter_mat",
        **kwargs
    ):

        super().__init__(
            workplane=workplane,
            rotation_axis=rotation_axis,
            extrusion_start_offset=extrusion_start_offset,
            extrude_both=False,
            name=name,
            material_tag=material_tag,
            stp_filename=stp_filename,
            stl_filename=stl_filename,
            distance=distance,
            **kwargs
        )

        self.center_point = center_point
        self.height = height
        self.width = width
        self.fillet_radius = fillet_radius
        self.add_fillet()

    def find_points(self):
        points = [
            (-self.width / 2, -self.height / 2),
            (self.width / 2, -self.height / 2),
            (self.width / 2, self.height / 2),
            (-self.width / 2, self.height / 2),
        ]
        points = [(e[0] + self.center_point[0], e[1] +
                   self.center_point[1]) for e in points]
        self.points = points

    def add_fillet(self):
        if "X" not in self.workplane:
            filleting_edge = "|X"
        if "Y" not in self.workplane:
            filleting_edge = "|Y"
        if "Z" not in self.workplane:
            filleting_edge = "|Z"

        if self.fillet_radius is not None and self.fillet_radius != 0:
            self.solid = self.solid.edges(filleting_edge).fillet(self.fillet_radius)
