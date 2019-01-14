# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 21:48:53 2018

@author: danielholt
"""

import colormap
import numpy as np
import pylab as pl

max_luminance = 100
min_luminance = 0
LCH = colormap.LCH_Spiral()[0]
LCH_zdr = colormap.LCH_Spiral(nc = 100, np = .3, offset = 0, reverse = 1, L_range = [max_luminance, min_luminance], name = 'LCH_zdr')[0]
LCH_wid = colormap.LCH_Spiral(nc = 100, np = .3, offset = 45, reverse = 0, L_range = [max_luminance, min_luminance], name = 'LCH_wid')[0]

#a = np.array([[-2,30]])
#pl.figure(figsize=(9,1.5))
#img = pl.imshow(a, cmap=LCH)
#pl.gca().set_visible(False)
#cax = pl.axes([0.1,0.2,0.8,0.6])
#pl.colorbar(orientation='horizontal',cax=cax)
#pl.savefig("E:\\colorbars\\reflectivity_colorbar.eps")
#
#
#b = np.array([[-1,2]])
#pl.figure(figsize=(9,1.5))
#img = pl.imshow(b, cmap=LCH_zdr)
#pl.gca().set_visible(False)
#cax = pl.axes([0.1,0.2,0.8,0.6])
#pl.colorbar(orientation='horizontal',cax=cax)
#pl.savefig("E:\\colorbars\\differential_reflectivity_colorbar.eps")
#
#
#c = np.array([[0,4]])
#pl.figure(figsize=(9,1.5))
#img = pl.imshow(c, cmap=LCH_wid)
#pl.gca().set_visible(False)
#cax = pl.axes([0.1,0.2,0.8,0.6])
#pl.colorbar(orientation='horizontal',cax=cax)
#pl.savefig("E:\\colorbars\\spectral_width_colorbar.eps")
#
#d = np.array([[-30,30]])
#pl.figure(figsize=(9,1.5))
#img = pl.imshow(d, cmap='seismic')
#pl.gca().set_visible(False)
#cax = pl.axes([0.1,0.2,0.8,0.6])
#pl.colorbar(orientation='horizontal',cax=cax)
#pl.savefig("E:\\colorbars\\velocity_colorbar.eps")

e = np.array([[-5,25]])
pl.figure(figsize=(9,1.5))
img = pl.imshow(e, cmap=LCH)
pl.gca().set_visible(False)
cax = pl.axes([0.1,0.2,0.8,0.6])
pl.colorbar(orientation='horizontal',cax=cax)
pl.savefig("H:\\colorbars\\AMS2019poster\\reflectivity_colorbar.png")

f = np.array([[-1,2]])
pl.figure(figsize=(9,1.5))
img = pl.imshow(f, cmap=LCH_zdr)
pl.gca().set_visible(False)
cax = pl.axes([0.1,0.2,0.8,0.6])
pl.colorbar(orientation='horizontal',cax=cax)
pl.savefig("H:\\colorbars\\AMS2019poster\\differential_reflectivity_colorbar.png")

g = np.array([[-20,20]])
pl.figure(figsize=(9,1.5))
img = pl.imshow(g, cmap='RdBu_r')
pl.gca().set_visible(False)
cax = pl.axes([0.1,0.2,0.8,0.6])
pl.colorbar(orientation='horizontal',cax=cax)
pl.savefig("H:\\colorbars\\AMS2019poster\\velocity_colorbar.png")

h = np.array([[0,4]])
pl.figure(figsize=(9,1.5))
img = pl.imshow(h, cmap=LCH_wid)
pl.gca().set_visible(False)
cax = pl.axes([0.1,0.2,0.8,0.6])
pl.colorbar(orientation='horizontal',cax=cax)
pl.savefig("H:\\colorbars\\AMS2019poster\\spectral_width_colorbar.png")

j = np.array([[0,1.25]])
pl.figure(figsize=(9,1.5))
img = pl.imshow(j, cmap='viridis')
pl.gca().set_visible(False)
cax = pl.axes([0.1,0.2,0.8,0.6])
pl.colorbar(orientation='horizontal',cax=cax)
pl.savefig("H:\\colorbars\\AMS2019poster\\snow_rate_colorbar.png")