# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 15:06:14 2014

@author: thecakeisalie

make_colormap by StackOverflow user unutbu

"""

import numpy as nump
import colorsys
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import colors
import sys
import seaborn

def LCH_Spiral(nc = 100, np = .4, offset = 30, reverse = 1, L_range = [100, 0], name = 'LCH'):

    """
    %LCH_SPIRAL Generates a monotonic luminance colormap with maximum color
    %saturation all based on the spherical CIE L*c*h colorsystem.
    %
    %   [mp] = LCH_Spiral( nc, np, offset );
    %
    %   nc          Number of colors (length of the colormap). Default = 64.
    %   np          Number of time to cycle through hue values. Default = 1.
    %   offset      Offset in degrees for the initial hue value
    %   reverse     If reverse == 1, the hue values will cycle backwards
    %               (R,B,G). If reverse == 0, the hue values will cycle
    %               normally (R,G,B).
    %   L_range     2 element array. Range of lightness values (i.e. [startL endL]).
    %               Acceptable range is 0 to 100 inclusive. If startL is less
    %               than endL the color table will move from dark to light.
    %               Otherwise, the opposite is true. Default = [100 0].
    %
    %   mp    Color map output in RGB
    %
    %   This function returns an n x 3 matrix containing the RGB entries
    %   used for colormaps in MATLAB figures. The colormap is designed
    %   to have a monotonically increasing luminance, while maximizing
    %   the color saturation. This is achieved by generating a line through the
    %   Lch colorspace that ranges from RBG = [0 0 0] to RGB = [1 1 1]. The
    %   luminance is based on human perception unlike the lightness value in
    %   the HSL color system or the RGB component average intensity.
    %
    %Inspired By:
    %   J. McNames, "An effective color scale for simultaneous color and
    %   gray-scale publications," IEEE Signal Processing Magazine, 2006.
    %
    %Written By: Matthew Miller, NCSU, 2010
    """
    
    #argument checking
    if np <= 0:
        print('np color period(s) must be a positive number')
        sys.exit(1)
    if offset < 0:
        print('hue offset value must be a positive degree value')
        sys.exit(1)
    if (nc <1) or (nc > 256):
        print('Please specify an integer number of colors between 1 and 256')
        sys.exit(1)
    if (reverse != 0) and (reverse != 1):
        print('reverse variable must be 0 for normal hue cycling or 1 for backwards hue cycling')
        sys.exit(1)
    if (len(L_range) != 2) and (isinstance(L_range, (int, long, float, complex)) != True):
        print('lightness range variable must be a 2 element numerical array')
        sys.exit(1)
        
    #define Lch colormap
    
    L = nump.linspace(L_range[0],L_range[1],nc)
    C = nump.sqrt(50**2-(L-50)**2)
    if reverse == 1:
        H = nump.linspace(360*np,0,nc)+offset
    else:
        H = nump.linspace(0,360*np,nc)+offset
    
    
    while sum(H>360)>0:
        H[H>360]=H[H>360]-360
    
    #convert to RGB
    mp = nump.zeros((nc,3))
    for i in range(nc):
        rgb=colorsys.hls_to_rgb(H[i]/100, L[i]/100, C[i]/100)
        mp[i,:] = rgb
    
    #last = nump.ones((nc,1))
    #mp = nump.concatenate((mp,last),1)  
    
    mp_255 = mp*255    
    hex_mp = []
    for i in range(nc):
        #p = []
        k = mp_255[i,:]
        #p.append(k[0])
        #p.append(k[1])
        #p.append(k[2])
        hexc = rgb_to_hex((int(k[0]),int(k[1]),int(k[2])))
        hex_mp.append(hexc)
    
    mymap = colors.ListedColormap(hex_mp, name = name) 
    
    #matplotlib.cm.register_cmap(name = name, cmap=mymap)
#    
#    #### Testing -------------------------------------------------------------
#    x = nump.linspace(0,1,21)
#    X,Y = nump.meshgrid(x,x)
#    Z = .5*(X+Y)
#    plt.pcolor(X,Y,Z, cmap=mymap, edgecolors='k')
#    plt.axis('equal')
#    plt.colorbar()
#    plt.title('Plot of x+y using colormap')
#    #### ---------------------------------------------------------------------
    
    return mymap, mp
    
    
def PID_Integer():
    """
    Colormap definition for PID field in ROSE data.
    """
        
    colors_hex = ['#996633','#663300','#66FF33','#009900','#336600','#CC0000','#E61616','#FF3333','#FF4D4D','#FF6666','#66FFFF','#52CCCC','#0099FF','#33CCFF','#FFC2E0','#FFFFAD','#F3E6C1','#FFD6AD','#CCCCFF']
                  
                  
    cmap_PID = colors.ListedColormap(colors_hex, name = 'PID')    
    
    
#    colors_RGB = []
#    for i in range(0, nump.size(colors_hex)):
#        color_RGB = hex_to_rgb(colors_hex[i])
#        colors_RGB.append((color_RGB/255)        
#        
#    cmap_PID = colors.ListedColormap(colors_RGB, name='PID')
    
    
#    x = nump.linspace(0,1,21)
#    X,Y = nump.meshgrid(x,x)
#    Z = .5*(X+Y)
#    plt.pcolor(X,Y,Z, cmap=cmap_PID, edgecolors='k')
#    plt.axis('equal')
#    plt.colorbar()
#    plt.title('Plot of x+y using colormap')
 
    return cmap_PID

def PID_Integer_CHILL():
    """
    Colormap definition for PID field in ROSE data.
    """
        
    #colors_hex = ['#30006A', '#440984', '#59199E', '#6F2AB4', '#853DC6', '#9B51D5', '#B066DF', '#C37DE5', '#D595E6', '#E5AEE3', '#F2C9DB', '#FFFFFF']
    colors_hex = ['#779CF6','#8079C7','#795898','#683C6C','#321023','#7C2742','#A4344C','#CC4552','#F35953']
    
    cmap_PID = colors.ListedColormap(colors_hex, name = 'PID')    
    
    
#    colors_RGB = []
#    for i in range(0, nump.size(colors_hex)):
#        color_RGB = hex_to_rgb(colors_hex[i])
#        colors_RGB.append((color_RGB/255)        
#        
#    cmap_PID = colors.ListedColormap(colors_RGB, name='PID')
    
    
#    x = nump.linspace(0,1,21)
#    X,Y = nump.meshgrid(x,x)
#    Z = .5*(X+Y)
#    plt.pcolor(X,Y,Z, cmap=cmap_PID, edgecolors='k')
#    plt.axis('equal')
#    plt.colorbar()
#    plt.title('Plot of x+y using colormap')
 
    return cmap_PID
    
def Vel1():
    
    cdict = {'red':  ((0.0, 0.0, 0.0),
                   (0.25,0.0, 0.0),
                   (0.5, 1.0, 1.0),
                   (0.75,1.0, 1.0),
                   (1.0, 0.4, 1.0)),
    
         'green': ((0.0, 0.0, 0.0),
                   (0.25,0., 0.),
                   (0.5, 0.1, 0.1),
                   (0.75,0., 0.),
                   (1.0, 0.0, 0.0)),
    
         'blue':  ((0.0, 0.0, 0.4),
                   (0.25,1.0, 1.0),
                   (0.5, 1.0, 0.8),
                   (0.75,0.0, 0.0),
                   (1.0, 0.0, 0.0))
        }
    
    vel1 = matplotlib.colors.LinearSegmentedColormap('Vel1', cdict) 
    plt.register_cmap(cmap = vel1)
    
    ## Testing
#    x = nump.linspace(0,1,21)
#    X,Y = nump.meshgrid(x,x)
#    Z = .5*(X+Y)
#    plt.pcolor(X,Y,Z, cmap='Vel1', edgecolors='k')
#    plt.axis('equal')
#    plt.colorbar()
#    plt.title('Plot of x+y using colormap')
    
    
    
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def convert_to_grey(x, vmin, vmax):
    dv = vmax-vmin
    grey = nump.floor(255*(x/dv))
    return grey


def cuckoo():
    cuckooBrownHue = 34
    cuckooGrayBlueHue= 174
    cuckooPalette = seaborn.diverging_palette(cuckooGrayBlueHue,cuckooBrownHue,center='light',as_cmap=True)
    return cuckooPalette


#def make_colormap(seq):
#    seq = [(None,) * 3, 0.0] + list(seq) + [1.0,(None,)*3]
#    cdict={'red':[],'green':[],'blue':[]}
#    for i,item in enumerate(seq):
#        if isinstance(item,float):
#            r1,g1,b1=seq[i-1]
#            r2,g2,b2=seq[i+1]
#            cdict['red'].append([item,r1,r2])
#            cdict['green'].append([item,g1,g2])
#            cdict['blue'].append([item,b1,b2])
#    return colors.LinearSegmentedColormap('CustomMap',cdict)
    
