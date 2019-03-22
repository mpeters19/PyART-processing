# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 12:35:27 2018

@author: danielholt

Version date: 1/29/2019
Daniel Hueholt
North Carolina State University
Undergraduate Research Assistant at Environment Analytics

"""

import pyart
import numpy as np
import string

def rasmussen_snow_rate(radar, radar_fieldnames):
    """
    DESCRIPTION: Calculates the Rasmussen snow rate from a given reflectivity field,
    then adds said field to the radar object.
    
    NOTE THAT THE NEW SNOW RATE FIELD IS NOT FORMATTED EXACTLY THE SAME AS A NORMAL PYART DATA FIELD
    PyART data fields are by default masked arrays with a data, mask, and fill_value component. The new 
    snow rate field will simply be an array.
    
    
    INPUTS:
    radar = A python object structure that contains radar information. Created
        by PyART in one of the pyart.io.read functions.
    radar_fieldnames = names of fields in the radar object
    
    OUTPUTS:
    radar = The original radar object but with the edited values for the 
        specified field.
        
    """
    
    reflectivity = radar.fields['reflectivity']['data'].data
    
    #Calculate the Rasmussen snow rate
    #This is the "wet snow" calculation
    #For details, see:
    #Rasmussen, Dixon, Vasiloff, Hage, Knight, Vivekanandan, and Xu (2003) Snow Nowcasting Using a Real-Time Correlation
    #   of Radar Reflectivity with Snow Gauge Accumulation. Journal of Applied  Meteorology. Journal of Applied Meteorology
    #   42 pp 20-36
    #Hoban, Nicole (2016) Observed Characteristics of Mesoscale Banding in Coastal Northeast U.S. Snow Storms. Unpublished
    #   Master's Thesis. North Carolina State University.
    divstep = np.divide(reflectivity,57.3)
    changetype = np.array(divstep,dtype = np.complex)
    rootstep = np.power(changetype,1/1.67)
    snow_rate = np.real(rootstep)
    
    snow_rate = np.array(snow_rate)
    
    radar.add_field_like('reflectivity','snow_rate',snow_rate,replace_existing=False)
    radar_fieldnames.append('snow_rate')
    
    return radar
    return radar_fieldnames

def kdp_second_derivative(radar, radar_fieldnames):
    """
    DESCRIPTION: Calculates the derivative of the two-way differential phase (Kdp)
    then adds said field to the radar object. Is this useful? Probably not!! But I thought
    this was calculating the actual Kdp at first so here we are
    
    NOTE THAT THE NEW FIELD IS NOT FORMATTED EXACTLY THE SAME AS A NORMAL PYART DATA FIELD
    PyART data fields are by default masked arrays with a data, mask, and fill_value component. The new 
    snow rate field will simply be an array.
    
    
    INPUTS:
    radar = A python object structure that contains radar information. Created
        by PyART in one of the pyart.io.read functions.
    radar_fieldnames = names of fields in the radar object
    
    OUTPUTS:
    radar = The original radar object but with the edited values for the 
        specified field.
        
    """
    phidp = radar.fields['specific_differential_phase']['data'].data
    
    kdp = np.diff(phidp)
    # This will now have a size -1 columns, as it is a difference of the original.
    # The size mismatch will prevent PyART from adding it properly to the radar object.
    # Hence, it must be padded.
    kdp = np.pad(kdp,[(0,0),(0,1)],'constant',constant_values=(np.nan))
    
    
    radar.add_field_like('reflectivity','kdp',kdp,replace_existing=False)
    radar_fieldnames.append('kdp')
    
    return radar
    return radar_fieldnames

def velocity_vertical_divergence(radar, radar_fieldnames):
    vdiv = radar.fields['dealiased_velocity']['data'].data
    
    # Take the derivative with respect to height
    vdiv = np.diff(vdiv,n=1,axis=0) #Python matrices start at 0
    # Pad the matrix to replace the missing row
    vdiv = np.pad(vdiv,[(0,1),(0,0)],'constant',constant_values=(np.nan))
    vdiv = np.abs(vdiv)
    
    radar.add_field_like('reflectivity','vdiv',vdiv,replace_existing=False)
    radar_fieldnames.append('vdiv')
    
    return radar
    return radar_fieldnames
    
    
    
    