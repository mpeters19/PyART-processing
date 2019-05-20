# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 16:54:10 2015

@author: thecakeisalie

Version date: 3/21/2019
Daniel Hueholt
North Carolina State University
Undergraduate Research Assistant at Environment Analytics

"""
import numpy as np
import quality_control
import Master_plotter
import nexrad_plotter
import pyart
import gc
import sys
import calculated_fields
import colormap
import time

def parse_filelist(filelist, inpath, outpath, CHILL, fields, ranges, plot_bool, cmaps,
                   colorbar_labels, x_lim, y_lim, scan_strat, dealias_bool, 
                   name2dealias, new_name, nyquist_vel, Z_mask, Zdr_mask, PhiDP_mask, rhoHV_mask,
                   NCP_mask, SNR_mask, Zdr_offset):
    
    # Loop through each file in the list
    length_filelist = np.size(filelist)
        
    for item in range(0,length_filelist):
        
        # Define the filename
        filename = filelist[item]
        if length_filelist==1:
            filename = filelist
            
        
        # Make full path to file
        fqfn = inpath + filename
        
        # Print the full path
        print(fqfn)
        
        # Construct radar object
        if CHILL==True:
            radar = pyart.io.read_uf(filename,field_names={
                    'DZ': 'reflectivity',
                    'VE': 'corrected_velocity',
                    'W2': 'spectrum_width',
                    'DR': 'corrected_differential_reflectivity',
                    'RH': 'cross_correlation_ratio',
                    'NC': 'normalized_coherent_power',
                    'DP': 'one_way_differential_phase',
                    'KD': 'two_way_differential_phase',
                        })
            
        else: 
            radar = pyart.io.read(fqfn)            
        
        
        ##Add custom-calculated fields
        #Add the snow rate field
        snow_rate_bool = True;
        if snow_rate_bool:
            radar = calculated_fields.rasmussen_snow_rate(radar,fields)
            ranges.append((0,1.25))
            cmaps.append('viridis') #or YlGnBu
            colorbar_labels.append('Snow rate (mm/hr)')
            
        #Add the "Kdp" field NOTE THIS IS CURSED THIS IS ACTUALLY SECOND DERIVATIVE OF PHIDP
        kdp_bool = False;
        if kdp_bool:
            radar = calculated_fields.kdp_second_derivative(radar,fields)
            ranges.append((-1.5,1.5))
            cuckooPalette = colormap.cuckoo()
            cmaps.append(cuckooPalette)
            colorbar_labels.append('Kdp (deg/km)')
      
        
        # Data quality
        #   Remove values outside of a given Z, PhiDP, RhoHV, NCP range        
        if dealias_bool == False:
            if Z_mask['bool'] == True:
                radar = quality_control.removeNoiseZ(radar,fields,Z_mask['range'][0],Z_mask['range'][1])
            if PhiDP_mask['bool'] == True:
                radar = quality_control.removeNoisePhiDP(radar,fields,PhiDP_mask['range'][0],PhiDP_mask['range'][1])
            if rhoHV_mask['bool'] == True:
                radar = quality_control.removeNoiseRhoHV(radar,fields,rhoHV_mask['range'][0],rhoHV_mask['range'][1])
            if NCP_mask['bool'] == True:
                radar = quality_control.removeNoiseNCP(radar,fields,NCP_mask['range'][0],NCP_mask['range'][1])
            if SNR_mask['bool'] == True:
                radar = quality_control.removeNoiseSNR(radar,fields,SNR_mask['range'][0],SNR_mask['range'][1])
        else:
            # Need to apply the masks before dealiasing, but a KeyError will occur based on
            # the mismatch between new_name and name2dealias
            #print fields
            # Replace new_name with name2dealias
            v_ind = fields.index(new_name)
            fields.remove(new_name)
            #print fields
            fields.insert(v_ind,name2dealias)
            
            despeckler = pyart.correct.despeckle_field(radar,'corrected_velocity',threshold=(-40,40))
            
            print(fields)
            if Z_mask['bool'] == True:
                radar = quality_control.removeNoiseZ(radar,fields,Z_mask['range'][0],Z_mask['range'][1])
            if Zdr_mask['bool'] == True:
                radar = quality_control.removeNoiseZdr(radar,fields,Zdr_mask['range'][0],Zdr_mask['range'][1])
            if PhiDP_mask['bool'] == True:
                radar = quality_control.removeNoisePhiDP(radar,fields,PhiDP_mask['range'][0],PhiDP_mask['range'][1])
            if rhoHV_mask['bool'] == True:
                radar = quality_control.removeNoiseRhoHV(radar,fields,rhoHV_mask['range'][0],rhoHV_mask['range'][1])
            if NCP_mask['bool'] == True:
                radar = quality_control.removeNoiseNCP(radar,fields,NCP_mask['range'][0],NCP_mask['range'][1])
            if SNR_mask['bool'] == True:
                radar = quality_control.removeNoiseSNR(radar,fields,SNR_mask['range'][0],SNR_mask['range'][1])
            #radar = quality_control.noiseMaskGeneral(radar,fields,Z_mask,rhoHV_mask)
            #Also, despeckle
            
            
            # Reverse the process
            
            fields.remove(name2dealias)
            fields.insert(v_ind,new_name)
#        #print "Jazzy"
#        #print fields
      
        # Account for Zdr offset
        if Zdr_offset['bool']:
            radar.fields['differential_reflectivity']['data'].data[0:len(radar.fields['differential_reflectivity']['data'].data)] = np.subtract(radar.fields['differential_reflectivity']['data'].data,Zdr_offset['offset'])
#            print('Success!')
        

        
        # Dealias velocity data if required
        if dealias_bool == True:
            radar = quality_control.dealias(radar, filename, outpath, name2dealias, new_name, nyquist_vel, 100, 100, despeckler, savefile=False)
            gc.collect()
        
        print("Dealiasing complete!")
        
        #Add the vertical derivative of dealiased velocity field - RHI only
        vdiv_bool = True # vdiv cannot be calculated in this way for PPIs
        if scan_strat == 'PPI':
            vdiv_bool = False
        if vdiv_bool:
            radar = calculated_fields.velocity_vertical_divergence(radar,fields)
            #ranges.append((0,3)) # X
            ranges.append((0,3)) # S
            cmaps.append('inferno')
            colorbar_labels.append('|vDiv| ms^(-1)/gate')
        
        radar = quality_control.removeMountainClutter(radar,fields)
#        cats = radar.get_nyquist_vel(1,check_uniform=False)
        #print(kittens)
        #time.sleep(10)
#        print(cats)
#        time.sleep(10)
        
        
        #for sweep_number
        #pytda.calc_turb_sweep(radar)
        
        # Set figure sizes
        if scan_strat == 'RHI':
            #for 0 to 6 km use [40,6]
            #for 0 to 9 km use [42,8]
            figsize = [42,8]#[40,6]#[40,12]#[14.66, 3.652]#[40, 12]#[49.82, 4]#[43.6, 3.5]#30,4 #25,4
        else:
            figsize = [16,16] #Same settings used for PPI and sector scans [16.346, 12]
        
        # Create and save plots
        
        # don't forget to work out levels and contours here too!!
        plot_contour_overlay_bool = False
        for bfc in range(len(fields)): #base field counter            
            for cfc in range(len(fields)): #contour field counter
                if plot_contour_overlay_bool:
                    base_field = fields[bfc]
                    contour_field = fields[cfc]
                    if base_field == contour_field:
                        continue
                #print(fields)
                #time.sleep(4)
                    Master_plotter.plot_contour_overlay(base_field, contour_field, radar, filename, outpath, scan_strat, ranges[bfc], cmaps[bfc], colorbar_labels[bfc], figsize, dealias_bool, x_lim, y_lim)
            

        NEXRAD = False
        if plot_bool == True:
            if NEXRAD:
                nexrad_plotter.plot( radar, filename, outpath, scan_strat, fields, ranges, cmaps, colorbar_labels, figsize, dealias_bool, x_lim, y_lim)
            else:
                Master_plotter.plot(radar, filename, outpath, scan_strat, fields, ranges, cmaps, colorbar_labels, figsize, dealias_bool, x_lim, y_lim)
            gc.collect()
        
            
        
        # Print how many files are left to go
        #numleft = (length_filelist - item -1)
        #print(numleft)
        del radar
        del filename
        del fqfn
        gc.collect()