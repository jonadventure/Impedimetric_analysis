#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 07:15:49 2020

@author: jonasvishart
"""

#_________________________________________
# IMPORT PACKAGES
#_________________________________________
import os
import sys
import pylab as p
import numpy as np
from basics import Load_data, Table, getFilepath
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.pyplot import *
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

#_________________________________________
#_________________________________________
# VARIABLES
#_________________________________________
values_row_start = 3 #Check EIS/ECS excel file,
                     #if values start from 3rd row
                     #then values_row_start = 3
scan_column = 5 #Check CV excel file, 
                #if scan column don't exist then scan_column = 0. 
                #If it is in first column, then scan_column = 1
Scan_number = 1 #only if scan_column exist
                #value is out of influence, if scan_column doesn't exist

potential_column = 1 #Check CV excel file, 
                   #if potential values in first column, then potential_column = 1
current_column = 3 #Check CV excel file, 
                   #if current values in second column, then current_column = 2
potential_unit = "V"
current_unit = "A"

num_decimals = 3 #number of decimals to round numbers
font_size = 14 #font size for labels
LinReg_start_index = 15 #how many indexes away from start and end point before regression is made
R2_accept_value = 0.90 #limit for how good linear reression must be


#_________________________________________
#_________________________________________
# DEFINE FUNCTIONS
#_________________________________________

def Peak_finder(Data, LinReg_start_index, R2_accept_value, Scan_number): 
    #Find index of upper and lower peak
    upperPeak_index = Data.iloc[:,1].idxmax()
    lowerPeak_index = Data.iloc[:,1].idxmin()

    x_upperPeak = Data.iloc[upperPeak_index,0] #x_value of peak
    y_upperPeak = Data.iloc[upperPeak_index,1] #y_value of peak
    x_lowerPeak = Data.iloc[lowerPeak_index,0]
    y_lowerPeak = Data.iloc[lowerPeak_index,1]
    
    #Find index of min and max potential
    min_potential = Data.iloc[:,0].idxmin()
    max_potential = Data.iloc[:,0].idxmax()
    final_index = Data.iloc[:,0].shape[0] #total nr. of indexes
    
    #If upperPeak is not found, then regression baseline is made on 100 indexes from max potential
    if upperPeak_index == max_potential:
        x_lin1 = np.array(Data.iloc[max_potential+LinReg_start_index:max_potential+100,0]).reshape(-1,1)
        y_lin1 = np.array(Data.iloc[max_potential+LinReg_start_index:max_potential+100,1]).reshape(-1,1)    
        fit1 = LinearRegression() 
        fit1.fit(x_lin1, y_lin1)
        y_pred1 = fit1.intercept_ + fit1.coef_[0]*Data.iloc[:,0]
    #Otherwise, best linear regression is found in the interval from peak to max potential
    #For each time the R2 value is below 0.90, then 5 indexes will be removed in the interval for regression
    else:    
        step_1 = np.arange(0,2*max_potential-upperPeak_index,5)
        step_1 = step_1[::-1]
        
        #define x- and y-data for linear regression
        for i in step_1:
            x_lin1 = np.array(Data.iloc[max_potential+LinReg_start_index:i,0]).reshape(-1,1)
            y_lin1 = np.array(Data.iloc[max_potential+LinReg_start_index:i,1]).reshape(-1,1)    
            fit1 = LinearRegression() 
            fit1.fit(x_lin1, y_lin1) #make linear fit
            y_pred1 = fit1.intercept_ + fit1.coef_[0]*Data.iloc[:,0] #define linear function on form y=b+ax
            R2_1_score = r2_score(y_lin1.reshape(1,-1)[0],y_pred1[max_potential+LinReg_start_index:i].to_numpy()) #R^2 value
            if R2_1_score > R2_accept_value: #R^2 must be greater than R2_accept_value
                break
    
    #If lowerPeak is not found, then regression baseline is made on 100 indexes from min potential
    if lowerPeak_index == min_potential:
        x_lin2 = np.array(Data.iloc[min_potential+LinReg_start_index:min_potential+100,0]).reshape(-1,1)
        y_lin2 = np.array(Data.iloc[min_potential+LinReg_start_index:min_potential+100,1]).reshape(-1,1)
        fit2 = LinearRegression() 
        fit2.fit(x_lin2, y_lin2)
        y_pred2 = fit2.intercept_ + fit2.coef_[0]*Data.iloc[:,0]
    #Otherwise, best linear regression is found in the interval from peak to min potential
    #For each time the R2 value is below 0.90, then 5 indexes will be removed in the interval for regression
    else:
        step_2 = np.arange(0,min_potential+final_index-lowerPeak_index,5)
        step_2 = step_2[::-1]
        for i in step_2:    
            x_lin2 = np.array(Data.iloc[min_potential+LinReg_start_index:i,0]).reshape(-1,1)
            y_lin2 = np.array(Data.iloc[min_potential+LinReg_start_index:i,1]).reshape(-1,1)
            fit2 = LinearRegression() 
            fit2.fit(x_lin2, y_lin2)
            y_pred2 = fit2.intercept_ + fit2.coef_[0]*Data.iloc[:,0]
            R2_2_score = r2_score(y_lin2.reshape(1,-1)[0],y_pred2[min_potential+LinReg_start_index:i].to_numpy())
            if R2_2_score > R2_accept_value:
                break
    #Define the regression baselines
    y_upperPeak_baseline = y_pred1[upperPeak_index]
    y_lowerPeak_baseline = y_pred2[lowerPeak_index]
    
    return y_pred1, y_pred2, x_upperPeak, y_upperPeak, x_lowerPeak, y_lowerPeak, y_upperPeak_baseline, y_lowerPeak_baseline
    
    
def CV_plot(filename, Data, number_decimals, y_pred1, y_pred2, x_upperPeak, y_upperPeak, x_lowerPeak, y_lowerPeak, y_upperPeak_baseline, y_lowerPeak_baseline):
    num_dec = '.'+'%s'% +num_decimals+'g'
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    #Plot baselines
    plt.plot(Data.iloc[:,0], y_pred1, color = "green")
    plt.plot(Data.iloc[:,0], y_pred2, color = "grey")
    
    #Draw arrows to indicate upper- and lower peak
    p.arrow( x_upperPeak, y_upperPeak, 0.0, y_upperPeak_baseline-y_upperPeak, fc="green", ec="green",head_width=0.001*y_upperPeak_baseline, head_length=0.001*y_upperPeak_baseline)
    p.arrow( x_lowerPeak, y_lowerPeak, 0.0, y_lowerPeak_baseline-y_lowerPeak, fc="grey", ec="grey",head_width=0.001*y_lowerPeak_baseline, head_length=0.001*y_lowerPeak_baseline)
    #Make the CV plot
    plt.plot(Data.iloc[:,0], Data.iloc[:,1], label='%s' % filename + '   Scan: ' + str(Scan_number))
    plt.rcParams["font.family"] = "georgia"
    #Add legend
    plt.legend(loc = 'lower right')
    #Add labels
    plt.xlabel(str("Potential applied / ")+str(potential_unit),fontsize=font_size)
    plt.ylabel(str("WE Current / ")+str(current_unit),fontsize=font_size)
    plt.title("Cyclic voltammetry, IUPAC conv. \n Oxidation peak: "+"E_pa="+ str(format(x_upperPeak,num_dec))+str(potential_unit)+",  i_pa="+
              str(format(y_upperPeak-y_upperPeak_baseline,num_dec))+str(current_unit)+"\n" + "Reduction peak: "+"E_pc="+ 
              str(format(x_lowerPeak,num_dec))+str(potential_unit)+",  i_pc="+str(format(y_lowerPeak-y_lowerPeak_baseline,num_dec))+str(current_unit),fontsize=font_size)
    ax1.yaxis.set_label_position("left")
    print(str("File: "),filename)
    print("|\u0394E|=", str(format(np.abs(x_upperPeak-x_lowerPeak),num_dec)),str(potential_unit)) #Find potential difference
    print("Oxidation peak: E_pa=", str(format(x_upperPeak,num_dec)),str(potential_unit)+",  i_pa=",str(format(y_upperPeak-y_upperPeak_baseline,num_dec)),str(current_unit))
    print("Reduction peak: E_pc=", str(format(x_lowerPeak,num_dec)),str(potential_unit)+",  i_pc=",str(format(y_lowerPeak-y_lowerPeak_baseline,num_dec)),str(current_unit))
    return ax1

#_________________________________________
#_________________________________________
# CV analysis
#_________________________________________
try:
    #Load data
    if scan_column > 0: #check whether scan_column is defined or not
        use_cols = [potential_column-1,current_column-1, scan_column-1] #columns to extract from imported data               
    else:
        use_cols = [potential_column-1,current_column-1] #columns to extract from imported data 
    message = "Select your CV file(s)"
    Loaded_data, filename, name = Load_data(message, use_cols,header=None, skiprows=values_row_start-1)
    
    #Choose where to save plots
    savingFolder = str(getFilepath("Choose saving folder"))
    
    E_pa = []
    E_pc = []
    E_dif = []
    i_pa = []
    i_pc = []
    
    try:
        for j in range(0,len(filename)):   
            num_dec = '.'+'%s'% +num_decimals+'g'
            #Define only data by selected scan
            if scan_column > 0:
                Scan_select = Loaded_data[j][Loaded_data[j].iloc[:,2] == Scan_number] 
            else: 
                Scan_select = Loaded_data[j]
            Scan_select = Scan_select.reset_index(drop=True)
            
            #Find the peaks
            y_pred1, y_pred2, x_upperPeak, y_upperPeak, x_lowerPeak, y_lowerPeak, y_upperPeak_baseline, y_lowerPeak_baseline = Peak_finder(Scan_select, LinReg_start_index, R2_accept_value, Scan_number)
    
            E_pa.append(float(format(x_upperPeak,num_dec)))
            E_pc.append(float(format(x_lowerPeak,num_dec)))
            E_dif.append(float(format(np.abs(x_upperPeak-x_lowerPeak),num_dec)))
            i_pa.append(float(format(y_upperPeak-y_upperPeak_baseline,num_dec)))
            i_pc.append(float(format(y_lowerPeak-y_lowerPeak_baseline,num_dec)))
            
            #Make a plot of the baselines and found peaks
            ax = CV_plot(filename[j], Scan_select, num_decimals, y_pred1, y_pred2, x_upperPeak, y_upperPeak, x_lowerPeak, y_lowerPeak, y_upperPeak_baseline, y_lowerPeak_baseline)
            #Display ticks as scientific if they are rounded to 0
            if round(max(Loaded_data[j].iloc[:,0])) == 0: 
                ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
            if round(max(Loaded_data[j].iloc[:,1])) == 0:
                ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
            plt.savefig(os.path.join(savingFolder, 'CV_with_baselines-' + str(filename[j]) + '.pdf'),bbox_inches='tight')
            plt.show()
            
        #_________________________________________
        #_________________________________________
        # OVERVIEW TABLE
        #_________________________________________

        #Table of characteristic values
        #Define column labels
        columns = ["E_pa / "+str(potential_unit), "E_pc / "+str(potential_unit),"|\u0394E| / "+str(potential_unit), 
                   "i_pa / "+str(current_unit), "i_pc / "+str(current_unit)]
        #Define row labels
        rows = []
        for i in filename:
            rows.append(str(i))
        #Make value matrix
        value_matrix = np.array(([E_pa,E_pc,E_dif,i_pa,i_pc])).T
           
        #Table - Main table
        print(str("Overview of imported data:"))
        table = Table(value_matrix,rows,columns,2,2,figsize=len(columns))
        plt.tight_layout()
        #Save plot
        plt.savefig(os.path.join(savingFolder, 'CV_Table-' + filename[0] + '.pdf'),bbox_inches='tight')
        plt.show()
    except:
        pass
    
    #Make a plot of all selected files, so redo same procedure as CV analysis step
    print("All in one plot: ")
    fig = plt.figure()
    ax3 = fig.add_subplot(1,1,1)
    for j in range(0,len(filename)):    
        #Define only data by selected scan
        if scan_column > 0:
            Scan_select = Loaded_data[j][Loaded_data[j].iloc[:,2] == Scan_number]
            legend_label = '%s' % filename[j] + '   Scan: ' + str(Scan_number)
        else: 
            Scan_select = Loaded_data[j]
            legend_label = '%s' % filename[j] 
        Scan_select = Scan_select.reset_index(drop=True)
        plt.plot(Scan_select.iloc[:,0], Scan_select.iloc[:,1], label=legend_label)
        plt.rcParams["font.family"] = "georgia"
        #Display ticks as scientific if they are rounded to 0
        if round(max(Loaded_data[j].iloc[:,0])) == 0:
            ax3.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
        if round(max(Loaded_data[j].iloc[:,1])) == 0:
            ax3.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
        
    # Make legend to the right of the plot
    box = ax.get_position()
    ax3.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax3.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #ax3.legend(loc='lower right')    
    plt.xlabel(str("Potential applied / ")+str(potential_unit),fontsize=font_size)
    plt.ylabel(str("WE current / ")+str(current_unit),fontsize=font_size)
    plt.title("Cyclic voltammetry, IUPAC conv.",fontsize=font_size)
    ax3.yaxis.set_label_position("left")
    
    #Save plot
    plt.savefig(os.path.join(savingFolder, 'CV_Plot-' + filename[0] + '.pdf'),bbox_inches='tight')
    plt.show()

except:
    sys.exit("Error in loading data. Please check you have selected a cyclic voltammetry excel/csv file and written the correct columns to be included.")
