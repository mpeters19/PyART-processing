# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 12:27:04 2015

@author: thecakeisalie
"""
import pyart
import string

def dealias(radar, filename, outpath, name2dealias, new_name, nyquist_vel, 
            skip_along_ray, skip_between_rays, savefile=True):
    """
    DESCRIPTION: Dealiases a specified field using the PyART
        dealiased_region_based function and can save off a separate cfradial 
        file with the new dealiased field.
        
    INPUTS:
    radar = A python object structure that contains radar information. Created
        by PyART in one of the pyart.io.read functions.
    filename = A string containing the name of the file.
    outpath = A string that specifies the full path to where the .png images
        will be saved. 
    name2dealias = A string that specifies which field in the radar object to
        dealias.
    new_name = A string specifying the name of the new dealiased field.
    nyquist_value = Numeric interger.
    skip_along_ray = Integer value. Maximum number of filtered gates to skip
        over when joining regions, gaps between region larger than this will 
        not be connected.  Parameters specify the maximum number of filtered 
        gates along a ray. Set to 0 to disable 
        unfolding across filtered gates.
    skip_between_rays = Integer value. Maximum number of filtered gates to skip
        over when joining regions, gaps between region larger than this will 
        not be connected.  Parameters specify the maximum number of filtered 
        gates between rays. Set to 0 to disable 
        unfolding across filtered gates.
    
    OPTIONAL INPUS:
    savefile = Default set to True. A boolean value. If True, will save a new 
        cfradial file containing the dealiased field. 
    
    OUTPUTS:
    radar = A python object structure that contains radar information with the 
        addition of the new dealiased field.
    """
    
    # Determine which sweeps have no data and extract only the ones that have data
    if nyquist_vel != None:
        good = []
        for i in range(radar.nsweeps):
            sweep = radar.get_slice(i)
            if radar.fields[name2dealias]['data'][sweep][0,:].flatten().count() != 0:
                good.append(i)
        radar = radar.extract_sweeps(good)
    
    # Dealias and add new dealiased field to radar object    
    corr_vel = pyart.correct.dealias_region_based(radar,vel_field=name2dealias,nyquist_vel=nyquist_vel,skip_along_ray=skip_along_ray,skip_between_rays=skip_between_rays,gatefilter=False,keep_original=False)
    radar.add_field(new_name, corr_vel, True)
       
    # Save a new file containing the dealiased field
    if savefile == True:
        split_file = string.split(filename, '.')    
        filesavename = "%s%s.%s.%s.%s.unfold.%s" % (outpath, split_file[0], split_file[1], split_file[2], split_file[3], split_file[4])
        pyart.io.write_cfradial(filesavename, radar)
        
    return radar
    
def set2range(radar, field, val_max, val_min):
    """
    DESCRIPTION: Finds instances where a value is out side of the specified 
        bounds and sets the value to the closest bound. Ex. The bounds are
        [-8,16]. A value of -10 will be corrected to -8 and a value of 30 will 
        be corrected to 16.
    
    INPUTS:
    radar = A python object structure that contains radar information. Created
        by PyART in one of the pyart.io.read functions.
    field = A string of the field name. Ex. "DBZ"
    val_max = Numeric value. Sets the maximum bound.
    val_min = Numeric value. Sets the minimum bound.
    
    OUTPUTS:
    radar = The original radar object but with the edited values for the 
        specified field.
    """
    # Check to see if values are in range
    over = (radar.fields[field]['data'].data > val_max)
    under = (radar.fields[field]['data'].data < val_min)
            
    radar.fields[field]['data'].data[over] = val_max
    radar.fields[field]['data'].data[under] = val_min
    
    return radar
    
def PPI_fixfilename(filename): 
    """
    DESCRIPTION: Fixes the inconsistencies in the ROSE file name schemes.
    
    INPUTS:
    filename = The orginal name of the file.
    
    OUTPUTS:
    filename = The corrected file name.
    """                 
    end = len(filename)
    if filename[end-17:end-15] == 's0':
        chopstr = filename[end-17:end-6]
        if chopstr[-1:] == '0':
            longchopstr = filename[end-17:end-5]
            filename = filename.replace(longchopstr, 'SUR_')
        filename = filename.replace(chopstr, 'SUR_')
    return filename
    
def fix_CHILL_PPI_sweep_start_end(radar):
    """
    DESCRIPTION: Fixes the CSU-CHILL PPI sweep start and end indices to omit 
    transitions between sweeps.
    
    INPUTS:
    radar = Python radar object containing CSU-CHILL data
    
    OUTPUTS:
    radar = Radar object with corrected start and end sweep indices.
    """
    radar.sweep_start_ray_index['data'] = [0,382,789,1208,1604,2027]
    radar.sweep_end_ray_index['data'] = [381,788,1176,1567,1993,2428]
    return radar