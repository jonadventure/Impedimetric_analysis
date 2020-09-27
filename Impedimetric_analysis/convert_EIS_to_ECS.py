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
from basics import getFilepath, Load_data

#_________________________________________
#_________________________________________
# VARIABLES
#_________________________________________
capacitance_unit = '(F)' #depends on unit for impedance
                       #SI-unit for capacitance is Farad (F)
values_row_start = 2 #Check EIS/ECS excel file,
                     #if values start from 2nd row
                     #then values_row_start = 2
frequency_column = 2 #Check EIS excel file,
                     #if frequency values in 2nd column, 
                     #then frequency_column = 2
Z_re_column = 3  #Check EIS excel file,
                 #if real impedance values in third column, 
                 #then Z_re_column = 3
Z_im_column = 4  #Check EIS excel file,
                  #if imaginary impedance values in fourth column, 
                  #then Z_img_column = 4 (assumed to be column of -Z_img)
Z_column = 5 #Check EIS excel file,
             #if Z values in fifth column, 
             #then Z_column = 5

#_________________________________________
#_________________________________________
# IMPORT DATA
#_________________________________________
try:
    #Load data
    use_cols = [frequency_column-1, Z_re_column-1, Z_im_column-1,Z_column-1] #define which columns to extract from data
    message = "Select your EIS file(s)"
    #Load data with column names
    Loaded_data, filename, name = Load_data(message,use_cols=None,header=0,skiprows=values_row_start-2, sep=";")
    ECS_data = Loaded_data.copy() #create copy of EIS data
    
    #Choose where to save ECS data file
    savingFolder = str(getFilepath("Choose saving folder"))
    
    #_________________________________________
    #_________________________________________
    # Transform EIS to ECS
    #_________________________________________
    #Converting from EIS to ECS is done by C*(ω) = 1/jωZ*
    # All are assumed measured in SI-units
    for i in range (0,len(filename)):
        frequency = Loaded_data[i].iloc[:,use_cols[0]]
        omega = 2*np.pi*frequency #define omega as w=2*pi*f
        Z_re = Loaded_data[i].iloc[:,use_cols[1]] #real of Z
        Z_im = Loaded_data[i].iloc[:,use_cols[2]] #imaginary of Z                                                              
        Z_combined = Z_re-1j*Z_im #note, given -Z_im column, 
                                  #so to bring on form Z=a+jb, 
                                  #we need "-" in front of Z_im 
        C = np.reciprocal(omega*1j*Z_combined) #conversion to ECS by C*(ω) = 1/jωZ*
        Cdot = np.real(C) #Re(C)
        Cdotdot = np.imag(C) #Im(C)    
        C_mag = np.sqrt(Cdot**2+Cdotdot**2) #magnitude of C
        
        #_________________________________________
        #_________________________________________
        #Creating ECS data 
        #but changing only columns with the conversion to ECS
        ECS_data[i].iloc[:,use_cols[1]]=Cdot
        ECS_data[i].iloc[:,use_cols[2]]=-Cdotdot #minus sign, 
                                                 #to get column -Im(C)
        ECS_data[i].iloc[:,use_cols[3]]=C_mag
        new_columns = {ECS_data[i].columns[use_cols[1]]: "C' ; Re(C) / "+str(capacitance_unit), 
                   ECS_data[i].columns[use_cols[2]]: "C'' ; Im(C) / "+str(capacitance_unit),
                   ECS_data[i].columns[use_cols[3]]: "C / "+str(capacitance_unit)}
        ECS_data[i] = ECS_data[i].rename(columns=new_columns )
    
        #Creating path to saving folder and name of file
        path = os.path.join(savingFolder, r'ECS-'+ filename[i]+".csv")
        #Save ECS data file
        ECS_data[i].to_csv(path, sep=';', index = None, header=True)
        
        print("The file", str(filename[i]), "is converted from EIS to ECS data and the converted file is saved.")
except:
    sys.exit("Error in loading data. Please check you have selected an EIS excel/csv file and written the correct columns to be included.")
