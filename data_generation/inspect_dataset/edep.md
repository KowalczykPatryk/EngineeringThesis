# HDF5 format - Hierarchical Data Format version 5

It has structure similar to filesystem where:
- group is like folder
- dataset is like file

Dataset type works similar to numpy ndarrays (interface).

# Units
Standard edep-sim also defines positions in the global geometry coordinate system and uses CLHEP (A Class Library for High Energy Physics) unit:
 - mm - distance
 - ns - time
 - MeV - energy

# Names/Shortcuts explained
- ass - association(s)
- pstep - particle step / particle simulation step
- cryo - cryostat - a specialized device used to maintain extremely low, stable cryogenic temperatures (often near absolute zero or below freezing) for samples, sensors, or scientific equipment
- lar_vol - Liquid Argon volume
- vertex - primary interaction/generation vertex - where vertex is a point where two or more lines meet
- drift - drift volume/region - where drift meaning is to move slowly or go off course because of outside forces like wind or water, without a fixed direction
- primary - particles initially supplied to Geant4
- proc - process
- subproc - subprocess
- pdg - Particle Data Group particle identification code - a standard integer-based numbering scheme used in particle physics and Monte Carlo event generators to uniquely identify particle species:
    - Quarks: Numbered 1 through 6 for down (d = 1), up (u = 2), strange (s = 3), charm (c = 4), bottom (b = 5), and top (t = 6).
    - Leptons: Numbered 11 through 18, covering the electron (11), electron neutrino (12), muon (13), muon neutrino (14), tau (15), and tau neutrino (16).
    - Gauge and Higgs Bosons: Codes 21 through 40, including the gluon (21), photon (22), Z Boson(23), W Boson (24), and Higgs boson (25).
- ke - kinetic energy
- de - deposited energy
- dx -  step length
- xs - cross section - the flat, two-dimensional shape you get when you slice straight through a solid, three-dimensional object
- diff_xs - differential cross section - a physical quantity that measures the probability that a particle will be scattered or deflected into a specific direction (defined by a solid angle) during a collision experiment

# edep.h5 file structure:

```python
ass: <HDF5 group "/ass" (3 members)>
  keys: ['particle_pstep_cryo', 'particle_pstep_drift', 'particle_pstep_lar_vol']
  attrs: {}
ass/particle_pstep_cryo: <HDF5 dataset "particle_pstep_cryo": shape (100,), type "|O">
ass/particle_pstep_drift: <HDF5 dataset "particle_pstep_drift": shape (100,), type "|O">
ass/particle_pstep_lar_vol: <HDF5 dataset "particle_pstep_lar_vol": shape (100,), type "|O">

event: <HDF5 group "/event" (1 members)>
  keys: ['geant4']
  attrs: {}
event/geant4: <HDF5 dataset "geant4": shape (100,), type "|V24">

particle: <HDF5 group "/particle" (1 members)>
  keys: ['geant4']
  attrs: {}
particle/geant4: <HDF5 dataset "geant4": shape (100,), type "|O">

primary: <HDF5 group "/primary" (1 members)>
  keys: ['geant4']
  attrs: {}
primary/geant4: <HDF5 dataset "geant4": shape (100,), type "|O">

pstep: <HDF5 group "/pstep" (1 members)>
  keys: ['lar_vol']
  attrs: {}
pstep/lar_vol: <HDF5 dataset "lar_vol": shape (100,), type "|O">

vertex: <HDF5 group "/vertex" (1 members)>
  keys: ['geant4']
  attrs: {}
vertex/geant4: <HDF5 dataset "geant4": shape (100,), type "|O">
```

# Structure inside each dataset
- ass/particle_pstep_cryo
    - array([('start', '<u8'), ('end', '<u8')]) - array filled with (start, end) tuples

- ass/particle_pstep_drift
    - array([('start', '<u8'), ('end', '<u8')]) - array filled with (start, end) tuples

- ass/particle_pstep_lar_vol
    - array([('start', '<u8'), ('end', '<u8')]) - array filled with (start, end) tuples

particle_pstep_cryo, particle_pstep_drift, particle_pstep_lar_vol
are particle-to-step mappings for three configured geometry regions:
cryo - cryostat, drift - drift region, lar_vol - liquid-argon volume

- event/geant4
    - [('run_id', '<i4'), ('event_id', '<i4'), ('num_vertices', '<i4'), ('num_primaries', '<i4'), ('num_particles', '<i4'), ('num_steps', '<i4')]

