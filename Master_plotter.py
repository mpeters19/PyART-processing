# -*- coding: utf-8 -*-
"""
Created on Fri May 30 15:06:17 2014

@author: thecakeisalie

Version date: 5/22/2019
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
import math
import scipy.ndimage as spyi
import time
import colormap


def contour_overlay(radar, sweepnum, contourField, baseField, ax, total_text, contourValues):
    """
    DESCRIPTION: Overlays contours on a plot of a different data type.
    
    INPUTS:
    radar = A python object structure that contatins radar information. Created by PyART
        in one of the pyart.io.read functions.
    sweepnum = The sweep number of the plot in question.
    contourField = Data key to be contoured.
    baseField = Data key referring to the base plot.
    ax = The plot in question.
    total_text = Text for the plot title.
    contourValues = Numpy array of desired values at which to draw contours
    
    Written by Daniel Hueholt
    Undergraduate Research Assistant at Environment Analytics
    Last major update: 5/20/2019
    """
    # Setup
    dataToContourRaw = radar.get_field(sweepnum,contourField)
    x,y,height = radar.get_gate_x_y_z(sweepnum,edges=False)
    x/=1000.0
    y/=1000.0
    height/=1000.0
    dataCoord = np.sqrt(x**2+y**2)*np.sign(y)
    dataCoord = -dataCoord
    dataToContourSmooth = spyi.gaussian_filter(dataToContourRaw,sigma=1.2)
    #contours=ax.contour(dataCoord,height,dataToContourSmooth,contourValues,linewidths=1.5,colors=('blue','white','red','orange','yellow'),linestyles='solid',antialiased=True)
    
    # Draw contours
    contourColormap = colormap.contourColors()
    contours=ax.contour(dataCoord,height,dataToContourSmooth,contourValues,linewidths=1.5,cmap=contourColormap,linestyles='solid',antialiased=True)
    contoured_field_is = 'Contoured field is ';
    long_spacer = '     '
    total_text = total_text+long_spacer+contoured_field_is+contourField
    #Make contour labels
    plt.clabel(contours,contourValues,fmt='%r',inline=True,fontsize=20) #%r
    #print("Contour section completed!")
    
    return total_text

   
def plot(radar, radar_type, filename, outpath, scan_strat, fields, ranges, cmaps, 
         colorbar_labels, figsize, dealias_bool, x_lim, y_lim, axis=None,
         title_flag=False,colorbar_flag = True):
    """
    DESCRIPTION: Plots polar RHI and PPI data from netCDF on a cartesian grid. 
    
    INPUTS:
    radar = A python object structure that contains radar information. Created
        by PyART in one of the pyart.io.read functions.
    radar_type = A string describing the radar type, e.g. 'CHILL','KASPR', etc.
    filename = A string containing the name of the file.
    outpath = A string that specifies the full path to where the .png images
        will be saved.
    scan_strat = String of either "RHI", "PPI", or "Sector".
    fields = A list of strings specifying which fields to plot. 
        Ex. ["DBZ", "VEL"]
    ranges = A list of tuples specifying the minimum and maximum values for 
        each field in order. The minimum value is the first number and the 
        maximum value is the second number. Ex. [(-10,65), (-30,30)]
    cmaps = A list containing strings or calls of the names of the colorbars used to 
        plot each field respectively. Ex. [LCH, "RdBu_r"]
    colorbar_labels = A list of strings that specify the colorbar labels on 
        each field respectively. Ex. ["Reflectivity (dBZ)", "Velocity (m/s)] 
    figsize = A list of numbers to specify the size of all the figures. The 
        same value is used for all figures. Ex. [14,12]
    dealias_bool = A boolean value where "True" will run the PyART dealiasing 
        algorithm over the velocity data and output a new netCDF file with a 
        dealiased velocity field called "VEL_D", and "False" will not run the 
        PyART dealiasing nor output a new netCDF file.
    x_lim = Array giving x-limits in kilometers
    y_lim = Array giving y-limits in kilometers.
    
    OPTIONAL INPUTS (set to None/False by default):
    axis = Default set to None. Sets whether to plot axis labels or not.
    title_flag = Default set to False. Set to True to plot title.
    colorbar_flag = Default set to True. Set to False to disable the colorbar.
    
    OUTPUTS:
    Plot(s) of RHI/PPI data.
    
    WEIRD QUIRKS:
    metadisp: Logical variable to control whether metatext (title, azimuth, etc.) is included in plots.
    x/y location of title text is set manually; do a find on "plt.figtext(" to find the relevant lines. (Locations are different for RHI and PPI, make sure you're changing the locations for the scan type you're trying to make!)
    
    """    
    for sweepnum in range(0, np.size(radar.sweep_number['data'])):
        
        if scan_strat == 'RHI':
            azi = gen_fun.get_azimuth(radar, sweepnum)
        else:
            azi = [] #Azimuth only matters for RHI scans
        
        for i in range(len(fields)):
            
            field = fields[i]
            try:
                cmap = cmaps[i]
            except IndexError:
                raise IndexError("Check to make sure number of colormaps is correct!")
                
            try:
                colorbar_label = colorbar_labels[i]
            except IndexError:
                raise IndexError("Check to make sure number of colorbar labels is correct!")
            
            vmin, vmax = ranges[i]                       
            
            # Check to see if values are in range
            #radar = quality_control.set2range(radar,field,vmax,vmin) #Not used in current CHILL processing
            
            # Instantiate PyART radar display object
            display = pyart.graph.RadarDisplay(radar)            
            
            # Clear and close any figures that might be open
            plt.clf()
            plt.close()
            
            # Initiate plot and specify size
            fig = plt.figure(figsize = figsize)
            ax = fig.add_subplot(111)
            
            if scan_strat == 'RHI':
                plt.subplots_adjust(left=0.05, right=.99, top=0.95, bottom=0.2)
            else:
                plt.subplots_adjust(left=0.1, right=.9, top=0.97, bottom=0.1)
            ax.set_facecolor('#CCCCCC') #Controls background color within the radar data display. Can be any Hex color code. Normal value: #CCCCCC (light gray)
                
            try:
#               Set up metadata text to be placed in figure (Currently implemented only for CHILL and KASPR)
                if radar_type=='CHILL':
                    y_text = filename[3:7]
                    m_text = filename[7:9]
                    d_text = filename[9:11]
                    h_text = filename[12:14]
                    min_text = filename[14:16]
                    s_text = filename[16:18]
                elif radar_type=='KASPR':
                    y_text = filename[17:21]
                    m_text = filename[21:23]
                    d_text = filename[23:25]
                    h_text = filename[26:28]
                    min_text = filename[28:30]
                    s_text = filename[30:32]
                elif radar_type=='NEXRAD':
                    y_text = filename[4:8]
                    m_text = filename[8:10]
                    d_text = filename[10:12]
                    h_text = filename[13:15]
                    min_text = filename[15:17]
                    s_text = filename[17:19]
                utc_text = ' UTC'
                spacer = ' '
                colon = ':'
                long_spacer = '     '
                time_text = y_text+spacer+m_text+spacer+d_text+long_spacer+h_text+colon+min_text+colon+s_text+utc_text #YYYY MM DD      HH:MM:SS UTC
                if scan_strat == 'RHI':
                    ang_text = 'azimuth = '
                    a_text = str(round(azi,1)) #Round azimuth to 1 decimal place for title text
                else:
                    ang_text = 'elevation = '
                    a_text = str(round(radar.fixed_angle['data'][sweepnum],2)) #Round tilt angle to 2 decimal places for title text

                degree_sym = u'\N{DEGREE SIGN}'
                angle_text = ang_text+a_text+degree_sym
                if (scan_strat=='Sector') or (scan_strat=='sector'):
                    sect_text = 'Sector PPI'
                    total_text = time_text+long_spacer+angle_text+long_spacer+sect_text
                else:
                    total_text = time_text+long_spacer+angle_text+long_spacer+scan_strat
                
                #caption_dict controls the text characteristics for all meta text on the figure
                #Common colors:
                #   UNCW teal: '#105456'
                caption_dict = {'fontname':'Open Sans',
                                'color': '#105456',
                                'size': 24,
                                'weight': 'bold'}
                metadisp = True #Logical to display metatext in figure
                    
                if scan_strat == 'RHI':
                    display.plot_rhi(field,sweepnum,vmin=vmin,vmax=vmax,title_flag=title_flag,cmap=cmap,axislabels=(axis, 'AGL (km)'),colorbar_flag=True,colorbar_label=colorbar_label)
                    display.set_limits(ylim=y_lim)
                    display.set_limits(xlim=x_lim)
                    display.set_aspect_ratio(aspect_ratio=1) #important!!
                    plt.yticks(np.arange(0,y_lim[1]+1,step=1))
                    if metadisp:
                        labeled = 'labeled_'                        
                        #plt.figtext(0.38,0.88,total_text,caption_dict) #Title the figure with the metatext 20180210
                        plt.figtext(0.38,0.915,total_text,caption_dict) #Title the figure with the metatext most
                        
                else:
                        display.plot_ppi(field, sweepnum, vmin = vmin, vmax = vmax, title_flag = title_flag, cmap = cmap, axislabels = (axis, "N-S distance (km)"),colorbar_flag=True, colorbar_label = colorbar_label)
                        
                        #Sector scan PARTIALLY IMPLEMENTED
                        if scan_strat == 'Sector':
                            #The edges of the sector are calculated using trigonometry
                            azi_lim = np.asarray([min(radar.azimuth['data']),max(radar.azimuth['data'])])
                            sec_angle = np.subtract([90,90],azi_lim)
                            range_lims = np.asarray([max(x_lim),max(y_lim)])
                            sec_rad = np.radians(sec_angle)
                            trig_sec = np.array([math.cos(sec_rad[0]),math.tan(sec_rad[1])])
                            offset = np.multiply(range_lims,trig_sec)
                            
                            #The sector edges are plotted as lines
                            #By default, the lines are solid and use the #105456 UNCW teal color
                            plt.plot([0,offset[0]],[0,range_lims[1]],color='#105456',linewidth=7)
                            plt.plot([0,range_lims[0]],[0,offset[1]],color='#105456',linewidth=7)
                            
                            #The sector edges are then used to create a domain of consistent size that moves with the sector.
                            #This is currently NOT fully adaptive--it assumes the range is 75km, and only works for certain sectors.
                            if (offset[0]<0) and (60+offset[1]-3>-60):
                                x_lim = [offset[1]-3,60+offset[1]-3]
                            else:
                                x_lim = [0,60]
                            
                            if (offset[1]<0) and (60+offset[1]-3>-60):
                                y_lim = [offset[1]-3,60+offset[1]-3]#[offset[1]-3,75-offset[1]-3]
                            else:
                                y_lim = [0,60]
                            
                            display.set_limits(ylim=y_lim)
                            display.set_limits(xlim=x_lim)
                            display.set_aspect_ratio(aspect_ratio=1)
                            #---SECTOR SCAN SETTINGS END HERE---

                        #This plots the line(s) of constant azimuth for paired PPI/RHI scan strategies
                        #For now, this is calculated manually. Many commonly-used values are below. Be careful: the trigonometry that 
                        #goes into these assumes the radar's range is 60km.
                        #plt.plot([0,22.29],[0,-30],color='#105456',linewidth=7)
                        #plt.plot([0,-89.12],[0,12.53],color='#105456',linewidth=5) #azi = 278
                        #plt.plot([0,-81.57],[0,-38.04],color='#105456',linewidth=5) #azi = 245
                        #plt.plot([0,12.53],[0,-89.12],color='#105456',linewidth=5) #azi = 173
                        
                        #plt.plot([0,-15.6],[0,-88.6],color='#105456',linewidth=5) #azi = 187.5
                        #plt.plot([0,-84.42],[0,31.2],color='#105456',linewidth=5) #azi = 280
                        
                        #plt.plot([0,81.6],[0,38.0],color='#105456',linewidth=5) #azi = 25
                        #plt.plot([0,-83.1],[0,34.4],color='#105456',linewidth=5) #azi = 292.5
                        
                        #plt.plot([0,-70.9],[0,24.4],color='#105456',linewidth=5) #azi = 289
                        #plt.plot([0,24.4],[0,70.9],color='#105456',linewidth=5) #azi = 19
                        #plt.plot([0,68.5],[0,30.5],color='#105456',linewidth=5) #azi = 24
                        #plt.plot([0,87.7],[0,-20.2],color='#105456',linewidth=5) #azi = 103
                        #plt.plot([0,64.7],[0,-62.5],color='#105456',linewidth=5) #azi = 134
                        #plt.plot([0,13.02],[0,-73.86],color='#105456',linewidth=5) #azi = 170
                        
                        #plt.plot([0,-64.95],[0,37.5],color='#105456',linewidth=5) #azi = 300 NOTE also same as azi=299 to two decimals
                        #plt.plot([0,-68],[0,31.7],color='#105456',linewidth=5) #azi = 295 NOTE also used as azi=294
                        #plt.plot([0,-25.65],[0,-70.48],color='#105456',linewidth=5) #azi = 200
                        #plt.plot([0,48.2],[0,-57.45],color='#105456',linewidth=5) #azi = 145
                        #plt.plot([0,64.95],[0,-37.5],color='#105456',linewidth=5) #azi = 120
                        
                        #plt.plot([0,-6.53],[0,-74.71],color='#105456',linewidth=5) #azi = 185
                        #plt.plot([0,-74.82],[0,5.23],color='#105456',linewidth=5) #azi = 274
                        
                        #plt.plot([0,-70],[0,0],color='#105456',linewidth=5) #azi=270 NOTE also used for azi = 271
                        #plt.plot([0,29.3],[0,-69],color='#105456',linewidth=5) #azi=157
                        #plt.plot([0,-65],[0,-37],color='#105456',linewidth=5) #azi=240 NOTE also used for azi = 243 and azi = 242 and azi = 239

                        display.set_limits(ylim=y_lim)
                        display.set_limits(xlim=x_lim)
                        display.set_aspect_ratio(aspect_ratio=1)
                        
                        if metadisp:
                            labeled = 'labeled_'
                            plt.figtext(0.17,0.905,total_text,caption_dict) #Title the figure with the metatext
                            
            except ValueError:
                print("Error in sweep!") #Prevents the plotter from failing silently on a large number of files
                continue
            
            #Control figure text: axis labels, axis tick labels, colorbar tick labels, and colorbar label
            for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels() + fig.axes[1].get_yticklabels() + [fig.axes[1].yaxis.label]):
                item.set_fontsize(30)
            #No colorbar version
#            for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
#                item.set_fontsize(26)
#            for item in ([ax.xaxis.label]):
#                item.set_fontsize(0)
 
            if scan_strat == 'RHI':
                if metadisp==True:
                    save_name = "%s%s%s.azi%d.%s.%d.png" %(outpath, labeled, filename, azi, field, sweepnum)
                else:
                    save_name = "%s%s.azi%d.%s.%d.png" %(outpath, filename, azi, field, sweepnum)
            else:
                ang = 'ang'
                a_save = ang+a_text
                if metadisp:
                    save_name = "%s%s%s.%s.%d.%s.png" %(outpath, labeled, filename, field, sweepnum, a_save)
                else:
                    save_name = "%s%s.%s.%d.%s.png" %(outpath, filename, field, sweepnum, a_save)
    
#            try:
#                save_name = gen_fun.get_savename(filename, sweepnum, outpath, scan_strat, field, azi, dealias_bool) #Legacy from original ROSE
#                if radar_type=='KASPR':
#                    raise ValueError #get_savename only works for 
#            except:
#                #print("Name is not ROSE or WSR88D compatible. Using generic save name.")
#                if scan_strat == 'RHI':
#                    if metadisp==True:
#                        save_name = "%s%s%s.azi%d.%s.%d.png" %(outpath, labeled, filename, azi, field, sweepnum)
#                    else:
#                        save_name = "%s%s.azi%d.%s.%d.png" %(outpath, filename, azi, field, sweepnum)
#                else:
#                    ang = 'ang'
#                    a_save = ang+a_text
#                    if metadisp:
#                        save_name = "%s%s%s.%s.%d.%s.png" %(outpath, labeled, filename, field, sweepnum, a_save)
#                    else:
#                        save_name = "%s%s.%s.%d.%s.png" %(outpath, filename, field, sweepnum, a_save)
                
            plt.close('all')
            fig.tight_layout()
            fig.savefig(save_name)
            del display
            gc.collect()
            
        print ("%s %d" % ('Sweep number', sweepnum))
        del azi
        del fig
        
        gc.collect()
        
def plot_contour_overlay(base_field, contour_field, radar, filename, outpath, scan_strat, ranges, cmaps, 
         colorbar_labels, figsize, dealias_bool, x_lim, y_lim, axis=None,
         title_flag=False,colorbar_flag = True):
    """
    DESCIPTION: Plots polar RHI and PPI data from netCDF on a cartesian grid.
    Overlays contours of another data type onto said RHI or PPI data.
    
    INPUTS: OUTDATED
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
        plot each field respectively. Ex. [LCH, "RdBu_r"]
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
            azi = [] #Azimuth only matters for RHI scans

        try:
            cmap = cmaps
        except IndexError:
            raise IndexError("Check to make sure number of colormaps is correct!")
            
        try:
            colorbar_label = colorbar_labels
        except IndexError:
            raise IndexError("Check to make sure number of colorbar labels is correct!")
        vmin, vmax = ranges                       
      
        # Check to see if values are in range
        #radar = quality_control.set2range(radar,field,vmax,vmin)
            
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
        ax.set_facecolor('#CCCCCC') #Can be any Hex color code. Normal value: #CCCCCC (light gray)
            
        try:
#               Set up metadata text to be placed in figure
#               This is controlled by manual logical variables below, but will be updated to reflect the obvious improvements below:
#                   set the radar type in start_script
#                   need to make metatext for other radars besides CHILL and KASPR, especially HF-S and StormRanger
            CHILL = True
            KASPR = False
            if CHILL:
                y_text = filename[3:7]
                m_text = filename[7:9]
                d_text = filename[9:11]
                h_text = filename[12:14]
                min_text = filename[14:16]
                s_text = filename[16:18]
            elif KASPR:
                y_text = filename[17:21]
                m_text = filename[21:23]
                d_text = filename[23:25]
                h_text = filename[26:28]
                min_text = filename[28:30]
                s_text = filename[30:32]
            utc_text = ' UTC'
            spacer = ' '
            colon = ':'
            long_spacer = '     '
            time_text = y_text+spacer+m_text+spacer+d_text+long_spacer+h_text+colon+min_text+colon+s_text+utc_text #YYYY MM DD      HH:MM:SS UTC
            if scan_strat == 'RHI':
                ang_text = 'azimuth = '
                a_text = str(round(azi,1))
            else:
                ang_text = 'elevation = '
                a_text = str(round(radar.fixed_angle['data'][sweepnum],2))

            degree_sym = u'\N{DEGREE SIGN}'
            angle_text = ang_text+a_text+degree_sym
            if (scan_strat=='Sector') or (scan_strat=='sector'):
                sect_text = 'Sector PPI'
                total_text = time_text+long_spacer+angle_text+long_spacer+sect_text
            else:
                total_text = time_text+long_spacer+angle_text+long_spacer+scan_strat
            
                #caption_dict controls the text characteristics for all meta text on the figure
                #Common colors:
                #   UNCW teal: '#105456'
            caption_dict = {'fontname':'Open Sans',
                            'color': '#105456',
                            'size': 24,
                            'weight': 'bold'}
                
            metadisp = True #Logical to display metatext in figure
                    
            if scan_strat == 'RHI':
                display.plot_rhi(base_field,sweepnum,vmin=vmin,vmax=vmax,title_flag=title_flag,cmap=cmap,axislabels=(axis, 'AGL (km)'),colorbar_flag=True,colorbar_label=colorbar_label)
                    
                #total_text = contour_overlay(radar,sweepnum,contour_field,base_field,ax,total_text,[0,5,10,15,20])
                total_text = contour_overlay(radar,sweepnum,contour_field,base_field,ax,total_text,[0])
                    
                display.set_limits(ylim=y_lim)
                display.set_limits(xlim=x_lim)
                display.set_aspect_ratio(aspect_ratio=1) #important!!
                plt.yticks(np.arange(0,y_lim[1]+1,step=1))

                    
                if metadisp:
                    labeled = 'labeled_'                        
                        #plt.figtext(0.38,0.88,total_text,caption_dict) #Place the metatext in the figure 20180210
                        #plt.figtext(0.38,0.906,total_text,caption_dict) #Place the metatext in the figure most
                    plt.figtext(0.38,0.915,total_text,caption_dict) #Place the metatext in the figure 20130409
                        

                        
            else:
                display.plot_ppi(base_field, sweepnum, vmin = vmin, vmax = vmax, title_flag = title_flag, cmap = cmap, axislabels = (axis, "N-S distance (km)"),colorbar_flag=True, colorbar_label = colorbar_label)

                        #Sector scan
                if scan_strat != 'PPI':
                            #The edges of the sector are calculated using trigonometry
                    azi_lim = np.asarray([min(radar.azimuth['data']),max(radar.azimuth['data'])])
                    sec_angle = np.subtract([90,90],azi_lim)
                    range_lims = np.asarray([max(x_lim),max(y_lim)])
                    sec_rad = np.radians(sec_angle)
                    trig_sec = np.array([math.cos(sec_rad[0]),math.tan(sec_rad[1])])
                    offset = np.multiply(range_lims,trig_sec)
                            
                            #The sector edges are plotted as lines
                            #By default, the lines are solid and use the #105456 UNCW teal color
                    plt.plot([0,offset[0]],[0,range_lims[1]],color='#105456',linewidth=7)
                    plt.plot([0,range_lims[0]],[0,offset[1]],color='#105456',linewidth=7)
                            
                            #The sector edges are then used to create a domain of consistent size that moves with the sector.
                            #This is currently NOT fully adaptive--it assumes the range is 75km, as at CSU-CHILL, and only works 
                            #for certain sectors.
                    if (offset[0]<0) and (75+offset[1]-3>-75):
                        x_lim = [offset[1]-3,75+offset[1]-3]
                    else:
                        x_lim = [0,75]
                            
                    if (offset[1]<0) and (75+offset[1]-3>-75):
                        y_lim = [offset[1]-3,75+offset[1]-3]#[offset[1]-3,75-offset[1]-3]
                    else:
                        y_lim = [0,75]
                            
                    display.set_limits(ylim=y_lim)
                    display.set_limits(xlim=x_lim)
                    display.set_aspect_ratio(aspect_ratio=1)
                            #---SECTOR SCAN SETTINGS END HERE---

                        #This plots the line(s) of constant azimuth for paired PPI/RHI scan strategies
                        #   For now, this is calculated manually.
                        #plt.plot([0,22.29],[0,-30],color='#105456',linewidth=7)
                        #plt.plot([0,-89.12],[0,12.53],color='#105456',linewidth=5) #azi = 278
                        #plt.plot([0,-81.57],[0,-38.04],color='#105456',linewidth=5) #azi = 245
                        #plt.plot([0,12.53],[0,-89.12],color='#105456',linewidth=5) #azi = 173
                        
                        #plt.plot([0,-15.6],[0,-88.6],color='#105456',linewidth=5) #azi = 187.5
                        #plt.plot([0,-84.42],[0,31.2],color='#105456',linewidth=5) #azi = 280
                        
                        #plt.plot([0,81.6],[0,38.0],color='#105456',linewidth=5) #azi = 25
                        #plt.plot([0,-83.1],[0,34.4],color='#105456',linewidth=5) #azi = 292.5
                        
                        #plt.plot([0,-70.9],[0,24.4],color='#105456',linewidth=5) #azi = 289
                        #plt.plot([0,24.4],[0,70.9],color='#105456',linewidth=5) #azi = 19
                        #plt.plot([0,68.5],[0,30.5],color='#105456',linewidth=5) #azi = 24
                        #plt.plot([0,87.7],[0,-20.2],color='#105456',linewidth=5) #azi = 103
                        #plt.plot([0,64.7],[0,-62.5],color='#105456',linewidth=5) #azi = 134
                        #plt.plot([0,13.02],[0,-73.86],color='#105456',linewidth=5) #azi = 170
                        
                        #plt.plot([0,-64.95],[0,37.5],color='#105456',linewidth=5) #azi = 300 NOTE also same as azi=299 to two decimals
                        #plt.plot([0,-68],[0,31.7],color='#105456',linewidth=5) #azi = 295 NOTE also used as azi=294
                        #plt.plot([0,-25.65],[0,-70.48],color='#105456',linewidth=5) #azi = 200
                        #plt.plot([0,48.2],[0,-57.45],color='#105456',linewidth=5) #azi = 145
                        #plt.plot([0,64.95],[0,-37.5],color='#105456',linewidth=5) #azi = 120
                        
                        #plt.plot([0,-6.53],[0,-74.71],color='#105456',linewidth=5) #azi = 185
                        #plt.plot([0,-74.82],[0,5.23],color='#105456',linewidth=5) #azi = 274
                        
                plt.plot([0,-70],[0,0],color='#105456',linewidth=5) #azi=270 NOTE also used for azi = 271
                plt.plot([0,29.3],[0,-69],color='#105456',linewidth=5) #azi=157
                plt.plot([0,-65],[0,-37],color='#105456',linewidth=5) #azi=240 NOTE also used for azi = 243 and azi = 242 and azi = 239
                        

                display.set_limits(ylim=y_lim)
                display.set_limits(xlim=x_lim)
                display.set_aspect_ratio(aspect_ratio=1)
                        
                if metadisp:
                    labeled = 'labeled_'
                    plt.figtext(0.17,0.905,total_text,caption_dict) #Place the metatext in the figure
                            
        except ValueError:
            print("Error in sweep!") #Prevents the plotter from failing silently on a large number of files
            continue
            
            #Control figure text: axis labels, axis tick labels, colorbar tick labels, and colorbar label
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels() + fig.axes[1].get_yticklabels() + [fig.axes[1].yaxis.label]):
            item.set_fontsize(30)
            #No colorbar version
