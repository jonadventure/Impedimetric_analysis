#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 13:35:48 2020

@author: jonasvishart
"""

##__________________________________________________________________________
##__________________________________________________________________________
# Basic useful functions

#All functions
# from basics import saveFile, importDatasheet, getFilepath, checkValuesInList
#data = importDatasheet(split = ";")
#filepath = getFilepath()
#savingFolder = getFilepath()
#saveFile(arrayVariable,filetype, savingFolder,filename)
#checkValuesInList(truevalues, List)

##__________________________________________________________________________
##__________________________________________________________________________

#Sorting command, so data files are loaded in order 0,1,2,...,9,10,...,n.
def sort_nice(liste): 
    import re
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(liste, key = alphanum_key)

##__________________________________________________________________________
##__________________________________________________________________________

def saveFile(arrayVariable,filetype, savingFolder,filename):
    import numpy as np
    np.savetxt(str(savingFolder) + "/" + str(filename) + '.' + str(filetype),arrayVariable,fmt='%s',delimiter=',')

##__________________________________________________________________________
##__________________________________________________________________________

def importDatasheet(split = ";"):
    # Import packages
    import pandas as pd
    import tkinter as tk
    from tkinter import filedialog, messagebox
    #_________________________________________
    #Create pop-up window
    root = tk.Tk() 
    root.attributes('-topmost',True)
    root.withdraw()
    root.update()
    #Get filepath
    data = filedialog.askopenfilenames(
                title = "Select data file", parent = root,
                filetypes = (("csv file","*.csv"),("all files","*.*")))
    data=str(data)
    data=data[2:-3]
    #Read file
    data = pd.read_csv(str(data),sep=str(split))
    
    messagebox.showinfo(message="Done!") 
    root.destroy()
    
    return data

##__________________________________________________________________________
##__________________________________________________________________________

def getFilepath(message):
    # Import packages
    import os  
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox
    #_________________________________________
    #Create pop-up window
    root = tk.Tk() 
    root.attributes('-topmost',True)
    root.withdraw()
    root.update()

    #Choosing saving folder
    message = str(message)
    messagebox.showinfo(message=message) #Give directions to what folder should be selected
    folder_path = filedialog.askdirectory(title = message, initialdir=os.getcwd()) #Gets path directory to folder
    
    messagebox.showinfo(message="Done!") 
    root.destroy()
    
    return folder_path
##__________________________________________________________________________
##__________________________________________________________________________
    
def checkValuesInList(truevalues, List):
    # Remember select column in a pd.DataFrame by data.iloc[:,0]
    import pandas as pd
    truevalues = pd.DataFrame(truevalues)
    List = pd.DataFrame(List)
    
    notFound = sorted(list(set(List.iloc[:,0])-set(truevalues.iloc[:,0])))
    
    if len(notFound) == 0:
        print("True. All values in list.")
    else:
        print("False. We found some values not in list. They are: " + str(notFound))

##__________________________________________________________________________
##__________________________________________________________________________
def Load_data(Message, use_cols=None, header=None, skiprows=1, sep=";"): 
    # Import packages
    import os  
    import pandas as pd
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox
    
    #Import data
    #Create pop-up window
    root = tk.Tk() 
    root.attributes('-topmost',True)
    root.withdraw()
    root.update()
    
    Message = str(Message)
    
    #Get filepath
    data = filedialog.askopenfilenames(
                title = Message, parent = root,
                filetypes = (("xlsx file","*.xlsx"),("csv file","*.csv"),("xls file","*.xls"),("all files","*.*")))
    data = list(data)
    messagebox.showinfo(message="Done!") 
    root.destroy()
    
    #Extract name of chosen file
    filename = []
    for i in range(0,len(data)):
        filename.extend([os.path.basename(data[i])])
    
    #Read the data, but skip the header
    # "usecols" selects only the needed data columns
    Loaded_data = []
        
    for i in range(0,len(filename)):
        if filename[i].endswith('.csv'):
            Loaded_data.extend([pd.read_csv(str(data[i]), usecols = use_cols, header=header, skiprows=skiprows, sep=sep)])
            filename[i]=str(filename[i])[:-4]
        elif filename[i].endswith('.xls'):
            Loaded_data.extend([pd.read_excel(str(data[i]), usecols = use_cols, header=header, skiprows=skiprows)])
            filename[i]=str(filename[i])[:-4]
        else:
            Loaded_data.extend([pd.read_excel(str(data[i]), usecols = use_cols, header=header, skiprows=skiprows)])
            filename[i]=str(filename[i])[:-5]
    
    name = "_".join(filename)

    return Loaded_data, filename, name
##__________________________________________________________________________
##__________________________________________________________________________

def Table(value_matrix, rows, columns, scale_width=2, scale_height=2, figsize = 6):
    import matplotlib.pyplot as plt
    #Table - Main table
    #plt.figure(figsize=(6,1))
    plt.figure(figsize=(figsize, 1))
    plt.rcParams["font.family"] = "georgia"
    ax = plt.subplot2grid((4,3), (0,0), colspan=2, rowspan=2)

    Table = ax.table(cellText=value_matrix,
                      rowLabels=rows,
                      colLabels=columns, loc="best")
    Table.set_fontsize(14)
    Table.scale(scale_width, scale_height)
    ax.axis("off")
    return Table
#scale_width*len(columns)
##__________________________________________________________________________
##__________________________________________________________________________
