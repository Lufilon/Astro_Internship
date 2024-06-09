# -*- coding: utf-8 -*-
"""
Created on Thu May 30 20:19:50 2024

@author: Luis-
"""

import numpy as np
import os



def save_data(data_path, title, latBins, lonBins, T_A_mean):
    np.save(f'{data_path}/latBins/{title}.npy', latBins)
    np.save(f'{data_path}/lonBins/{title}.npy', lonBins)
    np.save(f'{data_path}/T_A_mean/{title}.npy', T_A_mean)


def load_data(data_path, title):
    latBins = np.load(f'{data_path}/latBins/{title}.npy')
    lonBins = np.load(f'{data_path}/lonBins/{title}.npy')
    T_A_mean = np.load(f'{data_path}/T_A_mean/{title}.npy')
    
    return latBins, lonBins, T_A_mean


def catalogue(crater, latPos, lonPos, frameSize, effectVisible):
    if os.path.isfile('../../catalogue.xlsx'):
        with open('../../catalogue.xlsx', 'a') as f:
            f.write(f'{crater},{latPos},{lonPos},{frameSize},{effectVisible}\n')

    else:
        with open('../../catalogue.xlsx', 'w') as f:
            f.write('crater,latPos,lonPos,frameSize,effectVisible\n')
            f.write(f'{crater},{latPos},{lonPos},{frameSize},{effectVisible}\n')
