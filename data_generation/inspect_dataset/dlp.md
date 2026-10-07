If something is not descibed then check edep.md

# HDF5 format - Hierarchical Data Format version 5

It has structure similar to filesystem where:
- group is like folder
- dataset is like file

Dataset type works similar to numpy ndarrays (interface).

# Attributes of the file's root group

These attributes describe how edep.h5 was converted into the DLP-style voxel/2D representation.  
Physical geometry parameters:
- f.attrs['n_voxel']: 256 # number of voxels in each dimention
- f.attrs['voxel_mm']: 5.0 # size of each voxel in milimeters

A 3D image is conceptually a cube of 
256 × 256 × 256 voxels  
each voxel:  
5 mm × 5 mm × 5 mm  
and total:  
1280 mm × 1280 mm × 1280 mm
and a projected 2D image is 256 × 256, with one pixel corresponding spatially to
5 mm × 5 mm in its projection plane.

This tells the converter where to put that 1280-mm cube in detector coordinates:
- f.attrs['crop_mode']: maxcontain # Generate 32 possible 1.28-m crop cubes that all contain the interaction vertex, then select the cube containing the greatest total deposited energy.

Multiplier converting deposited energy in MeV into stored 2D pixel intensity:
- f.attrs['pixel_scale']: 100.0
pixel value = 100 x sum(energy deposited in each 3D voxel that projects onto that 2D pixel)

Minimum stored 2D pixel intensity - lower pixels become zero:
- f.attrs['pixel_threshold']: 10.0


- f.attrs['planes']: 0=XY 1=YZ 2=ZX; image2d[p][i,j], i along first axis
- f.attrs['seed']: 0 # Seed for random crop-position generation
- f.attrs['source']: runs/dlp_multi/job_0000/edep.h5

# Keys inside file's root group

```
<KeysViewHDF5 ['event_000000', 'event_000001', 'event_000002', 'event_000003', 'event_000004', 'event_000005', 'event_000006', 'event_000007', 'event_000008', 'event_000009', 'event_000010', 'event_000011', 'event_000012', 'event_000013', 'event_000014', 'event_000015', 'event_000016', 'event_000017', 'event_000018', 'event_000019', 'event_000020', 'event_000021', 'event_000022', 'event_000023', 'event_000024', 'event_000025', 'event_000026', 'event_000027', 'event_000028', 'event_000029', 'event_000030', 'event_000031', 'event_000032', 'event_000033', 'event_000034', 'event_000035', 'event_000036', 'event_000037', 'event_000038', 'event_000039', 'event_000040', 'event_000041', 'event_000042', 'event_000043', 'event_000044', 'event_000045', 'event_000046', 'event_000047', 'event_000048', 'event_000049', 'event_000050', 'event_000051', 'event_000052', 'event_000053', 'event_000054', 'event_000055', 'event_000056', 'event_000057', 'event_000058', 'event_000059', 'event_000060', 'event_000061', 'event_000062', 'event_000063', 'event_000064', 'event_000065', 'event_000066', 'event_000067', 'event_000068', 'event_000069', 'event_000070', 'event_000071', 'event_000072', 'event_000073', 'event_000074', 'event_000075', 'event_000076', 'event_000077', 'event_000078', 'event_000079', 'event_000080', 'event_000081', 'event_000082', 'event_000083', 'event_000084', 'event_000085', 'event_000086', 'event_000087', 'event_000088', 'event_000089', 'event_000090', 'event_000091', 'event_000092', 'event_000093', 'event_000094', 'event_000095', 'event_000096', 'event_000097', 'event_000098', 'event_000099']>
```


# dlp.h5 file structure (event_000000):

