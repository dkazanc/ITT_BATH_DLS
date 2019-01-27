#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPLv3 license (ASTRA toolbox)

Script to reconstruct tomographic X-ray data (ice cream crystallisation process)
obtained at Diamond Light Source (UK synchrotron), beamline I13

Dependencies: 
    * astra-toolkit, install conda install -c astra-toolbox astra-toolbox
    * CCPi-RGL toolkit (for regularisation), install with 
    conda install ccpi-regulariser -c ccpi -c conda-forge
    or conda build of  https://github.com/vais-ral/CCPi-Regularisation-Toolkit
    * TomoRec https://github.com/dkazanc/TomoRec

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
import matplotlib.pyplot as plt
#%%
# loading data 
h5f = h5py.File('data/data_icecream_1_slice_35_frames.h5','r')
data_norm = h5f['icecream_normalised'][:]
data_raw = h5f['icecream_raw'][:]
angles_rad = h5f['angles'][:]
h5f.close()
#%%

#%%
# loading FBP images
h5f = h5py.File('data/FBP_35timeframes.h5','r')
FBP_timeframes = h5f['FBP_timeframes'][:]
h5f.close()

# visualise FBP reconstructed sequence
"""
timeframe_no = np.size(FBP_timeframes,2)
for i in range(0, timeframe_no):
    plt.gray()
    plt.figure(1) 
    plt.imshow(FBP_timeframes[:,:,i],vmin=0, vmax=1)
    plt.show()
    plt.pause(0.1)
"""
plt.figure()
plt.imshow(FBP_timeframes[:,:,15], vmin=0, vmax=1, cmap="gray")
plt.title('FBP reconstruction, time frame 15')
plt.show()
#%%
# loading Iteratively reconstructed images
h5f = h5py.File('data/FISTATV_35timeframes.h5','r')
FISTA_TV_timeframes = h5f['FISTA_TV_timeframes'][:]
h5f.close()

"""
timeframe_no = np.size(FISTA_TV_timeframes,2)
for i in range(0, timeframe_no):
    plt.gray()
    plt.figure(1) 
    plt.imshow(FISTA_TV_timeframes[:,:,i],vmin=0, vmax=0.15)
    plt.show()
    plt.pause(0.1)
"""
plt.figure()
plt.imshow(FISTA_TV_timeframes[:,:,15], vmin=0, vmax=0.15, cmap="gray")
plt.title('FISTA TV reconstruction, time frame 15')
plt.show()
#%%
"""
print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print ("%%%%%%%%%%%%Reconstructing with FBP method %%%%%%%%%%%%%%%%%")
print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
from tomorec.methodsDIR import RecToolsDIR

N_size = 2500
timeframe_no = np.size(data_norm,2)
det_y_crop = [i for i in range(0,2374)]
FBP_timeframes = np.zeros((N_size, N_size, timeframe_no), dtype='float32')

for i in range(0, timeframe_no):
    RectoolsDIR = RecToolsDIR(DetectorsDimH = np.size(det_y_crop),  # DetectorsDimH # detector dimension (horizontal)
                    DetectorsDimV = None,  # DetectorsDimV # detector dimension (vertical) for 3D case only
                    AnglesVec = angles_rad[i,:], # array of angles in radians
                    ObjSize = N_size, # a scalar to define reconstructed object dimensions
                    device='gpu')
    FBP_timeframes[:,:,i] = RectoolsDIR.FBP(np.transpose(data_norm[det_y_crop,:,i]))
"""
#%%
print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print ("Reconstructing with FISTA PWLS-OS-TV method % %%%%%%%%%%%%%%")
print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
from tomorec.methodsIR import RecToolsIR

N_size = 2500
det_y_crop = [i for i in range(0,2374)]
timeframe_no = np.size(data_norm,2)
FISTA_TV_timeframes = np.zeros((N_size, N_size, timeframe_no), dtype='float32')

for i in range(0, timeframe_no):
    # set parameters and initiate a class object
    Rectools = RecToolsIR(DetectorsDimH = np.size(det_y_crop),  # DetectorsDimH # detector dimension (horizontal)
                    DetectorsDimV = None,  # DetectorsDimV # detector dimension (vertical) for 3D case only
                    AnglesVec = angles_rad[:,i], # array of angles in radians
                    ObjSize = N_size, # a scalar to define reconstructed object dimensions
                    datafidelity='PWLS',# data fidelity, choose LS, PWLS, GH (wip), Student (wip)
                    OS_number = 12, # the number of subsets, NONE/(or > 1) ~ classical / ordered subsets
                    tolerance = 1e-08, # tolerance to stop outer iterations earlier
                    device='gpu')

    lc = Rectools.powermethod(np.transpose(data_raw[det_y_crop,:,i])) # calculate Lipschitz constant (run once to initilise)

    FISTA_TV_timeframes[:,:,i] = Rectools.FISTA(np.transpose(data_norm[det_y_crop,:,i]), \
                              np.transpose(data_raw[det_y_crop,:,i]), \
                              iterationsFISTA = 10, \
                              regularisation = 'FGP_TV', \
                              regularisation_parameter = 0.0015,\
                              regularisation_iterations = 200,\
                              lipschitz_const = lc)
    """
    # Run FISTA-PWLS-OS reconstrucion algorithm 
    RecFISTA_PWLS = Rectools.FISTA(np.transpose(data_norm[det_y_crop,:,0]), \
                              np.transpose(data_raw[det_y_crop,:,0]), \
                              iterationsFISTA = 3, \
                              lipschitz_const = lc)
    """

#%%