import openmc


def build_plots(mats, pitch):
    """Return a Plots collection with one material-colored slice of the pin cell."""

    plot = openmc.Plot()
    plot.filename = 'pinplot'        # output will be pinplot.png
    plot.width = (pitch, pitch)      # field of view in cm, matches the unit cell
    plot.pixels = (400, 400)         # image resolution
    plot.basis = 'xy'                # slice plane (the default)
    plot.color_by = 'material'       # color each region by its material

    # colors are keyed by the Material objects themselves, not by name strings
    plot.colors = {
        mats["uo2"]: 'yellow',
        mats["zirconium"]: 'gray',
        mats["water"]: 'blue',
    }

    return openmc.Plots([plot])