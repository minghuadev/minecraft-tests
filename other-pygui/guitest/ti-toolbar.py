#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this program, we create a toolbar.

author: Jan Bodnar
last modified: December 2010
website: www.zetcode.com
"""

from PIL import Image, ImageTk
from Tkinter import Tk, Frame, Menu
from Tkinter import Button, LEFT, TOP, X, FLAT, RAISED



class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Toolbar")
        
        menubar = Menu(self.parent)
        self.fileMenu = Menu(self.parent, tearoff=0)
        self.fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=self.fileMenu)
        
        toolbar = Frame(self.parent, bd=1, relief=RAISED)

        self.img = Image.open("exit.png")
        eimg = ImageTk.PhotoImage(self.img)  

        exitButton = Button(toolbar, image=eimg, relief=FLAT,
            command=self.quit)
        exitButton.image = eimg
        exitButton.pack(side=LEFT, padx=2, pady=2)
       
        toolbar.pack(side=TOP, fill=X)
        self.parent.config(menu=menubar)
        self.pack()
        
       
    def onExit(self):
        self.quit()


def main():
  
    root = Tk()
    root.geometry("250x150+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

