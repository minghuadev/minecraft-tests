#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this script, we show how to
use the Scale widget.

author: Jan Bodnar
last modified: December 2010
website: www.zetcode.com
"""

from ttk import Frame, Label, Scale, Style
from Tkinter import Tk, BOTH, IntVar


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Scale")
        self.style = Style()
        self.style.theme_use("default")        
        
        self.pack(fill=BOTH, expand=1)

        scale = Scale(self, from_=0, to=100, 
            command=self.onScale)
        scale.place(x=20, y=20)

        self.var = IntVar()
        self.label = Label(self, text=0, textvariable=self.var)        
        self.label.place(x=130, y=70)

    def onScale(self, val):
     
        v = int(float(val))
        self.var.set(v)
         

def main():
  
    root = Tk()
    ex = Example(root)
    root.geometry("300x150+300+300")
    root.mainloop()  


if __name__ == '__main__':
    main()  

