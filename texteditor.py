from tkinter import Tk, scrolledtext, Menu , filedialog, END, messagebox, simpledialog, Text, PhotoImage, Wm, Image
from pathlib import Path
import os
from functools import partial
# Root for Main Window
root = Tk(className= 'Text Editor')
textArea = scrolledtext.ScrolledText(root, width = 100, height = 80, undo = True, maxundo = -1, fg="black")
#Setting Icon
iconpath= Path.cwd() / 'icons' / 'te.gif'
ticon =  Image('photo', file=str(iconpath))
icon= PhotoImage(str(iconpath))
root.tk.call('wm','iconphoto',root._w, ticon)
prevFile = None


# Functions
def newFile():
    if len(textArea.get('1.0', END+'-1c')) > 0:
        if messagebox.askyesno("Save?", "Do you wish to save?"):
            saveFile()
            fileSaved=True
            if fileSaved==True:
                textArea.delete('1.0' , END)
                fileSaved=False
        else:
            textArea.delete('1.0' , END)

def openFile():
    textArea.delete('1.0' , END)
    file = filedialog.askopenfile(parent=root, mode= 'rb', title="select a text file", filetypes=(("Text File", "*.txt"),("All files", "*.*")))
    global prevFile
    prevFile = file.name
    if file != None:
        contents = file.read()
        textArea.insert('1.0', contents)
        file.close()

def saveFile():
    global prevFile
    if prevFile != None:
        file = open(prevFile, 'w')
        data = textArea.get('1.0', END+'-1c')
        file.write(data)
        file.close()
    else:
        file = filedialog.asksaveasfile(mode= 'w', defaultextension= ".txt", filetypes=(("HTML File", "*.html"),("Text File", "*.txt"),("All files", "*.*")))
        if file != None:
            data = textArea.get('1.0', END+'-1c')
            file.write(data)
            prevFile = file.name 
            file.close()

def FindInFile():
    findString = simpledialog.askstring("Find...", "Enter Text")
    textData = textArea.get('1.0', END)
    occurances = textData.upper().count(findString.upper())
   
    if textData.upper().count(findString.upper()) > 0:
       messagebox.showinfo("Results", findString + " has multiple occurances, " + str(occurances))
    else:
       messagebox.showinfo("Results", "I've got nothing for you, sorry about that")

def UndoThing():
    Text.edit_undo(textArea)
def RedoThing():
    Text.edit_redo(textArea)

def printFile():
    os.startfile(prevFile, 'print')
def Exit():
    if messagebox.askyesno('Quit', "Are you sure you want to exit the program?"):
        if messagebox.askyesno("Save?", "Do you wish to save?"):
            saveFile()
            fileSaved=True
            if fileSaved==True:
                root.destroy()
                fileSaved=False
        else:
            root.destroy()

def about():
    messagebox.showinfo('About', ("A python Text editor by DiogoTheCoder\n Modified by CobaltGold\n\nPrint command only available in Windows OS"))

def count():
    textData= len(textArea.get('1.0', END).strip())
    messagebox.showinfo('Number of Words', "There are "+str(textData/5)+" words in this file")
# Menu Options
menu = Menu(root)
root.config(menu=menu)
fileMenu = Menu(menu)
menu.add_cascade(label = 'File', menu=fileMenu)
fileMenu.add_command(label = 'New', command=newFile)
fileMenu.add_command(label = 'Open', command=openFile)
fileMenu.add_command(label = 'Save', command=saveFile)
fileMenu.add_command(label = 'Find', command=FindInFile)
fileMenu.add_command(label = 'Print', command=printFile)
fileMenu.add_separator()
fileMenu.add_command(label = 'Exit', command=Exit)

helpMenu = Menu(menu)
menu.add_cascade(label= 'Help')
menu.add_cascade(label= 'About', command=about)

editMenu = Menu(menu)
menu.add_cascade(label= 'Edit', menu=editMenu)
editMenu.add_command(label = 'Undo', command=UndoThing)
editMenu.add_command(label = 'Redo', command=RedoThing)
editMenu.add_separator()
editMenu.add_command(label= 'Word Count', command=count)
textArea.pack()

# Keeps window open
root.mainloop()