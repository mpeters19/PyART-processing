# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 12:42:46 2015

@author: thecakeisalie
"""
import glob
import os
import numpy as np
import string
import quality_control
import cPickle as pickle

def get_azimuth(radar, sweepnum):
    """
    DESCIPTION: For RHI's, extracts the azimuth angle from the radar object.
    
    INPUTS:
    radar = A python object structure that contains radar information. Created
        by PyART in one of the pyart.io.read functions.
    sweepnum = Natural number, usually 0 or 1 (for up sweep and down sweep)
    
    OUTPUTS:
    azi = The azimuth angle for the secifies sweep number.
    """
    if sweepnum==0:
        azi = radar.azimuth['data'][0]
    else:
        azi = radar.azimuth['data'][np.size(radar.azimuth['data'])-1]
    return azi

def get_filelist(inpath, wildcard, savefile):
    """
    DESCRIPTION: Generates a list of files that contain the specified wildcard 
        file their file name that in the specified path.
        
    INPUTS:
    inpath = A string that specifies the path to the desired files. 
    wildcard = A string that sets the phrase which is common to all desired
        files. The files in the inpath directory will be sorted using this 
        variable.
    savefile = A boolean value where True will save off a text files containing
        the names of the desired files separated by a newline, "\n".
        
    OUPUTS:
    filelist = A list of desired file names.
    """
    # Determine all files in inpath that begin with wildcard
    os.chdir(inpath)
    ident = '*' + wildcard
    identifier = ident + '*'
    filenamelist = glob.glob(identifier)
    
    # Sort the list
    filelist = sorted(filenamelist)
    
    if savefile == True:
        # Save the list
        name = "filelist_%s.txt" % wildcard
        txtfile = open(name, "w")
        for item in filelist:
            txtfile.write("%s\n" % item)
        txtfile.close()
        
    return filelist

def get_savename(filename, sweepnum, outpath, scan_strat, field, azi, dealias_bool):
    """
    IN BETA!!!!
    DESCRIPTION: Constructs the proper names for saving plots and files.
    
    INPUTS:
    filename = A string containing the name of the file.
    sweepnum = A natural number which specifies which radar sweep.
    outpath = A string that specifies the full path to where the .png image or
        file will be saved.
    scan_strat = String of either "RHI" or "PPI".
    field = A string of the field name. Ex. "DBZ"
    azi = Specifies the azimuth angle. Can be obtained from get_azimuth. If 
        dealing with a "PPI", azi can be any value.
    dealias_bool = A boolean value. Set to True is the data has been dealiased.
        Otherwise, set to False.
    
    OUTPUTS:
    save_name = A string containing the full save name. 
    """
    if scan_strat == 'PPI':                  
        filename = quality_control.PPI_fixfilename(filename)
                
    if dealias_bool == True:
        split_file = string.split(filename, '.')
        if scan_strat == 'RHI': 
            save_name = "%s%s.%s.%s.%s_deg_%d.%s.%s.%d.png" % (outpath, split_file[0], split_file[1], split_file[2], split_file[3], azi, split_file[4], field, sweepnum)
        else:
            save_name = "%s%s.%s.%d.png" % (outpath, filename, field, sweepnum)
    if dealias_bool == False:
        split_file = string.split(filename, '.')
        if scan_strat == 'RHI':
            save_name = "%s%s.%s.%s.%s_deg_%d.%s.%s.%d.png" % (outpath, split_file[0], split_file[1], split_file[2], split_file[3], azi, split_file[5], field, sweepnum)
        else:
            save_name = "%s%s.%s.%s.%s.%s.%s.%d.png" % (outpath, split_file[0], split_file[1], split_file[2], split_file[3], split_file[5], field, sweepnum)            
    return save_name
 
def read_object(filename):
    """
    DESCRIPTION: Reads in a string from a file and interprets it as a pickle data
    strem.  The data stream is then reconstructed back into a Python object.
    
    INPUTS:
    filename = The full path to the file.
    
    OUTPUTS:
    obj = The reconstructed Python object.
    """
    obj = pickle.load(open(filename, "rb"))
    return obj    
    
def save_object(obj, filename):
    """
    DESCRIPTION: Saves Python object to a file by converting it into a byte stream.
    
    INPUTS:
    obj = The Python object you wish to save.
    filename = The full path + name of the file.
    
    OUTPUS: 
    The saved file containing the object.
    """
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)