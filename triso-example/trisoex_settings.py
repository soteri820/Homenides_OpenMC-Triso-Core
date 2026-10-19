import openmc


def build_settings(lower_left, upper_right, particles=1000, batches=100, inactive=10, seed=1):
    ## Return run settings for a k-eigenvalue calculation over a box-shaped region.

    ## starting neutron source
    # sample points uniformly in the box, but only keep ones that land in fuel
    # (this replaces the pincell's single point, which only worked because
    # the origin happened to be inside the fuel)
    space = openmc.stats.Box(lower_left, upper_right)
    source = openmc.IndependentSource(space=space, constraints={'fissionable': True})

    settings = openmc.Settings()
    settings.source = source

    # kernels are only ~4% of the volume, so ~96% of sampled points get thrown away
    # the default rejection limit would call that an error, so loosen it
    settings.source_rejection_fraction = 0.01

    ## run parameters
    # eigenvalue mode (k-effective) is the default
    settings.batches = batches
    settings.particles = particles
    # first generations are discarded so the fission source can settle
    settings.inactive = inactive

    # transport random number seed (default is 1, set explicitly so it is visible)
    settings.seed = seed

    ## Shannon entropy: a per-batch number that shows whether the source has settled
    # it is computed on a coarse mesh covering the same box
    entropy_mesh = openmc.RegularMesh()
    entropy_mesh.lower_left = lower_left
    entropy_mesh.upper_right = upper_right
    entropy_mesh.dimension = (4, 4, 4)
    settings.entropy_mesh = entropy_mesh

    return settings