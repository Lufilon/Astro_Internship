# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 17:31:26 2024

@author: Luis-
"""

import sys
import warnings
import numpy as np
import matplotlib.pyplot as plt


def binning_calc(lat, lon, lat_min, lat_max, lon_min, lon_max, T_A, bin_size,
                 bigger_mean=True):
    # mean over bins with size (bin_size x bin_size) and plot as pcolormesh
    if bigger_mean: # mean as in Siegler et al. (2020)
        latBins = np.arange(lat_min+bin_size, lat_max, bin_size) # exclude min and max
        lonBins = np.arange(lon_min+bin_size, lon_max, bin_size) # for usage of shade=auto

        latIndex_even = 2 * np.digitize(lat, latBins[::2]) # [::2] to increase to 2*bin_size
        latIndex_odd = 2 * np.digitize(lat, latBins[1:-1:2]) + 1 # 2*, +1 to shift to correct index
        lonIndex_even = 2 * np.digitize(lon, lonBins[::2]) # [1:-1:] to get every second odd one
        lonIndex_odd = 2 * np.digitize(lon, lonBins[1:-1:2]) + 1

        latIndex = np.concatenate((latIndex_even, latIndex_even, latIndex_odd, latIndex_odd))
        lonIndex = np.concatenate((lonIndex_even, lonIndex_odd, lonIndex_even, lonIndex_odd))

        latlon = np.unique((latIndex, lonIndex), axis=1) # runtime efficiency

        T_A_mean = np.full((4, latBins.size+2, lonBins.size+2), np.nan)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)

            for (val_i, val_j) in zip(latlon[0], latlon[1]):
                """
                TODO
                    Das hier müsste mit array snipping also [1:2] usw viel leichter gehen
                    Das ist so ein ziemlicher overkill?
                """

                index, = np.where((latIndex_even==val_i) & (lonIndex_even==val_j) | \
                                  (latIndex_even==val_i) & (lonIndex_odd==val_j) | \
                                  (latIndex_odd==val_i) & (lonIndex_even==val_j) | \
                                  (latIndex_odd==val_i) & (lonIndex_odd==val_j)) # search for all the values that are in this "box"
                T_A_mean[:, val_i, val_j] = np.nanmean(T_A[:, index], axis=1) # mean over them

        T_A_mean = T_A_mean[:, 1:-1:, 1:-1:]  # cut edges

    else: # simply mean over (bin_size x bin_size) bins
        latBins = np.arange(lat_min, lat_max+bin_size, bin_size)
        lonBins = np.arange(lon_min, lon_max+bin_size, bin_size)

        latIndex = np.digitize(lat, latBins)
        lonIndex = np.digitize(lon, lonBins)

        latlon = np.unique((latIndex, lonIndex), axis=1)

        T_A_mean = np.full((4, latBins.size+1, lonBins.size+1), np.nan)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)

            for (val_i, val_j) in zip(latlon[0], latlon[1]):
                index, = np.where((latIndex==val_i) & (lonIndex==val_j))
                T_A_mean[:, val_i, val_j] = np.nanmean(T_A[:, index], axis=1)

        T_A_mean = T_A_mean[:, 1:-1:, 1:-1:]

    return latBins, lonBins, T_A_mean


def binning_plot(plot_path, crater, title, latBins, lonBins, T_A_mean,
                 latLim=(-80, 80), lonLim=(180, 180), background=False,
                 sharedColorbar=False, biggerMean=True):
    latBins_2D, lonBins_2D = np.meshgrid(lonBins, latBins)

    latIndex =  np.where((latLim[0] < latBins) & (latBins < latLim[1]))
    lonIndex =  np.where((lonLim[0] < lonBins) & (lonBins < lonLim[1]))

    try:
        T_A_mean_windowed = T_A_mean[:, latIndex, lonIndex]
    
    except IndexError:
        print("Window out of bounds. lat in [-80, 80] & lon in [-180, 180]")
        sys.exit()

    if sharedColorbar:
        with warnings.catch_warnings():
            warnings.filterwarnings('error')

            try:
                vmin = np.nanmin(T_A_mean_windowed)
                vmax = np.nanmax(T_A_mean_windowed)
            
            except RuntimeWarning:  # excepts if no values in window
                raise ValueError()

    fig, axes = plt.subplots(2, 2, layout='constrained')
    axesTitles = ['3 GHz', '7.8 GHz', '19.35 GHz', '37 GHz']

    for i, ax in enumerate(fig.axes):
        ax.set_title(axesTitles[i])

        if background:
            ax.imshow(plt.imread('../../plots/moon_image.jpg'),
                      extent=(-180, 180, -90, 90))

        if not sharedColorbar:
            with warnings.catch_warnings():
                warnings.filterwarnings('error')

                try:
                    vmin = np.nanmin(T_A_mean_windowed[i])
                    vmax = np.nanmax(T_A_mean_windowed[i])

                except RuntimeWarning:  # excepts if no values in window
                    raise ValueError()

        im = ax.pcolormesh(latBins_2D, lonBins_2D, T_A_mean[i],
                           cmap='jet', shading='auto', vmin=vmin, vmax=vmax
                           )

        if not sharedColorbar:
            cbar = fig.colorbar(im, ax=ax)
            cbar.set_label('$T_A$ [K]')
            cbar.ax.tick_params(labelsize=12)

        ax.set_xbound(lonLim[0], lonLim[1])
        ax.set_ybound(latLim[0], latLim[1])
        ax.set_xticks(np.linspace(lonLim[0], lonLim[1], 5))
        ax.set_yticks(np.linspace(latLim[0], latLim[1], 5))
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.tick_params(axis='both', which='minor', labelsize=10)
        ax.grid(False)

    fig.supxlabel("lon [$\\degree$]")
    fig.supylabel("lat [$\\degree$]")
    
    if sharedColorbar:
        cbar = fig.colorbar(im, ax=axes.ravel().tolist())
        cbar.set_label('$T_A$ [K]')
        cbar.ax.tick_params(labelsize=12)

    fig.savefig(
        f'{plot_path}/shared={sharedColorbar}/Temperature_map_for_{title}.jpeg'
        )

    # close all plots for memory purposes
    plt.close('all')
