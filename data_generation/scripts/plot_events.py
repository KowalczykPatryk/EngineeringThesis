"""Event displays: 2D projections (value + label) with truth start/end markers.

Usage: python plot_events.py dlp.h5 outdir [n_events] [min_MeV]

Marked particles: every primary with deposits in the crop, plus every secondary
track-like particle (not e+-, gamma, neutron) with >= min_MeV (default 5) in the crop.
Each marked particle has one colour (see legend; "P" primary, "S" secondary):
  o  start = first energy deposit
  x  end   = last energy deposit
  v  track leaves the crop: last deposit inside the crop (true end is outside)
  ^  track enters the crop: first deposit inside the crop (true start is outside)
  s  photon: first deposit of its shower (conversion / Compton point)
Shower particles (e+-, gamma) get a start marker only.
Particles sharing a start point (e.g. all primaries at the vertex) are drawn as concentric rings.
Pixel index i spans [i, i+1) in these coordinates.
"""
import os
import sys

import h5py
import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D

from data_generation.scripts.lartpc_post import N_VOX, PLANES, to_voxel

AXES = "xyz"
NAMES = {11: "e-", -11: "e+", 13: "mu-", -13: "mu+", 22: "gamma", 211: "pi+", -211: "pi-",
         2212: "p", 2112: "n", 111: "pi0", 1000010020: "d", 1000010030: "t", 1000020040: "alpha"}
SHOWER = (11, 22)


def pname(pdg):
    if pdg in NAMES:
        return NAMES[pdg]
    if pdg > 1000000000:
        return f"ion Z={(pdg // 10000) % 1000} A={(pdg // 10) % 1000}"
    return str(pdg)


def in_crop(point_vox):
    return bool(np.all(np.isfinite(point_vox)) and np.all((point_vox >= 0) & (point_vox < N_VOX)))


def marked_particles(T, min_mev):
    prim = T["is_primary"] & (T["tree_de_in_crop"] > 0)
    sec = (~T["is_primary"] & ~np.isin(np.abs(T["pdg"]), SHOWER) & (T["pdg"] != 2112)
           & (T["de_in_crop"] >= min_mev))
    return T[prim | sec]


def draw_markers(A, a, b, marks, colors, o):
    ring = {}
    for c, t in zip(colors, marks):
        shower = abs(t["pdg"]) in SHOWER
        if t["n_steps"] == 0:  # photon: shower start
            s = to_voxel(t["tree_first_step"], o)
            if in_crop(s):
                A.plot(s[a], s[b], "s", mfc="none", mec=c, ms=11, mew=2)
            continue
        first, first_c = to_voxel(t["first_step"], o), to_voxel(t["first_step_in_crop"], o)
        last, last_c = to_voxel(t["last_step"], o), to_voxel(t["last_step_in_crop"], o)
        if in_crop(first):
            key = tuple(np.round(first, 1))
            k = ring[key] = ring.get(key, -1) + 1
            A.plot(first[a], first[b], "o", mfc="none", mec=c, ms=9 + 4 * k, mew=2)
        elif in_crop(first_c):
            A.plot(first_c[a], first_c[b], "^", mfc="none", mec=c, ms=10, mew=2)
        if shower:
            continue
        if in_crop(last):
            A.plot(last[a], last[b], "x", color=c, ms=10, mew=2.5)
        elif in_crop(last_c):
            A.plot(last_c[a], last_c[b], "v", mfc="none", mec=c, ms=10, mew=2)


def legend_label(t, T):
    kind = "P" if t["is_primary"] else "S"
    label = f"{kind} id{t['track_id']} {pname(t['pdg'])} KE {t['ke_start']:.0f} MeV"
    if not t["is_primary"]:
        parent = T[t["parent_track_id"]]
        label += f"  <- id{parent['track_id']} {pname(parent['pdg'])} ({t['creation_process'].decode()})"
    return label


def main(path, outdir, n=4, min_mev=5.0):
    os.makedirs(outdir, exist_ok=True)
    with h5py.File(path) as f:
        for name in list(f)[:n]:
            g = f[name]
            o = g.attrs["crop_origin_mm"]
            T = g["particles"][:]
            img, lab = g["image2d"][:], g["label2d"][:]
            marks = marked_particles(T, min_mev)
            colors = plt.cm.tab10(np.arange(len(marks)) % 10)

            fig, ax = plt.subplots(2, 3, figsize=(19, 10.5))
            for p, (a, b) in PLANES.items():
                panels = [(np.log10(np.where(img[p] > 0, img[p], np.nan)), dict(cmap="Greys", vmin=1, vmax=3.5), "energy (log10)"),
                          (lab[p], dict(cmap=ListedColormap(["white", "#f4b183", "#9dc3e6"]), vmin=0, vmax=2),
                           "label: orange shower, blue track")]
                for r, (data, kw, title) in enumerate(panels):
                    A = ax[r, p]
                    # data[i, j]: i along axis a (horizontal), j along axis b (vertical)
                    A.imshow(data.T, origin="lower", extent=(0, N_VOX, 0, N_VOX), interpolation="nearest", **kw)
                    draw_markers(A, a, b, marks, colors, o)
                    A.set_xlim(0, N_VOX)
                    A.set_ylim(0, N_VOX)
                    A.set_xlabel(f"{AXES[a]} [px]")
                    A.set_ylabel(f"{AXES[b]} [px]")
                    A.set_title(f"plane {p} ({AXES[a].upper()}{AXES[b].upper()}) {title}")

            particle_handles = [Line2D([], [], color=c, lw=4, label=legend_label(t, T)) for c, t in zip(colors, marks)]
            key_handles = [Line2D([], [], ls="", marker=m, mfc="none", mec="k", color="k", ms=9, mew=2, label=l) for m, l in [
                ("o", "start (first deposit)"), ("x", "end (last deposit)"),
                ("v", "leaves crop (last deposit inside)"), ("^", "enters crop (first deposit inside)"),
                ("s", "photon: shower start")]]
            fig.legend(handles=particle_handles, loc="upper left", bbox_to_anchor=(0.755, 0.97), fontsize=9,
                       title=f"particles (primaries + secondary tracks >= {min_mev:g} MeV)")
            fig.legend(handles=key_handles, loc="lower left", bbox_to_anchor=(0.755, 0.05), fontsize=9, title="markers")
            fig.suptitle(name)
            fig.tight_layout(rect=(0, 0, 0.75, 0.97))
            fig.savefig(f"{outdir}/{name}.png", dpi=80)
            plt.close(fig)
            print("wrote", f"{outdir}/{name}.png")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 4,
         float(sys.argv[4]) if len(sys.argv) > 4 else 5.0)
