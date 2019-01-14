# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 12:35:27 2018

@author: danielholt

Version date: 12/7/2018
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

#def two_way_differential_phase(radar, radar_fieldnames):
#    """
#    DESCRIPTION: Calculates the two-way differential phase (Kdp)
#    then adds said field to the radar object.
#    
#    NOTE THAT THE NEW FIELD IS NOT FORMATTED EXACTLY THE SAME AS A NORMAL PYART DATA FIELD
#    PyART data fields are by default masked arrays with a data, mask, and fill_value component. The new 
#    snow rate field will simply be an array.
#    
#    
#    INPUTS:
#    radar = A python object structure that contains radar information. Created
#        by PyART in one of the pyart.io.read functions.
#    radar_fieldnames = names of fields in the radar object
#    
#    OUTPUTS:
#    radar = The original radar object but with the edited values for the 
#        specified field.
#        
#    """
#    phidp = radar.fields['specific_differential_phase']
#    
#    phidp = np.diff(phidp)
    
    
    
    