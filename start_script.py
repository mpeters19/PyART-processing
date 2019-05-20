# -*- coding: utf-8 -*-
"""
STARTING POINT FOR PYART PROCESSING

DESCRIPTION: Use this script to easily process and plot radar data in PyART.

WORKFLOW:
    inpath
    outpath
    wildcard
    specials
    scan_strat
    fields
    ranges
    x_lim
    y_lim
    colorbar_labels
    dealias_bool
        name2dealias
        new_name
        nyquist_vel
    cmaps


Created on Thu Aug 06 14:01:55 2015

@author: thecakeisalie

Version date: 04/21/2019
Daniel Hueholt
North Carolina State University
Undergraduate Research Assistant at Environment Analytics

"""
# Load necessary packages (set appropriate working directory!)
import colormap
import gen_fun
import run_fun
import gc
#import tracemalloc
import numpy as np
from multiprocessing import Process

#tracemalloc.start()

######### Define Variables #############
### Path Variables (strings)
inpath = 'H:\\store radar files\\CSU-CHILL\\20180121\\p2\\PPI\\'
outpath = 'H:\\radar output\\testImages\\1_gatefilter\\'

### File and Data Variables ###

# String
wildcard = 'CHX' #Common wildcards are below
#KXA: Dallas HF-S
#KXAS: NBC5 StormRanger
#KASPR: SBU Ka-band
#CHX: CSU-CHILL X-band
#CHL: CSU-CHILL S-band
# Use start_script_NEXRAD script to process NEXRAD data

# Special import specifiers
CHILL = True #CHILL files use a special variant of the UF format; this tells PyART to use the correct fieldname mapping

# String
scan_strat = 'PPI' #Possible entries are below
#PPI: Plan view at a specific angle
#Sector: Plan view at a confined set of azimuths, IN PROGRESS
#RHI: Cross section along a specific azimuth
# PyART can be used with other scan strategies but these are not yet supported in this toolkit.

# List of strings (field names)
#HF-S: ['DBZH','DBZV','ZDR','RHOHV','PHIDP','SNRHC','SNRVC','dealiasVELH']
#StormRanger:
#KASPR: ['correlation_coefficient','differential_phase','differential_reflectivity','linear_depolarization_ratio','linear_depolarization_ratio_hc_hh','mean_doppler_velocity','mean_doppler_velocity_folded','reflectivity','reflectivity_xpol_htx','reflectivity_xpol_vtx','snr','snr_xpol_htx','snr_xpol_vtx','spectrum_width']
#KASPR (commonly-used): ['correlation_coefficient','differential_reflectivity','PyART_dealiased_velocity','reflectivity','spectrum_width','linear_depolarization_ratio','snr']
#CSU-CHILL: ['reflectivity','corrected_velocity','corrected_differential_reflectivity','spectrum_width','cross_correlation_ratio','normalized_coherent_power','specific_differential_phase']

fields = ['reflectivity','dealiased_velocity','corrected_differential_reflectivity','spectrum_width','cross_correlation_ratio','normalized_coherent_power','one_way_differential_phase','two_way_differential_phase']

# List of numeric tuples (ranges for data)
# ORDER OF THESE MUST MATCH ORDER OF FIELDS
#ranges = [(0,60),(0,60),(-20,0),(0,1),(0,180),(0,1),(0,1),(-40,40)] #HF-S, with broken Zdr
#ranges = #StormRanger
#ranges = [(0.5,1),(-2,2),(-35,35),(-5,40),(0,3),(-40,-20),(0,100)] #KASPR (commonly-used) (winter)
#ranges = [(-5,65),(-40,40),(-3,5),(0,8),(0.5,1),(0,1),(-5,5)] #CSU-CHILL (summer)
ranges = [(-5,25),(-20,20),(-1,2),(0,4),(0.4,1),(0,1),(-60,-120),(-1.5,1.5)] #CSU-CHILL (winter)
#ranges = [(-5,25),(-40,40),(-1,2),(0,8),(0.4,1),(0,1),(-30,-60),(-0.5,0.5)] #CSU-CHILL (winter) S-band

### Plotting Variables ###

# Boolean
plot_bool = True

