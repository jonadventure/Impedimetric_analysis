#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 12:34:00 2020

@author: jonasvishart
"""

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
x_values = 2 #Check EIS excel file,
                     #if frequency values in 2nd column, 
                     #then x_values = 2
y_values = 5  #Check EIS excel file,
                  #if y values in fifth column, 
                  #then y_values = 5
                
x_lim_plot = [] # if empty [ ] => no limit on plot x-axis is set! Otherwise, e.g [0,200]
y_lim_plot = [] # if empty [ ] => no limit on plot y-axis is set! Otherwise, e.g [0,200]

x_label = "Frequency / Hz"
y_label = "Phase / °"

title = "Bode Diagram"


save_title = 'Bodeplot_Phase-'

font_size = 14 #font size for labels

#_________________________________________
#_________________________________________
# IMPORT DATA
#_________________________________________
try:
    #Load data
    use_cols = [x_values-1, y_values-1] #define which columns to extract from data
    message = "Select your EIS file(s)"
    #Load data with column names
    Loaded_data, filename, name = Load_data(message,use_cols,header=0,skiprows=values_row_start-2, sep=";")
    #Only use data in selected x_limit
    for j in range(0,len(filename)):
        if len(x_lim_plot) == 2: 
            Loaded_data[j] = Loaded_data[j].sort_values(by=Loaded_data[j].columns[0])
            Loaded_data[j] = Loaded_data[j][Loaded_data[j].iloc[:,0]>x_lim_plot[0]]
            Loaded_data[j] = Loaded_data[j][Loaded_data[j].iloc[:,0]<x_lim_plot[1]]
    
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
        plt.plot(Loaded_data[i].iloc[:,0], Loaded_data[i].iloc[:,1], label='%s' % filename[i] )
    plt.rcParams["font.family"] = "georgia"
    #Display ticks as scientific if they are rounded to 0
    if round(max(Loaded_data[i].iloc[:,0])) == 0:
        ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
    if round(max(Loaded_data[i].iloc[:,1])) == 0:
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
    
    # Make legend to the right of the plot
    ax.set_xscale('log')
    #ax.set_yscale('log')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #ax3.legend(loc='lower right')    
    plt.xlabel(str(x_label),fontsize=font_size)
    plt.ylabel(str(y_label),fontsize=font_size)
    plt.title(title,fontsize=font_size)
    ax.yaxis.set_label_position("left")
    
    #Set limits on x- and y-range
    if len(x_lim_plot) == 2: 
        plt.xlim((x_lim_plot[0], x_lim_plot[1]))
    if len(y_lim_plot) == 2:
        plt.ylim((y_lim_plot[0], y_lim_plot[1]))
    
    #Save plot
    plt.savefig(os.path.join(savingFolder, str(save_title) + filename[0] + '.pdf'),bbox_inches='tight')
    plt.show()
        
except:
    sys.exit("Error in loading data. Please check you have selected an EIS excel/csv file and written the correct columns to be included.")
