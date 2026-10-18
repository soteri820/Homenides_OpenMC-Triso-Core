import openmc

from materials import build_materials
from geometry import build_geometry
from settings import build_settings
from tallies import build_tallies
from plotting import build_plots

# unit cell width in cm; one value drive both geometry and the plots
PITCH = 1.26

def main():
    ## 1. build each physical aspect
    mats = build_materials()
    geometry, fuel_cell = build_geometry(mats, PITCH)
    settings = build_settings()
    tallies = build_tallies(fuel_cell)
    plot = build_plots(mats, PITCH)

    ## 2. write the .xml input files for OpenMC to read
    openmc.Materials(list(mats.values())).export_to_xml()
    geometry.export_to_xml()
    settings.export_to_xml()
    tallies.export_to_xml()
    plot.export_to_xml()

    ## 3. run the eigenvalue calculation (as was defined in settings.py)
    openmc.run()

    ## 4. read k-effective back from the results file
    with openmc.StatePoint(f"statepoint.{settings.batches}.h5") as sp:
        print(f"\nk-effective = {sp.keff}")

    ## 5. run OpenMC in plot mode to write pinplot.png
    openmc.plot_geometry()

# runs main() when this file is executed directly
if __name__ == "__main__":
    main()