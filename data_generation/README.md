Simulation of LArTPC events (edep-sim) turned into DLP-style 2D/3D images with per-particle truth.

## Running simulation
For a new machine / clean checkout, the sequence is:

#### 1. Clone main repository
```bash
git clone https://github.com/KowalczykPatryk/EngineeringThesis
cd EngineeringThesis
```
#### 2. Download pinned submodules
```bash
git submodule update --init --recursive
```
#### 3. Create/install the native software environment
```bash
cd data_generation
pixi install
```
[pixi](https://pixi.sh)  
The command `pixi install` reads project's configuration file (`pyproject.toml` or `pixi.toml`), resolves all dependencies and their exact versions into a lock file (`pixi.lock`), and builds a local environment inside a `.pixi` directory.
#### 4. Activate that environment for building
```bash
eval "$(pixi shell-hook)"
```
Running `eval "$(pixi shell-hook)"` is the way to activate a project environment within current terminal session without opening a brand-new shell.  
The `$()` syntax tells shell to run the command inside the parentheses first and capture whatever text it prints out.  
`pixi shell-hook` prints a plain-text script containing all the environment variables needed to run project.  
`eval` takes that text script and executes it directly inside current shell session.
#### 5. Build DLPGenerator
```bash
cd DLPGenerator
source setup.sh
make -j"$(nproc)"
cd ../..
```
#### 6. Apply local edep-sim patches
```bash
git -C data_generation/edep-sim apply --check ../patches/edep-sim/0001-geant4-11.4-compatibility.patch
git -C data_generation/edep-sim apply ../patches/edep-sim/0001-geant4-11.4-compatibility.patch

git -C data_generation/edep-sim apply --check ../patches/edep-sim/0002-kill-stuck-low-energy-tracks.patch
git -C data_generation/edep-sim apply ../patches/edep-sim/0002-kill-stuck-low-energy-tracks.patch
```
#### 7. Make DLPGenerator/local paths visible
```bash
source data_generation/env.sh
cd data_generation
```
#### 8. Configure edep-sim
```bash
cmake \
    -S edep-sim \
    -B edep-sim-build \
    -DCMAKE_INSTALL_PREFIX="$PWD/edep-sim-install" \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
    -DCMAKE_PREFIX_PATH="$PWD/.pixi/envs/default" \
    -DEXPAT_ROOT="$PWD/.pixi/envs/default"
```
#### 9. Compile
```bash
cmake --build edep-sim-build -j"$(nproc)"
```
#### 10. Install locally
```bash
cmake --install edep-sim-build
```
#### 11. Export paths
```bash
source env.sh
```
#### 12. Verify
```bash
which edep-sim
```
#### 13. Running simulation
```bash
./runs/dlp_multi/make_job.sh 0 100
```
where:  
`0` - job ID  
`100` - number of Geant4 events


## edem-sim in nutshell

edep-sim is a wrapper around Geant4: Geant4 performs the actual propagation/interactions of particles in matter, while edep-sim provides a ready-to-use application around it, with geometry loading, event generators, macro commands and persistence/output.

## DLPGenerator in nutshell

DLPGenerator is upstream's configurable synthetic particle-event generator: YAML describes interaction/particle content, positions, energies, etc.

## Simulation result
The results of the simulations are placed in the `runs/dlp_multi/job_XXXX/` (XXXX is the job id) folder and stored in the edep.h5 file. The structure and content of edep.h5 file is described in the `insect_dataset/edep.md`.

## Extracting images from an existing simulation file

The raw simulation file `edep.h5` is not in git (it is ~400 MB for 100 events so placed in gitignore). You need to run simulation. 


```bash
uv sync

# 1. edep.h5 -> dlp.h5 (3D voxels, 2D images, 2D labels, particle truth)
uv run python lartpc_post.py runs/dlp_multi/job_0000/edep.h5 runs/dlp_multi/job_0000/dlp.h5 --seed 0

# 2. dlp.h5 -> PNG event displays (first 6 events)
uv run python plot_events.py runs/dlp_multi/job_0000/dlp.h5 runs/dlp_multi/plots 6
```

Run both from the repository root (`plot_events.py` imports `lartpc_post`). PNGs are written to `runs/dlp_multi/plots/event_XXXXXX.png`. An optional 4th argument to `plot_events.py` sets the minimum deposited energy [MeV] for marking secondary tracks (default 5).

### Using the arrays directly

```python
import h5py
f = h5py.File("runs/dlp_multi/job_0000/dlp.h5")
g = f["event_000000"]
img   = g["image2d"][:]    # (3, 256, 256): planes XY, YZ, ZX; energy*100, pixels < 10 set to 0
label = g["label2d"][:]    # (3, 256, 256): 0 background, 1 shower, 2 track
vox   = g["voxels/coords"][:], g["voxels/energy"][:], g["voxels/label"][:]   # sparse 3D
truth = g["particles"][:]  # per-particle table
```

`img[p][i, j]`: `i` runs along the first axis of the plane name and `j` along the second
(for XY, `i` = x and `j` = y). Plot with `imshow(img[p].T, origin="lower")`.

See `edep_h5_structure.md` for the layout of `edep.h5`, and the docstring of `lartpc_post.py`
for the conventions used in `dlp.h5`.



