import openmc

def build_tallies(fuel_cell):
    ## must define what the script will record
    # return tallies fro the U235 reaction rate in the fuel cell

    ## filter: where to record events
    # only events that happen inside the fuel cell count
    cell_filter = openmc.CellFilter(fuel_cell)

    ## tally is the definition of what to record
    tally = openmc.Tally(name='U235 Reaction Rates')
    tally.filters = [cell_filter]

    # limit scores to u235 (would otherwise get totals over all nuclides)
    tally.nulides = ['U235']

    # total interaction rate, fission, absorption (capture + fission), radiative capture
    tally.scores = ['total', 'fission', 'absorption', '(n,gamma)']

    return openmc.Tallies([tally])