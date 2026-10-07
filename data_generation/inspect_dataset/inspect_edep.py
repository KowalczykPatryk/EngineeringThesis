import h5py # https://docs.h5py.org/en/stable/high/group.html

#
# group - like a directory, can contain datasets and other groups
# dataset - like a file, contains data (numpy array)

#
# keys are the names of the datasets and groups in a group
# 

# here are used structured dtypes from numpy, which are like C structs, with named fields of different types


# |V24 24 bytes of raw data, no interpretation
# |O object, a Python object (e.g. a numpy array of arbitrary shape and dtype)

# numpy dtype appears as object if HDF5 datasets are variable-length datasets

# in some cases the records stored inside those variable-length elements 
# are structured dtypes, and numpy has two ways of displaying structured 
# dtypes depending on whether their memory layout is simple or contains 
# explicit offsets/padding


# 1. [('run_id', '<i4'), ('event_id', '<i4')]- this is normal structured dtype
# it is when each element (event) has the same size, number of elements
# example is f["event/geant4"]

# 2. dataset has outer dtype equal object when one event refers to array of variable-length
# that is why inner dtype is [('start','<u8'), ('end','<u8')] and outer is object
# it cannot be represented as (100, N) because because there is no single N that is constant
# Instead HDF5 uses a variable-length (VLEN) datatype. h5py maps HDF5 
# variable-length arrays to a NumPy object dtype, because NumPy's normal 
# numeric dtypes require fixed-size elements.
# this can be check using h5py.check_vlen_dtype(dset.dtype)
# example is f["ass/particle_pstep_drift"]

# 3. example f["particle/geant4"] also has varibale-length dataset but
# inner dtype is displayed like this dtype={'names': [...], 'formats': [...], 'offsets': [...]}
# This is still a normal numpy structured dtype. It is simply being 
# displayed using numpy's more general dictionary representation.
# The short form assumes that fields can be laid out naturally one after another.

