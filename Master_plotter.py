# -*- coding: utf-8 -*-
"""
Created on Fri May 30 15:06:17 2014

@author: thecakeisalie

Version date: 7/9/2018
Daniel Hueholt
North Carolina State University
Undergraduate Research Assistant at Environment Analytics
"""

# Import required modules
import numpy as np
import gc
import pyart
from matplotlib import pyplot as plt
import gen_fun
import quality_control

   
def plot(radar, filename, outpath, scan_strat, fields, ranges, cmaps, 
         colorbar_labels, figsize, dealias_bool, x_lim, y_lim, axis=None,
         title_flag=False,colorbar_flag = False):
    """
    DESCIPTION: Plots polar RHI and PPI data from netCDF on a cartesian grid. 
    
    INPUTS:
    radar = A python object structure that contains radar information. Created
        by PyART in one of the pyart.io.read functions.
    filename = A string containing the name of the file.
    outpath = A string that specifies the full path to where the .png images
        will be saved.
    scan_strat = String of either "RHI" or "PPI".
    fields = A list of strings specifying which fields to plot. 
        Ex. ["DBZ", "VEL"]
    ranges = A list of tuples specifying the minimum and maximum values for 
        each field in order. The minimum value is the first number and the 
        maximum value is the second number. Ex. [(-10,65), (-30,30)]
    cmaps = A list containing strings or calls of the names of the colorbars used to 
        plot each field respectively. Ex. [LCH, "seismic"]
    colorbar_labels = A list of strings that specify the colorbar labels on 
        each field respectively. Ex. ["Reflectivity (dBZ)", "Velocity (m/s)] 
    figsize = A list of numbers to specify the size of all the figures. The 
        same value is used for all figures. Ex. [14,12]
    dealias_bool = A boolean value where "True" will run the PyART dealiasing 
        algorithm over the velocity data and output a new netCDF file with a 
        dealiased velocity field called "VEL_D", and "False" will not run the 
        PyART dealiasing nor output a new netCDF file.
    
    OPTIONAL INPUTS (set to None/False by default):
    axis = Default set to None. Sets whether to plot axis labels or not.
    title_flag = Default set to False. Set to True to plot title.
    colorbar_flag = Default set to False. Set to True to plot colorbar.
    
    OUTPUTS:
    Plot(s) of RHI/PPI data.
    """    
    for sweepnum in range(0, np.size(radar.sweep_number['data'])):
        if scan_strat == 'RHI':
            azi = gen_fun.get_azimuth(radar, sweepnum)
        else:
            azi = []
        for i in range(len(fields)):
            
            # Set variables
            field = fields[i]
            cmap = cmaps[i]
            colorbar_label = colorbar_labels[i]
            vmin, vmax = ranges[i]                       
            
            # Check to see if values are in range
            radar = quality_control.set2range(radar,field,vmax,vmin)
            gc.collect()
            
            # Make radar display
            display = pyart.graph.RadarDisplay(radar)            
            
            # Clear any figures that might be open and close them
            plt.clf()
            plt.close()
            
            # Initiate plot and specify size
            fig = plt.figure(figsize = figsize)
            ax = fig.add_subplot(111)
            if scan_strat == 'RHI':
                plt.subplots_adjust(left=0.05, right=.99, top=0.95, bottom=0.2)
            else:
                plt.subplots_adjust(left=0.1, right=.9, top=0.97, bottom=0.1)
            #ax.set_axis_bgcolor('LightGray')
            ax.set_facecolor('LightGray')
                        
            # Plat fields and set limits
            if scan_strat == 'RHI':
                display.plot_rhi(field,sweepnum,vmin=vmin,vmax=vmax,title_flag=title_flag,cmap=cmap,axislabels=(axis, 'AGL (km)'),colorbar_flag=colorbar_flag,colorbar_label=colorbar_label)
                display.set_limits(ylim=y_lim)
                display.set_limits(xlim=x_lim)
            else:
                display.plot_ppi(field, sweepnum, vmin = vmin, vmax = vmax, title_flag = title_flag, cmap = cmap, axislabels = (axis, "N-S distance (km)"),colorbar_flag=colorbar_flag, colorbar_label = colorbar_label)
                display.set_limits(ylim=y_lim)
                display.set_limits(xlim=x_lim)
                
            for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
                item.set_fontsize(20)
            
            try:
                save_name = gen_fun.get_savename(filename, sweepnum, outpath, scan_strat, field, azi, dealias_bool)
            except:
                print "Name is not ROSE or WSR88D compatable. Using generic save name."
                if scan_strat == 'RHI':
                    save_name = "%s%s.azi%d.%s.%d.png" %(outpath, filename, azi, field, sweepnum)
                else:
                    save_name = "%s%s.%s.%d.png" %(outpath, filename, field, sweepnum)
                
            plt.close('all')
            fig.savefig(save_name)
            del display
            gc.collect()
            
        print ("%s %d" % ('Sweep number', sweepnum))
        del azi
        
        gc.collect()

               