# Numeric tuple
#x_lim = [-375,375] #HF-S PPI
#x_lim =  #StormRanger
#x_lim = [-30,30] #KASPR PPI
#x_lim = [0,30] #KASPR RHI
#x_lim = [0,50] #CSU-CHILL Bragg waves RHI
#x_lim = [0,75] #CSU-CHILL RHI
if scan_strat == 'PPI':
    x_lim = [-60,60] #CSU-CHILL PPI
if scan_strat == 'RHI':
    x_lim = [0,60]
# Numeric tuple
#y_lim = [-375,375] #HF-S PPI
#y_lim = #StormRanger
#y_lim = [-30,30] #KASPR PPI
#y_lim = [0,8] #KASPR RHI
#y_lim = [0,5] #CSU-CHILL Bragg waves RHI
#y_lim = [0,16] #CSU-CHILL RHI (summer)
if scan_strat == 'PPI':
    y_lim = [-60,60] #CSU-CHILL PPI
    
if scan_strat == 'RHI':
    y_lim = [0,9]

# List of strings (colorbar labelsl)
#colorbar_labels = ['DBZ (dBZ)','DBZ (dBZ)','ZDR (DB)','rhoHV','PhiDP','SNR','SNR','V (m/s)'] #HF-S
#colorbar_labels = #StormRanger
#colorbar_labels = ['rhoHV','PhiDP','ZDR (DB)','V (m/s)','DBZ (dBZ)','Width (m/s)'] #KASPR few
#colorbar_labels = ['rhoHV','Zdr (dB)','V (m/s)','Z (dBZ)','Spectral Width (m/s)','LDR (dB)','SNR'] #KASPR common
colorbar_labels = ['DBZ (dBZ)','V (m/s)','ZDR (dB)','Width (m/s)','rhoHV','NCP','PhiDP (deg)','KDP (deg/km)'] #CSU-CHILL
#colorbar_labels = ['DBZ (dBZ)','V (m/s)','ZDR (dB)','Width (m/s)','rhoHV'] #CSU-CHILL
#colorbar_labels = ['DBZ (dBZ)','V (m/s)','ZDR (dB)','NCP','rhoHV'] #CSU-CHILL
#colorbar_labels = ['DBZ (dBZ)','V (m/s)'] #CSU-CHILL
#colorbar_labels = ['DBZ (dBZ)','rhoHV'] #CSU-CHILL

print("Plotting Variables section complete!")

### Dealiasing Variables ###
# Boolean
dealias_bool = True

# String
#name2dealias = 'VELH' #HF-S
#name2dealias = #StormRanger
#name2dealias = 'mean_doppler_velocity_folded' #KASPR
name2dealias = 'corrected_velocity' #CSU-CHILL
# String
#new_name = 'dealiasVELH' #HF-S
#new_name = #StormRanger
#new_name = 'PyART_dealiased_velocity' #KASPR
new_name = 'dealiased_velocity' #CSU-CHILL

# Numeric value; if working with ROSE data, set to None. 
#nyquist_vel = 8.5048 #HF-S
#nyquist_vel= 9.999 #KASPR
nyquist_vel = 25.893 #X-band CHILL
#nyquist_vel = 27.5039 #S-band CHILL
#nyquist_vel = 26.389

print("Dealiasing Variables section complete!")
#######################################

# Adject inpath and outpath for easier writing
inpath = inpath + '\\'
outpath = outpath + '\\'

print(inpath)
print(outpath)

# Load color maps
# L_range is the luminance range; if the colors come out too dark then raise the minimum
# luminance value
max_luminance = 100
min_luminance = 0
LCH = colormap.LCH_Spiral()[0]
LCH_zdr = colormap.LCH_Spiral(nc = 100, np = .3, offset = 0, reverse = 1, L_range = [max_luminance, min_luminance], name = 'LCH_zdr')[0]
LCH_wid = colormap.LCH_Spiral(nc = 100, np = .3, offset = 45, reverse = 0, L_range = [max_luminance, min_luminance], name = 'LCH_wid')[0]
Int = colormap.PID_Integer()
IntCHILL = colormap.PID_Integer_CHILL()
cuckooPalette = colormap.cuckoo()


