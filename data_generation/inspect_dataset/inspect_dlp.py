import h5py

if __name__ == "__main__":
    # inspecting Deep Learn Physics (dlp) file
    with h5py.File("runs/dlp_multi/job_0000/dlp.h5", "r") as f:
        print("Root group:", f.name) # name of the root group of the HDF5 file - result: /
        print("f.keys():", f.keys())
        # <KeysViewHDF5 ['event_000000', 'event_000001', 'event_000002', 'event_000003', 'event_000004', 'event_000005', 'event_000006', 'event_000007', 'event_000008', 'event_000009', 'event_000010', 'event_000011', 'event_000012', 'event_000013', 'event_000014', 'event_000015', 'event_000016', 'event_000017', 'event_000018', 'event_000019', 'event_000020', 'event_000021', 'event_000022', 'event_000023', 'event_000024', 'event_000025', 'event_000026', 'event_000027', 'event_000028', 'event_000029', 'event_000030', 'event_000031', 'event_000032', 'event_000033', 'event_000034', 'event_000035', 'event_000036', 'event_000037', 'event_000038', 'event_000039', 'event_000040', 'event_000041', 'event_000042', 'event_000043', 'event_000044', 'event_000045', 'event_000046', 'event_000047', 'event_000048', 'event_000049', 'event_000050', 'event_000051', 'event_000052', 'event_000053', 'event_000054', 'event_000055', 'event_000056', 'event_000057', 'event_000058', 'event_000059', 'event_000060', 'event_000061', 'event_000062', 'event_000063', 'event_000064', 'event_000065', 'event_000066', 'event_000067', 'event_000068', 'event_000069', 'event_000070', 'event_000071', 'event_000072', 'event_000073', 'event_000074', 'event_000075', 'event_000076', 'event_000077', 'event_000078', 'event_000079', 'event_000080', 'event_000081', 'event_000082', 'event_000083', 'event_000084', 'event_000085', 'event_000086', 'event_000087', 'event_000088', 'event_000089', 'event_000090', 'event_000091', 'event_000092', 'event_000093', 'event_000094', 'event_000095', 'event_000096', 'event_000097', 'event_000098', 'event_000099']>
        print("f.values():", f.values()) # result: ValuesViewHDF5(<HDF5 file "dlp.h5" (mode r)>)
        print("f.attrs():", dict(f.attrs)) 
        # {'crop_mode': 'maxcontain', 'n_voxel': np.int64(256), 'pixel_scale': np.float64(100.0), 'pixel_threshold': np.float64(10.0), 'planes': '0=XY 1=YZ 2=ZX; image2d[p][i,j], i along first axis', 'seed': np.int64(0), 'source': 'runs/dlp_multi/job_0000/edep.h5', 'voxel_mm': np.float64(5.0)}
        print("f.attrs['crop_mode']:", f.attrs['crop_mode'])
        print("f.attrs['n_voxel']:", f.attrs['n_voxel'])
        print("f.attrs['pixel_scale']:", f.attrs['pixel_scale'])
        print("f.attrs['pixel_threshold']:", f.attrs['pixel_threshold'])
        print("f.attrs['planes']:", f.attrs['planes'])
        print("f.attrs['seed']:", f.attrs['seed'])
        print("f.attrs['source']:", f.attrs['source'])
        print("f.attrs['voxel_mm']:", f.attrs['voxel_mm'])
        
        print("f['event_000000']:", f['event_000000']) # f['event_000000']: <HDF5 group "/event_000000" (4 members)>
        print("f['event_000000'].keys():", f['event_000000'].keys()) # f['event_000000'].keys(): <KeysViewHDF5 ['image2d', 'label2d', 'particles', 'voxels']>
        print("f['event_000000'].attrs():", dict(f['event_000000'].attrs)) # f['event_000000'].attrs(): {'crop_origin_mm': array([  23.82781021, -277.5767728 , -746.05935879]), 'event_id': np.int64(0), 'passed_threshold': np.True_, 'vertex_mm': array([ 454.05764771,  -85.21905518, -169.62496948])}
        
        print("f['event_000000']['image2d']:", f['event_000000/image2d']) # f['event_000000']['image2d']: <HDF5 dataset "image2d": shape (3, 256, 256), type "<f4">
        print("f['event_000000']['image2d'].dtype:", f['event_000000/image2d'].dtype) # float32
        print("f['event_000000']['image2d'][:]:", f['event_000000/image2d'][:])
        # [[[0. 0. 0. ... 0. 0. 0.]
            # [0. 0. 0. ... 0. 0. 0.]
            # [0. 0. 0. ... 0. 0. 0.]
            # ...
            # [0. 0. 0. ... 0. 0. 0.]
            # [0. 0. 0. ... 0. 0. 0.]
            # [0. 0. 0. ... 0. 0. 0.]]

            # [[0. 0. 0. ... 0. 0. 0.]
            # [0. 0. 0. ... 0. 0. 0.]
            # [0. 0. 0. ... 0. 0. 0.]
            # ...
            # [0. 0. 0. ... 0. 0. 0.]
            # [0. 0. 0. ... 0. 0. 0.]
            # [0. 0. 0. ... 0. 0. 0.]]

            # [[0. 0. 0. ... 0. 0. 0.]
            # [0. 0. 0. ... 0. 0. 0.]
            # [0. 0. 0. ... 0. 0. 0.]
            # ...
            # [0. 0. 0. ... 0. 0. 0.]
            # [0. 0. 0. ... 0. 0. 0.]
            # [0. 0. 0. ... 0. 0. 0.]]]
            
        print("f['event_000000']['label2d']:", f['event_000000/label2d']) # <HDF5 dataset "label2d": shape (3, 256, 256), type "|u1">
        print("f['event_000000']['label2d'].dtype:", f['event_000000/label2d'].dtype) # uint8
        print("f['event_000000']['label2d'][:]:", f['event_000000/label2d'][:])
        
        print("f['event_000000']['particles']:", f['event_000000/particles']) # <HDF5 dataset "label2d": shape (3, 256, 256), type "|u1">
        print("f['event_000000']['particles'].dtype:", f['event_000000/particles'].dtype) # uint8
        # print("f['event_000000']['particles'][:]:", f['event_000000/particles'][:])
        
        print("f['event_000000']['voxels']:", f['event_000000/voxels']) # <HDF5 group "/event_000000/voxels" (3 members)>
        print("f['event_000000']['voxels'].keys():", f['event_000000/voxels'].keys()) # <KeysViewHDF5 ['coords', 'energy', 'label']>
        print("f['event_000000']['voxels'].attrs:", dict(f['event_000000/voxels/coords'].attrs)) # {}
        
        print("f['event_000000']['voxels/coords']:", f['event_000000/voxels/coords']) # <HDF5 dataset "coords": shape (1472, 3), type "|u1">
        print("f['event_000000']['voxels/coords'].dtype:", f['event_000000/voxels/coords'].dtype) # uint8
        
        print("f['event_000000']['voxels/energy']:", f['event_000000/voxels/energy']) # <HDF5 dataset "energy": shape (1472,), type "<f4">
        print("f['event_000000']['voxels/energy'].dtype:", f['event_000000/voxels/energy'].dtype) # float32
        
        print("f['event_000000']['voxels/label']:", f['event_000000/voxels/label']) # <HDF5 dataset "label": shape (1472,), type "|u1">
        print("f['event_000000']['voxels/label'].dtype:", f['event_000000/voxels/label'].dtype) # uint8
        
        