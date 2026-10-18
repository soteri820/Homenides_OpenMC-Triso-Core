import openmc

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