#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
script to read additive manufacturing data from the stack of tiffs
"""


from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# 1st dataset
folder_path1='rawdata/Example2/50mms/p_'
dataset50mms = np.zeros((1001, 512, 1280), dtype='uint16')

for i in range(0,1000):
    if (i < 10):
        fileadd = '0000' + str(i)
    elif ((i >= 10) and (i < 100)):
        fileadd = '000' + str(i)
    elif ((i >= 100) and (i < 1000)):
        fileadd = '00' + str(i)
    elif ((i >= 1000) and (i < 10000)):
        fileadd = '0' + str(i)
    else:
        fileadd = str(i)
    im = Image.open(folder_path1 + fileadd + '.tif')
    dataset50mms[i,:,:] = np.array(im)

plt.figure() 
plt.imshow(dataset50mms[150,:,:],vmin=100, vmax=255)
plt.title('frame1')

plt.figure() 
plt.imshow(dataset50mms[250,:,:],vmin=100, vmax=255)
plt.title('frame2')
plt.show()

#%%
# 2nd dataset
folder_path2='rawdata/Example2/400mms/p_'
dataset400mms = np.zeros((501, 512, 1280), dtype='uint16')

for i in range(0,500):
    if (i < 10):
        fileadd = '0000' + str(i)
    elif ((i >= 10) and (i < 100)):
        fileadd = '000' + str(i)
    elif ((i >= 100) and (i < 1000)):
        fileadd = '00' + str(i)
    elif ((i >= 1000) and (i < 10000)):
        fileadd = '0' + str(i)
    else:
        fileadd = str(i)
    im = Image.open(folder_path2 + fileadd + '.tif')
    dataset400mms[i,:,:] = np.array(im)
    
plt.figure() 
plt.imshow(dataset400mms[150,:,:],vmin=100, vmax=255)
plt.title('frame1')

plt.figure() 
plt.imshow(dataset400mms[250,:,:],vmin=100, vmax=255)
plt.title('frame2')
plt.show()

#%%
# 3rd dataset
folder_path3='rawdata/Example1/Invar36_150w_5mms_3/p_'
dataset5mms = np.zeros((3001, 504, 1280), dtype='uint16')

for i in range(0,3000):
    if (i < 10):
        fileadd = '0000' + str(i)
    elif ((i >= 10) and (i < 100)):
        fileadd = '000' + str(i)
    elif ((i >= 100) and (i < 1000)):
        fileadd = '00' + str(i)
    elif ((i >= 1000) and (i < 10000)):
        fileadd = '0' + str(i)
    else:
        fileadd = str(i)
    im = Image.open(folder_path3 + fileadd + '.tif')
    dataset5mms[i,:,:] = np.array(im)

plt.figure() 
plt.imshow(dataset5mms[300,:,:],vmin=100, vmax=255)
plt.title('frame1')

plt.figure() 
plt.imshow(dataset5mms[600,:,:],vmin=100, vmax=255)
plt.title('frame2')
plt.show()
