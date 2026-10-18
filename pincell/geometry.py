import openmc


def build_geometry(mats, pitch):
    ### Build the pin cell geometry. Returns (geometry, fuel_cell).

    ## Defining material surfaces
    # three axially infinite cylinders from top view, centered at origin #radii in cm
    # these are all only thin surfaces, not yet volumes
    fuel_outer_radius = openmc.ZCylinder(r=0.39)
    clad_inner_radius = openmc.ZCylinder(r=0.40)
    clad_outer_radius = openmc.ZCylinder(r=0.46)



    ## Defining Volumes from these Surfaces
    # "-surface" means that inside that surface we're creating a volume
    # "+surface" means that outside that surface we're creating a volume
    # "surface" & "surface" means the union/intersection of these regions
    
    # creating the fuel cell as whats inside the fuel outer radius, and of material uo2
    fuel = openmc.Cell(name='fuel')
    fuel.fill = mats["uo2"]
    fuel.region = -fuel_outer_radius

    # creating gap between fuel rod and cladding to allow for thermal expansion of fuel
    # gap has no fill, is treated as void
    gap = openmc.Cell(name='air gap')
    gap.region = +fuel_outer_radius & -clad_inner_radius

    # creating the clad volume itself
    clad = openmc.Cell(name='clad')
    clad.fill = mats["zirconium"]
    clad.region = +clad_inner_radius & -clad_outer_radius



    ## Defining Boundary Planes 
    # four planes forming square around origin, with width of pitch
    # reflective material type means neutrons bounce back after hitting the wall
    # mimics behavior of infinite lattice of similar pins
    left = openmc.XPlane(-pitch / 2, boundary_type='reflective')
    right = openmc.XPlane(pitch / 2, boundary_type='reflective')
    bottom = openmc.YPlane(-pitch / 2, boundary_type='reflective')
    top = openmc.YPlane(pitch / 2, boundary_type='reflective')



    ## Defining the Moderator Cell
    # water fills the square box, but not the inside of the cladding
    moderator = openmc.Cell(name='moderator')
    moderator.fill = mats["water"]
    moderator.region = +left & -right & +bottom & -top & +clad_outer_radius

    ## Defining the Universe
    # universe is collection of cells, root universe is the top level universe
    # returns the geometry and the fuel cell
    root_universe = openmc.Universe(cells=(fuel, gap, clad, moderator))
    return openmc.Geometry(root_universe), fuel