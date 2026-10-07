"""Convert edep-sim (DLP HDF5 fork) output into DLP-style 2D/3D images with exact particle truth.

Conventions (DLP v0.1.0 multi-particle sample):
  - 128 cm crop cube, 0.5 cm voxels -> 256^3 voxels / 256x256 images
  - planes: 0 = XY, 1 = YZ, 2 = ZX; image2d[p][i, j] with i along the first axis
    of the plane name (x for XY) and j along the second (y for XY). This is
    larcv's (col, row) order: pixel id = col * 256 + row.
  - pixel value = summed energy deposit [MeV] * 100; pixels < 10 set to 0;
    event dropped if any plane has < 5 pixels >= 10
  - labels: 0 background, 1 shower (|pdg| in 11, 22), 2 track (everything else);
    voxel/pixel containing both -> track

Coordinates: detector frame in mm (edep-sim/Geant4 native). Crop frame "voxel
units" = (mm - crop_origin_mm) / 5; a point at voxel coordinate u lies in voxel
floor(u). All truth and deposits share one frame (no space-charge distortion).

Usage: python lartpc_post.py edep.h5 out.h5 [--crop maxcontain|random|center] [--seed N] [--keep-all]
"""
import argparse

import h5py
import numpy as np

VOXEL_MM = 5.0
N_VOX = 256
CROP_MM = VOXEL_MM * N_VOX
PIXEL_SCALE = 100.0
PIXEL_THRESHOLD = 10.0
MIN_PIXELS = 5
PLANES = {0: (0, 1), 1: (1, 2), 2: (2, 0)}  # plane -> (axis i, axis j); axis order x, y, z
SHOWER_PDG = (11, 22)
INVALID_INT = np.iinfo(np.int32).max

LABEL_SHOWER, LABEL_TRACK = 1, 2

PARTICLE_DTYPE = np.dtype([
    ("track_id", "i4"), ("parent_track_id", "i4"), ("ancestor_track_id", "i4"),
    ("pdg", "i4"), ("is_primary", "?"), ("mass", "f4"),
    ("creation_process", "S32"), ("end_process", "S32"),
    ("ke_start", "f4"), ("ke_end", "f4"),
    ("start", "f4", 4),              # creation vertex x,y,z [mm], t [ns]
    ("end", "f4", 4),                # track end point
    ("first_step", "f4", 4),         # midpoint of first energy-deposit step
    ("first_step_edge", "f4", 3),    # start edge of that step (midpoint - dx/2 * direction)
    ("last_step", "f4", 4),          # midpoint of last energy-deposit step
    ("first_step_in_crop", "f4", 4), # first / last deposit inside the crop (NaN if none)
    ("last_step_in_crop", "f4", 4),
    ("n_steps", "i4"), ("de_total", "f4"), ("de_in_crop", "f4"),
    # same, over the particle and all its descendants (e.g. shower start of a photon)
    ("tree_first_step", "f4", 4), ("tree_de_total", "f4"), ("tree_de_in_crop", "f4"),
])


def event_arrays(f, ev):
    return (f["particle/geant4"][ev], f["pstep/lar_vol"][ev],
            f["ass/particle_pstep_lar_vol"][ev], f["vertex/geant4"][ev])


def choose_crop(xyz_mm, de, vertex_mm, mode, rng, n_candidates=32):
    """Lower corner of the crop [mm]; the vertex is always inside the crop."""
    if mode == "center":
        return vertex_mm - CROP_MM / 2
    cand = vertex_mm - rng.uniform(0, CROP_MM, size=(1 if mode == "random" else n_candidates, 3))
    if mode == "random":
        return cand[0]
    contained = [de[np.all((xyz_mm >= o) & (xyz_mm < o + CROP_MM), axis=1)].sum() for o in cand]
    return cand[int(np.argmax(contained))]


