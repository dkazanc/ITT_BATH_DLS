#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
# reading and reconstructing I23 (DLS) data to demonstrate alignment problems
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
from tomorec.supp.suppTools import normaliser

# loading data 
h5f = h5py.File('data/i23_12641.h5','r')
data_raw = h5f['data_raw'][:]
darks = h5f['darks'][:]
flats = h5f['flats'][:]
angles = h5f['angles'][:]
h5f.close()
angles_rad = angles*np.pi/180.0
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
#%%
# using normaliser from TomoRec package
data_norm = normaliser(data_raw[:,:,150:160], flats[:,:,150:160], darks[:,:,150:160], log='log')
# remove nan's
data_norm = np.where(np.isfinite(data_norm), data_norm, 0)
#%%
# Reconstructing normalised data
from tomorec.methodsDIR import RecToolsDIR

N_size = 1000
detectHoriz, anglesNum, slices = np.shape(data_norm)
det_y_crop = [i for i in range(115,detectHoriz)]

RectoolsDIR = RecToolsDIR(DetectorsDimH = np.size(det_y_crop),  # DetectorsDimH # detector dimension (horizontal)
                    DetectorsDimV = None,  # DetectorsDimV # detector dimension (vertical) for 3D case only
                    AnglesVec = angles_rad, # array of angles in radians
                    ObjSize = N_size, # a scalar to define reconstructed object dimensions
                    device='gpu')
FBP = RectoolsDIR.FBP(np.transpose(data_norm[det_y_crop,:,0]))

plt.figure()
plt.imshow(FBP, vmin=0, vmax=0.003, cmap="gray")
plt.title('FBP reconstruction')
plt.show()
