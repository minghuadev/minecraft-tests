#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this script, we show how to
use the Listbox widget.

author: Jan Bodar
last modified: December 2010
website: www.zetcode.com
"""

from ttk import Frame, Label, Style
from Tkinter import Tk, BOTH, Listbox, StringVar, END


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Listbox") 
        
        self.pack(fill=BOTH, expand=1)

        acts = ['Scarlett Johansson', 'Rachel Weiss', 
            'Natalie Portman', 'Jessica Alba']

        lb = Listbox(self)
        for i in acts:
            lb.insert(END, i)
            
        lb.bind("<<ListboxSelect>>", self.onSelect)    
            
        lb.place(x=20, y=20)

        self.var = StringVar()
        self.label = Label(self, text=0, textvariable=self.var)        
        self.label.place(x=20, y=210)

    def onSelect(self, val):
      
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)   

        self.var.set(value)
         

def main():
  
    root = Tk()
    ex = Example(root)
    root.geometry("300x250+300+300")
    root.mainloop()  


if __name__ == '__main__':
    main()  

