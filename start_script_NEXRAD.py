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

Version date: 10/26/2018
Daniel Hueholt
North Carolina State University
Undergraduate Research Assistant at Environment Analytics

"""
# Load necessary packages (set appropriate working directory!)
import colormap
import gen_fun
import run_fun
import gc

######### Define Variables #############
### Path Variables (strings)
inpath = 'F:\\444_NEXRAD\\' #'H:\\store radar files\\NEXRAD\\KFTG\\untarred\\'
outpath = 'F:\\444_NEXRAD\\output\\'#'H:\\radar output\\NEXRAD\\KFTG\\20180201\\'

### File and Data Variables ###

# String
wildcard = 'KLTX' #Common wildcards are below
#KXA: Dallas HF-S
#KXAS: NBC5 StormRanger
#KASPR: SBU Ka-band
#CHX: CSU-CHILL X-band
#CHL: CSU-CHILL S-band

# Special import specifiers
CHILL = False #CHILL files use a special variant of the UF format; this tells PyART to use the correct fieldname mapping

# String
scan_strat = 'PPI' #Possible entries are below
#PPI: Plan view at a specific angle
#Sector: Plan view at a confined set of azimuths
#RHI: Cross section along a specific azimuth
# PyART can be used with other scan strategies but these are not yet supported in this toolkit.

# List of strings (field names)
#HF-S: ['DBZH','DBZV','ZDR','RHOHV','PHIDP','SNRHC','SNRVC','dealiasVELH']
#StormRanger:
#KASPR: ['correlation_coefficient','differential_phase','differential_reflectivity','linear_depolarization_ratio','linear_depolarization_ratio_hc_hh','mean_doppler_velocity','mean_doppler_velocity_folded','reflectivity','reflectivity_xpol_htx','reflectivity_xpol_vtx','snr','snr_xpol_htx','snr_xpol_vtx','spectrum_width']
#KASPR (commonly-used): ['correlation_coefficient','differential_reflectivity','PyART_dealiased_velocity','reflectivity','spectrum_width','linear_depolarization_ratio','snr']
#CSU-CHILL: ['reflectivity','corrected_velocity','corrected_differential_reflectivity','spectrum_width','cross_correlation_ratio','normalized_coherent_power','specific_differential_phase']

#fields = ['reflectivity','dealiased_velocity','corrected_differential_reflectivity','spectrum_width','cross_correlation_ratio','normalized_coherent_power','specific_differential_phase']
fields = ['reflectivity','dealiased_velocity','spectrum_width','cross_correlation_ratio','differential_reflectivity']#,'dealiased_velocity','spectrum_width']

# List of numeric tuples (ranges for data)
# ORDER OF THESE MUST MATCH ORDER OF FIELDS
#ranges = [(0,60),(0,60),(-20,0),(0,1),(0,180),(0,1),(0,1),(-40,40)] #HF-S, with broken Zdr
#ranges = #StormRanger
#ranges = [(0.5,1),(-2,2),(-35,35),(-5,40),(0,3),(-40,-20),(0,100)] #KASPR (commonly-used) (winter)
#ranges = [(-5,35), (-30,30),(-2,2),(0,5),(0,1.2),(0,1),(-15,15)] #CSU-CHILL (winter)
#ranges = [(-5,30),(-30,30),(-1,2),(0,4),(0.5,1),(0,1),(-2,2)] #CSU-CHILL (winter)
#ranges = [(-5,65),(-40,40),(-3,5),(0,8),(0.5,1),(0,1),(-5,5)] #CSU-CHILL (summer)
#ranges = [(-5,65),(-40,40),(-3,5),(0,8),(0.5,1),(0,1),(-5,5)] #CSU-CHILL (summer)
#ranges = [(-5,25),(-20,20),(-1,2),(0,4),(0.4,1),(0,1),(-2,2)] #CSU-CHILL (winter)
ranges = [(-5,50),(-50,50),(0,12),(0,1),(-4,4)]#,(-20,20),(-1,2),(0,4),(0.4,1)] #
#ranges = [(-5,25),(-20,20)] #CSU-CHILL (winter)
#ranges = [(-5,25),(0,1)] #CSU-CHILL (winter)

### Plotting Variables ###

# Boolean
plot_bool = True

# Numeric tuple
#x_lim = [-375,375] #HF-S PPI
#x_lim =  #StormRanger
x_lim = [-150,150] #NEXRAD PPI
# Numeric tuple
y_lim = [-150,150] #NEXRAD PPI

# List of strings (colorbar labelsl)
#colorbar_labels = ['DBZ (dBZ)','DBZ (dBZ)','ZDR (DB)','rhoHV','PhiDP','SNR','SNR','V (m/s)'] #HF-S
#colorbar_labels = #StormRanger
#colorbar_labels = ['rhoHV','PhiDP','ZDR (DB)','V (m/s)','DBZ (dBZ)','Width (m/s)'] #KASPR few
#colorbar_labels = ['rhoHV','Zdr (dB)','V (m/s)','Z (dBZ)','Spectral Width (m/s)','LDR (dB)','SNR'] #KASPR common
#colorbar_labels = ['DBZ (dBZ)','V (m/s)','ZDR (dB)','Width (m/s)','rhoHV','NCP','PhiDP'] #CSU-CHILL
colorbar_labels = ['DBZ (dBZ)','V (m/s)','Width (m/s)','rhoHV','Zdr (dB)'] #CSU-CHILL
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
name2dealias = 'velocity' #NEXRAD, hopefully
# String
#new_name = 'dealiasVELH' #HF-S
#new_name = #StormRanger
#new_name = 'PyART_dealiased_velocity' #KASPR
new_name = 'dealiased_velocity' #CSU-CHILL

# Numeric value; if working with ROSE data, set to None. 
#nyquist_vel = 8.5048 #HF-S
#nyquist_vel= 9.999 #KASPR
nyquist_vel = 26.389 #KCYS 2018 02 01

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

#cmaps = [LCH,LCH,LCH_zdr,'bone_r','cividis','copper','copper','seismic'] #HF-S
#cmaps = #StormRanger
#cmaps = ['bone_r','cividis',LCH_zdr,'seismic',LCH,LCH_wid] #KASPR few
#cmaps = ['bone_r',LCH_zdr,'RdBu_r',LCH,LCH_wid,'inferno','copper'] #KASPR common RdBu_r
#cmaps = [LCH,'RdBu_r',LCH_zdr,LCH_wid,'bone_r','copper','cividis'] #CSU-CHILL
cmaps = [LCH,'RdBu_r',LCH_wid,'bone_r',LCH_zdr]#,'RdBu_r',LCH_zdr,LCH_wid,'bone_r'] #CSU-CHILL
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
#   Common rhoHV ranges: (0.5, 1.2) (good for most cases)
#   Common NCP rnages: (0.05, 1.2) (good for most cases)

Z_mask = {
        "bool": False,
        "range": (-35,25)
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
        "bool": False,
        "range": (0.45, 1.2)
        }

NCP_mask = {
        "bool": False,
        "range": (0.05, 1.2)
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
run_fun.parse_filelist(filelist, inpath, outpath, CHILL, fields, ranges, plot_bool, 
                       cmaps, colorbar_labels, x_lim, y_lim, scan_strat, 
                       dealias_bool, name2dealias, new_name, nyquist_vel, Z_mask, Zdr_mask, PhiDP_mask,
                       rhoHV_mask, NCP_mask, SNR_mask, Zdr_offset)
                       
gc.collect()

print("Completed!")