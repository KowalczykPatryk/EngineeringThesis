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

## Submodule patches

