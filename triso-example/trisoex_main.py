import argparse
import os

import numpy as np
import openmc

from trisoex_materials import build_triso_materials
from trisoex_geometry import build_geometry
from trisoex_settings import build_settings
from trisoex_tallies import build_tallies
from trisoex_plotting import build_plots

def build_model(seed=1, particles=1000, batches=100, inactive=10):
    ## Assembles every piece into one openmc.Model

    mats = build_triso_materials()
    geometry, kernel = build_geometry(mats)

    ## the settings need the box bounds, which the geometry already knows
    lower_left, upper_right = geometry.bounding_box
    settings = build_settings(lower_left, upper_right, particles=particles, batches=batches, inactive=inactive, seed=seed)

    return openmc.Model(
        geometry = geometry,
        materials = openmc.Materials(mats.values()),
        settings=settings,
        tallies = build_tallies(kernel),
        plots = build_plots(mats),
    )
def run_one(seed, workdir, make_plots=False, **kwargs):
    """Run a single eigenvalue calculation in its own folder. Returns the statepoint path."""

    # each run gets its own folder so XML and output files never overwrite each other
    os.makedirs(workdir, exist_ok=True)
    model = build_model(seed=seed, **kwargs)

    if make_plots:
        model.plot_geometry(cwd=workdir)
    return model.run(cwd=workdir)


def report(statepoint_path):
    """Print k-eff, the entropy trend, and the tally sanity checks."""

    with openmc.StatePoint(statepoint_path) as sp:
        print("k-effective:", sp.keff)
        print("entropy, last 5 batches:", np.round(sp.entropy[-5:], 3))

        rates = sp.get_tally(name='kernel reaction rates').get_pandas_dataframe()
        print(rates[['nuclide', 'score', 'mean', 'std. dev.']].to_string(index=False))

        nu_fission = rates[rates['score'] == 'nu-fission']['mean'].sum()
        print("nu-fission summed over U235 + U238:", round(nu_fission, 4))

        return sp.keff.nominal_value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seeds', type=int, default=1,
                        help='number of transport seeds to run (1..N)')
    parser.add_argument('--particles', type=int, default=1000)
    parser.add_argument('--batches', type=int, default=100)
    parser.add_argument('--inactive', type=int, default=10)
    args = parser.parse_args()

    keffs = []
    for seed in range(1, args.seeds + 1):
        path = run_one(seed, workdir=f'run_seed_{seed}', make_plots=(seed == 1),
                       particles=args.particles, batches=args.batches,
                       inactive=args.inactive)
        keffs.append(report(path))

    ## spread across seeds should be about the size of the reported +/-
    if len(keffs) > 1:
        print(f"\nseeds 1..{len(keffs)}: mean k = {np.mean(keffs):.5f}, "
              f"spread (std) = {np.std(keffs, ddof=1):.5f}")


# runs only with `python3 triso.py`, not when another file imports this one
if __name__ == "__main__":
    main()