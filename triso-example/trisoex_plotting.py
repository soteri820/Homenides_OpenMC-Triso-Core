import openmc


def _material_plot(name, mats, width_cm, pixels=800, origin=(0, 0, 0), basis='xy'):
    """Return one 2D slice plot, colored by material."""

    plot = openmc.Plot(name=name)
    plot.filename = name
    plot.basis = basis
    plot.origin = origin
    plot.width = (width_cm, width_cm)
    plot.pixels = (pixels, pixels)
    plot.color_by = 'material'

    ## one color per material, keyed by the Material objects themselves
    plot.colors = {
        mats['triso_fuel']: 'red',
        mats['buffer']: 'yellow',
        mats['ipyc']: 'blue',
        mats['sic']: 'green',
        mats['opyc']: 'purple',
        mats['matrix']: 'gray',
    }
    return plot


def build_plots(mats, side_cm=1.0):
    """Return two plots: the whole compact cube, and a zoomed view of the layers."""

    ## overview: the full cross-section through the middle of the cube
    # a little wider than the cube so the edges are visible
    overview = _material_plot('triso_overview', mats, width_cm=side_cm * 1.05)

    ## zoom: 0.2 cm across is about 2 particle diameters, enough to see the layers
    zoom = _material_plot('triso_zoom', mats, width_cm=0.2, pixels=1000)

    return openmc.Plots([overview, zoom])


# runs only with `python3 triso_plotting.py`, not when another file imports this one
if __name__ == "__main__":
    from triso_materials import build_triso_materials

    print(build_plots(build_triso_materials()))