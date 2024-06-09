# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 16:17:38 2024

@author: Luis-
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.io import loadmat
from alive_progress import alive_bar

from save_and_load import save_data, load_data, catalogue
from rock_abundance import rock_abundance
from subsetting import sample_reduction, low_freq_corr, lat_norm
from binning import binning_calc, binning_plot
from plot_settings import plot_settings
plot_settings(purpose='presentation_single', style='seaborn-v0_8')

"""
README:
    Setting:
        background: show reference image as alpha plot in thermal maps
        sharedColorbar: share colorbar in thermal maps
        bigerMean: interpolate for increased coverage with same resolution
        masked: mask data in rock abundance plots to highlight features
    Plot parameters:
        crater: name of crater, will be used for creation of directories
        latPos: latitude center position
        lonPos: longitude center position
        frameSize: size of square frame
    Path of rock abundance .tif file needs to be adjusted in rock_abundance.py
"""
# settings for the colormap and rock abundance plot
background = False  # reference image of moon for orientation
sharedColorbar = False  # share colorbar for colormaps
biggerMean = True  # calculate bigger mean according to Siegler et al. (2020)
masked = True  # mask data out of range of rock abundance

# crater name and viewing area in degree - value in [-80, 80] and [-180, 180]
crater = 'tycho'
latPos = -43
lonPos = -11
frameSize = 40

# round to .5 accuracy to avoid problems with binning
latLim = (round(2*(latPos - frameSize/2))/2, round(2*(latPos + frameSize/2))/2)
lonLim = (round(2*(lonPos - frameSize/2))/2, round(2*(lonPos + frameSize/2))/2)

# create directories for saving of plots
plot_path = f'../../plots/map/biggerMean={biggerMean}/{crater}'
data_path = f'../CE-2 MRM Data/biggerMean={biggerMean}'

Path('../../plots/fit').mkdir(parents=True, exist_ok=True)
Path(f'{plot_path}/shared={sharedColorbar}').mkdir(parents=True, exist_ok=True)
Path(f'{data_path}/latBins').mkdir(parents=True, exist_ok=True)
Path(f'{data_path}/lonBins').mkdir(exist_ok=True)
Path(f'{data_path}/T_A_mean').mkdir(exist_ok=True)

# size of bins = pixel size --> each pixel is mean of 2 * pixel_size
bin_size = 0.5  # in degree - Siegler chooses 0.25, but we sample time aswell

# data import
mat = loadmat('../CE-2 MRM Data/CE2_data.mat')

# for index i in mat['CE2_dat][:, i] see 'CE-2 MRM Data/CE2_data.xlsx'
T_A_raw = np.stack(
    (mat['CE2_data'][:, 0], mat['CE2_data'][:, 1],
     mat['CE2_data'][:, 2], mat['CE2_data'][:, 3])
    )
lon_raw, lat_raw = mat['CE2_data'][:, 6], mat['CE2_data'][:, 7]
loc_time_raw = mat['CE2_data'][:, 9]

# disregard latitudes > 80 degree and < -80 degree
lat_min, lat_max = -80, 80
lon_min, lon_max = -180, 180

loc_time_raw, lat_raw, lon_raw, T_A_raw = sample_reduction(
    loc_time_raw, lat_raw, lon_raw, T_A_raw,
    condition=lat_raw, lower=lat_min, upper=lat_max
    )

loc_time_raw, lat_raw, lon_raw, T_A_raw = sample_reduction(
    loc_time_raw, lat_raw, lon_raw, T_A_raw,
    condition=lon_raw, lower=lon_min, upper=lon_max
    )

# sample the data to same hours using local time to assure surface temperature
with alive_bar(24) as bar:  # progress bar to console
    for i in range(0, 24):
        time_min, time_max = i, i+1

        title = f"{time_min}h-{time_max}h_local_time"

        try:
            latBins, lonBins, T_A_mean = load_data(data_path, title)

        except OSError:
            loc_time, lat, lon, T_A = sample_reduction(
                loc_time_raw, lat_raw, lon_raw, T_A_raw,
                condition=loc_time_raw, lower=time_min, upper=time_max
            )

            # corrections and normalization according to Siegler et al. (2020)
            T_A = low_freq_corr(loc_time, T_A)

            # latitude normalization
            T_A = lat_norm(lat, lon, T_A, title)

            # calculate the bins
            latBins, lonBins, T_A_mean = binning_calc(
                lat, lon, lat_min, lat_max, lon_min, lon_max,
                T_A, bin_size, biggerMean
                )

            save_data(data_path, title, latBins, lonBins, T_A_mean)

        try:
            binning_plot(
                plot_path, crater, title, latBins, lonBins, T_A_mean,
                latLim, lonLim, background, sharedColorbar, biggerMean
                )

        except ValueError:
            print(f"Cannot draw map for {title}")
            bar()
            continue

        bar()

# create rock abundance map for comparison
rock_abundance(latLim, lonLim, crater, vmin=0.004, vmax=0.02, masked=masked,
                biggerMean=biggerMean)  # vmin is global average (Bandfield et al. (2011))

# create/append the catalogue
effectVisible = input("Is the effect visible? [y/n]:")

catalogue(crater, latPos, lonPos, frameSize, effectVisible)

# close all plots for memory purposes
plt.close('all')
