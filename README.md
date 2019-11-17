# PyART Processing

Environment Analytics code written to aid in the processing, analysis, and visualization of radar data through the [ARM PyART](https://github.com/ARM-DOE/pyart) python package. Functions and documentation were originally created by Sara Berry in 2015. Software has been maintained by Daniel Hueholt since 2018. This code is designed to work with PyART 1.9.2 and Python 3.6.7.  

## General workflow
1. Open spyder.
2. Open start_script.py
3. Check the manual variables and change as appropriate. The documentation in the script explains how to do this.
4. Run start_script.py!  

## Setup (in Spyder) before running scripts for the first time
From start_script, go to Run->Configuration per file.  
In the “Console” pane, choose the “Execute in an external system terminal” radio button.  
      The default iPython console can't use multiprocessing functions; this executes code in a cmd window instead.  
In the “External system terminal” pane, check the “Interact with the Python console after execution” box.  
      This prevents the cmd window from closing when an error occurs.

## Even if the code works, some warnings appear in the console! Don’t panic.
**DeprecationWarning about interpretation as integer (tracks to seaborn palettes line 777)**  
Generated in external package seaborn, which is used to generate our Kdp colormap. It warns about a future problem when Python drops support for a variable conversion used in seaborn. There isn’t an obvious way for us to fix this; hopefully the seaborn group will update the package before this becomes an issue. For now, it has no effect on the code beyond the console warning.  

**RuntimeWarnings about invalid values encountered in roots, greater than, and less than (tracks to various functions in quality_control, region_dealias, and calculated_fields)**  
These warnings are generated when certain functions encounter NaN values. There is no effect on the code beyond generating a console warning.

## Code description
### Environment Analytics PyART processing toolkit
**calculated_fields** calculates derived variables from observations, and adds the new fields back into the radar object. Contains the following functions:  
      **rasmussen_snow_rate**: Calculates snow rate by rescaling reflectivity.  
      **kdp_derivative**: Takes the derivative of Kdp for CHILL data. (Written by accident; no practical use yet)  
      **velocity_vertical_divergence**: Derives vertical divergence of horizontal velocity (RHI only)  

**colorbars** saves images of colorbars. Useful for posters and presentations.  

**colormap** makes custom colormaps used for radar plotting. Contains the following functions:  
      **LCH_spiral**: Matthew Miller’s luminance-conserving map. Ported to Python by Sara Berry.  
      **PID_Integer**: Qualitative colormap used for PhiDP data in ROSE.  
      **PID_Integer_CHILL**: Qualitative colormap designed for PhiDP data in CHILL. Obsolete.  
      **contourColors**: 6 distinct colors, each high-contrast against many radar backgrounds.  
      **rgb_to_hex**: Converts RGB colors to hex color.  
      **convert_to_grey**: Converts a color to a greyscale color.  
      **cuckoo**: Luminance-conserving and red-green safe diverging colormap.  
      
**Master_plotter** takes care of plotting the data that has been processed by the rest of the toolkit. Contains the following functions:  
      **contour_overlay**: Overlays contours on a base plot.  
      **plot**: Generates and saves the standard RHI/PPI plots we know and love!! 
      
**quality_control** contains functions that manage dealiasing, masking, mountain removal, and similar tasks. Contains the following functions:  
      **dealias**: Manages velocity dealiasing using the PyART region-based algorithm.  
      **set2range**: Restricts values to a given range.  
      **removeNoiseZ**: Removes values across all fields outside a given Z range.  
      **removeNoiseZdr**: Removes values across all fields outside a given Zdr range.  
      **removeNoiseRhoHV**: Removes values across all fields outside a given rhoHV range.  
      **removeNoisePhiDP**: Removes values across all fields outside a given PhiDP range.  
      **removeNoiseNCP**: Removes values across all fields outside a given NCP range.  
      **removeNoiseSNR**: Removes values across all fields outside a given SNR range.  
      **removeMountainClutter**: Attempts to kill mountain return.  
      **PPI_fixfilename**: Fixes filenames for PPIs. Applies to ROSE project only.  
      **fix_CHILL_PPI_sweep_start_end**: Matches up PPI sweeps from CHILL. Applies to ROSE.  

**run_fun** contains the parse_filelist function, which manages the radar data processing tasks (e.g. importing data, dealiasing, masks, calculating derived fields) by referring to PyART and custom functions. Data is then passed to Master_plotter.  

**start_script** is where all input variables are set, then passed to the functions that take care of the rest of the radar processing. This is the only place where manual input is needed. See comment and description within the code for details.  



### Modified PyART files
**cfradial** is modified to fix issue with radars that record their units as “seconds” instead of “seconds since epoch.”
**nexrad_level2** is updated to use np.frombuffer instead of np.fromstring, which is now deprecated.  
**radar** has a fix for the float/integer mismatch that occurs in KASPR data.  
**radardisplay** edits the colorbar so it takes up only a small portion of the figures.  
**uffile** now uses np.frombuffer instead of np.fromstring, which is deprecated.  

## Sources and Credit
PyART citation:
Helmus, J.J. & Collis, S.M., (2016). The Python ARM Radar Toolkit (Py-ART), a Library for Working with Weather Radar Data in the Python Programming Language. Journal of Open Research Software. 4(1), p.e25. DOI: [http://doi.org/10.5334/jors.119](http://doi.org/10.5334/jors.119)