#cmaps = [LCH,LCH,LCH_zdr,'bone_r','cividis','copper','copper','seismic'] #HF-S
#cmaps = #StormRanger
#cmaps = ['bone_r','cividis',LCH_zdr,'seismic',LCH,LCH_wid] #KASPR few
#cmaps = ['bone_r',LCH_zdr,'RdBu_r',LCH,LCH_wid,'inferno','copper'] #KASPR common RdBu_r
cmaps = [LCH,'RdBu_r',LCH_zdr,LCH_wid,'bone_r','copper','magma',cuckooPalette] #CSU-CHILL
#cmaps = [LCH,'RdBu_r',LCH_zdr,LCH_wid,'bone_r'] #CSU-CHILL
#cmaps = [LCH,'RdBu_r',LCH_zdr,'copper','bone_r'] #CSU-CHILL
#cmaps = [LCH,'RdBu_r'] #CSU-CHILL
#cmaps = [LCH,'bone_r'] #CSU-CHILL

#cmaps = [LCH,'seismic',LCH_zdr,LCH_wid,'bone_r','copper','cividis'] #CSU-CHILL

print ("Colormaps section complete!")
# Make filelist
filelist = gen_fun.get_filelist(inpath, wildcard, False)

# Plausibility check on inputs
if len(cmaps)!=len(colorbar_labels):
    raise IndexError('Check number of colormaps and colorbars!')

print ("Filelist complete!")

# Data quality
#   Remove values outside of a given Z, PhiDP, RhoHV, NCP range
#   Common Z ranges: (-5, 50) (KASPR), (-10, 80) (HF-S)
#   Common PhiDP ranges: (0, 180) (HF-S)
#   Common rhoHV ranges: (0.45, 1.2) (good for most cases)
#   Common NCP rnages: (0.05, 1.2) (good for most cases)

Z_mask = {
        "bool": False,
        "range": (-5,45)
        }

Zdr_mask = {
        "bool": False,
        "range": (-2,2)
}

PhiDP_mask = {
        "bool": False,
        "range": (-5, 5)
        }

rhoHV_mask = {
        "bool": True,
        "range": (0.45, 1.2)
        }

NCP_mask = {
        "bool": False,
        "range": (0.15, 1.2)
        }

SNR_mask = {
        "bool": False,
        "range": (8, 100)
        }

#   Account for Zdr offset on radars such as KASPR, HF-S
Zdr_offset = {
        "bool": False,
        "offset": 1.2
        }

# Parse through filelist and process

if __name__== '__main__':
        length_filelist = np.size(filelist)
        print("Processing in progress!")
        for item in range(0,length_filelist):
            filelist_ind=filelist[item]
            p = Process(target=run_fun.parse_filelist,args=(filelist_ind, inpath, outpath, CHILL, fields, ranges, plot_bool, 
                                                                            cmaps, colorbar_labels, x_lim, y_lim, scan_strat, 
                                                                            dealias_bool, name2dealias, new_name, nyquist_vel, Z_mask, Zdr_mask, PhiDP_mask,
                                                                            rhoHV_mask, NCP_mask, SNR_mask, Zdr_offset))
            p.start()
            print(p.is_alive())
            p.join()
            p.terminate()
            numleft = (length_filelist - item -1)
            print(numleft)
            
        print("Completed!")


#run_fun.parse_filelist(filelist_first, inpath, outpath, CHILL, fields, ranges, plot_bool, 
#                       cmaps, colorbar_labels, x_lim, y_lim, scan_strat, 
#                       dealias_bool, name2dealias, new_name, nyquist_vel, Z_mask, Zdr_mask, PhiDP_mask,
#                       rhoHV_mask, NCP_mask, SNR_mask, Zdr_offset)
#
#run_fun.parse_filelist(filelist_second, inpath, outpath, CHILL, fields, ranges, plot_bool, 
#                       cmaps, colorbar_labels, x_lim, y_lim, scan_strat, 
#                       dealias_bool, name2dealias, new_name, nyquist_vel, Z_mask, Zdr_mask, PhiDP_mask,
#                       rhoHV_mask, NCP_mask, SNR_mask, Zdr_offset)
#
#                       
gc.collect()
#
#snapshot = tracemalloc.take_snapshot()
#top_stats = snapshot.statistics('lineno')
#
#print("[ Top 10 ]")
#for stat in top_stats[:10]:
#    print(stat)