```python
event_000000: <HDF5 group "/event_000000" (4 members)>
  keys: <KeysViewHDF5 ['image2d', 'label2d', 'particles', 'voxels']>
  attrs: {'crop_origin_mm': array([  23.82781021, -277.5767728 , -746.05935879]), 'event_id': np.int64(0), 'passed_threshold': np.True_, 'vertex_mm': array([ 454.05764771,  -85.21905518, -169.62496948])}
  crop_origin_mm - it is the lower corner of the 3D crop cube in original detector coordinates. This attribute is what enables convertion between detector coordinates and DLP voxel coordinates.
  event_id - correspondes to event id in original edep file. A useful subtlety is that the group name and this attribute are not conceptually the same thing. They just happend here to be the same.
  passed_threshold - this tells whether the event passed the converter''s minimum 2D image-content requirement, described in lartpc_post.py.
  vertex_mm - this is the position of the first Geant4 interaction vertex in the original detector coordinate system, not a voxel coordinate. If an event contained several vertices, this metadata stores only the position of the first one, and that is also the vertex used to choose the crop.


event_000000/image2d: <HDF5 dataset "image2d": shape (3, 256, 256), type "<f4">
  3 - planes XY, YZ, ZX
  256 - first axis (ex. x in XY plane)
  256 - second axis (ex. y in XY plane)
  stores sum of the deposited energies * 100


event_000000/label2d: <HDF5 dataset "label2d": shape (3, 256, 256), type "|u1">
  3 - planes XY, YZ, ZX
  256 - first axis (ex. x in XY plane)
  256 - second axis (ex. y in XY plane)
  stores 3 possible values:
  0 background, 1 shower, 2 track


event_000000/particles: <HDF5 dataset "particles": shape (971,), type "|V237">
  stores particles in format:
  [
('track_id', '<i4') - unique ID of this particle/track within the event.

('parent_track_id', '<i4') - track ID of the particle that directly created this particle; -1 means primary particle.

('ancestor_track_id', '<i4') - track ID of the original/root ancestor of this particle.

('pdg', '<i4') - PDG particle code, e.g. 11 = electron, 22 = photon, 2212 = proton.

('is_primary', '?') - True if the particle is primary, i.e. parent_track_id == -1.

('mass', '<f4') - particle rest mass.

('creation_process', 'S32') - name of the Geant4 process that created the particle, stored as a string up to 32 bytes.

('end_process', 'S32') - name of the Geant4 process associated with the end of the particle track.

('ke_start', '<f4') - kinetic energy of the particle at the beginning of its track, in MeV.

('ke_end', '<f4') - kinetic energy of the particle at the end of its track, in MeV.

('start', '<f4', (4,)) - particle creation point [x, y, z, t], with x,y,z in mm and t in ns.

('end', '<f4', (4,)) - particle track end point [x, y, z, t], with x,y,z in mm and t in ns.

('first_step', '<f4', (4,)) - midpoint [x, y, z, t] of the particle's first energy-depositing step; NaN if it has no steps.

('first_step_edge', '<f4', (3,)) - spatial start edge [x, y, z] of the first energy-depositing step, reconstructed from its midpoint, direction and dx; in mm.

('last_step', '<f4', (4,)) - midpoint [x, y, z, t] of the particle's last energy-depositing step.

('first_step_in_crop', '<f4', (4,)) - first energy-depositing step midpoint [x, y, z, t] that lies inside the selected crop; NaN if none.

('last_step_in_crop', '<f4', (4,)) - last energy-depositing step midpoint [x, y, z, t] that lies inside the selected crop; NaN if none.

('n_steps', '<i4') - number of psteps associated with this particle.

('de_total', '<f4') - total deposited energy summed over all steps of this particle, in MeV.

('de_in_crop', '<f4') - deposited energy from this particle's steps that lie inside the crop, in MeV.

('tree_first_step', '<f4', (4,)) - earliest first energy-depositing step [x, y, z, t] among this particle and all of its descendants.

('tree_de_total', '<f4') - total deposited energy of this particle plus all of its descendants, in MeV.

('tree_de_in_crop', '<f4') - total deposited energy inside the crop from this particle plus all of its descendants, in MeV.
  ]

event_000000/voxels: <HDF5 group "/event_000000/voxels" (3 members)>
  keys: <KeysViewHDF5 ['coords', 'energy', 'label']>
  attrs: {}

event_000000/voxels/coords: <HDF5 dataset "coords": shape (1472, 3), type "|u1">
  stores coordinates [x_voxel, y_voxel, z_voxel] of every occupied voxel inside the 256×256×256 crop. Each coordinate is an integer from 0 to 255. There are 1472 occupied voxels in this event.

event_000000/voxels/energy: <HDF5 dataset "energy": shape (1472,), type "<f4">
  stores total deposited energy [MeV] in each occupied voxel. Energy deposits from all psteps falling into the same voxel are summed.

event_000000/voxels/label: <HDF5 dataset "label": shape (1472,), type "|u1">
  stores the particle-class label of each occupied voxel: 1 = shower, 2 = track. If both shower and track deposits occur in the same voxel, label 2 (track) wins.

```

