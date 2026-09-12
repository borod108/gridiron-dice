#-----------------------------------------------------------------------------
# Name:        MyListBox
# Purpose:     Generic Listbox class.  Parent window and list are passed in
#
# Author:      Rick
#
# Created:     11/14/2016
# Copyright:   (c) Rick 2016
# Licence:     <your licence>
#-----------------------------------------------------------------------------

import Tkinter as tk

class MyListBox(object):
    def __init__(self, teamlist, parent,col):

        self.value = ""         #Initialize the listbox return value
        self.listframe = parent
        names = tk.StringVar(value=teamlist) #bind choices into a stringVar

#Label the listbox
        label = tk.Label(self.listframe, text="Pick a team:")
 
 #Add a scrollbar to the listbox       
        scrollbar = tk.Scrollbar(self.listframe)
        scrollbar.pack(side="right",fill = "y")
        

#Create the listbox
        self.listbox = tk.Listbox(self.listframe, listvariable=names, 
                                  height=8,selectmode="single", 
                                  exportselection=0)
#        

#Add a button to close the list box
        button = tk.Button(self.listframe, text="OK", 
                           command=self.listframe.destroy)


        label.pack(side="top", fill="x")        #Label goes on top
        self.listbox.pack(side="top", fill="x") #Display listbox
        
        button.pack()                           #Display button
        
        self.listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # add binding
        self.listbox.bind('<<ListboxSelect>>', self.getSelection)

    # function associated with binding
    def getSelection(self, event):
        widget = event.widget               #widget in this case is a listbox
        selection=widget.curselection()     #Get index of selected item

        self.value = widget.get(selection[0])   #get value of selected item
     

    # separate function for wait_window and the return of the selection
    def returnValue(self):
        self.listframe.wait_window()    #Wait until listbox is closed
        return self.value               #Return item selected from the listbox

 
