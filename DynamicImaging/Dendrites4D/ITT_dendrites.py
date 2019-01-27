#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPLv3 license (ASTRA toolbox)

Script to reconstruct tomographic X-ray data (dendritic growth process)
obtained at Diamond Light Source (UK synchrotron), beamline I12

Dependencies: 
    * astra-toolkit, install conda install -c astra-toolbox astra-toolbox
    * CCPi-RGL toolkit (for regularisation), install with 
    conda install ccpi-regulariser -c ccpi -c conda-forge
    or conda build of  https://github.com/vais-ral/CCPi-Regularisation-Toolkit
    * TomoRec https://github.com/dkazanc/TomoRec

<<<
IF THE SHARED DATA ARE USED FOR PUBLICATIONS/PRESENTATIONS etc., PLEASE CITE:
D. Kazantsev et al. 2017. Model-based iterative reconstruction using 
higher-order regularization of dynamic synchrotron data. 
Measurement Science and Technology, 28(9), p.094004.
>>>
@author: Daniil Kazantsev: https://github.com/dkazanc
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt

#%%
# loading data 
h5f = h5py.File('data/sinoDendr_80frames.h5','r')
data_norm = h5f['dataset1'][:]
h5f.close()
h5f = h5py.File('data/angles_dend_80frames.h5','r')
angles = h5f['dataset1'][:]
h5f.close()
angles_rad = angles*np.pi/180.0
data_norm = np.swapaxes(np.swapaxes(data_norm,1,2),0,2)
#%%
#%%
# loading FBP images
h5f = h5py.File('data/FBP_80timeframes.h5','r')
FBP_timeframes = h5f['FBP_recon'][:]
h5f.close()

"""
# visualise FBP reconstructed sequence
timeframe_no = np.size(FBP_timeframes,2)
fig = plt.figure()
plt.rcParams.update({'font.size': 20})
plt.title('FBP reconstructions')
for i in range(0, timeframe_no):
    plt.gray()
    plt.imshow(FBP_timeframes[:,:,i],vmin=0, vmax=5)
    plt.show()
    plt.pause(0.1)
    #fig.savefig('FBP'+str(i)+'.png', dpi=160)
"""

plt.figure()
plt.imshow(FBP_timeframes[:,:,20], vmin=0, vmax=7, cmap="gray")
plt.title('FBP reconstruction, time frame 20')
plt.show()

#%%
# loading Iteratively reconstructed images
h5f = h5py.File('data/FISTATV_80timeframes.h5','r')
FISTA_TV_timeframes = h5f['FISTA_TV_timeframes'][:]
h5f.close()

"""
timeframe_no = np.size(FISTA_TV_timeframes,2)
fig = plt.figure()
plt.rcParams.update({'font.size': 19})
plt.title('FISTA-TV reconstructions')
for i in range(0, timeframe_no):
    plt.gray()
    plt.imshow(FISTA_TV_timeframes[:,:,i],vmin=0, vmax=5)
    plt.show()
    plt.pause(0.1)
    fig.savefig('FISTA_TV'+str(i)+'.png', dpi=160)
"""
plt.figure()
plt.imshow(FISTA_TV_timeframes[:,:,20], vmin=0, vmax=5, cmap="gray")
plt.title('FISTA TV reconstruction, time frame 20')
plt.show()
#%%
print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print ("%%%%%%%%%%%%Reconstructing with FBP method %%%%%%%%%%%%%%%%%")
print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
from tomorec.methodsDIR import RecToolsDIR

N_size = 950
detectHoriz, anglesNum, timeframe_no = np.shape(data_norm)
FBP_timeframes = np.zeros((N_size, N_size, timeframe_no), dtype='float32')

for i in range(0, timeframe_no):
    RectoolsDIR = RecToolsDIR(DetectorsDimH = detectHoriz,  # DetectorsDimH # detector dimension (horizontal)
                    DetectorsDimV = None,  # DetectorsDimV # detector dimension (vertical) for 3D case only
                    AnglesVec = angles_rad[i,:], # array of angles in radians
                    ObjSize = N_size, # a scalar to define reconstructed object dimensions
                    device='gpu')
    FBP_timeframes[:,:,i] = RectoolsDIR.FBP(np.transpose(data_norm[:,:,i]))
#%%
print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print ("Reconstructing with FISTA PWLS-OS-TV method % %%%%%%%%%%%%%%")
print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
from tomorec.methodsIR import RecToolsIR

N_size = 950
detectHoriz, anglesNum, timeframe_no = np.shape(data_norm)
FISTA_TV_timeframes = np.zeros((N_size, N_size, timeframe_no), dtype='float32')

for i in range(0, timeframe_no):
    # set parameters and initiate a class object
    Rectools = RecToolsIR(DetectorsDimH = detectHoriz,  # DetectorsDimH # detector dimension (horizontal)
                    DetectorsDimV = None,  # DetectorsDimV # detector dimension (vertical) for 3D case only
                    AnglesVec = angles_rad[i,:], # array of angles in radians
                    ObjSize = N_size, # a scalar to define reconstructed object dimensions
                    datafidelity='LS',# data fidelity, choose LS, PWLS, GH (wip), Student (wip)
                    OS_number = 12, # the number of subsets, NONE/(or > 1) ~ classical / ordered subsets
                    tolerance = 1e-08, # tolerance to stop outer iterations earlier
                    device='gpu')

    lc = Rectools.powermethod() # calculate Lipschitz constant (run once to initilise)

    FISTA_TV_timeframes[:,:,i] = Rectools.FISTA(np.transpose(data_norm[:,:,i]), \
                              iterationsFISTA = 12, \
                              regularisation = 'FGP_TV', \
                              regularisation_parameter = 0.0025,\
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