import openmc

def build_settings():
    ## Return the run settings for the pin cell k-eigenvalue calculation

    # starting a neutron source
    # a single point at the origin, which is inside the fuel
    # neutrons must start somewhere fissionable
    point = openmc.stats.Point((0,0,0))
    source = openmc.IndependentSource(space=point)

    ## run parameters
    settings = openmc.Settings()
    settings.source = source

    # eigenvalue mode (k-effective) is the default, so no run_mode line is needed
    # 100 generations of 1000 neutrons each
    settings.batches = 100
    settings.particles = 1000

    # the first 10 generations are discarded so the fission source can settle into its true shape
    # the remaining 90 count toward k-eff and tallies
    settings.inactive = 10

    return settings

#