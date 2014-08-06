#!/usr/bin/python
#https://wiki.python.org/moin/Intro%20to%20programming%20with%20Python%20and%20Tkinter

from Tkinter import *           # Importing the Tkinter (tool box) library 
root = Tk()                     # Create a background window
                                # Create a list
li = 'Carl Patrick Lindsay Helmut Chris Gwen'.split()
listb = Listbox(root)           # Create a listbox widget
for item in li:                 # Insert each item within li into the listbox
    listb.insert(0,item)

listb.pack()                    # Pack listbox widget
root.mainloop()                 # Execute the main event handler


