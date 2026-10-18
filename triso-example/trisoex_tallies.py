import numpy as np
import openmc


def build_tallies(kernel_cell):
    """Return tallies for reaction rates and neutron spectrum in the fuel kernels."""

    ## filter: WHERE to record events
    # kernel_cell is one cell inside the shared particle universe, but it appears
    # once per particle (~900 times). A CellFilter adds up every copy, so this
    # gives the total over all kernels in the compact.
    cell_filter = openmc.CellFilter(kernel_cell)

    ## tally 1: reaction rates in the kernels, split by uranium isotope
    rates = openmc.Tally(name='kernel reaction rates')
    rates.filters = [cell_filter]
    rates.nuclides = ['U235', 'U238']
    # total interaction, fission, absorption (capture + fission), radiative capture,
    # and neutrons produced per fission (nu-fission, used for the k-eff sanity check)
    rates.scores = ['total', 'fission', 'absorption', '(n,gamma)', 'nu-fission']

    ## tally 2: flux and fission rate as a function of neutron energy
    # 100 log-spaced bins from 0.01 meV to 20 MeV (eV units)
    # log spacing because the interesting physics spans 9 orders of magnitude
    energy_filter = openmc.EnergyFilter(np.logspace(np.log10(1e-5), np.log10(2e7), 101))
    spectrum = openmc.Tally(name='kernel spectrum')
    spectrum.filters = [cell_filter, energy_filter]
    spectrum.scores = ['flux', 'fission']

    return openmc.Tallies([rates, spectrum])


# runs only with `python3 triso_tallies.py`, not when another file imports this one
if __name__ == "__main__":
    from triso_materials import build_triso_materials
    from triso_geometry import build_geometry

    _, kernel = build_geometry(build_triso_materials())
    print(build_tallies(kernel))