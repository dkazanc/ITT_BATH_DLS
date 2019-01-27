#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
# reading and reconstructing I23 data to demonstrate alighnment problems
"""

# reading i23 data

import h5py
import numpy as np
import matplotlib.pyplot as plt
from tomorec.supp.suppTools import normaliser

#vert_tuple = [i for i in range(250,1400)] # selection of vertical slices
vert_tuple = [i for i in range(500,650)] # selection of vertical slice

# reading darks and flats
darks_list = h5py.File("rawdata/12639.nxs",'r')
flats_list = h5py.File("rawdata/12640.nxs",'r')

(det_z, det_y) = np.shape(darks_list['/entry1/instrument/pco1600_dio_hdf/data'][0,:,:])

darks = darks_list['/entry1/instrument/pco1600_dio_hdf/data'][:,vert_tuple,:]
flats = flats_list['/entry1/instrument/pco1600_dio_hdf/data'][:,vert_tuple,:]

flats = np.swapaxes(np.swapaxes(flats,2,0),2,1)
darks = np.swapaxes(np.swapaxes(darks,2,0),2,1)

darks_list.close()
flats_list.close()
#%%
fig= plt.figure()
plt.rcParams.update({'font.size': 21})
for i in range(0,40):
    plt.subplot(121)
    plt.imshow(flats[:,i,:], vmin=250, vmax=37000, cmap="gray")
    plt.title('Flat field image')
    plt.subplot(122)
    plt.imshow(darks[:,i,:], vmin=0, vmax=1000, cmap="gray")
    plt.title('Dark field image')
    plt.pause(.1)
    plt.show()
    fig.savefig('flatsdarks'+str(i)+'.png', dpi=100)
#%%
proj_list = h5py.File('rawdata/12641.nxs','r')
data_raw = np.zeros((10, np.size(vert_tuple), det_y), dtype='uint16')
data_raw[0,:,:] = proj_list['/entry1/instrument/pco1600_dio_hdf/data'][0,vert_tuple,:] # 0 angle projection
data_raw[1,:,:] = proj_list['/entry1/instrument/pco1600_dio_hdf/data'][200,vert_tuple,:] 
data_raw[2,:,:] = proj_list['/entry1/instrument/pco1600_dio_hdf/data'][400,vert_tuple,:] 
data_raw[3,:,:] = proj_list['/entry1/instrument/pco1600_dio_hdf/data'][600,vert_tuple,:] 
data_raw[4,:,:] = proj_list['/entry1/instrument/pco1600_dio_hdf/data'][800,vert_tuple,:]
data_raw[5,:,:] = proj_list['/entry1/instrument/pco1600_dio_hdf/data'][1000,vert_tuple,:]
data_raw[6,:,:] = proj_list['/entry1/instrument/pco1600_dio_hdf/data'][1200,vert_tuple,:]
data_raw[7,:,:] = proj_list['/entry1/instrument/pco1600_dio_hdf/data'][1400,vert_tuple,:]
data_raw[8,:,:] = proj_list['/entry1/instrument/pco1600_dio_hdf/data'][1600,vert_tuple,:]
data_raw[9,:,:] = proj_list['/entry1/instrument/pco1600_dio_hdf/data'][1800,vert_tuple,:]

angles = proj_list['/entry1/instrument/tomoScanDevice/gon_omega'][:] # extract angles
data_raw = np.swapaxes(np.swapaxes(data_raw,2,0),2,1)
#%%
fig = plt.figure()
plt.rcParams.update({'font.size': 21})
plt.title('Raw projection data')
for i in range(0,10):
    im = data_raw[:,i,:]
    plt.imshow(im, vmin=0, vmax=50000, cmap="gray")
    plt.pause(.5)
    plt.show
    fig.savefig('raw'+str(i)+'.png', dpi=100)
#%%
data_norm = normaliser(data_raw, flats, darks, log='log')
proj_list.close()
#%%
fig = plt.figure()
plt.rcParams.update({'font.size': 21})
plt.title('Incorrectly normalised projection data')
for i in range(0,10):
    im = data_norm[:,i,:]
    plt.imshow(im, vmin=-1, vmax=1, cmap="gray")
    plt.pause(.5)
    plt.show
    #fig.savefig('corr'+str(i)+'.png', dpi=100)