# Equations
How we got from edep cordinates to dlp cordinates (described in lartpc_post.py):


### 1. Physical size of the crop

The physical side length of the cubic crop is

$$
L_{\mathrm{crop}} = N_{\mathrm{vox}} \cdot s_{\mathrm{vox}}
$$

where:

- $L_{\mathrm{crop}}$ — physical side length of the crop, in mm,
- $N_{\mathrm{vox}}$ — number of voxels along one spatial axis,
- $s_{\mathrm{vox}}$ — physical side length of one voxel, in mm.

For this dataset:

$$
L_{\mathrm{crop}} = 256 \cdot 5\ \mathrm{mm}
= 1280\ \mathrm{mm}
= 1.28\ \mathrm{m}
$$

Therefore, the represented volume is

$$
1.28\ \mathrm{m} \times 1.28\ \mathrm{m} \times 1.28\ \mathrm{m}.
$$

---

### 2. Detector coordinates to continuous voxel coordinates

A point expressed in detector coordinates can be transformed to coordinates relative to the DLP voxel grid using

$$
\mathbf{u}
=
\frac{
\mathbf{r}_{\mathrm{mm}}
-
\mathbf{o}_{\mathrm{mm}}
}{
s_{\mathrm{vox}}
}
$$

where:

- $\mathbf{r}_{\mathrm{mm}} = (x,y,z)$ — point in the original detector coordinate system, in mm,
- $\mathbf{o}_{\mathrm{mm}} = (x_0,y_0,z_0)$ — `crop_origin_mm`, the lower corner of the crop, in mm,
- $s_{\mathrm{vox}} = 5\ \mathrm{mm}$ — voxel size,
- $\mathbf{u} = (u_x,u_y,u_z)$ — continuous coordinates measured in voxel units.

For example:

$$
u_x = \frac{x-x_0}{5\ \mathrm{mm}}.
$$

The value $u_x$ does not have to be an integer.

---

### 3. Detector coordinates to voxel indices

The integer voxel index is obtained by taking the floor:

$$
\mathbf{i}
=
\left\lfloor
\frac{
\mathbf{r}_{\mathrm{mm}}
-
\mathbf{o}_{\mathrm{mm}}
}{
s_{\mathrm{vox}}
}
\right\rfloor.
$$

For the individual axes:

$$
i_x =
\left\lfloor
\frac{x-x_0}{5\ \mathrm{mm}}
\right\rfloor,
$$

$$
i_y =
\left\lfloor
\frac{y-y_0}{5\ \mathrm{mm}}
\right\rfloor,
$$

$$
i_z =
\left\lfloor
\frac{z-z_0}{5\ \mathrm{mm}}
\right\rfloor.
$$

where:

- $(x,y,z)$ — detector coordinates in mm,
- $(x_0,y_0,z_0)$ — `crop_origin_mm`,
- $(i_x,i_y,i_z)$ — integer voxel indices.

Valid voxel indices satisfy

$$
0 \le i_x,i_y,i_z < 256.
$$

---

### 4. Physical region covered by the crop

If

$$
\mathbf{o}_{\mathrm{mm}}
=
(x_0,y_0,z_0)
$$

is the crop origin, then the crop contains points satisfying

$$
x_0 \le x < x_0 + L_{\mathrm{crop}},
$$

$$
y_0 \le y < y_0 + L_{\mathrm{crop}},
$$

$$
z_0 \le z < z_0 + L_{\mathrm{crop}}.
$$

Since

$$
L_{\mathrm{crop}} = 1280\ \mathrm{mm},
$$

the crop covers

$$
[x_0,x_0+1280\ \mathrm{mm})
\times
[y_0,y_0+1280\ \mathrm{mm})
\times
[z_0,z_0+1280\ \mathrm{mm}).
$$

The lower boundary is included and the upper boundary is excluded.

---

### 5. Energy stored in a 3D voxel

Several `pstep` energy deposits may fall into the same voxel. Their energies are summed:

$$
E_{\mathrm{voxel}}
=
\sum_{k \in \mathrm{voxel}} \Delta E_k
$$

where:

- $\Delta E_k$ — `de` of particle step $k$, in MeV,
- $E_{\mathrm{voxel}}$ — total deposited energy in the voxel, in MeV.

Therefore, `voxels/energy` stores energy in

$$
\mathrm{MeV}.
$$

---

### 6. Projection from 3D voxels to a 2D pixel

For a given projection, all 3D voxels that have the same two visible coordinates are summed.