- particle/geant4
    - array({'names': ['x', 'y', 'z', 't', 'px', 'py', 'pz', 'ke', 'end_x', 'end_y', 'end_z', 'end_t', 'end_px', 'end_py', 'end_pz', 'end_ke', 'track_id', 'parent_track_id', 'ancestor_track_id', 'pdg', 'mass', 'proc_start', 'subproc_start', 'proc_name_start', 'proc_end', 'subproc_end', 'proc_name_end'], 'formats': ['<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<i4', '<i4', '<i4', '<i4', '<f4', '<i4', '<i4', 'O', '<i4', '<i4', 'O'], 'offsets': [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 96, 128, 132, 136], 'itemsize': 168})

- primary/geant4
    - array({'names': ['px', 'py', 'pz', 'ke', 'interaction_id', 'track_id', 'pdg', 'mass', 'name'], 'formats': ['<f4', '<f4', '<f4', '<f4', '<i4', '<i4', '<i4', '<f4', 'O'], 'offsets': [0, 4, 8, 12, 16, 20, 24, 28, 32], 'itemsize': 64})

- pstep/lar_vol
    - array({'names': ['x', 'y', 'z', 't', 'theta', 'phi', 'p', 'pdg', 'track_id', 'ancestor_track_id', 'de', 'dx', 'proc_start', 'subproc_start', 'proc_stop', 'subproc_stop'], 'formats': ['<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<i4', '<i4', '<i4', '<f4', '<f4', '<i4', '<i2', '<i4', '<i2'], 'offsets': [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60], 'itemsize': 64})

- vertex/geant4
    - array({'names': ['x', 'y', 'z', 't', 'energy_sum', 'ke_sum', 'num_particles', 'generator', 'reaction', 'filename', 'generator_vertex_id', 'xs', 'diff_xs', 'weight', 'probability', 'interaction_id'], 'formats': ['<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<i4', 'O', 'O', 'O', '<i4', '<f4', '<f4', '<f4', '<f4', '<i2'], 'offsets': [0, 4, 8, 12, 16, 20, 24, 32, 64, 96, 128, 132, 136, 140, 144, 148], 'itemsize': 152})

# Explanation what each dataset and group stores

All datasets have shape of (100,) so one single element inside it refers to one event. But this elment might be array of structured dtypes.

- event/geant4 - is one fixed summary record per event
    - run_id - Geant4 run identifier
    - event_id - event number within run
    - num_vertices - number of primary interaction vertices
    - num_primaries - number of particles initially injected into Geant4
    - num_particles - number of saved Geant4 particle/trajectory records
    - num_steps - number of stored particle-step records for all particles in one event combined

- vertex/geant4 - vertex is where one interaction/generation operation created one or more primary particles
    - x, y, z, t - vertex cordinates and vertex global time
    - energy_sum - sum of total energies of primaries attached to vertex
    - ke_sum - sum of kinetic energies of those primaries
    - num_particles - number of primary particles originating at this vertex
    generator metadata
    - generator - name of external event generator | not used
    - reaction - textual description/code of generator interaction | not used
    - filename - source generator file | not used
    - generator_verted_id - vertex/interaction ID in original generator input | not used
    - xs - total cross section for reaction that produced vertex | not used
    - diff_xs - differential cross section for generated kinematics | not used
    - weight - Monte-Carlo event/interaction weight | not used
    - probability - overall generated interaction probability | not used
    - interaction_id - event-local ID used by this HDF representation to link this vertex to other objects | not used

- primary/geant4 - primary particles injected into Geant4, where A primary is a particle supplied to Geant4 before transport begins
    - px, py, pz - initial momentum components
    - ke - initial kinetic energy
    - interaction_id - vertex/interaction this primary belongs to
    - track_id - track identifier assigned to primary
    - pdg - PDG Monte-Carlo particle code
    - mass - particle rest mass
    - name - Geant4 particle name

- particle/geant4 - particles/tracks created during Geant4 transport (it is called transport because of how software moves particles through matter)
    - x, y, z, t - starting coordinates and starting global time
    - px, py, pz - initial momentums
    - ke - initial kinetic energy
    - end_x, end_y, end_z, end_t - final cordinates and final global time
    - end_px, end_py, end_pz - final momentums
    - end_ke - final kinetic energy
    - track_id - ID of this track
    - parent_track_id - ID of particle that directly created this one
    - ancestor_track_id - ultimate/root ancestor used for truth grouping
    - pdg - particle species
    - mass - rest mass
    - proc_start - the Geant4 process type type that created the trajectory point
    - subproc_start - the Geant4 subprocess type type that created the trajectory point
    - proc_name_start - the Geant4 process name type that created the trajectory point
    
    Some examples of Geant4 processes:
        - 0	NotDefined
        - 1 Transportation
        - 2	Electromagnetic
        - 3	Optical
        - 4	Hadronic
        - 5	Photolepton-hadron
        - 6	Decay
        - 7	General
        - 8	Parameterisation
        - 9	UserDefined
        - 10 Parallel
        - 11 Phonon
    - proc_end -
    - subproc_end -
    - proc_name_end -

