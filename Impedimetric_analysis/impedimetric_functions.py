#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 23:16:40 2020

@author: jonasvishart
"""
#_________________________________________
# CV ANALYSIS
#_________________________________________
from matplotlib.pyplot import *
from scipy.optimize import curve_fit
def Analysis_CV(values_row_start_get, x_column_get,y_column_get,scan_column_get,scan_number_get,
                LinReg_start_index_get,R2_accept_value_get,potential_unit, current_unit, num_decimals): 
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
    from sklearn.metrics import r2_score
    from sklearn.linear_model import LinearRegression
    
    #_________________________________________
    #_________________________________________
    # VARIABLES
    #_________________________________________
    values_row_start = int(values_row_start_get) #Check EIS/ECS excel file,
                         #if values start from 3rd row
                         #then values_row_start = 3
    scan_column = int(scan_column_get) #Check CV excel file, 
                    #if scan column don't exist then scan_column = 0. 
                    #If it is in first column, then scan_column = 1
    Scan_number = int(scan_number_get) #only if scan_column exist
                    #value is out of influence, if scan_column doesn't exist
    
    potential_column = int(x_column_get) #Check CV excel file, 
                       #if potential values in first column, then potential_column = 1
    current_column = int(y_column_get) #Check CV excel file, 
                       #if current values in second column, then current_column = 2
    potential_unit = str(potential_unit)
    current_unit = str(current_unit)
    
    num_decimals = int(num_decimals) #number of decimals to round numbers
    font_size = 14 #font size for labels
    LinReg_start_index = int(LinReg_start_index_get) #how many indexes away from start and end point before regression is made
    R2_accept_value = float(R2_accept_value_get) #limit for how good linear reression must be
    
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
        plt.title("Cyclic voltammetry, IUPAC conv.\n Oxidation peak: "+"E_pa="+ str(format(x_upperPeak,num_dec))+str(potential_unit)+",  i_pa="+
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
        markers = ['.',',','o','v','^','>','<','1','2','3','4','s','p','*','h','H','+','x','D','d','|','_']
        for j in range(0,len(filename)):    
            #Define only data by selected scan
            if scan_column > 0:
                Scan_select = Loaded_data[j][Loaded_data[j].iloc[:,2] == Scan_number]
                legend_label = '%s' % filename[j] + '   Scan: ' + str(Scan_number)
            else: 
                Scan_select = Loaded_data[j]
                legend_label = '%s' % filename[j] 
            Scan_select = Scan_select.reset_index(drop=True)
            plt.plot(Scan_select.iloc[:,0], Scan_select.iloc[:,1], label=legend_label, marker=markers[j])
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

#_________________________________________
# EIS ANALYSIS
#_________________________________________
def Analysis_EIS(values_row_start_get, x_column_get,y_column_get,x_start_get, x_end_get,
                 y_start_get, y_end_get, unit,cir_pt1_index, cir_pt2_index):
    #_________________________________________
    # IMPORT PACKAGES
    #_________________________________________
    import os
    import sys
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mtick
    from sklearn.metrics import r2_score
    from sklearn.linear_model import LinearRegression
    from basics import getFilepath, Load_data, Table
    
    #_________________________________________
    #_________________________________________
    # VARIABLES
    #_________________________________________
    
    Analysis = ["impedance",str(unit)]  #[method,unit] 
                                  #method is "impedance" or "capacitance"
                                  #unit is only used as label
    #Analysis = ["capacitance","F"]
    
    values_row_start = int(values_row_start_get) #Check EIS/ECS excel file,
                         #if values start from 2nd row
                         #then values_row_start = 2
    Real_column = int(x_column_get) #Check EIS/ECS excel file,
                    #if Re(Z) or Re(C) values in third column, 
                    #then Real_column = 3
    Imag_column = int(y_column_get) #Check EIS/ECS excel file,
                    #if Im(Z) or Im(C) values in fourth column, 
                    #then Imag_column = 4 (assumed to be column of -Im(Z) or -Im(C))                              
    if len(x_start_get)==0 or len(x_end_get)==0:
        x_lim_plot = [ ]
    else:
        x_lim_plot = [float(x_start_get),float(x_end_get)] # if empty [ ] => no limit on plot x-axis is set! Otherwise, e.g [0,200]
    
    if len(y_start_get)==0 or len(y_end_get)==0:
        y_lim_plot = [ ]
    else:
        y_lim_plot = [float(y_start_get),float(y_end_get)] # if empty [ ] => no limit on plot y-axis is set! Otherwise, e.g [0,200]
    
    cir_pt1_index = int(cir_pt1_index) #to circle fit, nr. index away from first index
    cir_pt2_index = int(cir_pt2_index) #to circle fit, nr. index away to left of end of circle!!
    
    num_decimals = 3 #number of decimals to round numbers
    font_size = 14 #fontsize in labels
    
    
    #_________________________________________
    #_________________________________________
    # IMPORT DATA
    #_________________________________________
    try:
        #Load data
        use_cols = [Real_column-1, Imag_column-1] #columns to extract from imported data
        message = "Select your EIS file(s)"
        Loaded_data, filename, name = Load_data(message, use_cols, header=None, skiprows=values_row_start-1)
        
        #Only use data in selected x_limit
        for j in range(0,len(filename)):
            if len(x_lim_plot) == 2: 
                Loaded_data[j] = Loaded_data[j].sort_values(by=Loaded_data[j].columns[0])
                Loaded_data[j] = Loaded_data[j][Loaded_data[j].iloc[:,0]>x_lim_plot[0]]
                Loaded_data[j] = Loaded_data[j][Loaded_data[j].iloc[:,0]<x_lim_plot[1]]
    
        #Choose where to save plots
        savingFolder = str(getFilepath("Choose saving folder"))
        
        #_________________________________________
        #_________________________________________
        # Curve fit
        #_________________________________________
        
        num_dec = '.'+'%s'% +num_decimals+'g'
        D_list = []
        Lin_func_list = []
        Lin_interval = []
            
        try:
            for j in range(0,len(filename)):
                #_________________________________________
                #_________________________________________
                # Linear fit
                #_________________________________________ 
                
                #sort data from smallest to greatest x-value
                sorted_data = Loaded_data[j].sort_values(by=Loaded_data[j].columns[0])
                x_lin1 = sorted_data.iloc[:,0]
                y_lin1 = sorted_data.iloc[:,1]
    
                y_lin1 = y_lin1[::-1] # flips y-coordinates, so the characteristic linear curve gets negative slope
                slope_2 = np.gradient(y_lin1) # calculate slope
                slope_2_index = np.where(np.round(slope_2,0) > -1) # find index where linear curce stops (end of semicircle)
    
                print(str("File: "),filename[j])
                if slope_2_index[0][0] == 0: #if no positive slope was found then slope_2_index[0][0]=0
                    circle_end_index = len(y_lin1)
                    print("No linear curve was found.")
                else:
                    slope_2_value = slope_2_index[0][0] #index where slope > -1
                    circle_end_index = len(y_lin1)-slope_2_value 
                    x_reg = np.array(sorted_data.iloc[circle_end_index:,0]).reshape(-1,1) #x_data from end of circle to last point
                    y_reg = np.array(sorted_data.iloc[circle_end_index:,1]).reshape(-1,1) #y_data from end of circle to last point
                    fit1 = LinearRegression() 
                    fit1.fit(x_reg, y_reg) #make linear fit
                    y_pred1 = fit1.intercept_ + fit1.coef_[0]*sorted_data.iloc[:,0] #define regression on form y=b+ax
                    R2_1_score = r2_score(y_reg.reshape(1,-1)[0],y_pred1[circle_end_index:].to_numpy()) #compute R^2 value
                    
                    print(str("Linear function:"),format(fit1.coef_[0][0],num_dec),str("x +"), format(fit1.intercept_[0],num_dec))
                    print(str("Linear interval: ["),format(sorted_data.iloc[circle_end_index,0],num_dec),str(","),format(sorted_data.iloc[len(x_lin1)-1,0],num_dec),str("]"))
                #_________________________________________
                #_________________________________________
                # Circle fit
                #_________________________________________
                def func(x, X_c, R): #define function for "non-linear least squares" fit
                    return R**2-(x-X_c)**2 #Y^2=R^2-(x-X_c)^2, rewritten form of (x-X_c)^2+Y^2=R^2
                #only include data from selected start point to end of semicircle minus second selected point
                xdata = sorted_data.iloc[cir_pt1_index:circle_end_index-cir_pt2_index,0]
                #only include data from selected start point to end of semicircle minus second selected point
                ydata = sorted_data.iloc[cir_pt1_index:circle_end_index-cir_pt2_index,1]
                
                #solve non linear system
                popt, pcov = curve_fit(func, np.array(xdata), np.array(ydata**2))
                D=2*popt[1] #diameter of semicircle
                print("Diameter:",D)
                print(str("Resist Charge Transfer:"),format(D,num_dec))
                print("\n")
                D_list.append(float(format(D,num_dec)))
            #_________________________________________
            #_________________________________________
            # DIAMETER TABLE
            #_________________________________________
            # Make Diameter table
            if len(D_list)>1: #if only 1 selected file, no need to compare to any other file
                columns_1 = ["Resist Charge Transfer / "+str(Analysis[1])]
                rows_1 = []
                for i in filename: #filename is list of all selected files with their filename
                    rows_1.append(str(i))
                value_matrix = np.array((D_list)).reshape(1,len(D_list)).T #define value matrix
                        
                #Table - Main table
                print(str("Diameter overview:"))
                Table(value_matrix,rows_1,columns_1,scale_width=2,scale_height=2, figsize=1.5)
                plt.tight_layout()
                #Save plot
                plt.savefig(os.path.join(savingFolder, 'Diameter-' + filename[0] + '.pdf'), bbox_inches='tight')
                plt.show() 
            
            #_________________________________________
            #_________________________________________
            # DIAMETER DIFFERENCE TABLE
            #_________________________________________
            # Make Diameter difference table
            if len(D_list)>1: #if only 1 selected file, no need to compare to any other file
                columns = []
                
                rows = []
                for i in range(0,len(filename)): #create labels to top column and left row
                    columns.append(str(filename[i])+str("\n Resist Charge Transfer: ")+str(D_list[i])+str(" ")+str(Analysis[1]))
                    rows.append(str(filename[i])+str("\n Resist Charge Transfer: ")+str(D_list[i])+str(" ")+str(Analysis[1]))
    
                D_difference = []
                for j in range(0,len(D_list)):
                    for i in range(0,len(D_list)):
                        D_difference.append(D_list[i]-D_list[j])
                D_matrix = np.array(np.round(D_difference,5)).reshape(len(D_list),len(D_list))
                        
                #Table - Main table
                print(str("Resist Charge Transfer difference matrix, \u0394Diameter:"))
                Table(D_matrix,rows,columns,scale_width=2.5, scale_height=2,figsize=len(columns)) #this scale works best
                #Save plot
                plt.savefig(os.path.join(savingFolder, 'Dif_diameter' + filename[0] + '.pdf'),bbox_inches='tight')
                plt.show()
    
            #_________________________________________
            #_________________________________________
            # DIAMETER BAR CHART
            #_________________________________________
            # Make Diameter bar chart 
            if len(D_list)>1: #if only 1 selected file, no need to compare to any other file
                fig, ax = plt.subplots()  
                y_pos = np.arange(len(filename)) #for ticks on y-axis
                plt.barh(y_pos, D_list, align='center', alpha=0.8, color="cornflowerblue")
                plt.yticks(y_pos, filename) #place the ticks on y-axis
                plt.xlabel("Resist Charge Transfer / "+str(Analysis[1]))
                plt.title("Overview of Resist Charge Transfer for each file")
                plt.xlim((0,1.23*max(D_list))) #make xlim great enough for text to be next to bar
                #Position diameter value next to each bar
                for i, v in enumerate(D_list):
                    ax.text(v+(0.01*max(D_list)), i, str(v), color='black', fontweight='bold')
                #Display ticks as scientific if they are rounded to 0
                if round(max(Loaded_data[i].iloc[:,0])) == 0:
                    ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
                if round(max(Loaded_data[i].iloc[:,1])) == 0:
                    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
                plt.savefig(os.path.join(savingFolder, 'Bar_diameter-' + filename[0] + '.pdf'),bbox_inches='tight')
                print("Diameter overview (Bar chart):")
                plt.show()
        except:
            pass
        #_________________________________________
        #_________________________________________
        # EIS/ECS plot
        #_________________________________________
        # Make the EIS/ECS plot
        # Based on input determine whether to label as EIS or ECS
        symbol = ["Z","C"]
        if str.lower(Analysis[0]) == "impedance":
            symbol = "Z"
            Title = "Impedance"
        elif str.lower(Analysis[0]) == "capacitance":
            symbol = "C"
            Title = "Capacitance"
        else:
            symbol = "unit"
            Title = "Undefined"
        
        print("All in one plot: ")
        fig = plt.figure()
        plt.rcParams["font.family"] = "georgia"
        
        #Constrain axes
        plt.gca().set_aspect('equal', adjustable='box')
        ax = fig.add_subplot(1, 1, 1)
        
        #Define list of different plotting markers
        markers = ['.',',','o','v','^','>','<','1','2','3','4','s','p','*','h','H','+','x','D','d','|','_']
        for i in range(0,len(filename)): 
            plt.plot(Loaded_data[i].iloc[:,0], Loaded_data[i].iloc[:,1], label='%s' % filename[i], marker=markers[i])
    
        # Put a legend to the right of the current axis
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        #Make labels 
        plt.xlabel(str(symbol)+"'  ; Re("+str(symbol)+") / "+str(Analysis[1]),fontsize=font_size)
        plt.ylabel("-"+str(symbol)+"''  ; -Im("+str(symbol)+") / "+str(Analysis[1]),fontsize=font_size)
        plt.title(str(Title)+" Nyquist", fontsize=font_size)
        ax.yaxis.set_label_position("left")
        #Set limits on x- and y-range
        if len(x_lim_plot) == 2: 
            plt.xlim((x_lim_plot[0], x_lim_plot[1]))
        if len(y_lim_plot) == 2:
            plt.ylim((y_lim_plot[0], y_lim_plot[1]))
        
        #Display ticks as scientific if they are rounded to 0
        if round(max(Loaded_data[i].iloc[:,0])) == 0:
            ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
        if round(max(Loaded_data[i].iloc[:,1])) == 0:
            ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
            
        #Save plot
        plt.savefig(os.path.join(savingFolder, 'Plot-' + filename[0] + '.pdf'),bbox_inches='tight')
        plt.show()
    except:
        sys.exit("Error in loading data. Please check you have selected an EIS/ECS excel/csv file and written the correct columns to be included.")
        
        
def Plots_all_imported(values_row_start_get, x_column_get,y_column_get,x_start_get, x_end_get,
                       y_start_get, y_end_get, x_label, y_label, plot_title):
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
    
    values_row_start = int(values_row_start_get) #Check EIS/ECS excel file,
                         #if values start from 2nd row
                         #then values_row_start = 2
    x_values = int(x_column_get) #Check EIS excel file,
                         #if frequency values in 2nd column, 
                         #then x_values = 2
    y_values = int(y_column_get)  #Check EIS excel file,
                      #if y values in fifth column, 
                      #then y_values = 5
                    
    if len(x_start_get)==0 or len(x_end_get)==0:
        x_lim_plot = [ ]
    else:
        x_lim_plot = [float(x_start_get),float(x_end_get)] # if empty [ ] => no limit on plot x-axis is set! Otherwise, e.g [0,200]
    
    if len(y_start_get)==0 or len(y_end_get)==0:
        y_lim_plot = [ ]
    else:
        y_lim_plot = [float(y_start_get),float(y_end_get)] # if empty [ ] => no limit on plot y-axis is set! Otherwise, e.g [0,200]

    x_label = str(x_label)
    y_label = str(y_label)
    
    title = str(plot_title)
    
    
    save_title = str(plot_title)
    
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
    

