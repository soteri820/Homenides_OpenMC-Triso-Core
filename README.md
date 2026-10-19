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

Run each project from its own folder:

```
cd <project_folder>
python <main_script>.py
```

<!-- Fill in the actual folder and script names for each project. -->

## Repo Structure

```
.
├── pincell/                    # UO2 pincell project
├── triso/                      # TRISO project
├── kaleidos-mockup_claude/     # Claude-generated Kaleidos core image (modeling is a future step)
└── README.md
```

<!-- Update folder and file names to match the repo. -->

## Acknowledgments

- The OpenMC development team and documentation, for the original examples.
- Claude (Anthropic), for refactoring and commenting the code and generating the Kaleidos core mockup.