- pstep/lar_vol - individual particle steps / energy deposits
    - x, y, z, t - center/midpoint cordinates of step and time associated with midpoint
    - theta - polar angle of step direction
    - phi - azimuthal angle 
    - p - momentum magnitude
    - pdg - particle type at this step
    - track_id - track to which step belongs
    - ancestor_track_id - root truth ancestor
    - de - energy deposited during step
    - dx - full step length
    - proc_start - process type associated with beginning of step
    - subproc_start - subprocess at beginning
    - proc_stop - process producing/limiting end of step
    - subproc_stop - corresponding subprocess

    It stores midpoint of the step but start and end can be calculated using polar, azimuthal angles and step length:
        - unit_direction = [sin(theta)*cos(phi), sin(theta)*sin(phi), cos(theta)]
        - start = midpoint - dx/2 * unit_direction
        - end = midpoint + dx/2 * unit_direction

- ass/particle_pstep_lar_vol - associations between datasets, particle-step association for the LAr volume
    - start - first step number that belongs to particle 0, included
    - end - last step number that belongs to particle 0, excluded

    example:
    - steps_for_particle_0 = psteps[0:1636] where start=0, end=1636
    - steps_for_particle_1 = psteps[1636:23990]
    - steps_for_particle_2 = psteps[23990:31278]

# Example of data for event 0

- ass/particle_pstep_cryo - unused by this simulation
    - array([])

- ass/particle_pstep_drift - unused by this simulation
    - array([])

- ass/particle_pstep_lar_vol
    - array([(     0,   1636) (  1636,  23990) ( 23990,  31278) ( 31278,  57215) ( 57215,  65558) ( 65558,  65667) ( 65667,  65814) ( 65814,  65861) ( 65861,  65873) ( 65873,  65956) ( 65956,  65971) ( 65971,  65982)....])

- event/geant4
    - (0, 0, 1, 5, 971, 100149)

- particle/geant4
    - array([( 1.89307910e+03,   929.9026   ,   608.0228   , 2.21622448e+01, -2.51386619e+00,  4.63717384e+01,  8.34425201e+01, 1.22520015e-01,  1.89307910e+03,  9.29902649e+02,  6.08023010e+02, 2.21625290e+01, -0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0.00000000e+00, 969, 936, 0, 1000180400, 3.7215539e+04, 4, 111, b'hadElastic', 7,  -1, b'NoProcess') ( 1.89307910e+03,   929.9026   ,   608.0228   , 2.21622448e+01, -2.51386619e+00,  4.63717384e+01,  8.34425201e+01, 1.22520015e-01,  1.89307910e+03,  9.29902649e+02,  6.08023010e+02, 2.21625290e+01, -0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0.00000000e+00, 969, 936, 0, 1000180400, 3.7215539e+04, 4, 111, b'hadElastic', 7,  -1, b'NoProcess')....])

- primary/geant4
    - array([(228.85394, -875.6387 , -337.97647 , 965.5871 , 0, 0, 11, 0.5109989, b'e-'),
    (324.57947,  203.21617,   88.357376, 393.00848, 0, 1, 22, 0.       , b'gamma'),
    (270.62653,  -82.39224, -198.17245 , 345.39764, 0, 2, 22, 0.       , b'gamma')])

- pstep/lar_vol
    - array([(454.0333 , -85.22389 , -169.66838, 1.7473249e-04, 2.622038 , -2.9453895 , 4.4672430e+02, -211,   0, 0, 0.01835992, 0.09999998, 0,  -1, 7, 401)
    (453.98462, -85.23354 , -169.75519, 5.2419817e-04, 2.622724 , -2.9462137 , 4.4670508e+02, -211,   0, 0, 0.01836   , 0.09999998, 7, 401, 7, 401)....])

- vertex/geant4
    - array([(454.05765, -85.219055, -169.62497, 0., 3611.449, 2919.167, 5, b'', b'', b'', 2147483647, 3.4028235e+38, 3.4028235e+38, 3.4028235e+38, 3.4028235e+38, 0)])

1 vertex -> 5 primaries -> 971 particles -> 100149 steps

# How many elements has each array inside dataset and what are the ranges of values for each field

How many elements inside each dataset:

- vertex/geant4
    - lenght range: [1, 1]

- primary/geant4
    - lenght range: [2, 5]

- particle/geant4
    - lenght range: [59, 3765]

- pstep/lar_vol
    - lenght range: [7731, 138718]

- ass/particle_pstep_lar_vol
    - lenght range: [60, 3766]

