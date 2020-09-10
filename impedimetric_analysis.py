#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 14:11:08 2020

@author: jonasvishart
"""
# Import packages
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image


root = tk.Tk() 
root.title('Impedimetric analysis')
root.geometry("400x400")

# Drop down boxes
options = ["CV-analysis", 
           "EIS-analysis", 
           "ECS-analysis"]

def selected_analysis(analysis):
    if clicked.get() == options[0]:
        import Analysis_CV
    elif clicked.get() == options[1]:
        import Analysis_EIS_ECS
    elif clicked.get() == options[2]:
        import Analysis_EIS_ECS
    else:
        pass
        
# Make frame
frame = LabelFrame(root,text="Select analysis", padx=5, pady=5)
frame.pack(padx=10, pady=10)

clicked = StringVar() 
value = StringVar()
def onclick():
    input_value = value.get()
    print(input_value)
    
Text = 'Text'
L = Label(root, text=str(Text)).pack(side = LEFT)
E = Entry(root, text=value, bd=2).pack(side =RIGHT)

    
    

    
clicked.set(options[0])

dropAnalys = OptionMenu(frame, clicked, *options, command=selected_analysis)
dropAnalys.pack()



run_button = Button(root,text="Run!",command = onclick())
run_button.pack()
root.mainloop()