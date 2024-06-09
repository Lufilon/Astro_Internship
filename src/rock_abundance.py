# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:53:02 2024

@author: Luis-
"""

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import PIL
PIL.Image.MAX_IMAGE_PIXELS = 825753600


def rock_abundance(latLim, lonLim, crater, vmin=0.004, vmax=0.02, masked=False,
                   biggerMean=True):
    # change path to where you placed "RA_SAM_70Sto70N.tif"
    ra = PIL.Image.open('C:/Users/Luis-/Documents/Deviner Data/RA_SAM_70Sto70N.tif')

    im_array = np.array(ra)

    # order in lat caused by behaviour of .tif file and +70/-70 range
    ra_array_windowed = im_array[
        int((70 - latLim[1]) * 128) : int((70 - latLim[0]) * 128),
        int((lonLim[0] + 180) * 128) : int((lonLim[1] + 180) * 128)
        ]

    latBins = np.linspace(latLim[1], latLim[0], ra_array_windowed[0].size)

    lonBins = np.linspace(lonLim[0], lonLim[1], ra_array_windowed[1].size)

    latBins_2D, lonBins_2D = np.meshgrid(lonBins, latBins)

    fig, ax = plt.subplots()

    if masked:
        ra_array_windowed = ma.masked_where(
            ~((vmin < ra_array_windowed) & (ra_array_windowed < vmax)),
            ra_array_windowed
            )
    # 0.004 is mean rock abundance for the moon --> only above mean included
    im = ax.pcolormesh(latBins_2D, lonBins_2D, ra_array_windowed,
                       cmap='jet', norm=colors.LogNorm(vmin=vmin, vmax=vmax)
                       )

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Rock abundance [-]')
    cbar.ax.tick_params(labelsize=14)

    ax.set_xlabel("lon [$\\degree$]", fontsize=16)
    ax.set_ylabel("lat [$\\degree$]", fontsize=16)
    ax.set_xticks(np.linspace(lonLim[0], lonLim[1], 5))
    ax.set_yticks(np.linspace(latLim[0], latLim[1], 5))
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=10)
    ax.grid(False)

    fig.savefig(
        f'../../plots/map/biggerMean={biggerMean}/{crater}/rock_abundance.tif'
        )

    plt.close()
