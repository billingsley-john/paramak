"""
This example creates a ball reactor using the BallReactor parametric shape
"""

import paramak

def main():


    my_reactor = paramak.BallReactor(
                                    inner_bore_radial_thickness=50,
                                    inboard_tf_leg_radial_thickness = 200,
                                    center_column_radial_thickness= 50,
                                    inner_plasma_gap_radial_thickness = 50,
                                    plasma_radial_thickness = 100,
                                    outer_plasma_gap_radial_thickness = 50,
                                    firstwall_radial_thickness=5,
                                    blanket_radial_thickness=100,
                                    blanket_rear_wall_thickness=10,
                                    elongation=2,
                                    triangularity=0.55,
                                    number_of_tf_coils=16,
    )

    my_reactor.export_stp()

    my_reactor.export_neutronics_description()


if __name__ == "__main__":
    main()
