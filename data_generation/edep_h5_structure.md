# edep.h5 file structure

Raw output of the edep-sim fork (DLP HDF5 format), e.g. `runs/dlp_multi/job_0000/edep.h5` (100 events).

Every dataset holds **one entry per event**, and each entry is a variable-length table:
`f["particle/geant4"][ev]` is the particle table of event `ev`. Units: **mm, ns, MeV**.

```
edep.h5
├── event/geant4                   one row per event: run_id, event_id, num_vertices,
│                                  num_primaries, num_particles, num_steps
├── vertex/geant4[ev]              interaction vertex: x,y,z,t, ke_sum, energy_sum, num_particles
├── primary/geant4[ev]             particles fired by the generator: pdg, name, px,py,pz, ke, track_id
├── particle/geant4[ev]            EVERY particle Geant4 tracked (~1.5k per event)
│                                    creation: x,y,z,t, px,py,pz, ke, proc_name_start
│                                    end:      end_x..end_t, end_px..end_ke, proc_name_end
│                                    family:   track_id, parent_track_id (-1 = primary), ancestor_track_id
│                                    pdg, mass
├── pstep/lar_vol[ev]              every energy-deposit step in the LAr (~50k–160k per event)
│                                    x,y,z,t (step midpoint), dx (≤0.1 mm), de
│                                    theta,phi,p (momentum at step start)
│                                    track_id, ancestor_track_id, pdg, proc_start/proc_stop
└── ass/particle_pstep_lar_vol[ev] index linking particles to their steps: (start, end) per particle
    (ass/…_cryo, …_drift)          same for other volumes; empty in this geometry
```

## How the tables connect

- **Row index is the track id:** in `particle/geant4`, row `i` is the particle with `track_id == i`. The first rows are the primaries.
- **Particle to steps:** `ass[ev][i] = (start, end)` means particle `i`'s steps are `pstep/lar_vol[ev][start:end]`. They are contiguous and ordered in time. There is one extra entry at the end, for steps from particles that weren't saved; it has been empty in every test.
- **Particle to parent:** `parent_track_id` is a row index too. A parent's row always comes before its children's rows, so you can walk the family tree in one pass.

## Things to keep in mind

- **Photons and neutrons:** they have particle rows but usually no steps, because they don't deposit energy directly; their daughters do.
- **Recommended fields:** the verified truth is in `x, y, z, t`, `end_*`, `parent_track_id` and the steps. `end_ke` looks wrong for particles that decay.
- **No detector response:** these are true deposits in one common coordinate frame, with no drift, readout or distortion.

## Time stamps

- `pstep/lar_vol` field `t`: the time of every step.
- `particle/geant4` fields `t` and `end_t`: when each particle was created and when it ended.
- `vertex/geant4` field `t`: the vertex time.

## Example: read the steps of one track

```python
import h5py
f = h5py.File("runs/dlp_multi/job_0000/edep.h5")
S = f["pstep/lar_vol"][0]; A = f["ass/particle_pstep_lar_vol"][0]   # event 0
s, e = A[3]["start"], A[3]["end"]                                     # track id 3
S["x"][s:e], S["y"][s:e], S["z"][s:e], S["t"][s:e]                    # time-ordered steps
```
