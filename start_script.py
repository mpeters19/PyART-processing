# -*- coding: utf-8 -*-
"""
STARTING POINT FOR PYART PROCESSING

DESCRIPTION:


Created on Thu Aug 06 14:01:55 2015

@author: thecakeisalie
"""
# Load neccessary packages (set appropriate working directory!)
import colormap
import gen_fun
import run_fun
import gc

######### Define Variables #############
### Path Variables (strings)
inpath = 'C:\\Users\\thecakeisalie\\Documents\\Python Scripts\\pyart_processing\\test_set'
outpath = 'C:\\Users\\thecakeisalie\\Documents\\Python Scripts\\pyart_processing\\test_set\\images'

### File and Data Variables ###
## Make sure these are what you want to ultimately plot!
# String
wildcard = 'X2013'
# String
scan_strat = 'PPI'
# List of strings
fields = ['reflectivity', 'dealiased_velocity', 'spectrum_width'] #'differential_reflectivity'] #, 'PID']
# List of numeric tuples
ranges = [(-10,65), (-30.0, 30.0), (0., 8.0), (-2.0, 6.0)] #, (0, 18)]

### Plotting Variables ###
# Boolean
plot_bool = True
# Numeric tuple
x_lim = [-300,300]
# Numeric tuple
y_lim = [-300,300]
# List of strings
colorbar_labels = ['DBZ (dBZ)', 'VEL (m/s)',  'WIDTH (m/s)', 'ZDR (dB)'] #, 'PID']

### Dealiasing Variables ###
# Boolean
dealias_bool = True
# String
name2dealias = 'velocity'
# String
new_name = 'dealiased_velocity'
# Numeric value; if working with ROSE data, set to None. 
nyquist_vel = 30
#######################################

# Adject inpath and outpath for easier writing
inpath = inpath + '\\'
outpath = outpath + '\\'

# Load color maps
LCH = colormap.LCH_Spiral()[0]
LCH_zdr = colormap.LCH_Spiral(nc = 100, np = .3, offset = 0, reverse = 1, L_range = [100, 0], name = 'LCH_zdr')[0]
LCH_wid = colormap.LCH_Spiral(nc = 100, np = .3, offset = 45, reverse = 0, L_range = [100, 0], name = 'LCH_wid')[0]
Int = colormap.PID_Integer()

cmaps = [LCH, 'seismic', LCH_wid , LCH_zdr, Int]

# Make filelist
filelist = gen_fun.get_filelist(inpath, wildcard, False)

# Parse through filelist and process
run_fun.parse_filelist(filelist, inpath, outpath, fields, ranges, plot_bool, 
                       cmaps, colorbar_labels, x_lim, y_lim, scan_strat, 
                       dealias_bool, name2dealias, new_name, nyquist_vel)
                       
gc.collect()