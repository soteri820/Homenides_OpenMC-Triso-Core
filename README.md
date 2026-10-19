# OpenMC Learning Projects: UO2 Pincell and TRISO Fuel

Two small OpenMC models I built to learn how the library works, plus a mockup of the Radiant Kaleidos core that sets up the next step. Both models are modified versions of examples from the [OpenMC documentation](https://docs.openmc.org/), split into separate files and heavily commented.

## About This Repo

- **Source material.** Both projects come from the OpenMC documentation examples. The physics setups are theirs. What I changed is the structure.
- **Claude's role.** Claude refactored the provided example code into separate, less overwhelming files and added explicit commentary explaining what each piece does. That commentary is how I learned how the library works.
- **Timeline.** All of this was done on Sunday, October 18 and Monday morning, October 19, 2026.
- **My level of understanding.** I have a strong but not complete understanding of everything in here. I am currently taking reactor physics and have not completed it yet, so some of the physics and some modeling choices are things I am still learning. If something looks off, it may well be.

## Projects

### 1. UO2 Pincell (PWR-style)

A classic pressurized water reactor pincell:

- UO2 fuel
- Gap
- Zirconium cladding
- Water moderator
- Criticality calculation (k-effective)

Based on the pincell example in the OpenMC documentation.

### 2. TRISO Fuel Model

A TRISO fuel model representing an infinite TRISO compact, the cylindrical-style fuel form used in high temperature gas-cooled reactors. Each particle has the usual layered structure (fuel kernel, buffer, pyrolytic carbon, silicon carbide, outer pyrolytic carbon) and the particles are packed in a graphite matrix. Reflective boundaries make the compact effectively infinite.

Based on the TRISO example in the OpenMC documentation.

### 3. Kaleidos Mockup (`kaleidos-mockup_claude/`)

A Claude-generated image of the Kaleidos core. This is not a working model yet. It is the target for the next phase of the project.

**Planned next steps:** model the core in OpenMC using what I learned from the two completed examples above. The plan is:

- Use a quartered geometry with reflective boundary conditions on the cut walls, so only a quarter of the core needs to be simulated.
- Model how reactivity changes as the boron absorber arcs on the control drums are rotated.

## Requirements

This repo relies on OpenMC, so it needs one of the following:

- **Windows:** run inside a Docker container with OpenMC installed.
- **Linux:** run natively with OpenMC installed.

You will also need cross section data available to OpenMC (the `OPENMC_CROSS_SECTIONS` environment variable pointing to your `cross_sections.xml`).

### Running with Docker (Windows)

1. Install Docker Desktop.
2. Start a container with OpenMC and mount this repo into it:

   ```
   docker run -it --rm -v "%cd%":/work -w /work <openmc-image> bash
   ```

   Replace `<openmc-image>` with the OpenMC image you are using. In PowerShell, use `${PWD}` instead of `%cd%`.
3. Inside the container, run the scripts as described below.

### Running natively (Linux)

Install OpenMC (see the [OpenMC install guide](https://docs.openmc.org/en/stable/usersguide/install.html)), set up cross section data, then run the scripts from the repo root.

## Usage

Run each project from its own folder.

**UO2 pincell**

```
cd pincell
python pincell_main.py
```

Writes the OpenMC input files, runs the eigenvalue calculation, prints k-effective, and writes `pinplot.png`.

**TRISO compact**

```
cd triso-example
python trisoex_main.py
```

Optional flags: `--seeds N` (run N transport seeds and report the spread in k), `--particles`, `--batches`, `--inactive`. Each seed runs in its own `run_seed_<N>/` folder, and the plots are written for seed 1.

## Results

Fill these in after running each model.

| Model | k-effective | Settings | Notes |
|---|---|---|---|
| UO2 pincell | _TBD_ ± _TBD_ | 100 batches, 10 inactive, 1000 particles | |
| TRISO compact | _TBD_ ± _TBD_ | 100 batches, 10 inactive, 1000 particles | |

Multi-seed TRISO run (`python trisoex_main.py --seeds 3`): mean k = _TBD_, spread (std) = _TBD_

Cross section library and OpenMC version used: _TBD_

![UO2 pincell geometry](pincell/pinplot.png)
![TRISO compact overview](triso-example/run_seed_1/triso_overview.png)
![TRISO particle layers](triso-example/run_seed_1/triso_zoom.png)

## Repo Structure

```
.
├── pincell/                    # UO2 pincell project
├── triso-example/              # TRISO compact project
├── kaleidos-mockup_claude/     # Claude-generated Kaleidos core image (modeling is a future step)
│   └── kaleidos_mockup.png
└── README.md
```

## Acknowledgments

- The OpenMC development team and documentation, for the original examples.
- Claude (Anthropic), for refactoring and commenting the code and generating the Kaleidos core mockup.
