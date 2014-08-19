#
#u1.py
#

import Tkinter as Tw
##import ttk
import tkFileDialog

import os, sys
#sys.path.append("C:/python27/Lib/site-packages") # for PIL package installed differently
from PIL import Image, ImageTk

toproot = Tw.Tk()
def toproot_init():
    toproot.tk.call('wm', 'iconphoto', toproot._w, ImageTk.PhotoImage(file="lens-icon.png"))
    top_winfo_w = toproot.winfo_screenwidth()
    top_winfo_h = toproot.winfo_screenheight()
    top_w = top_winfo_w / 10 * 5
    top_h = top_winfo_h / 10 * 5
    toproot.title("test title %d x %d over %d x %d" % (top_w, top_h, top_winfo_w, top_winfo_h))
    toproot.geometry('%dx%d+%d+%d' % (top_w, top_h,(top_winfo_w-top_w)/2,(top_winfo_h-top_h)/2))
toproot_init()

# pane left
paneleft = Tw.Frame(toproot, relief=Tw.RAISED, border=5)
paneleft.grid(row=0,column=0, sticky=Tw.E, padx=2, pady=2)

myshow = Tw.Label(paneleft, text="my left pane", relief=Tw.RAISED, padx=16, pady=16)
myshow.pack()

# pane right
paneright = Tw.Frame(toproot, relief=Tw.RAISED, border=5)
paneright.grid(row=0,column=1, sticky=Tw.N+Tw.E+Tw.S+Tw.W, padx=2, pady=2, ipadx=10, ipady=10)

# pane right frame
root = Tw.Frame(paneright, relief=Tw.RAISED, border=5)
root.pack(expand=1,fill=Tw.BOTH, padx=10, pady=10, ipadx=10, ipady=10)

##style = ttk.Style(root)
##style.configure("TFrame", background="#ff33")

image = Image.open("lens-page.jpg")
photo = ImageTk.PhotoImage(image)
mylabel = Tw.Label(root, text="my label text", image=photo, relief=Tw.RAISED, padx=16, pady=16)
mylabel.pack(expand=1,fill=Tw.BOTH, padx=10,pady=10)

mystatus = Tw.Label(root, text="my status text")
mystatus.pack(expand=1,fill=Tw.BOTH)

btnholder = Tw.Frame(root, relief=Tw.RAISED, border=5)
btnholder.pack(side=Tw.LEFT, padx=10, pady=10)

btnholderLine1 = Tw.Frame(btnholder, relief=Tw.RAISED, border=5)
btnholderLine1.grid(row=0, column=0, sticky=Tw.E, padx=2, pady=2)
btnholderLine2 = Tw.Frame(btnholder, relief=Tw.RAISED, border=5)
btnholderLine2.grid(row=1, column=0, padx=2, pady=2)


def choosedir():
    options = {}
    options['initialdir'] = 'C:\\'
    options['mustexist'] = True
    options['parent'] = root
    options['title'] = 'This is a title but choose a folder with your image files in it...'
    return tkFileDialog.askdirectory(**options)

def chooseopenfile():
    options = {}
    options['defaultextension'] = '.jpg'
    options['filetypes'] = [('jpeg files', '.jpg'), ('text files', '.txt'), ('all files', '.*')]
    options['initialdir'] = 'C:\\'
    options['initialfile'] = 'myfile.txt'
    options['parent'] = root
    options['title'] = 'This is a title but choose a jpg file...'
    return tkFileDialog.askopenfile(mode='rb', **options)

def choosefile():
    options = {}
    options['defaultextension'] = '.jpg'
    options['filetypes'] = [('jpeg files', '.jpg'), ('text files', '.txt'), ('all files', '.*')]
    options['initialdir'] = 'C:\\'
    options['initialfile'] = 'myfile.txt'
    options['parent'] = root
    options['title'] = 'This is a title but choose a jpg file...'
    return tkFileDialog.askopenfilenames(**options)

def createthumb(infile):
        size = 128, 128
        outfile = os.path.splitext(infile)[0] + ".thumbnail.jpg"
        if infile != outfile:
            try:
                im = Image.open(infile)
                im.thumbnail(size)
                im.save(outfile, "JPEG")
            except IOError:
                print "cannot create thumbnail for", infile
        return outfile

def createthumblist(infilelist):
        for infile in infilelist:
            try:
                im = Image.open(infile)
                print infile, im.format, "%dx%d" % im.size, im.mode
            except IOError:
                pass

callcount = 0
longstr = "long "
callstr = ""
def btnact():
    global callcount
    callcount = callcount + 1
    global longstr
    longstr = longstr + "long "
    disp = "status update call count %d of a %s line." % (callcount,longstr)
    mystatus.config(text=disp)
    global callstr
    callmode = (callcount & 1)
    isfile = False
    isfilelen = 0
    if callmode == 0:
        filein = choosedir()
        callstr = " open folder with callmode %d " % callmode
    else:
        filein = choosefile()
        callstr = " open file with callmode %d " % callmode
        isfile = True
    if isfile:
        print "type of filein %s " % type(filein)
        if isinstance(filein, tuple):  # tuple of (default,select)
            print " is tuple %s " % str(filein)
            x,filein = filein
        print "type of filein %s " % type(filein)
        try:
            f = open(filein, "rb")
            img = f.read()
            isfilelen = len(img)
            f.close()
            ofile = createthumb(filein)
            createthumblist([filein, ofile])

            image22 = Image.open(ofile)
            photo22 = ImageTk.PhotoImage(image22)
            mylabel.config(image=photo22, border=14)
            mylabel.photo = photo22
        except:
            pass
    disp2 = " call count %d filein %s callstr %s file len %d" % (callcount, filein, callstr, isfilelen)
    mystatus.config(text=disp+disp2)

mybutton1 = Tw.Button(btnholderLine1, text="my button text", command=btnact)
mybutton1.pack(side=Tw.LEFT, padx=5, pady=5)
mybutton2 = Tw.Button(btnholderLine1, text="my button2 text dummy")
mybutton2.pack(side=Tw.LEFT, padx=5, pady=5)

mybutton2 = Tw.Button(btnholderLine2, text="my quit text", command=root.quit)
mybutton2.pack(padx=5, pady=5)

# menu bar
def menu_act():
    toproot.quit()
def menu_init():
    menubar = Tw.Menu(toproot)
    toproot.config(menu=menubar)
    
    fileMenu = Tw.Menu(menubar)
    fileMenu.add_command(label="Exit", command=menu_act)
    menubar.add_cascade(label="File", menu=fileMenu)

    editMenu = Tw.Menu(menubar)
    editMenu.add_command(label="Exit", command=menu_act)
    menubar.add_cascade(label="Edit", menu=editMenu)
menu_init()

root.mainloop()

if __name__ == '__main__':
    pass #main()  


#http://effbot.org/imagingbook/introduction.htm


