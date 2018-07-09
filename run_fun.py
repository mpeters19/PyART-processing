# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 16:54:10 2015

@author: thecakeisalie
"""
import numpy as np
import quality_control
import Master_plotter
import pyart
import gc

def parse_filelist(filelist, inpath, outpath, fields, ranges, plot_bool, cmaps,
                   colorbar_labels, x_lim, y_lim, scan_strat, dealias_bool, 
                   name2dealias, new_name, nyquist_vel):
    # Loop through each file in the list
    length_filelist = np.size(filelist)
    for item in range(0,length_filelist):
        
        # Define the filename
        filename = filelist[item]
        
        # Make full path to file
        fqfn = inpath + filename
        
        # Construct radar object
        radar = pyart.io.read(fqfn)
        
        # Dealias velocity data if required
        if dealias_bool == True:
            radar = quality_control.dealias(radar, filename, outpath, name2dealias, new_name, nyquist_vel, 100, 100, savefile=False)
            gc.collect()
        
        # Set figure sizes
        if scan_strat == 'PPI':
            figsize = [14, 12]
        if scan_strat == 'RHI':
            figsize = [25, 4]
            
        # Create and save plots
        if plot_bool == True:
            Master_plotter.plot(radar, filename, outpath, scan_strat, fields, ranges, cmaps, colorbar_labels, figsize, dealias_bool, x_lim, y_lim)
            gc.collect()
        
        # Print how many files are left to go
        numleft = (length_filelist - item -1)
        print numleft
        del radar
        del filename
        del fqfn
        gc.collect()