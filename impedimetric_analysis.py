#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 14:11:08 2020

@author: jonasvishart
"""
# Import packages
import tkinter as tk
from tkinter import Button, END, Entry, Label, LabelFrame, OptionMenu, StringVar
#from PIL import ImageTk, Image
from impedimetric_functions import Analysis_CV, Analysis_EIS, Plots_all_imported

class App:
    def __init__(self,master):
        self.master = master
        master.title('Impedimetric analysis')
        master.geometry("400x400")
        
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
        # Run button
        #_____________________________
        self.run_button = Button(master,text="Run!",command = self.onclick)
        self.run_button.grid(row=12,column=1)
        
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
            self.variable4 = self.entry_box('x_start',5,1,"")
            self.variable5 = self.entry_box('x_end',6,1,"")
            self.variable6 = self.entry_box('y_start',7,1,"")
            self.variable7 = self.entry_box('y_end',8,1,"")
            self.variable8 = self.entry_box('impedance_unit',9,1,"Ω")
            self.variable9 = self.entry_box('circle_point1_index',10,1,1)
            self.variable10 = self.entry_box('circle_point2_index',11,1,5)
        

        
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