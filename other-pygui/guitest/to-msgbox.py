#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this program, we show various
message boxes.

author: Jan Bodnar
last modified: January 2011
website: www.zetcode.com
"""

from ttk import Frame, Button, Style
from Tkinter import Tk, BOTH
import tkMessageBox as box


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Message boxes")
        self.style = Style()
        self.style.theme_use("default")        
        self.pack()
        
        error = Button(self, text="Error", command=self.onError)
        error.grid()
        warning = Button(self, text="Warning", command=self.onWarn)
        warning.grid(row=1, column=0)
        question = Button(self, text="Question", command=self.onQuest)
        question.grid(row=0, column=1)
        inform = Button(self, text="Information", command=self.onInfo)
        inform.grid(row=1, column=1)


    def onError(self):
        box.showerror("Error", "Could not open file")
        
    def onWarn(self):
        box.showwarning("Warning", "Deprecated function call")
        
    def onQuest(self):
        box.askquestion("Question", "Are you sure to quit?")
        
    def onInfo(self):
        box.showinfo("Information", "Download completed")
         

def main():
  
    root = Tk()
    ex = Example(root)
    root.geometry("300x150+300+300")
    root.mainloop()  


if __name__ == '__main__':
    main()  

