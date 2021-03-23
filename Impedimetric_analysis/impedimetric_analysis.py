#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 14:11:08 2020

@author: jonasvishart
"""
#_____________________________
# Presetting
#_____________________________
#Change directory to location of Python script
import os, sys
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
sys.path.append(dname)

# Import packages
import tkinter as tk
from tkinter import Button, END, Entry, Label, LabelFrame, OptionMenu, StringVar
#from PIL import ImageTk, Image
from impedimetric_functions import Analysis_CV, Analysis_EIS, Plots_all_imported


#_____________________________
# GUI setup
#_____________________________
class App:
    def __init__(self,master):
        self.master = master
        master.title('Impedimetric analysis')
        master.geometry("500x400")
        
        # Drop down boxes
        self.options = ["CV-analysis", 
                   "EIS-analysis", 
                   "Plot imported files"]
        self.clicked = StringVar()
        self.clicked.set(self.options[0])
        
        # Make frame
        self.frame = LabelFrame(master,text="Select analysis", height=5, width=5)
        self.frame.grid(row=0,column=1)
        #_____________________________
        # Dropdown menu
        #_____________________________
        dropAnalys = OptionMenu(self.frame, self.clicked, *self.options)
        dropAnalys.grid(row=0, column=1)
        
        self.clicked.trace("w",self.change) #track if something happens to variable
        
        #_____________________________
        # Initial Entry boxes
        #_____________________________
        self.variable1 = self.entry_box('values_row_start',2,1,3)
        self.variable2 = self.entry_box('potential_column',3,1,1)
        self.variable3 = self.entry_box('current_column',4,1,3)
        self.variable4 = self.entry_box('scan_column (0 if none)',5,1,5)
        self.variable5 = self.entry_box('Scan_number',6,1,3)
        self.variable6 = self.entry_box('LinReg_start_index',7,1,15)
        self.variable7 = self.entry_box('R2_accept_value',8,1,0.90)
        self.variable8 = self.entry_box('potential_unit',9,1,"V")
        self.variable9 = self.entry_box('current_unit',10,1,"A")
        self.variable10 = self.entry_box('Number of decimals',11,1,3)
        
        #_____________________________
        # Info boxes
        #_____________________________
        self.button1 = Button(master, text = "info",command=self.info_box1).grid(row=2, column=2)
        self.button2 = Button(master, text = "info", command=self.info_box2).grid(row=3, column=2)
        self.button3 = Button(master, text = "info", command=self.info_box3).grid(row=4, column=2)
        self.button4 = Button(master, text = "info", command=self.info_box4).grid(row=5, column=2)
        self.button5 = Button(master, text = "info", command=self.info_box5).grid(row=6, column=2)
        self.button6 = Button(master, text = "info", command=self.info_box6).grid(row=7, column=2)
        self.button7 = Button(master, text = "info", command=self.info_box7).grid(row=8, column=2)
        self.button8 = Button(master, text = "info", command=self.info_box8).grid(row=9, column=2)
        self.button9 = Button(master, text = "info", command=self.info_box9).grid(row=10, column=2)
        self.button10 = Button(master, text = "info", command=self.info_box10).grid(row=11, column=2)

                
        #_____________________________
        # Run button
        #_____________________________
        self.run_button = Button(master,text="Run!",command = self.onclick)
        self.run_button.grid(row=12,column=1)
        
    #_____________________________
    # Info boxes - Text definitions
    #_____________________________ 
    def info_box1(self):
        Text = "The row for which the First value appears in the excel/csv file."
        tk.messagebox.showinfo("Info",str(Text))
    
    def info_box2(self):
        if self.clicked.get() == self.options[0]:
            Text = "Check your excel/csv file and list the column number of where the Potential (V) values appear."
        elif self.clicked.get() == self.options[1]:
            Text = "Check your excel/csv file and list the column number of where the Real part of impedance values appear."
        elif self.clicked.get() == self.options[2]:
            Text = "CCheck your excel/csv file and list the column number of where the x-values appear."
        tk.messagebox.showinfo("Info",str(Text))
    
    def info_box3(self):
        if self.clicked.get() == self.options[0]:
            Text = "Check your excel/csv file and list the column number of where the Current (I) values appear."
        elif self.clicked.get() == self.options[1]:
            Text = "Check your excel/csv file and list the column number of where the Imaginary part of impedance values appear."
        elif self.clicked.get() == self.options[2]:
            Text = "Check your excel/csv file and list the column number of where the y-values appear."
        tk.messagebox.showinfo("Info",str(Text))
    
    def info_box4(self):
        if self.clicked.get() == self.options[0]:
            Text = "Check your excel/csv file and list the column number of where the Scan number indication appear."
        elif self.clicked.get() == self.options[1]:
            Text = "Insert value for Start interval of Real part of impedance values. NB: both Z_R_start and Z_R_end must be inserted for the interval range to be created."
        elif self.clicked.get() == self.options[2]:
            Text = "Insert value for Start interval of x-values. NB: both x_start and x_end must be inserted for the interval range to be created."
        tk.messagebox.showinfo("Info",str(Text))
    
    def info_box5(self):
        if self.clicked.get() == self.options[0]:
            Text = "The Scan number you want to include for plotting."
        elif self.clicked.get() == self.options[1]:
            Text = "Insert value for End interval of Real part of impedance values. NB: both Z_R_start and Z_R_end must be inserted for the interval range to be created."
        elif self.clicked.get() == self.options[2]:
            Text = "Insert value for End interval of x-values. NB: both x_start and x_end must be inserted for the interval range to be created."
        tk.messagebox.showinfo("Info",str(Text))
    
    def info_box6(self):
        if self.clicked.get() == self.options[0]:
            Text = "The number of indexes away from start and end value, in between regression is made."
        elif self.clicked.get() == self.options[1]:
            Text = "Insert value for Start interval of Imaginary part of impedance values. NB: both Z_Im_start and Z_Im_end must be inserted for the interval range to be created."
        elif self.clicked.get() == self.options[2]:
            Text = "Insert value for Start interval of y-values. NB: both y_start and y_end must be inserted for the interval range to be created."
        tk.messagebox.showinfo("Info",str(Text))
    
    def info_box7(self):
        if self.clicked.get() == self.options[0]:
            Text = "Minimum value for how good linear reression must be in order to create mandatory baselines."
        elif self.clicked.get() == self.options[1]:
            Text = "Insert value for End interval of Imaginary part of impedance values. NB: both Z_Im_start and Z_Im_end must be inserted for the interval range to be created."
        elif self.clicked.get() == self.options[2]:
            Text = "Insert value for End interval of y-values. NB: both y_start and y_end must be inserted for the interval range to be created."
        tk.messagebox.showinfo("Info",str(Text))        

    def info_box8(self):
        if self.clicked.get() == self.options[0]:
            Text = "Type the Potential unit."
        elif self.clicked.get() == self.options[1]:
            Text = "Type the Impedance unit."
        elif self.clicked.get() == self.options[2]:
            Text = "Type the x-label."
        tk.messagebox.showinfo("Info",str(Text))  
    
    def info_box9(self):
        if self.clicked.get() == self.options[0]:
            Text = "Type the Current unit."
        elif self.clicked.get() == self.options[1]:
            Text = "Type the starting index number to be used in the semicircle fit."
        elif self.clicked.get() == self.options[2]:
            Text = "Type the y-label."
        tk.messagebox.showinfo("Info",str(Text))  
    
    def info_box10(self):
        if self.clicked.get() == self.options[0]:
            Text = "Number of decimals to be displayed in output plots."
        elif self.clicked.get() == self.options[1]:
            Text = "Type the number of indexes to the left of the semicircle end that defines the final interval of the semicircle fit."
        elif self.clicked.get() == self.options[2]:
            Text = "Type the plot-title."
        tk.messagebox.showinfo("Info",str(Text))  
    #_____________________________
    # Entry boxes
    #_____________________________
    def entry_box(self,Text, row, column, default_input, width = 20):
        Text = str(Text)
        Label(self.master, text=str(Text),width = width).grid(row=row)
        E = Entry(self.master)
        E.insert(END,str(default_input))
        E.grid(row=row, column=column) 
        return E

    def change(self, *args):
        if self.clicked.get() == self.options[0]:
            self.variable1 = self.entry_box('values_row_start',2,1,3)
            self.variable2 = self.entry_box('potential_column',3,1,1)
            self.variable3 = self.entry_box('current_column',4,1,3)
            self.variable4 = self.entry_box('scan_column (0 if none)',5,1,5)
            self.variable5 = self.entry_box('Scan_number',6,1,3)
            self.variable6 = self.entry_box('LinReg_start_index',7,1,15)
            self.variable7 = self.entry_box('R2_accept_value',8,1,0.90)
            self.variable8 = self.entry_box('potential_unit',9,1,"V")
            self.variable9 = self.entry_box('current_unit',10,1,"A")
            self.variable10 = self.entry_box('Number of decimals',11,1,3)
        
         
        elif self.clicked.get() == self.options[1]:
            self.variable1 = self.entry_box('values_row_start',2,1,2)
            self.variable2 = self.entry_box('Z_R_column',3,1,3)
            self.variable3 = self.entry_box('Z_Im_column',4,1,4)
            self.variable4 = self.entry_box('Z_R_start',5,1,"")
            self.variable5 = self.entry_box('Z_R_end',6,1,"")
            self.variable6 = self.entry_box('Z_Im_start',7,1,"")
            self.variable7 = self.entry_box('Z_Im_end',8,1,"")
            self.variable8 = self.entry_box('impedance_unit',9,1,"Ω")
            self.variable9 = self.entry_box('circle_point1_index',10,1,0)
            self.variable10 = self.entry_box('circle_point2_index',11,1,0)
        

        
        elif self.clicked.get() == self.options[2]:
            self.variable1 = self.entry_box('values_row_start',2,1,2)
            self.variable2 = self.entry_box('x_column',3,1,2)
            self.variable3 = self.entry_box('y_column',4,1,5)
            self.variable4 = self.entry_box('x_start',5,1,"")
            self.variable5 = self.entry_box('x_end',6,1,"")
            self.variable6 = self.entry_box('y_start',7,1,"")
            self.variable7 = self.entry_box('y_end',8,1,"")
            self.variable8 = self.entry_box('x_label',9,1,"")
            self.variable9 = self.entry_box('y_label',10,1,"")
            self.variable10 = self.entry_box('plot_title',11,1,"")
        else:
            pass

    #_____________________________
    # Save input in entry boxes and function for run-command
    #_____________________________
    
    def onclick(self,*args): 
        self.variable1_get = self.variable1.get()
        self.variable2_get = self.variable2.get()
        self.variable3_get = self.variable3.get()
        self.variable4_get = self.variable4.get()
        self.variable5_get = self.variable5.get()
        self.variable6_get = self.variable6.get()
        self.variable7_get = self.variable7.get()
        self.variable8_get = self.variable8.get()
        self.variable9_get = self.variable9.get()
        self.variable10_get = self.variable10.get()
        values = [int(self.variable1_get),int(self.variable2_get),int(self.variable3_get),str(self.variable4_get),str(self.variable5_get),
                  str(self.variable6_get),str(self.variable7_get),str(self.variable8_get),str(self.variable9_get),str(self.variable10_get)]
        
        #option to close tkinter window
        self.close_window

        if self.clicked.get() == self.options[0]:
            Analysis_CV(values[0], values[1],values[2],values[3],values[4],values[5],values[6],values[7],values[8],values[9])
            
        elif self.clicked.get() == self.options[1]:
            Analysis_EIS(values[0], values[1],values[2],values[3],values[4],values[5],values[6],values[7],values[8],values[9])
            
        elif self.clicked.get() == self.options[2]:
            Plots_all_imported(values[0], values[1],values[2],values[3],values[4],values[5],values[6],values[7],values[8],values[9])
        else:
            pass
        
    def close_window(self): 
        self.master.destroy()
#_____________________________
# Create root
#_____________________________
root = tk.Tk() 
gui = App(root)
root.mainloop()