For the XY projection:

$$
E_{XY}(i_x,i_y)
=
\sum_{i_z} E_{\mathrm{voxel}}(i_x,i_y,i_z).
$$

For the YZ projection:

$$
E_{YZ}(i_y,i_z)
=
\sum_{i_x} E_{\mathrm{voxel}}(i_x,i_y,i_z).
$$

For the ZX projection:

$$
E_{ZX}(i_z,i_x)
=
\sum_{i_y} E_{\mathrm{voxel}}(i_x,i_y,i_z).
$$

Thus, the 2D images are energy projections rather than slices through the 3D volume.

---

### 7. Stored 2D pixel value

The deposited energy projected onto a 2D pixel is multiplied by `pixel_scale`:

$$
P = S_{\mathrm{pixel}} \cdot E_{\mathrm{proj}}
$$

where:

- $P$ — stored value in `image2d`,
- $S_{\mathrm{pixel}}$ — `pixel_scale`,
- $E_{\mathrm{proj}}$ — total projected deposited energy in MeV.

For this dataset:

$$
S_{\mathrm{pixel}} = 100,
$$

therefore

$$
\boxed{
P = 100 \cdot E_{\mathrm{proj}}[\mathrm{MeV}]
}
$$

Examples:

$$
0.01\ \mathrm{MeV} \rightarrow 1,
$$

$$
0.10\ \mathrm{MeV} \rightarrow 10,
$$

$$
1.00\ \mathrm{MeV} \rightarrow 100.
$$

---

### 8. Recovering energy from a 2D pixel value

Before considering thresholding, the projected deposited energy can be recovered using

$$
E_{\mathrm{proj}}
=
\frac{P}{S_{\mathrm{pixel}}}.
$$

For this dataset:

$$
\boxed{
E_{\mathrm{proj}}[\mathrm{MeV}]
=
\frac{P}{100}
}
$$

For example, a pixel value of

$$
P=37
$$

corresponds to

$$
E_{\mathrm{proj}}
=
\frac{37}{100}
=
0.37\ \mathrm{MeV}.
$$

---

### 9. Pixel threshold expressed as energy

Pixels are retained only if

$$
P \ge P_{\mathrm{threshold}},
$$

where

$$
P_{\mathrm{threshold}} = 10.
$$

Using

$$
P=100E_{\mathrm{proj}},
$$

the corresponding energy threshold is

$$
E_{\mathrm{threshold}}
=
\frac{P_{\mathrm{threshold}}}{S_{\mathrm{pixel}}}.
$$

Therefore:

$$
E_{\mathrm{threshold}}
=
\frac{10}{100}
=
0.1\ \mathrm{MeV}.
$$

Thus:

$$
\boxed{
E_{\mathrm{proj}} \ge 0.1\ \mathrm{MeV}
}
$$

is required for a 2D pixel to remain nonzero.

If

$$
E_{\mathrm{proj}} < 0.1\ \mathrm{MeV},
$$

then both its image value and label are changed to zero.

---

### 10. Event threshold

An event passes the converter's image threshold only when every projection contains at least 5 pixels above the pixel threshold.

For every projection $p$:

$$
N_p
=
\#\left\{
(i,j):
P_p(i,j)\ge10
\right\}.
$$

The event passes when

$$
\boxed{
N_{XY}\ge5
\quad\land\quad
N_{YZ}\ge5
\quad\land\quad
N_{ZX}\ge5
}
$$

Since a value of `10` corresponds to $0.1$ MeV, this means that each projection must contain at least 5 pixels with at least

$$
0.1\ \mathrm{MeV}
$$

of projected deposited energy.

---

### 11. Direction vector from `theta` and `phi`

For a particle step, its unit direction vector is reconstructed from `theta` and `phi` as

$$
\hat{\mathbf{d}}
=
\begin{pmatrix}
\sin\theta\cos\phi \\
\sin\theta\sin\phi \\
\cos\theta
\end{pmatrix}.
$$

Equivalently,

$$
d_x=\sin\theta\cos\phi,
$$

$$
d_y=\sin\theta\sin\phi,
$$

$$
d_z=\cos\theta.
$$

where:

- $\theta$ — polar angle, in radians,
- $\phi$ — azimuthal angle, in radians,
- $\hat{\mathbf{d}}$ — unit vector pointing in the direction of the particle step.

Because it is a unit vector:

$$
|\hat{\mathbf{d}}|=1.
$$

