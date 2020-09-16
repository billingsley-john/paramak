from paramak import RotateStraightShape


class PoloidalFieldCoilCase(RotateStraightShape):
    """Creates a casing for a reactangular coil from inputs that
    describe the existing coil and the thickness of the casing required.

    Args:
        height (float): the vertical (z axis) height of the coil (cm).
        width (float): the horizontal(x axis) width of the coil (cm).
        center_point (tuple of floats): the center of the coil (x,z) values (cm).
        casing_thickness (tuple of floats): the thickness of the coil casing (cm).

    Keyword Args:
        name (str): the legend name used when exporting a html graph of the shape.
        color (sequences of 3 or 4 floats each in the range 0-1): the color to use when
            exportin as html graphs or png images.
        material_tag (str): The material name to use when exporting the neutronics description.
        stp_filename (str): The filename used when saving stp files as part of a reactor.
        azimuth_placement_angle (float or iterable of floats): The angle or angles to use when
            rotating the shape on the azimuthal axis.
        rotation_angle (float): The rotation angle to use when revolving the solid (degrees).
        workplane (str): The orientation of the CadQuery workplane. Options are XY, YZ or XZ.
        intersect (CadQuery object): An optional CadQuery object to perform a boolean intersect with
            this object.
        cut (CadQuery object): An optional CadQuery object to perform a boolean cut with this object.
        union (CadQuery object): An optional CadQuery object to perform a boolean union with this object.
        tet_mesh (str): Insert description.
        physical_groups (type): Insert description.

    Returns:
        a paramak shape object: A shape object that has generic functionality with points determined by the find_points() method. A CadQuery solid of the shape can be called via shape.solid.
    """

    def __init__(
        self,
        casing_thickness,
        coil_height,
        coil_width,
        center_point,
        rotation_angle=360,
        stp_filename="PoloidalFieldCoilCase.stp",
        stl_filename="PoloidalFieldCoilCase.stl",
        color=(0.5, 0.5, 0.5),
        azimuth_placement_angle=0,
        name=None,
        material_tag="pf_coil_case_mat",
        **kwargs
    ):

        default_dict = {
            "points": None,
            "workplane": "XZ",
            "solid": None,
            "intersect": None,
            "cut": None,
            "union": None,
            "tet_mesh": None,
            "physical_groups": None,
        }

        for arg in kwargs:
            if arg in default_dict:
                default_dict[arg] = kwargs[arg]

        super().__init__(
            name=name,
            color=color,
            material_tag=material_tag,
            stp_filename=stp_filename,
            stl_filename=stl_filename,
            azimuth_placement_angle=azimuth_placement_angle,
            rotation_angle=rotation_angle,
            hash_value=None,
            **default_dict
        )

        self.center_point = center_point
        self.height = coil_height
        self.width = coil_width
        self.casing_thickness = casing_thickness

    @property
    def points(self):
        self.find_points()
        return self._points

    @points.setter
    def points(self, value):
        self._points = value

    @property
    def center_point(self):
        return self._center_point

    @center_point.setter
    def center_point(self, value):
        self._center_point = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    def find_points(self):
        """Finds the XZ points joined by straight connections that describe the 2D
        profile of the poloidal field coil case shape."""

        points = [
            (
                self.center_point[0] + self.width / 2.0,
                self.center_point[1] + self.height / 2.0,
            ),  # upper right
            (
                self.center_point[0] + self.width / 2.0,
                self.center_point[1] - self.height / 2.0,
            ),  # lower right
            (
                self.center_point[0] - self.width / 2.0,
                self.center_point[1] - self.height / 2.0,
            ),  # lower left
            (
                self.center_point[0] - self.width / 2.0,
                self.center_point[1] + self.height / 2.0,
            ),  # upper left
            (
                self.center_point[0] + self.width / 2.0,
                self.center_point[1] + self.height / 2.0,
            ),  # upper right
            (
                self.center_point[0] + \
                (self.casing_thickness + self.width / 2.0),
                self.center_point[1] + \
                (self.casing_thickness + self.height / 2.0),
            ),
            (
                self.center_point[0] + \
                (self.casing_thickness + self.width / 2.0),
                self.center_point[1] - \
                (self.casing_thickness + self.height / 2.0),
            ),
            (
                self.center_point[0] - \
                (self.casing_thickness + self.width / 2.0),
                self.center_point[1] - \
                (self.casing_thickness + self.height / 2.0),
            ),
            (
                self.center_point[0] - \
                (self.casing_thickness + self.width / 2.0),
                self.center_point[1] + \
                (self.casing_thickness + self.height / 2.0),
            ),
            (
                self.center_point[0] + \
                (self.casing_thickness + self.width / 2.0),
                self.center_point[1] + \
                (self.casing_thickness + self.height / 2.0),
            ),
            (
                self.center_point[0] + self.width / 2.0,
                self.center_point[1] + self.height / 2.0,
            ),  # upper right
        ]

        self.points = points