def voxelize(xyz_mm, de, is_track, origin_mm):
    """Sparse 3D voxels: coords (N,3) uint8, energy [MeV] float32, label uint8."""
    idx = np.floor((xyz_mm - origin_mm) / VOXEL_MM).astype(np.int64)
    inside = np.all((idx >= 0) & (idx < N_VOX), axis=1)
    idx, de, is_track = idx[inside], de[inside], is_track[inside]
    flat = (idx[:, 0] * N_VOX + idx[:, 1]) * N_VOX + idx[:, 2]
    uniq, inv = np.unique(flat, return_inverse=True)
    energy = np.bincount(inv, weights=de, minlength=len(uniq)).astype(np.float32)
    track = np.bincount(inv, weights=is_track, minlength=len(uniq)) > 0
    coords = np.stack([uniq // N_VOX**2, (uniq // N_VOX) % N_VOX, uniq % N_VOX], axis=1).astype(np.uint8)
    label = np.where(track, LABEL_TRACK, LABEL_SHOWER).astype(np.uint8)
    return coords, energy, label, inside


def project(coords, energy, label):
    """2D images (3,256,256) float32 and labels (3,256,256) uint8, DLP thresholding."""
    image = np.zeros((3, N_VOX, N_VOX), np.float32)
    lab = np.zeros((3, N_VOX, N_VOX), np.uint8)
    for p, (a, b) in PLANES.items():
        np.add.at(image[p], (coords[:, a], coords[:, b]), energy * PIXEL_SCALE)
        np.maximum.at(lab[p], (coords[:, a], coords[:, b]), label)  # track (2) wins over shower (1)
    below = image < PIXEL_THRESHOLD
    image[below] = 0
    lab[below] = 0
    return image, lab


def particle_table(P, S, A, inside_step):
    n = len(P)
    T = np.zeros(n, PARTICLE_DTYPE)
    for name in ("track_id", "parent_track_id", "ancestor_track_id", "pdg", "mass"):
        T[name] = P[name]
    T["is_primary"] = P["parent_track_id"] == -1
    T["creation_process"] = P["proc_name_start"]
    T["end_process"] = P["proc_name_end"]
    T["ke_start"], T["ke_end"] = P["ke"], P["end_ke"]
    T["start"] = np.stack([P["x"], P["y"], P["z"], P["t"]], axis=1)
    T["end"] = np.stack([P["end_x"], P["end_y"], P["end_z"], P["end_t"]], axis=1)
    nan4 = np.full(4, np.nan, np.float32)
    for i in range(n):
        s, e = int(A[i]["start"]), int(A[i]["end"])
        T["n_steps"][i] = e - s
        if e == s:
            T["first_step"][i] = T["last_step"][i] = nan4
            T["first_step_in_crop"][i] = T["last_step_in_crop"][i] = nan4
            T["first_step_edge"][i] = np.nan
            continue
        steps = S[s:e]  # time-ordered, all with de > 0 (checked on production output)
        first, last = steps[0], steps[-1]
        T["first_step"][i] = (first["x"], first["y"], first["z"], first["t"])
        T["last_step"][i] = (last["x"], last["y"], last["z"], last["t"])
        th, ph = first["theta"], first["phi"]
        direction = np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])
        T["first_step_edge"][i] = np.array([first["x"], first["y"], first["z"]]) - 0.5 * first["dx"] * direction
        T["de_total"][i] = steps["de"].sum()
        in_crop = np.flatnonzero(inside_step[s:e])
        T["de_in_crop"][i] = steps["de"][in_crop].sum()
        if len(in_crop):
            fc, lc = steps[in_crop[0]], steps[in_crop[-1]]
            T["first_step_in_crop"][i] = (fc["x"], fc["y"], fc["z"], fc["t"])
            T["last_step_in_crop"][i] = (lc["x"], lc["y"], lc["z"], lc["t"])
        else:
            T["first_step_in_crop"][i] = T["last_step_in_crop"][i] = nan4

    # Accumulate over descendants; parents always precede children in edep-sim output.
    assert np.all(T["parent_track_id"] < np.arange(n)), "parent after child"
    T["tree_first_step"] = T["first_step"]
    T["tree_de_total"], T["tree_de_in_crop"] = T["de_total"], T["de_in_crop"]
    for i in range(n - 1, -1, -1):
        j = T["parent_track_id"][i]
        if j < 0:
            continue
        T["tree_de_total"][j] += T["tree_de_total"][i]
        T["tree_de_in_crop"][j] += T["tree_de_in_crop"][i]
        ti, tj = T["tree_first_step"][i][3], T["tree_first_step"][j][3]
        if not np.isnan(ti) and (np.isnan(tj) or ti < tj):
            T["tree_first_step"][j] = T["tree_first_step"][i]
    return T


def process(in_path, out_path, crop="maxcontain", seed=0, keep_all=False):
    rng = np.random.default_rng(seed)
    stats = dict(n_in=0, n_out=0, unassociated_steps=0)
    with h5py.File(in_path, "r") as f, h5py.File(out_path, "w") as out:
        out.attrs.update(voxel_mm=VOXEL_MM, n_voxel=N_VOX, crop_mode=crop, seed=seed, source=str(in_path),
                         planes="0=XY 1=YZ 2=ZX; image2d[p][i,j], i along first axis",
                         pixel_scale=PIXEL_SCALE, pixel_threshold=PIXEL_THRESHOLD)
        n_events = len(f["event/geant4"])
        for ev in range(n_events):
            stats["n_in"] += 1
            P, S, A, V = event_arrays(f, ev)
            n = len(P)
            stats["unassociated_steps"] += int(A[n]["end"] - A[n]["start"]) if len(A) > n else 0
            xyz = np.stack([S["x"], S["y"], S["z"]], axis=1).astype(np.float64)
            de = S["de"].astype(np.float64)
            # unassociated steps (track_id invalid) have pdg invalid -> labelled track
            is_track = ~np.isin(np.abs(S["pdg"]), SHOWER_PDG)
            vertex = np.array([V[0]["x"], V[0]["y"], V[0]["z"]], np.float64)

            origin = choose_crop(xyz, de, vertex, crop, rng)
            coords, energy, label, inside = voxelize(xyz, de, is_track, origin)
            image, lab2d = project(coords, energy, label)
            passed = all((image[p] >= PIXEL_THRESHOLD).sum() >= MIN_PIXELS for p in range(3))
            if not passed and not keep_all:
                continue

            g = out.create_group(f"event_{ev:06d}")
            g.attrs.update(event_id=int(f["event/geant4"][ev]["event_id"]), crop_origin_mm=origin,
                           vertex_mm=vertex, passed_threshold=passed)
            comp = dict(compression="gzip", compression_opts=4, shuffle=True)
            g.create_dataset("voxels/coords", data=coords, **comp)
            g.create_dataset("voxels/energy", data=energy, **comp)
            g.create_dataset("voxels/label", data=label, **comp)
            g.create_dataset("image2d", data=image, **comp)
            g.create_dataset("label2d", data=lab2d, **comp)
            g.create_dataset("particles", data=particle_table(P, S, A, inside), **comp)
            stats["n_out"] += 1
    return stats


def to_voxel(points_mm, origin_mm):
    """Detector mm -> crop voxel units (float). Voxel index = floor of this."""
    return (np.asarray(points_mm)[..., :3] - origin_mm) / VOXEL_MM


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--crop", choices=["maxcontain", "random", "center"], default="maxcontain")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--keep-all", action="store_true", help="keep events failing the 2D pixel threshold")
    args = ap.parse_args()
    print(process(args.input, args.output, args.crop, args.seed, args.keep_all))


if __name__ == "__main__":
    main()
