#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 14:25:31 2020

@author: jonasvishart
"""

#_________________________________________
# IMPORT PACKAGES
#_________________________________________
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from basics import getFilepath, Load_data

#_________________________________________
#_________________________________________
# VARIABLES
#_________________________________________

values_row_start = 2 #Check EIS/ECS excel file,
                     #if values start from 2nd row
                     #then values_row_start = 2
frequency_column = 2 #Check EIS excel file,
                     #if frequency values in 2nd column, 
                     #then frequency_column = 2
phase_column = 6

Z_column = 5 #Check EIS excel file,
             #if Z values in fifth column, 
             #then Z_column = 5
phase_unit = "°"
magnitude_unit = "Ω"
font_size = 14 #font size for labels

#_________________________________________
#_________________________________________
# IMPORT DATA
#_________________________________________
try:
    #Load data
    use_cols = [frequency_column-1, phase_column-1, Z_column-1] #define which columns to extract from data
    message = "Select your EIS file(s)"
    #Load data with column names
    Loaded_data, filename, name = Load_data(message,use_cols,header=0,skiprows=values_row_start-2, sep=";")
    
    #Choose where to save ECS data file
    savingFolder = str(getFilepath("Choose saving folder"))
    
    #_________________________________________
    #_________________________________________
    # Bode plot of PHASE
    #_________________________________________
    # All are assumed measured in SI-units
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)  
    for i in range (0,len(filename)):
        frequency = Loaded_data[i].iloc[:,0]
        omega = 2*np.pi*frequency #define omega as w=2*pi*f
        plt.plot(frequency, Loaded_data[i].iloc[:,2], label='%s' % filename[i] )
    plt.rcParams["font.family"] = "georgia"
    #Display ticks as scientific if they are rounded to 0
    if round(max(Loaded_data[i].iloc[:,0])) == 0:
        ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
    if round(max(Loaded_data[i].iloc[:,2])) == 0:
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
    
    # Make legend to the right of the plot
    ax.set_xscale('log')
    #ax.set_yscale('log')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #ax3.legend(loc='lower right')    
    plt.ylabel(str("Phase / ")+str(phase_unit),fontsize=font_size)
    plt.xlabel(str("Frequency / Hz"),fontsize=font_size)
    plt.title("Bode Diagram",fontsize=font_size)
    ax.yaxis.set_label_position("left")
    
    #Save plot
    plt.savefig(os.path.join(savingFolder, 'Bodeplot_Phase-' + filename[0] + '.pdf'),bbox_inches='tight')
    plt.show()
    
    #_________________________________________
    #_________________________________________
    # Bode plot of MAGNITUDE
    #_________________________________________
    # All are assumed measured in SI-units
    fig = plt.figure()
    ax2 = fig.add_subplot(1,1,1)  
    for i in range (0,len(filename)):
        frequency = Loaded_data[i].iloc[:,0]
        omega = 2*np.pi*frequency #define omega as w=2*pi*f
        plt.plot(frequency, Loaded_data[i].iloc[:,1], label='%s' % filename[i] )
    # Make legend to the right of the plot
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    box = ax2.get_position()
    ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #ax3.legend(loc='lower right')    
    plt.ylabel(str("Magnitude / ")+str(magnitude_unit),fontsize=font_size)
    plt.xlabel(str("Frequency / Hz"),fontsize=font_size)
    plt.title("Bode Diagram",fontsize=font_size)
    ax2.yaxis.set_label_position("left")
    
    #Save plot
    plt.savefig(os.path.join(savingFolder, 'Bodeplot_Mag-' + filename[0] + '.pdf'),bbox_inches='tight')
    plt.show()
except:
    sys.exit("Error in loading data. Please check you have selected an EIS excel/csv file and written the correct columns to be included.")
