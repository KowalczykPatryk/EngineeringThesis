## Where files and subrepositories come from

Some files or subrepositories in this repository that were needed to create simulation of LArTPC events were copied or adapted from other projects.

Submodules (`edep-sim`, `DLPGenerator`) are listed in `.gitmodules`. Any local changes to them are in `patches/`.

Separate files are from [simlar repository](https://github.com/DeepLearnPhysics/simlar) from commit `f8ba881e996e6aecef8b5ea03df7fd6d43d991e1`

## Mapping from sources to this repo and what was changed

| File here | Upstream file | Changes |
|---|---|---|
| `runs/dlp_multi/geometry/BigLArCube.gdml` | `generator/geometry/BigLArCube.gdml` | none (byte-identical copy) |
| `runs/dlp_multi/make_job.sh` (macro written to `g4.mac`) | `generator/biglarbox.mac` | per-job random seeds; config file renamed to `gen.yaml` |
| `runs/dlp_multi/dlp_multi.yaml` | `generator/mpvmpr_ccmu.yaml` | only the YAML layout is reused; particle content is the DLP v0.1.0 multi-particle recipe |

## Reason of each file explained

- BigLArCube.gdml - it describes the detector geometry Geant4 should simulate. GDML means Geometry Description Markup Language.

- g4.mac - the macro that controls how edep-sim/Geant4 runs. A .mac file is a Geant4 macro (a list of runtime commands).

- dlp_multi.yaml - is the configuration for DLPGenerator. It describes the initial state of each simulated interaction: how many primary particles to create, which particle species are allowed, their kinetic energies, where the common vertex is, and how randomness is seeded.

## Submodule patches

A .patch is essentially a textual Git diff.

- 0001-geant4-11.4-compatibility.patch - compatibility updates for newer version of Geant4
- 0002-kill-stuck-low-energy-tracks.patch - it is intended to protect simulation jobs against pathological tracks that remain alive for excessive numbers of tiny/low-energy steps.

