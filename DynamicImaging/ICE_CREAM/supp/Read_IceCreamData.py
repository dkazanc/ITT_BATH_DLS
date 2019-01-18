#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to reconstruct tomographic X-ray data (ice cream crystallisation process)
obtained at Diamond Light Source (UK synchrotron), beamline I13

<<<
IF THE SHARED DATA ARE USED FOR PUBLICATIONS/PRESENTATIONS etc., PLEASE CITE:
E. Guo et al. 2018. Revealing the microstructural stability of a 
three-phase soft solid (ice cream) by 4D synchrotron X-ray tomography.
Journal of Food Engineering, vol.237
>>>
@author: Daniil Kazantsev: https://github.com/dkazanc
"""

import h5py
import numpy as np
#import matplotlib.pyplot as plt
from fista.tomo.suppTools import normaliser

vert_tuple = [i for i in range(1040,1041)] # selection of vertical slices

data_numbers = ['70875','70885','70891','70900','70910', '70917', '70926', '70934', '70937', '70942', '70945', '70950', '70954', '70959', '70964', '70969', '70972', '70974', '70976', '70978', '70980', '70984', '70988', '70991', '70996', '71000', '71004', '71009', '71014', '71018', '71022', '71028', '71034', '71040', '71048']

data_norm_t = np.zeros((2560, 901, np.size(data_numbers)), dtype='float32')
data_raw_t = np.zeros((2560, 901, np.size(data_numbers)), dtype='float32')
angles_t = np.zeros((901, np.size(data_numbers)), dtype='float32')

# reading darks and flats
darks_list = h5py.File("70873.nxs",'r')
flats_list = h5py.File("70874.nxs",'r')

(det_z, det_y) = np.shape(darks_list['entry1/tomo_entry/data/data'][0,:,:])
darks = np.zeros((20, np.size(vert_tuple), det_y), dtype='uint16')
flats = np.zeros((20, np.size(vert_tuple), det_y), dtype='uint16')

# removing the last frame froms darks & flats
for i in range(0,19):
    darks[i,:,:]= darks_list['entry1/tomo_entry/data/data'][i,vert_tuple,:]
    flats[i,:,:]= flats_list['entry1/tomo_entry/data/data'][i,vert_tuple,:]

flats = np.swapaxes(np.swapaxes(flats,2,0),2,1)
darks = np.swapaxes(np.swapaxes(darks,2,0),2,1)

darks_list.close()
flats_list.close()
#%%

# reading projection data in a loop
for i in range(0,np.size(data_numbers)):
    proj_list = h5py.File(data_numbers[i]+'.nxs','r')
    data_raw = proj_list['entry1/tomo_entry/data/data'][:,vert_tuple,:]
    angles = proj_list['entry1/tomo_entry/data/rotation_angle'][:]
    angles_rad = angles*(np.pi/180.0)
    # normalise the data, required format is [detectorsHoriz, Projections, Slices]
    data_raw = np.swapaxes(np.swapaxes(data_raw,2,0),2,1)
    data_norm = normaliser(data_raw, flats, darks, log='log')
    data_norm = data_norm*1000.0
    data_raw = np.float32(np.divide(data_raw, float(np.max(data_raw)))) # normalise raw data
    data_norm_t[:,:,i] = data_norm[:,:,0]
    data_raw_t[:,:,i] = data_raw[:,:,0]
    angles_t[:,i] = angles_rad
    proj_list.close()

"""
# saving data if needed
h5f = h5py.File('data_icecream_1_slice_35_frames.h5', 'w')
h5f.create_dataset('icecream_normalised', data=data_norm_t)
h5f.create_dataset('icecream_raw', data=data_raw_t)
h5f.create_dataset('angles', data=angles_t)
h5f.close()
"""
#%%
# loading data 
h5f = h5py.File('data_icecream_1_slice_35_frames.h5','r')
data_norm = h5f['icecream_normalised'][:]
data_raw = h5f['icecream_raw'][:]
angles_rad = h5f['angles'][:]
h5f.close()