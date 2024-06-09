# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 13:15:43 2024

@author: Luis-
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def sample_reduction(loc_time, lat, lon, T_A, condition, lower, upper):
    valid_ind, = np.where((lower < condition) & (condition < upper))

    loc_time = loc_time[valid_ind]
    lat = lat[valid_ind]
    lon = lon[valid_ind]
    T_A = T_A[:, valid_ind]

    return loc_time, lat, lon, T_A


def low_freq_corr(loc_time, T_A):
    # corrections according to Siegler et al. (2020)
    A_3Ghz, B_3Ghz = 12, 8
    A_78Ghz, B_78Ghz = 18, 8

    T_A[0] += A_3Ghz - (B_3Ghz * np.abs(np.cos(loc_time * 2*np.pi / 24)))
    T_A[1] += A_78Ghz - (B_78Ghz * np.abs(np.cos(loc_time * 2*np.pi / 24)))

    return T_A


def lat_norm(lat, lon, T_A, title):
    # latitude normalization according to Siegler et al. (2020)
    fit = np.empty((4, lat.size))

    fig, axes = plt.subplots(2, 2)

    axes_titles = ['3 GHz', '7.8 GHz', '19.35 GHz', '37 GHz']
    for i, ax in enumerate(fig.axes):
        def func(x, A, B):
            return A * np.cos(x)**B

        popt, pcov = curve_fit(
            func, np.deg2rad(lat), T_A[i], p0=(0, 150), method="lm"
        )

        fit[i] = func(np.deg2rad(lat), *popt)

        ax.set_title(axes_titles[i])
        
        ax.scatter(lat, T_A[i], s=8)
        ax.scatter(lat, fit[i], s=8, label="$T_A = " + "{:.2f}".format(popt[0]) +
                   "\cos\\vartheta^{" + "{:.2f}".format(popt[1]) + "}$")
        ax.legend(loc='upper right')

    fig.supxlabel("$\\vartheta$ [$\degree$]")
    fig.supylabel("$T_A$ [K]")
    fig.tight_layout()

    fig.savefig(f'../../plots/fit/lat_norm_fit_for_{title}.jpeg')

    T_A = T_A * fit[:, np.argmax(fit[3]), np.newaxis] / fit[:,]

    return T_A
