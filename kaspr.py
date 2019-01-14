# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 16:30:48 2018

@author: danielholt
"""

import netCDF4
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import pyart
import matplotlib as m

inpath = 'E:\\store radar files\\KASPR\\KASPR_PP_MOMENTS_20180104-140247.rhi.nc'#'C:\\Users\\danielholt\\My Documents\\vCHILL\\pyart_processing\\test_set'

radar = pyart.io.read_cfradial(inpath)

nplots = radar.nsweeps
feide_angle = radar.fixed_angle['data']

display = pyart.graph.RadarDisplay(radar)

fig3 = plt.figure(figsize=[25,20])
ax3 = fig3.add_subplot(111)
display.plot('DBZ',0,vmin=-45,vmax=40,mask_outside=False,ax=ax3)
display.set_limits(ylim=[0,15],ax=ax3)
display.plot_grid_lines()