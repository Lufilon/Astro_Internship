# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 13:45:33 2024

@author: Luis-
"""

import matplotlib as mpl


"""
TODO
    Schriftgrößen in plots für präsentierbare bilder wählen, verallgemeinert
"""

def plot_settings(purpose, style='seaborn-v0_8'):
    mpl.pyplot.style.use(style)
    mpl.rcParams['agg.path.chunksize'] = 10000
    # mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=[
        # 'teal', 'coral', 'lightblue', 'lime', 'turquoise',
        # 'darkgreen', 'tan', 'salmon', 'gold'])

    # mpl.pyplot.rcParams.update({'axes.titlesize': 'x-large'})

    if purpose=='thesis':  # TODO - ausprobieren
        mpl.rcParams['figure.figsize'] = (8, 6)
        mpl.rcParams['figure.dpi'] = 600
        mpl.rcParams.update({'font.size': 12})

    elif purpose=='presentation_single':
        mpl.rcParams['figure.figsize'] = (13.33, 7.5)
        mpl.rcParams['figure.dpi'] = 96
        mpl.rcParams.update({'font.size': 18})

    elif purpose=='presentation_double':
        mpl.rcParams['figure.figsize'] = (5, 3)
        mpl.rcParams['figure.dpi'] = 96
        mpl.rcParams.update({'font.size': 10})

    elif purpose=='paper':
        mpl.rcParams['figure.figsize'] = (3.54, 3.54)
        mpl.rcParams['figure.dpi'] = 600
        mpl.rcParams.update({'font.size': 6})

    else:
        raise Exception(
            "Not a valid purpose, try 'report', 'presentation' or 'paper'"
                        )

        