if __name__ == "__main__":
    
    # inspecting Energy Deposition (edep) file
    with h5py.File("runs/dlp_multi/job_0000/edep.h5", "r") as f:
        print(f.name) # name of the root group of the HDF5 file - result: /
        print(f.keys()) # result: <KeysViewHDF5 ['ass', 'event', 'particle', 'primary', 'pstep', 'vertex']>
        print(f.values()) # result: ValuesViewHDF5(<HDF5 file "edep.h5" (mode r)>)
        print(dict(f.attrs)) # {} - attributes of the root group of the HDF5 file
        
        # ass - association between particles and steps
        
        print(f[list(f.keys())[0]]) # <HDF5 group "/ass" (3 members)>
        print(f[list(f.keys())[0]].keys()) # <KeysViewHDF5 ['particle_pstep_cryo', 'particle_pstep_drift', 'particle_pstep_lar_vol']>
        print(dict(f[list(f.keys())[0]].attrs)) # {} - attributes of the ass group
        print(list(f[list(f.keys())[0]].keys())[0]) # particle_pstep_cryo
        print(type(list(f[list(f.keys())[0]].keys())[0])) # <class 'str'>
        print(f["ass/particle_pstep_cryo"]) # <HDF5 dataset "particle_pstep_cryo": shape (100,), type "|O">
        print(f["ass/particle_pstep_cryo"].dtype) # object
        print(dict(f["ass/particle_pstep_cryo"].attrs)) # {}
        print(type(f["ass/particle_pstep_cryo"])) # <class 'h5py._hl.dataset.Dataset'>
        print(f["ass/particle_pstep_cryo"][:])
        # [array([], dtype=[('start', '<u8'), ('end', '<u8')])
        # array([], dtype=[('start', '<u8'), ('end', '<u8')]) ....
        print(f["ass/particle_pstep_cryo"][0]) # [] - maybe because it is only memoryview of the data, not the actual data?
        print(list(f[list(f.keys())[0]].keys())[1]) # particle_pstep_drift
        print(type(list(f[list(f.keys())[0]].keys())[1])) # <class 'str'>
        print(f["ass/particle_pstep_drift"]) # <HDF5 dataset "particle_pstep_drift": shape (100,), type "|O">
        print(f["ass/particle_pstep_drift"].dtype) # object
        print(dict(f["ass/particle_pstep_drift"].attrs)) # {}
        print(type(f["ass/particle_pstep_drift"])) # <class 'h5py._hl.dataset.Dataset'>
        print(f["ass/particle_pstep_drift"][:])
        # [array([], dtype=[('start', '<u8'), ('end', '<u8')])
        # array([], dtype=[('start', '<u8'), ('end', '<u8')]) ....
        print(f["ass/particle_pstep_drift"][0]) # [] - maybe because it is only memoryview of the data, not the actual data?
        print(list(f[list(f.keys())[0]].keys())[2]) # particle_pstep_lar_vol
        print(type(list(f[list(f.keys())[0]].keys())[2])) # <class 'str'>
        print(f["ass/particle_pstep_lar_vol"]) # <HDF5 dataset "particle_pstep_lar_vol": shape (100,), type "|O">
        print(f["ass/particle_pstep_lar_vol"].dtype) # object
        print(dict(f["ass/particle_pstep_lar_vol"].attrs)) # {}
        print(type(f["ass/particle_pstep_lar_vol"])) # <class 'h5py._hl.dataset.Dataset'>
        print(f["ass/particle_pstep_lar_vol"][:])
        #  array([(    0,     0), (    0,     0), (    0,  4076), ...,
        #         (71048, 71051), (71051, 71052), (71052, 71052)],
        #        dtype=[('start', '<u8'), ('end', '<u8')])
        #  array([(    0,  4849), ( 4849,  4849), ( 4849,  4849), ...,
        #         (82475, 82476), (82476, 82477), (82477, 82477)],
        #        dtype=[('start', '<u8'), ('end', '<u8')])            ]
        print("Here",f["ass/particle_pstep_lar_vol"][0])
        # [(     0,   1636) (  1636,  23990) ( 23990,  31278) ( 31278,  57215)
        # ( 57215,  65558) ( 65558,  65667) ( 65667,  65814) ( 65814,  65861)
        # ( 65861,  65873) ( 65873,  65956) ( 65956,  65971) ( 65971,  65982)....


        # event group

        print(f[list(f.keys())[1]]) # <HDF5 group "/event" (1 members)>
        print(f[list(f.keys())[1]].keys()) # <KeysViewHDF5 ['geant4']>
        print(list(f[list(f.keys())[1]].keys())[0]) # geant4
        print(type(list(f[list(f.keys())[1]].keys())[0])) # <class 'str'>
        print(f["event/geant4"]) # <HDF5 dataset "geant4": shape (100,), type "|V24">
        print(f["event/geant4"].dtype) # [('run_id', '<i4'), ('event_id', '<i4'), ('num_vertices', '<i4'), ('num_primaries', '<i4'), ('num_particles', '<i4'), ('num_steps', '<i4')]
        print(type(f["event/geant4"])) # <class 'h5py._hl.dataset.Dataset'>
        print(dict(f["event/geant4"].attrs)) # {}
        print(f["event/geant4"][:])
        # [(0,  0, 1, 5,  971, 100149) (0,  1, 1, 3, 1181,  40547)
        # (0,  2, 1, 2,  403,   9052) (0,  3, 1, 4, 1041,  39522) ....
        print(f["event/geant4"][0]) # (0, 0, 1, 5, 971, 100149)
        
        
        # particle group
        
        print(f[list(f.keys())[2]]) # <HDF5 group "/particle" (1 members)>
        print(f[list(f.keys())[2]].keys()) # <KeysViewHDF5 ['geant4']>
        print(list(f[list(f.keys())[2]].keys())[0]) # geant4
        print(type(list(f[list(f.keys())[2]].keys())[0])) # <class 'str'>
        print(f["particle/geant4"]) # <HDF5 dataset "geant4": shape (100,), type "|O">
        print(f["particle/geant4"].dtype) # object
        print(type(f["particle/geant4"])) # <class 'h5py._hl.dataset.Dataset'>
        print(dict(f["particle/geant4"].attrs)) # {}
        print(f["particle/geant4"][:])
        # ...,
        # (597.41815, -594.836  , -546.106  , 1.3143911, -7.3562860e-01, -6.4749897e-01,  6.9078636e-01, 7.9234678e-01, 595.7905 , -594.6377  , -545.8249 , 1.3256267 , -0.00056697,  0.00054422,  0.00015997, 0.00080201, 2828, 2819, 0, 11, 0.5109989, 2,   2, b'eIoni', 2,  2, b'eIoni'),
        # (595.5823 , -594.8688 , -546.0464 , 1.3231062,  1.9456871e-03,  1.0825536e-02,  3.6388633e-03, 1.1585304e-02, 595.6084 , -594.7232  , -545.99744, 1.3236257 ,  0.        ,  0.        ,  0.        , 0.        , 2829, 2828, 0, 22, 0.       , 2,   3, b'eBrem', 2, 12, b'phot'),
        # (595.6084 , -594.7232 , -545.99744, 1.3236257,  6.5643542e-02, -2.1684764e-02,  6.2082428e-02, 8.3790049e-03, 595.60876, -594.7233  , -545.99713, 1.3236355 ,  0.        , -0.        ,  0.        , 0.        , 2830, 2829, 0, 11, 0.5109989, 2,  12, b'phot', 7, -1, b'NoProcess')],
        # dtype={'names': ['x', 'y', 'z', 't', 'px', 'py', 'pz', 'ke', 'end_x', 'end_y', 'end_z', 'end_t', 'end_px', 'end_py', 'end_pz', 'end_ke', 'track_id', 'parent_track_id', 'ancestor_track_id', 'pdg', 'mass', 'proc_start', 'subproc_start', 'proc_name_start', 'proc_end', 'subproc_end', 'proc_name_end'], 'formats': ['<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<i4', '<i4', '<i4', '<i4', '<f4', '<i4', '<i4', 'O', '<i4', '<i4', 'O'], 'offsets': [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 96, 128, 132, 136], 'itemsize': 168})]
        print(f["particle/geant4"][0])
        # 2.18895168e+01, -0.00000000e+00,  0.00000000e+00, -0.00000000e+00, 0.00000000e+00, 968, 936, 0, 1000180400, 3.7215539e+04, 4, 111, b'hadElastic', 7,  -1, b'NoProcess')
        # ( 1.89307910e+03,   929.9026   ,   608.0228   , 2.21622448e+01, -2.51386619e+00,  4.63717384e+01,  8.34425201e+01, 1.22520015e-01,  1.89307910e+03,  9.29902649e+02,  6.08023010e+02, 2.21625290e+01, -0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0.00000000e+00, 969, 936, 0, 1000180400, 3.7215539e+04, 4, 111, b'hadElastic', 7,  -1, b'NoProcess')
        # ( 4.05880829e+02,   -95.25955  ,  -249.54614  , 3.33900928e-01,  3.83416355e-01, -3.20022404e-01, -6.03046954e-01, 4.23991978e-01,  4.05884583e+02, -9.55082321e+01, -2.49768356e+02, 3.38722944e-01,  0.00000000e+00, -0.00000000e+00, -0.00000000e+00, 0.00000000e+00, 970, 540, 0,         11, 5.1099890e-01, 2,   2, b'eIoni', 7,  -1, b'NoProcess')]


        # primary group
        
        
        print(f[list(f.keys())[3]]) # <HDF5 group "/primary" (1 members)>
        print(f[list(f.keys())[3]].keys()) # <KeysViewHDF5 ['geant4']>
        print(list(f[list(f.keys())[3]].keys())[0]) # geant4
        print(type(list(f[list(f.keys())[3]].keys())[0])) # <class 'str'>
        print(f["primary/geant4"]) # <HDF5 dataset "geant4": shape (100,), type "|O">
        print(f["primary/geant4"].dtype) # object
        print(type(f["primary/geant4"])) # <class 'h5py._hl.dataset.Dataset'>
        print(dict(f["primary/geant4"].attrs)) # {}
        print(f["primary/geant4"][:])
        # s': [0, 4, 8, 12, 16, 20, 24, 28, 32], 'itemsize': 64})
        # array([(228.85394, -875.6387 , -337.97647 , 965.5871 , 0, 0, 11, 0.5109989, b'e-'),
        # (324.57947,  203.21617,   88.357376, 393.00848, 0, 1, 22, 0.       , b'gamma'),
        # (270.62653,  -82.39224, -198.17245 , 345.39764, 0, 2, 22, 0.       , b'gamma')],
        # dtype={'names': ['px', 'py', 'pz', 'ke', 'interaction_id', 'track_id', 'pdg', 'mass', 'name'], 'formats': ['<f4', '<f4', '<f4', '<f4', '<i4', '<i4', '<i4', '<f4', 'O'], 'offsets': [0, 4, 8, 12, 16, 20, 24, 28, 32], 'itemsize': 64})]
        print(f["primary/geant4"][0])
        # [(-217.54044 ,  -43.238388, -387.7747 , 328.4496 , 0, 0, -211, 139.5701 , b'pi-')
        # ( 317.72894 , -162.96503 , -556.511  , 563.95154, 0, 1,   13, 105.65837, b'mu-')
        # ( 755.83704 ,  102.33985 , -510.34476, 374.19485, 0, 2, 2212, 938.27203, b'proton')
        # ( -79.30045 ,  553.94226 , -562.9315 , 695.08887, 0, 3,   13, 105.65837, b'mu-')
        # (  -8.209221,  576.7169  ,  922.6992 , 957.48206, 0, 4, -211, 139.5701 , b'pi-')]
        
        
        # pstep group
        
        print(f[list(f.keys())[4]]) # <HDF5 group "/pstep" (1 members)>
        print(f[list(f.keys())[4]].keys()) # <KeysViewHDF5 ['lar_vol']>
        print(list(f[list(f.keys())[4]].keys())[0]) # lar_vol
        print(type(list(f[list(f.keys())[4]].keys())[0])) # <class 'str'>
        print(f["pstep/lar_vol"]) # <HDF5 dataset "lar_vol": shape (100,), type "|O">
        print(f["pstep/lar_vol"].dtype) # object
        print(type(f["pstep/lar_vol"])) # <class 'h5py._hl.dataset.Dataset'>
        print(dict(f["pstep/lar_vol"].attrs)) # {}
        print(f["pstep/lar_vol"][:])
        # ...,
        # (788.21045, -892.5478 , -130.28343 , 3.2991476, 2.5425677 , -1.4456644 , 3.5592452e-01, 11, 2071, 0, 0.04366415, 0.1       , 7, 401, 7, 401),
        # (788.22174, -892.5612 , -130.30579 , 3.299354 , 1.9111974 , -0.06100636, 2.7240783e-01, 11, 2071, 0, 0.06807441, 0.07656685, 7, 401, 2,   2),
        # (488.30502, -681.58405,  123.544426, 1.3844821, 0.45060012,  1.4462515 , 8.9405105e-02, 11, 2072, 0, 0.00776227, 0.00185615, 0,  -1, 2,   2)],
        # dtype={'names': ['x', 'y', 'z', 't', 'theta', 'phi', 'p', 'pdg', 'track_id', 'ancestor_track_id', 'de', 'dx', 'proc_start', 'subproc_start', 'proc_stop', 'subproc_stop'], 'formats': ['<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<i4', '<i4', '<i4', '<f4', '<f4', '<i4', '<i2', '<i4', '<i2'], 'offsets': [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60], 'itemsize': 64})
        # array([(505.86844, -237.78467, -408.74033, 1.6678206e-04, 1.9281931 , -1.315158  , 9.6609796e+02, 11,    0, 0, 0.0196333, 0.09999999, 0,  -1, 7, 401),
        # (505.89212, -237.87532, -408.7753 , 5.0034618e-04, 1.927943  , -1.3152691 , 9.6607837e+02, 11,    0, 0, 0.0196333, 0.09999999, 7, 401, 7, 401),
        # (505.91574, -237.96599, -408.81024, 8.3391031e-04, 1.927799  , -1.3157836 , 9.6605872e+02, 11,    0, 0, 0.0196333, 0.09999999, 7, 401, 7, 401),
        # ...,
        # (595.7968 , -594.64374, -545.82666, 1.3255614e+00, 1.3699893 ,  2.3766649 , 2.6087981e-01, 11, 2828, 0, 0.0627416, 0.06660558, 7, 401, 2,   2),
        # (595.6084 , -594.7232 , -545.99744, 1.3233659e+00, 1.2512951 ,  1.3929638 , 1.1585304e-02, 22, 2829, 0, 0.0032063, 0.        , 0,  -1, 2,  12),
        # (595.6086 , -594.72327, -545.99725, 1.3236306e+00, 0.83907574, -0.31905517, 9.2916802e-02, 11, 2830, 0, 0.008379 , 0.0021087 , 0,  -1, 2,   2)],
        # dtype={'names': ['x', 'y', 'z', 't', 'theta', 'phi', 'p', 'pdg', 'track_id', 'ancestor_track_id', 'de', 'dx', 'proc_start', 'subproc_start', 'proc_stop', 'subproc_stop'], 'formats': ['<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<i4', '<i4', '<i4', '<f4', '<f4', '<i4', '<i2', '<i4', '<i2'], 'offsets': [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60], 'itemsize': 64})]
        print(f["pstep/lar_vol"][0])
        # [(454.0333 , -85.22389 , -169.66838, 1.7473249e-04, 2.622038 , -2.9453895 , 4.4672430e+02, -211,   0, 0, 0.01835992, 0.09999998, 0,  -1, 7, 401)
        # (453.98462, -85.23354 , -169.75519, 5.2419817e-04, 2.622724 , -2.9462137 , 4.4670508e+02, -211,   0, 0, 0.01836   , 0.09999998, 7, 401, 7, 401)
        # (453.93597, -85.24313 , -169.84203, 8.7366515e-04, 2.6223993, -2.9466364 , 4.4668585e+02, -211,   0, 0, 0.01836007, 0.09999998, 7, 401, 7, 401)
        # ...
        # (405.90848, -95.56557 , -249.76448, 3.3809298e-01, 0.8943909,  2.3950593 , 4.2592534e-01,   11, 970, 0, 0.03387651, 0.1       , 7, 401, 7, 401)
        # (405.8812 , -95.52527 , -249.74501, 3.3840159e-01, 1.5891978,  1.9399334 , 3.7079769e-01,   11, 970, 0, 0.04084631, 0.1       , 7, 401, 7, 401)
        # (405.87836, -95.505035, -249.75691, 3.3863363e-01, 2.5922086, -0.47400743, 2.9594469e-01,   11, 970, 0, 0.07951201, 0.09970926, 7, 401, 2,   2)]
        
        
        
        # vertex group
        
        print(f[list(f.keys())[5]]) # <HDF5 group "/vertex" (1 members)>
        print(f[list(f.keys())[5]].keys()) # <KeysViewHDF5 ['geant4']>
        print(list(f[list(f.keys())[5]].keys())[0]) # geant4
        print(type(list(f[list(f.keys())[5]].keys())[0])) # <class 'str'>
        print(f["vertex/geant4"]) # <HDF5 dataset "geant4": shape (100,), type "|O">
        print(f["vertex/geant4"].dtype) # object
        print(f["vertex/geant4"].dtype.metadata)
        print(type(f["vertex/geant4"])) # <class 'h5py._hl.dataset.Dataset'>
        print(dict(f["vertex/geant4"].attrs)) # {}
        print(f["vertex/geant4"][:])
        # array([(187.67291, -396.78845, 151.10606, 0., 1431.2256, 1431.2256, 2, b'', b'', b'', 2147483647, 3.4028235e+38, 3.4028235e+38, 3.4028235e+38, 3.4028235e+38, 0)],
        # dtype={'names': ['x', 'y', 'z', 't', 'energy_sum', 'ke_sum', 'num_particles', 'generator', 'reaction', 'filename', 'generator_vertex_id', 'xs', 'diff_xs', 'weight', 'probability', 'interaction_id'], 'formats': ['<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<i4', 'O', 'O', 'O', '<i4', '<f4', '<f4', '<f4', '<f4', '<i2'], 'offsets': [0, 4, 8, 12, 16, 20, 24, 32, 64, 96, 128, 132, 136, 140, 144, 148], 'itemsize': 152})
        # array([(505.8566, -237.73935, -408.72284, 0., 1703.9934, 1703.9932, 3, b'', b'', b'', 2147483647, 3.4028235e+38, 3.4028235e+38, 3.4028235e+38, 3.4028235e+38, 0)],
        # dtype={'names': ['x', 'y', 'z', 't', 'energy_sum', 'ke_sum', 'num_particles', 'generator', 'reaction', 'filename', 'generator_vertex_id', 'xs', 'diff_xs', 'weight', 'probability', 'interaction_id'], 'formats': ['<f4', '<f4', '<f4', '<f4', '<f4', '<f4', '<i4', 'O', 'O', 'O', '<i4', '<f4', '<f4', '<f4', '<f4', '<i2'], 'offsets': [0, 4, 8, 12, 16, 20, 24, 32, 64, 96, 128, 132, 136, 140, 144, 148], 'itemsize': 152})]
        print(f["vertex/geant4"][0])
        # [(454.05765, -85.219055, -169.62497, 0., 3611.449, 2919.167, 5, b'', b'', b'', 2147483647, 3.4028235e+38, 3.4028235e+38, 3.4028235e+38, 3.4028235e+38, 0)]
        
        
        
        def show(name, obj):
            print(f"{name}: {obj}")
            if isinstance(obj, h5py.Group):
                print(f"  keys: {list(obj.keys())}")
                print(f"  attrs: {dict(obj.attrs)}")
            # elif isinstance(obj, h5py.Dataset):
            #     print(f"  shape: {obj.shape}, dtype: {obj.dtype}")
            #     print(f"  attrs: {dict(obj.attrs)}")
            #     print(f"  data: {obj[:]}")
            # else:
            #     print("  Unknown object type")
                
        f.visititems(show)
        
        print(f["event/geant4"][0]["num_steps"] == len(f["pstep/lar_vol"][0])) # True - number of steps in the event is equal to the number of steps in the pstep/lar_vol dataset for that event
        
        i = 0

        event = f["event/geant4"][i]
        particles = f["particle/geant4"][i]
        primaries = f["primary/geant4"][i]
        vertices = f["vertex/geant4"][i]
        steps = f["pstep/lar_vol"][i]
        ass = f["ass/particle_pstep_lar_vol"][i]

        print("vertices:", event["num_vertices"], len(vertices))

        print("primaries:", event["num_primaries"], len(primaries))

        print("particles:", event["num_particles"], len(particles))

        print("steps:", event["num_steps"], len(steps))
        
        minimum, maximum = -1, -1
        for event_number in range(len(f["event/geant4"])):
            event = f["event/geant4"][event_number]
            if minimum == -1 or event["num_steps"] < minimum:
                minimum = event["num_steps"]
            if maximum == -1 or event["num_steps"] > maximum:
                maximum = event["num_steps"]
        print("min steps:", min)
        print("max steps:", max)
        
        minimum, maximum = -1, -1
        for event_number in range(len(f["event/geant4"])):
            event = f["event/geant4"][event_number]
            if minimum == -1 or event["run_id"] < minimum:
                minimum = event["run_id"]
            if maximum == -1 or event["run_id"] > maximum:
                maximum = event["run_id"]
        print("min run ID:", min)
        print("max run ID:", max)
        
        minimum, maximum = -1, -1
        for event_number in range(len(f["event/geant4"])):
            event = f["event/geant4"][event_number]
            if minimum == -1 or event["event_id"] < minimum:
                minimum = event["event_id"]
            if maximum == -1 or event["event_id"] > maximum:
                maximum = event["event_id"]
        print("min event ID:", min)
        print("max event ID:", max)
        
        minimum, maximum = -1, -1
        for event_number in range(len(f["event/geant4"])):
            event = f["event/geant4"][event_number]
            if minimum == -1 or event["num_vertices"] < minimum:
                minimum = event["num_vertices"]
            if maximum == -1 or event["num_vertices"] > maximum:
                maximum = event["num_vertices"]
        print("min vertices:", min)
        print("max vertices:", max)
        
        minimum, maximum = -1, -1
        for event_number in range(len(f["event/geant4"])):
            event = f["event/geant4"][event_number]
            if minimum == -1 or event["num_primaries"] < minimum:
                minimum = event["num_primaries"]
            if maximum == -1 or event["num_primaries"] > maximum:
                maximum = event["num_primaries"]
        print("min primaries:", min)
        print("max primaries:", max)
        
        minimum, maximum = -1, -1
        for event_number in range(len(f["event/geant4"])):
            event = f["event/geant4"][event_number]
            if minimum == -1 or event["num_particles"] < minimum:
                minimum = event["num_particles"]
            if maximum == -1 or event["num_particles"] > maximum:
                maximum = event["num_particles"]
        print("min particles:", min)
        print("max particles:", max)
        
        minimum, maximum = -1, -1
        for event_number in range(len(f["event/geant4"])):
            event = f["event/geant4"][event_number]
            if minimum == -1 or event["num_particles"] < minimum:
                minimum = event["num_particles"]
            if maximum == -1 or event["num_particles"] > maximum:
                maximum = event["num_particles"]
        print("min particles:", min)
        print("max particles:", max)
        
                
        minimum, maximum = -1, -1
        for event_number in range(len(f["event/geant4"])):
            if minimum == -1 or len(f["ass/particle_pstep_lar_vol"][event_number]) < minimum:
                minimum = len(f["ass/particle_pstep_lar_vol"][event_number])
            if maximum == -1 or len(f["ass/particle_pstep_lar_vol"][event_number]) > maximum:
                maximum = len(f["ass/particle_pstep_lar_vol"][event_number])
        print("min associations:", min)
        print("max associations:", max)
        
        print("-----")
        minimum, maximum = -1, -1
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                if minimum == -1 or f["vertex/geant4"][event_number][vertex_number]["x"] < minimum:
                    minimum = f["vertex/geant4"][event_number][vertex_number]["x"]
                if maximum == -1 or f["vertex/geant4"][event_number][vertex_number]["x"] > maximum:
                    maximum = f["vertex/geant4"][event_number][vertex_number]["x"]
        print(f"min x: {min}, max x: {max}")
        minimum = -1
        maximum = -1
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                if minimum == -1 or f["vertex/geant4"][event_number][vertex_number]["y"] < minimum:
                    minimum = f["vertex/geant4"][event_number][vertex_number]["y"]
                if maximum == -1 or f["vertex/geant4"][event_number][vertex_number]["y"] > maximum:
                    maximum = f["vertex/geant4"][event_number][vertex_number]["y"]
        print(f"min y: {min}, max y: {max}")
        minimum = -1
        maximum = -1
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                if minimum == -1 or f["vertex/geant4"][event_number][vertex_number]["z"] < minimum:
                    minimum = f["vertex/geant4"][event_number][vertex_number]["z"]
                if maximum == -1 or f["vertex/geant4"][event_number][vertex_number]["z"] > maximum:
                    maximum = f["vertex/geant4"][event_number][vertex_number]["z"]
        print(f"min z: {min}, max z: {max}")
        minimum = -1
        maximum = -1
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                if minimum == -1 or f["vertex/geant4"][event_number][vertex_number]["t"] < minimum:
                    minimum = f["vertex/geant4"][event_number][vertex_number]["t"]
                if maximum == -1 or f["vertex/geant4"][event_number][vertex_number]["t"] > maximum:
                    maximum = f["vertex/geant4"][event_number][vertex_number]["t"]
        print(f"min t: {min}, max t: {max}")
        minimum = -1
        maximum = -1
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                if minimum == -1 or f["vertex/geant4"][event_number][vertex_number]["energy_sum"] < minimum:
                    minimum = f["vertex/geant4"][event_number][vertex_number]["energy_sum"]
                if maximum == -1 or f["vertex/geant4"][event_number][vertex_number]["energy_sum"] > maximum:
                    maximum = f["vertex/geant4"][event_number][vertex_number]["energy_sum"]
        print(f"min energy_sum: {min}, max energy_sum: {max}")
        minimum = -1
        maximum = -1
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                if minimum == -1 or f["vertex/geant4"][event_number][vertex_number]["ke_sum"] < minimum:
                    minimum = f["vertex/geant4"][event_number][vertex_number]["ke_sum"]
                if maximum == -1 or f["vertex/geant4"][event_number][vertex_number]["ke_sum"] > maximum:
                    maximum = f["vertex/geant4"][event_number][vertex_number]["ke_sum"]
        print(f"min ke_sum: {min}, max ke_sum: {max}")
        minimum = -1
        maximum = -1
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                if minimum == -1 or f["vertex/geant4"][event_number][vertex_number]["num_particles"] < minimum:
                    minimum = f["vertex/geant4"][event_number][vertex_number]["num_particles"]
                if maximum == -1 or f["vertex/geant4"][event_number][vertex_number]["num_particles"] > maximum:
                    maximum = f["vertex/geant4"][event_number][vertex_number]["num_particles"]
        print(f"min num_particles: {min}, max num_particles: {max}")
        
        
        print("\n-- generator --")
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                print(f["vertex/geant4"][event_number][vertex_number]["generator"], end=", ")
                
        print("\n-- reaction --")
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                print(f["vertex/geant4"][event_number][vertex_number]["reaction"], end=", ")
                
        print("\n-- filename --")
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                print(f["vertex/geant4"][event_number][vertex_number]["filename"], end=", ")

        print("\n-- generator_vertex_id --")
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                print(f["vertex/geant4"][event_number][vertex_number]["generator_vertex_id"], end=", ")

        print("\n-- xs --")
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                print(f["vertex/geant4"][event_number][vertex_number]["xs"], end=", ")

        print("\n-- diff_xs --")
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                print(f["vertex/geant4"][event_number][vertex_number]["diff_xs"], end=", ")

        print("\n-- weight --")
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                print(f["vertex/geant4"][event_number][vertex_number]["weight"], end=", ")

        print("\n-- probability --")
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                print(f["vertex/geant4"][event_number][vertex_number]["probability"], end=", ")

        print("\n-- interaction_id --")
        for event_number in range(len(f["event/geant4"])):
            for vertex_number in range(len(f["vertex/geant4"][event_number])):
                print(f["vertex/geant4"][event_number][vertex_number]["interaction_id"], end=", ")
                
        
        
        print("\n-- primary/geant4 --")
        
        print("\n-- px --")
        minimum, maximum = -1, -1
        for event_number in range(len(f["event/geant4"])):
            for primary_number in range(len(f["primary/geant4"][event_number])):
                if minimum == -1 or f["primary/geant4"][event_number][primary_number]["px"] < minimum:
                    minimum = f["primary/geant4"][event_number][primary_number]["px"]
                if maximum == -1 or f["primary/geant4"][event_number][primary_number]["px"] > maximum:
                    maximum = f["primary/geant4"][event_number][primary_number]["px"]
        print(f"min px: {min}, max px: {max}")
                
        print("\n-- py --")
        minimum, maximum = -1, -1
        for event_number in range(len(f["event/geant4"])):
            for primary_number in range(len(f["primary/geant4"][event_number])):
                if minimum == -1 or f["primary/geant4"][event_number][primary_number]["py"] < minimum:
                    minimum = f["primary/geant4"][event_number][primary_number]["py"]
                if maximum == -1 or f["primary/geant4"][event_number][primary_number]["py"] > maximum:
                    maximum = f["primary/geant4"][event_number][primary_number]["py"]
        print(f"min py: {min}, max py: {max}")

        print("\n-- pz --")
        minimum, maximum = -1, -1
        for event_number in range(len(f["event/geant4"])):
            for primary_number in range(len(f["primary/geant4"][event_number])):
                if minimum == -1 or f["primary/geant4"][event_number][primary_number]["pz"] < minimum:
                    minimum = f["primary/geant4"][event_number][primary_number]["pz"]
                if maximum == -1 or f["primary/geant4"][event_number][primary_number]["pz"] > maximum:
                    maximum = f["primary/geant4"][event_number][primary_number]["pz"]
        print(f"min pz: {min}, max pz: {max}")
                
        print("\n-- ke --")
        minimum, maximum = -1, -1
        for event_number in range(len(f["event/geant4"])):
            for primary_number in range(len(f["primary/geant4"][event_number])):
                if minimum == -1 or f["primary/geant4"][event_number][primary_number]["ke"] < minimum:
                    minimum = f["primary/geant4"][event_number][primary_number]["ke"]
                if maximum == -1 or f["primary/geant4"][event_number][primary_number]["ke"] > maximum:
                    maximum = f["primary/geant4"][event_number][primary_number]["ke"]
        print(f"min ke: {min}, max ke: {max}")
        
        print("\n-- interaction_id --")
        for event_number in range(len(f["event/geant4"])):
            for primary_number in range(len(f["primary/geant4"][event_number])):
                print(f["primary/geant4"][event_number][primary_number]["interaction_id"], end=", ")
                
        print("\n-- track_id --")
        for event_number in range(len(f["event/geant4"])):
            for primary_number in range(len(f["primary/geant4"][event_number])):
                print(f["primary/geant4"][event_number][primary_number]["track_id"], end=", ")
                
        print("\n-- pdg --")
        for event_number in range(len(f["event/geant4"])):
            for primary_number in range(len(f["primary/geant4"][event_number])):
                print(f["primary/geant4"][event_number][primary_number]["pdg"], end=", ")
                
        print("\n-- mass --")
        minimum, maximum = -1, -1
        for event_number in range(len(f["event/geant4"])):
            for primary_number in range(len(f["primary/geant4"][event_number])):
                if minimum == -1 or f["primary/geant4"][event_number][primary_number]["mass"] < minimum:
                    minimum = f["primary/geant4"][event_number][primary_number]["mass"]
                if maximum == -1 or f["primary/geant4"][event_number][primary_number]["mass"] > maximum:
                    maximum = f["primary/geant4"][event_number][primary_number]["mass"]
        print(f"min mass: {min}, max mass: {max}")
        
        print("\n-- name --")
        for event_number in range(len(f["event/geant4"])):
            for primary_number in range(len(f["primary/geant4"][event_number])):
                print(f["primary/geant4"][event_number][primary_number]["name"], end=", ")
                
        
        # print("\n-- particle/geant4 --")
        
        # print("\n-- x --")
        # minimum, maximum = -1, -1
        # count = 0
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["x"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["x"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["x"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["x"]
        #         count += 1
        #     print(f"event {event_number} has {len(f['particle/geant4'][event_number])} particles")
        # print(f"min x: {min}, max x: {max}")
        
        # print("\n-- y --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["y"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["y"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["y"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["y"]
        # print(f"min y: {min}, max y: {max}")
        
        # print("\n-- z --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["z"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["z"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["z"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["z"]
        # print(f"min z: {min}, max z: {max}")
        
        # print("\n-- t --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["t"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["t"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["t"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["t"]
        # print(f"min t: {min}, max t: {max}")
        
        # print("\n-- px --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["px"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["px"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["px"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["px"]
        # print(f"min px: {min}, max px: {max}")
        
        # print("\n-- py --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["py"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["py"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["py"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["py"]
        # print(f"min py: {min}, max py: {max}")
        
        # print("\n-- pz --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["pz"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["pz"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["pz"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["pz"]
        # print(f"min pz: {min}, max pz: {max}")
        
        # print("\n-- ke --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["ke"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["ke"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["ke"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["ke"]
        # print(f"min ke: {min}, max ke: {max}")
        
        # print("\n-- end_x --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["end_x"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["end_x"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["end_x"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["end_x"]
        # print(f"min end_x: {min}, max end_x: {max}")
        
        # print("\n-- end_y --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["end_y"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["end_y"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["end_y"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["end_y"]
        # print(f"min end_y: {min}, max end_y: {max}")
        
        # print("\n-- end_z --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["end_z"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["end_z"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["end_z"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["end_z"]
        # print(f"min end_z: {min}, max end_z: {max}")
        
        # print("\n-- end_t --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["end_t"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["end_t"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["end_t"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["end_t"]
        # print(f"min end_t: {min}, max end_t: {max}")
        
        # print("\n-- end_px --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["end_px"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["end_px"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["end_px"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["end_px"]
        # print(f"min end_px: {min}, max end_px: {max}")
        
        # print("\n-- end_py --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["end_py"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["end_py"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["end_py"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["end_py"]
        # print(f"min end_py: {min}, max end_py: {max}")
        
        # print("\n-- end_pz --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["end_pz"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["end_pz"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["end_pz"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["end_pz"]
        # print(f"min end_pz: {min}, max end_pz: {max}")
        
        # print("\n-- end_ke --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["end_ke"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["end_ke"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["end_ke"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["end_ke"]
        # print(f"min end_ke: {min}, max end_ke: {max}")
        
        # print("\n-- track_id --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["track_id"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["track_id"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["track_id"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["track_id"]
        # print(f"min track_id: {min}, max track_id: {max}")
        
        # print("\n-- parent_track_id --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["parent_track_id"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["parent_track_id"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["parent_track_id"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["parent_track_id"]
        # print(f"min parent_track_id: {min}, max parent_track_id: {max}")
        
        # print("\n-- ancestor_track_id --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["ancestor_track_id"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["ancestor_track_id"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["ancestor_track_id"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["ancestor_track_id"]
        # print(f"min ancestor_track_id: {min}, max ancestor_track_id: {max}")
        
        # print("\n-- pdg --")
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         print(f["particle/geant4"][event_number][particle_number]["pdg"], end=", ")
                
        # print("\n-- mass --")
        # minimum, maximum = -1, -1
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         if minimum == -1 or f["particle/geant4"][event_number][particle_number]["mass"] < minimum:
        #             minimum = f["particle/geant4"][event_number][particle_number]["mass"]
        #         if maximum == -1 or f["particle/geant4"][event_number][particle_number]["mass"] > maximum:
        #             maximum = f["particle/geant4"][event_number][particle_number]["mass"]
        # print(f"min mass: {min}, max mass: {max}")
        
        # print("\n-- proc_start --")
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         print(f["particle/geant4"][event_number][particle_number]["proc_start"], end=", ")
                
        # print("\n-- subproc_start --")
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         print(f["particle/geant4"][event_number][particle_number]["subproc_start"], end=", ")
                
        # print("\n-- proc_name_start --")
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         print(f["particle/geant4"][event_number][particle_number]["proc_name_start"], end=", ")
                
        # print("\n-- proc_end --")
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         print(f["particle/geant4"][event_number][particle_number]["proc_end"], end=", ")
                
        # print("\n-- subproc_end --")
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         print(f["particle/geant4"][event_number][particle_number]["subproc_end"], end=", ")
                
        # print("\n-- proc_name_end --")
        # for event_number in range(len(f["event/geant4"])):
        #     for particle_number in range(len(f["particle/geant4"][event_number])):
        #         print(f["particle/geant4"][event_number][particle_number]["proc_name_end"], end=", ")
        
        import numpy as np


        def print_ranges(dset):
            first_event = next(
                event for event in dset
                if len(event) > 0
            )

            fields = first_event.dtype.names

            ranges = {}

            for field in fields:
                field_dtype = first_event.dtype.fields[field][0]

                if np.issubdtype(field_dtype, np.number):
                    ranges[field] = [np.inf, -np.inf]
                else:
                    all_values = set()
                    for event in dset:
                        values = event[field]
                        all_values.update(set(values))
                    print(f"{field:25} ", all_values)

            for event in dset:
                if len(event) == 0:
                    continue

                for field in ranges:
                    values = event[field]

                    local_min = np.nanmin(values)
                    local_max = np.nanmax(values)

                    if local_min < ranges[field][0]:
                        ranges[field][0] = local_min

                    if local_max > ranges[field][1]:
                        ranges[field][1] = local_max

            for field, (minimum, maximum) in ranges.items():
                print(
                    f"{field:25} "
                    f"min={minimum:<15} "
                    f"max={maximum}"
                )
            
        print("\nparticle/geant4")
        print_ranges(f["particle/geant4"])    
            
        print("pstep/lar_vol")
        print_ranges(f["pstep/lar_vol"])

        print("\nass/particle_pstep_lar_vol")
        print_ranges(f["ass/particle_pstep_lar_vol"])