What are the ranges of values for each field:

- event/geant4
    - run_id - [0, 0]
    - event_id - [0, 99]

- vertex/geant4 
    - x - [-698.0606079101562, 695.9432373046875]
    - y - [-697.3170166015625, 697.4024658203125]
    - z - [-699.3424682617188, 685.9307861328125]
    - t - [0.0, 0.0]
    - energy_sum - [295.3836364746094, 4799.7734375]
    - ke_sum - [237.13619995117188, 3708.5458984375]
    - num_particles - [2, 5]
    - generator - [all b'']
    - reaction - [all b'']
    - filename - [all b'']
    - generator_verted_id - [all 2147483647] 
    - xs - [all 3.4028235e+38]
    - diff_xs - [all 3.4028235e+38]
    - weight - [all 3.4028235e+38]
    - probability - [all 3.4028235e+38]
    - interaction_id - [all 0]

- primary/geant4
    - px - [-964.8463134765625, 1070.5587158203125]
    - py - [-974.8192138671875, 941.4342651367188]
    - pz - [-863.2645263671875, 981.5859375]
    - ke - [53.67119598388672, 995.5284423828125]
    - interaction_id - [all 0]
    - track_id - [0, 4]
    - pdg - [-211, 11, 13, 22, 211, 2212] # negative pion, electron, negative muon, positive pion, proton
    - mass - [0.0, 938.2720336914062]
    - name - [b'pi-', b'pi+', b'mu-', b'proton', b'gamma', b'e-']

- particle/geant4 - 
    - x - [-1999.9085693359375, 1998.770751953125]
    - y - [-1999.561767578125, 1999.6993408203125]
    - z - [-1999.802734375, 1999.9969482421875]
    - t - [0.0, 4179.25732421875]
    - px - [-964.8463134765625, 1070.5587158203125]
    - py - [-974.8192138671875, 941.4342651367188]
    - pz - [-863.2645263671875, 1082.2183837890625]
    - ke - [0.00010007772652897984, 995.5285034179688]
    - end_x - [-2500.0, 2500.0]
    - end_y - [-2500.0, 2500.0]
    - end_z - [-2500.0, 2500.0]
    - end_t - [0.003195510245859623, 5036.79150390625]
    - end_px - [-340.26336669921875, 576.5888671875]
    - end_py - [-621.20166015625, 608.438720703125]
    - end_pz - [-556.4063720703125, 515.8944091796875]
    - end_ke - [0.0, 785.09619140625]
    - track_id - [0, 3764]
    - parent_track_id - [-1, 3758]
    - ancestor_track_id - [0, 2824]
    - pdg - 
    - mass - [0.0, 38149.00390625]
    - proc_start - [0, 7]
    - subproc_start - [-1, 401]
    - proc_name_start - [b'', b'conv', b'annihil', b'phot', b'photonNuclear', b'hIoni', b'eBrem', b'pi+Inelastic', b'hBertiniCaptureAtRest', b'hadElastic', b'muIoni', b'Decay', b'pi-Inelastic', b'CoulombScat', b'protonInelastic', b'nCaptureXS', b'eIoni', b'dInelastic', b'compt', b'muMinusCaptureAtRest', b'neutronInelastic']
    - proc_end - [1, 7]
    - subproc_end - [-1, 401]
    - proc_name_end - [b'conv', b'annihil', b'Transportation', b'phot', b'photonNuclear', b'hIoni', b'ionIoni', b'pi+Inelastic', b'hBertiniCaptureAtRest', b'Decay', b'muIoni', b'eBrem', b'NoProcess', b'pi-Inelastic', b'protonInelastic', b'nCaptureXS', b'eIoni', b'dInelastic', b'Step Limit', b'muMinusCaptureAtRest', b'neutronInelastic']

- pstep/lar_vol
    - x - [-1999.9820556640625, 1999.99609375]
    - y - [-1999.99853515625, 1999.9981689453125]
    - z - [-1999.9998779296875, 1999.99853515625]
    - t - [0.00016678206156939268, 1999.99853515625]
    - theta - [0.0008206272614188492, 3.139775276184082]
    - phi - [-3.141592502593994, 3.1415910720825195]
    - p - [0.010001841932535172, 1162.405029296875]
    - pdg - 
    - track_id - [0, 3764]
    - ancestor_track_id - [0, 2824]
    - de - [1.974691166140019e-08, 10.760823249816895]
    - dx - [0.0, 0.10000485926866531]
    - proc_start - [0, 7]
    - subproc_start - [-1, 401]
    - proc_stop - [1, 7]
    - subproc_stop - [1, 401]

- ass/particle_pstep_lar_vol
    - start - [0, 138718]
    - end - [0, 138718]