---

### 12. Reconstructing the beginning of a particle step

The stored `pstep` position

$$
\mathbf{r}_{\mathrm{mid}}
=
(x,y,z)
$$

is the midpoint of the step.

If `dx` is the full physical length of the step, its starting edge is

$$
\boxed{
\mathbf{r}_{\mathrm{start}}
=
\mathbf{r}_{\mathrm{mid}}
-
\frac{dx}{2}\hat{\mathbf{d}}
}
$$

where:

- $\mathbf{r}_{\mathrm{mid}}$ — stored `(x,y,z)` pstep position, in mm,
- $dx$ — full step length, in mm,
- $\hat{\mathbf{d}}$ — unit direction vector.

This is what the converter stores as `first_step_edge` for the first energy-deposit step of a particle.

---

### 13. Reconstructing the end of a particle step

Similarly, the other edge of the segment is

$$
\boxed{
\mathbf{r}_{\mathrm{end}}
=
\mathbf{r}_{\mathrm{mid}}
+
\frac{dx}{2}\hat{\mathbf{d}}
}
$$

Therefore the segment can be reconstructed exactly from

$$
(x,y,z,\theta,\phi,dx).
$$

Its full vector is

$$
\mathbf{r}_{\mathrm{end}}
-
\mathbf{r}_{\mathrm{start}}
=
dx\,\hat{\mathbf{d}}.
$$

---

### 14. Total deposited energy of one particle

If the particle owns steps from index `start` up to but not including `end`, then

$$
E_{\mathrm{particle}}
=
\sum_{k=\mathrm{start}}^{\mathrm{end}-1}
\Delta E_k.
$$

In the DLP particle table this is stored as

```text
de_total
```

and has units of MeV.

The number of associated steps is

$$
\boxed{
N_{\mathrm{steps}}
=
\mathrm{end}-\mathrm{start}
}
$$

and is stored as

```text
n_steps.
```

---

### 15. Deposited energy of one particle inside the crop

Only the particle's steps lying inside the selected crop contribute to `de_in_crop`:

$$
E_{\mathrm{particle,crop}}
=
\sum_{k\in\text{particle steps inside crop}}
\Delta E_k.
$$

Therefore:

$$
0
\le
E_{\mathrm{particle,crop}}
\le
E_{\mathrm{particle}}.
$$

Both values are measured in MeV.

---

### 16. Deposited energy of a complete particle tree

For a particle $i$, the converter also sums the deposited energy of the particle and all of its descendants.

If $\mathcal{T}(i)$ denotes the particle together with its entire descendant tree, then

$$
\boxed{
E_{\mathrm{tree},i}
=
\sum_{j\in\mathcal{T}(i)}
E_{\mathrm{particle},j}
}
$$

This is stored as

```text
tree_de_total
```

in MeV.

Similarly, inside the crop:

$$
\boxed{
E_{\mathrm{tree,crop},i}
=
\sum_{j\in\mathcal{T}(i)}
E_{\mathrm{particle,crop},j}
}
$$

which is stored as

```text
tree_de_in_crop.
```

---

### 17. Projection indexing convention

The projection mapping is

$$
0\rightarrow XY,
$$

$$
1\rightarrow YZ,
$$

$$
2\rightarrow ZX.
$$

The corresponding indexing is

```text
image2d[0][x, y]   # XY
image2d[1][y, z]   # YZ
image2d[2][z, x]   # ZX
```

Therefore, unlike a conventional image written as `[row, column]`, the first spatial index follows the **first coordinate written in the plane name**.


---

### 18. Vertex position in voxel coordinates

Given the detector-space interaction vertex

$$
\mathbf{v}_{\mathrm{mm}}
=
\texttt{vertex\_mm},
$$

its continuous crop-relative voxel coordinates are

$$
\boxed{
\mathbf{v}_{\mathrm{vox}}
=
\frac{
\mathbf{v}_{\mathrm{mm}}
-
\mathbf{o}_{\mathrm{mm}}
}{
5\ \mathrm{mm}
}
}
$$

and the voxel containing the vertex is

$$
\boxed{
\mathbf{i}_{\mathrm{vertex}}
=
\left\lfloor
\mathbf{v}_{\mathrm{vox}}
\right\rfloor
}.
$$

---

# How many elements has each array inside dataset and what are the ranges of values for each field

How many elements inside each dataset (range of values):

What are the ranges of values for each field (range of values):