#            for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
#                item.set_fontsize(26)
#            for item in ([ax.xaxis.label]):
#                item.set_fontsize(0)
            
  
        #try:
          #  if KASPR==True:
         #       print("not yet")
                #    raise ValueError #This is some dark magick but it's Hallowe'en so thematic I guess??
                #save_name = gen_fun.get_savename(filename, sweepnum, outpath, scan_strat, field, azi, dealias_bool)
        #except:
            #print "Name is not ROSE or WSR88D compatible. Using generic save name."
        if scan_strat == 'RHI':
            if metadisp:
                save_name = "%s%s%s.azi%d.%s.contour%s.%d.png" %(outpath, labeled, filename, azi, base_field, contour_field, sweepnum)
            else:
                save_name = "%s%s.azi%d.%s.contour%s.%d.png" %(outpath, filename, azi, base_field, contour_field, sweepnum)
        else:
            print("not yet")
                    #ang = 'ang'
                    #a_save = ang+a_text
                    #if metadisp:
                        #save_name = "%s%s%s.%s.%d.%s.png" %(outpath, labeled, filename, field, sweepnum, a_save)
                    #else:
                     #   save_name = "%s%s.%s.%d.%s.png" %(outpath, filename, field, sweepnum, a_save)
                
        plt.close('all')
        fig.tight_layout()
        fig.savefig(save_name)
        
        del display
            #del contourField
        gc.collect()
            
    print ("%s %d" % ('Sweep number', sweepnum))
    del azi
    del fig
        
        
    gc.collect()
    
