import numpy as np
import openmc
import openmc.model

## TRISO dimensions
# outer radius of each layer in micrometers, going outward:
# kernel, buffer, inner PyC, SiC 
LAYER_RADII_UM = [215.0, 315.0, 350.0, 385.0]
# (outer PyC has no inner, only the full particle radius)
PARTICLE_RADIUS_UM = 425.0
# conversion factor bc OpenMC works in cm
UM_TO_CM = 1e-4

def build_triso_universe(mats):
    ## returns the universe describing SINGULAR TRISO particle, centered at origin

    ## surfaces of four nested spheres
    spheres = [openmc.Sphere(r=r * UM_TO_CM) for r in LAYER_RADII_UM]

    ## cells: one per layer
    # -sphere means inside that sphere, +sphere means outside that sphere
    # a shell is outside the smaller sphere and inside the next one, so use & to join them
    kernel = openmc.Cell(name='kernel', fill=mats['triso_fuel'], region=-spheres[0])
    buffer = openmc.Cell(name='buffer', fill=mats['buffer'], region=+spheres[0] & -spheres[1])
    ipyc = openmc.Cell(name='ipyc', fill=mats['ipyc'], region=+spheres[1] & -spheres[2])
    sic = openmc.Cell(name='sic', fill=mats['sic'], region=+spheres[2] & -spheres[3])
    # outermost has no bounding sphere of its own, merely extends outwards to the particle radius
    opyc = openmc.Cell(name="opyc", fill=mats['opyc'], region=+spheres[3])

    return openmc.Universe(name='triso_particle', cells=[kernel, buffer, ipyc, sic, opyc])

## has a seemingly odd quirk where the outermost layer extends to the bound of this universe, without a hard definition of that shell
## but thats okay because like main will make use of that variable or something like yeah

def build_box_region(side_cm=1.0, boundary_type='reflective'):
    ## Returns a cube region centered at origin, to pack particles into

    ## six planes, two per axis
    half = side_cm/2
    min_x = openmc.XPlane(x0=-half, boundary_type=boundary_type)
    max_x = openmc.XPlane(x0=half, boundary_type=boundary_type)
    min_y = openmc.YPlane(y0=-half, boundary_type=boundary_type)
    max_y = openmc.YPlane(y0=half, boundary_type=boundary_type)
    min_z = openmc.ZPlane(z0=-half, boundary_type=boundary_type)
    max_z = openmc.ZPlane(z0=half, boundary_type=boundary_type)

    # this is the return of the six sided cube
    return +min_x & -max_x & +min_y & -max_y & +min_z & -max_z

def pack_triso_particles(triso_univ, region, packing_fraction=0.3, seed=124848351):
    ## randomly places non-overlapping particles in the region, returns TRISO objects.

    outer_radius = PARTICLE_RADIUS_UM * UM_TO_CM

    ## Choose the particle center locations
    # pf is the packing fraction (amount of region volume taken up by particles)
    # seed makes the random layout identical on each run
    centers = openmc.model.pack_spheres(
        radius=outer_radius, region=region, pf=packing_fraction, seed=seed
    )

    ##turn each center into a cell
    # each TRISO is a cell, a sphere of outer_radius, filled with the shared universe,
    # shifted so that the universe's origin sits at that center
    return [openmc.model.TRISO(outer_radius, triso_univ, c) for c in centers]

def build_compact_cell(trisos, region, matrix, shape=(3,3,3)):
    ## return a cell filled with a lattice that holds the particles in matrix graphite

    compact = openmc.Cell(name='compact', region=region)

    ##size the lattice exactly to cover the region
    lower_left, upper_right = compact.region.bounding_box
    pitch = (upper_right - lower_left) / shape

    ## sort particles into lattice cells, with graphite as the background
    lattice = openmc.model.create_triso_lattice(
        trisos, lower_left, pitch, shape, matrix
    )
    compact.fill = lattice
    return compact

def build_geometry(mats, side_cm=1.0, packing_fraction=0.3):
    ## Standalone test geometry: one TRISO-filled cube. Returns (geometry, kernel_cell).

    triso_univ = build_triso_universe(mats)
    region = build_box_region(side_cm)
    trisos = pack_triso_particles(triso_univ, region, packing_fraction)
    compact = build_compact_cell(trisos, region, mats['matrix'])

    geometry = openmc.Geometry(openmc.Universe(cells=[compact]))

    # tallies need the kernel cell, which lives inside the particle universe
    kernel = next(c for c in triso_univ.cells.values() if c.name == 'kernel')
    return geometry, kernel

# runs only with `python3 triso_geometry.py`, not when another file imports this one
if __name__ == "__main__":
    from triso_materials import build_triso_materials

    mats = build_triso_materials()
    univ = build_triso_universe(mats)
    region = build_box_region(1.0)
    trisos = pack_triso_particles(univ, region)

    outer_radius = PARTICLE_RADIUS_UM * UM_TO_CM
    centers = np.vstack([t.center for t in trisos])
    print("particles:", len(trisos))
    print("packing fraction:", len(trisos) * 4 / 3 * np.pi * outer_radius**3 / 1.0)
    print("center min:", centers.min(axis=0))
    print("center max:", centers.max(axis=0))