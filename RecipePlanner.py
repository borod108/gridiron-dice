from Tkinter import *  # We will want all of the methods/objects from Tkinter

import Tkinter  # All of the widgets that we will need
import Tkinter as tk  # Provides a shortcut for the Tkinter - not sure why we need all of
# this but it works for Python 2.7
from openpyxl import *  # Import Excel Library

#import os  Import os and sys libraries for file management
#import sys
#import tkMessageBox  # Needed to send message to the screen alerting the user about


# something

# ********************************************************************************************
# CLASS CODE
# -----------------------------------------------------------------------------
# Class Name:    RecipeLists
# Purpose:        This class contains methods and attributes that allow the user to select a
#                       recipe, or choose a random selection.  Ultimately, it will allow the user to 
#                       input an ingredient and a list of recipes using that ingredient will be 
#                      displayed
# Author:          Rick Burney
# Created:        02/1/2022
# Copyright:     (c) Rick 2022
# -----------------------------------------------------------------------------
class RecipeLists:

    # -----------------------------------------------------------------------------
    # Constructor Name:
    # Purpose:        Initialization for the RecipeLists class.  Controls the scope of certain attributes
    # Author:          Rick Burney
    # Created:        02/1/2022
    # Copyright:     (c) Rick 2022
    # -----------------------------------------------------------------------------
    def __init__(self, ws, ListOfPointers, SubList, LengthList, Index):

        self._ws = ws  # Entire recipe worksheet

        # List of pointers that define the start of each sublist
        self._ListOfPointers = ListOfPointers
        self._SubList = SubList  # User-selected recipe sublist
        self._EndRow = 0  # This is the row of 'End' of the recipe list.  Will be filled in by
        # SubListPointer

        self._LengthList = LengthList
        self.Index = Index  # Index used to select the recipe within the sublist

    # -----------------------------------------------------------------------------
    # Function Name:    SubListPointer
    # Purpose:               Parses through the entire recipe list and creates a list of pointers to a
    #                             "sublist" of recipes, e.g. pasta or chicken.  The pointer will index into the
    #                             EXCEL recipe list (row number) and the start of the sublist will be row+1
    # Author:                 Rick Burney
    # Created:                02/1/2022
    # Copyright:            (c) Rick 2022
    # -----------------------------------------------------------------------------
    def SubListPointer(self):

        # Initialize the sublist pointer to 1
        SLPointer = 1

        # Until the end of the recipe list is reached, read in a row and see if the column 2 cell has a
        # non-empty value.  If so, this cell contains the category of the sublist (e.g. "Appetizers") and
        # the row is the pointer value that is appended to the pointer list for each of the recipe
        # sublists
        i = 0  # Row index
        while self._ws.cell(row=SLPointer, column=2).value != "End":
            if self._ws.cell(row=SLPointer, column=2).value != None:
                self._ListOfPointers.append(SLPointer)  # add pointer to list
            SLPointer += 1  # Go to the next row
            i += 1  # Increment the row pointer
        self._EndRow = i
        self._ListOfPointers.append(self._EndRow)  # Append the End row to the List of pointers
        return self._ListOfPointers  # return the list of pointers

    # -----------------------------------------------------------------------------
    # Function Name:    ListLengths
    # Purpose:               Creates a list of the number of recipes in each of the recipe sublists
    # Author:                 Rick Burney
    # Created:                02/1/2022
    # Copyright:            (c) Rick 2022
    # -----------------------------------------------------------------------------
    def ListLengths(self):

        # Go through _ListOfPointers (for x in list)
        LOPlength = len(self._ListOfPointers) - 1  # Takes into account the End row

        # Compute the lengths of each sublist and return the length list.  The list length is actually 1
        # less than computed since the sublist starts one row below the heading
        for i in range(0, LOPlength):
            ListLength = self._ListOfPointers[i + 1] - self._ListOfPointers[i] - 1
            self._LengthList.append(ListLength)
        return self._LengthList

    # Growth Option - Consider a method that actually creates the sublists after which we can
    # retire the length list

    # -----------------------------------------------------------------------------
    # Function Name:    DisplayList
    # Purpose:               Displays the sublist of recipes that was chosen by the user.  The display
    #                             is a listbox from which the user can select a single recipe.
    # Author:                 Rick Burney
    # Created:                02/1/2022
    # Copyright:            (c) Rick 2022
    # -----------------------------------------------------------------------------
    def DisplayList(self):

        print(Index)

    # -----------------------------------------------------------------------------
    # Function Name:    Exclusions
    # Purpose:               Recompiles the sublist into a master list but some sublists are excluded.
    #                             This allows the user to make a random selection across all of the lists
    #                             but say for dinner, we don't want a beverage to be chosen as the main
    #                             course
    # Author:                 Rick Burney
    # Created:                02/18/2022
    # Copyright:            (c) Rick 2022
    # -----------------------------------------------------------------------------
    def Exclusions(self):

        # The following pointers will be used to build the Entree List
        # 1  = Barbecue
        # 2  = Beef
        # 5  = Chicken
        # 12 = Fish
        # 14 = Indian
        # 15 = Instant Pot
        # 17 = Mexican
        # 18 = Middle Eastern
        # 19 = Miscellaneous
        # 21 = Pasta
        # 22 = Pork
        # 23 = Potatoes
        # 24 = Rice/Risotto
        # 25 = Salad
        # 29 = Seafood
        # 30 = Soup
        # 31 = Stuffing
        # 32 = Turkey
        # 33 = Vegetables

        EntreeList = []  # Start with an empty list

        EntreePointers = [1, 2, 5, 12, 14, 15, 17, 18, 19, 21, 22, 23, 24, 25, 29, 30, 31, 32,
                          33]  # Entree list pointers
        for x in EntreePointers:
            SubList = []  # Start with an empty sublist
            row = self._ListOfPointers[x] + 1  # ID the first row of the sublist
            lastrow = row + self._LengthList[x]  # ID the last row of the sublist
            for i in range(row, lastrow):  # Populate the sublist
                SubList.append(ws.cell(row=i, column=3).value)
            EntreeList += SubList  # Combine sublists
        return EntreeList

    # -----------------------------------------------------------------------------
    # Function Name:    RandomSelect
    # Purpose:               Makes a random selection within either a sublist or the reconstructed
    #                             list
    # Author:                 Rick Burney
    # Created:                02/1/2022
    # Copyright:            (c) Rick 2022
    # -----------------------------------------------------------------------------
    def RandomSelect(self):

        print()

    # -----------------------------------------------------------------------------
    # Function Name:    DisplaySelection
    # Purpose:               Displays the selected recipe in a field.  Ultimately, a link to the recipe
    #                              will be provided
    # Author:                 Rick Burney
    # Created:                02/1/2022
    # Copyright:            (c) Rick 2022
    # -----------------------------------------------------------------------------
    def DisplaySelection(self):

        print()

        # CLASS CODE


# ********************************************************************************************


# -----------------------------------------------------------------------------
# Function Name:    PopulateListBox
# Purpose:               When any button is pressed, the list of pointers, sublist length list and 
#                             an index is passed in.  This callback function pulls out the recipe sublist 
#                             from the main recipe list
# Author:                 Rick Burney
# Created:                02/16/2022
# Copyright:            (c) Rick 2022
# -----------------------------------------------------------------------------
def PopulateListBox(SubList):
    global Mainlb  # Listboxes need to be global
    global Overflowframelb
    global MaxNumListBoxEntries  # If exceeded, spill into the next listbox, and then the next
    global Overflowframelb1
    global SelectedOption

    Mainlb.delete(0, END)  # First, clear the listboxes
    Overflowframelb.delete(0, END)
    Overflowframelb1.delete(0, END)

    # Case of number of listbox elements <= MaxNumListBoxEntries
    if len(SubList) <= MaxNumListBoxEntries:
        for i in range(0, len(SubList)):  # Populate listbox with selected sublist
            Mainlb.insert(i, SubList[i])

    # Case of number of listbox elements <= 2*MaxNumListBoxEntries
    elif len(SubList) <= 2 * MaxNumListBoxEntries:
        for i in range(0, MaxNumListBoxEntries):  # Populate two listboxes
            Mainlb.insert(i, SubList[i])
        for i in range(MaxNumListBoxEntries, len(SubList)):
            Overflowframelb.insert(i, SubList[i])

    # Case of number of listbox elements > 2*MaxNumListBoxEntries
    else:
        for i in range(0, MaxNumListBoxEntries):  # Populate three listboxes
            Mainlb.insert(i, SubList[i])
        for i in range(MaxNumListBoxEntries, 2 * MaxNumListBoxEntries):
            Overflowframelb.insert(i, SubList[i])
        for i in range(2 * MaxNumListBoxEntries, len(SubList)):
            Overflowframelb1.insert(i, SubList[i])


# -----------------------------------------------------------------------------
# Function Name:    go
# Purpose:               Processes the main listbox "double-click" selection
# Author:                 Rick Burney
# Created:                02/16/2022
# Copyright:            (c) Rick 2022
# -----------------------------------------------------------------------------
def go(event):
    global Mainlb           # Listboxes need to be global
    global MainlbSelection  # Listbox selections need to be global
    global SelectedOption   # Selected Option Label

    Mainlbcs = Mainlb.curselection()                # Select a recipe from the sublist
    MainlbSelection = Mainlb.get(Mainlbcs)          # This actually retrieves the listbox selection for further use
    SelectedOption.config(text=MainlbSelection)     # Write the selection to the selection field (label)


# -----------------------------------------------------------------------------
# Function Name:    go1
# Purpose:               Processes the first overflow listbox "double-click" selection.  Only allowing 64 items per lbox
# Author:                 Rick Burney
# Created:                02/16/2022
# Copyright:            (c) Rick 2022
# -----------------------------------------------------------------------------
def go1(event):
    global Overflowframelb              # Listboxes need to be global
    global OverflowframelbSelection     # Listbox selections need to be global
    global SelectedOption               # Selected Option Label

    Overflowframelbcs = Overflowframelb.curselection()                  # Select a recipe from the sublist
    OverflowframelbSelection = Overflowframelb.get(Overflowframelbcs)
    SelectedOption.config(text=OverflowframelbSelection)  # Write  selection to field


# -----------------------------------------------------------------------------
# Function Name:    go2
# Purpose:               Processes the first overflow listbox "double-click" selection
# Author:                 Rick Burney
# Created:                02/16/2022
# Copyright:            (c) Rick 2022
# -----------------------------------------------------------------------------
def go2(event):
    global Overflowframelb1  # Listboxes need to be global
    global Overflowframelb1Selection  # Listbox selections need to be global
    global SelectedOption  # Selected Option Label

    Overflowframelb1cs = Overflowframelb1.curselection()  # Select recipe from the sublist
    Overflowframelb1Selection = Overflowframelb1.get(Overflowframelb1cs)
    SelectedOption.config(text=Overflowframelb1Selection)  # Write  selection to field


# -----------------------------------------------------------------------------
# Function Name:    ButtPress
# Purpose:               When any button is pressed, the list of pointers, sublist length list and 
#                             an index is passed in.  This callback function pulls out the recipe sublist 
#                             from the main recipe list
# Author:                 Rick Burney
# Created:                02/16/2022
# Copyright:            (c) Rick 2022
# -----------------------------------------------------------------------------
def ButtPress(ws, ListOfPointers, LOP, Index):
    global SubList

    SubList = []  # Start with an empty sublist
    row = ListOfPointers[Index] + 1  # ID the first row of the sublist
    lastrow = row + LOP[Index]  # ID the last row of the sublist
    for i in range(row, lastrow):  # Populate the sublist
        SubList.append(ws.cell(row=i, column=3).value)
    PopulateListBox(SubList)


# -----------------------------------------------------------------------------
# Function Name:    RandSelect
# Purpose:               When any button is pressed, the list of pointers, sublist length list and 
#                             an index is passed in.  This callback function pulls out the recipe sublist 
#                             from the main recipe list
# Author:                 Rick Burney
# Created:                02/18/2022
# Copyright:            (c) Rick 2022
# -----------------------------------------------------------------------------
def RandSelect():
    import random  # Used for a random selection of a SubList

    global SubList
    global SelectedOption  # Selected Option Label

    NumberOfRecipes = len(SubList)
    SelectedRecipe = SubList[random.randint(0, NumberOfRecipes - 1)]
    SelectedOption.config(text=SelectedRecipe)  # Write  selection to field


# -----------------------------------------------------------------------------
# Function Name:    SurpriseMe
# Purpose:               When any button is pressed, the list of pointers, sublist length list and 
#                             an index is passed in.  This callback function pulls out the recipe sublist 
#                             from the main recipe list
# Author:                 Rick Burney
# Created:                02/18/2022
# Copyright:            (c) Rick 2022
# -----------------------------------------------------------------------------
def SurpriseMe():
    import random  # Used for a random selection of an entree

    global EntreeList
    global SelectedOption  # Selected Option Label

    NumberOfRecipes = len(EntreeList)
    SelectedRecipe = EntreeList[random.randint(0, NumberOfRecipes - 1)]
    SelectedOption.config(text=SelectedRecipe)  # Write  selection to field


# -----------------------------------------------------------------------------
# Function Name:    NonDairyIceCreamSelect
# Purpose:               Going to a different worksheet on the recipe workbook, select a non-dairy ice cream.
#                             Remember to switch back to the main recipe worksheet.  This will populate the Sublist
#                             with non-dairy ice cream selections and then the user needs to use the RandSelect()
#                             function to make a random selection.  Or, they can simply make a manual selection.
# Author:                 Rick Burney
# Created:                02/21/2022
# Copyright:            (c) Rick 2022
# -----------------------------------------------------------------------------
def NonDairyIceCreamSelect(wb):
    global SubList
    global SelectedOption  # Selected Option Label

    SubList = []  # Clear list

    ws = wb["Ice Creams"]  # Activate Non-Dairy Ice Cream Worksheet.  Sheet 2


    # Read in list of recipes, keying on the "End"
    i = 1  # Row index
    while ws.cell(row=i, column=1).value != "End":  # Until "End" is reached
        SubList.append(ws.cell(row=i, column=2).value)  # Build Sublist
        i += 1
    ws = wb["On the Computer"]  # Activate the main worksheet
    PopulateListBox(SubList)  # Display the Sublist


# -----------------------------------------------------------------------------
# Function Name:    QuitApp
# Purpose:               Exits the App
# Author:                 Rick Burney
# Created:                01/27/2022
# Copyright:            (c) Rick 2022
# -----------------------------------------------------------------------------
def QuitApp():
    global wb  # Easier if this is global so workbook can be closed without having to be passed in

    root.destroy()  # Quit the application


def TestPrintSublist():
    global SubList


# ***************************MAIN LOOP****************************************

# Program starts here.  To initialize tkinter, we have to create a Tk root widget, which is a window with a
# title bar and other decoration provided by the window manager. The root widget has to be created before
# any other widgets and there can only be one root widget.
root = Tkinter.Tk()

# Have the display grab the focus.  Commented this out.  Delete on 6/4/2022
#os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

root.geometry("2000x1350")  # Set size of window (width x height)
root.config(bg="skyblue")  # Specify a background color

# root.configure(background='red')   #Set main window background to grey.  DELETE on 3/28

leftframe = Frame(root, height=200, width=400, bg='grey')  # Create the left window frame
leftframe.grid(row=0, column=0, padx=10, pady=5)  # Place the left frame
rightframe = Frame(root, height=200, width=400, bg='grey')  # Create the right window frame
rightframe.grid(row=0, column=1, padx=10, pady=5)

ButtonWidth = 16
MaxNumListBoxEntries = 64

# Appetizer Button.  This button selects appetizer recipes
AppetizerButton = Tkinter.Button(leftframe, text="Appetizers",
                                 command=lambda: ButtPress(ws, ListOfPointers, LOP, 0),
                                 width=ButtonWidth, justify=CENTER, padx=10)
AppetizerButton.grid(column=0, row=0)

# Barbecue Button.  This button selects barbecue recipes
BarbecueButton = Tkinter.Button(leftframe, text="Barbecue",
                                command=lambda: ButtPress(ws, ListOfPointers, LOP, 1), width=ButtonWidth,
                                justify=CENTER, padx=10)
BarbecueButton.grid(column=0, row=1)

# Beef Button.  This button selects beef recipes
BeefButton = Tkinter.Button(leftframe, text="Beef", command=lambda: ButtPress(ws, ListOfPointers, LOP, 2),
                            width=ButtonWidth, justify=CENTER, padx=10)
BeefButton.grid(column=0, row=2)

# Breads Button.  This button selects bread recipes
BreadsButton = Tkinter.Button(leftframe, text="Breads",
                              command=lambda: ButtPress(ws, ListOfPointers, LOP, 3), width=ButtonWidth,
                              justify=CENTER, padx=10)
BreadsButton.grid(column=0, row=3)

# Breakfast Button.  This button selects breakfast recipes
BreakfastButton = Tkinter.Button(leftframe, text="Breakfast",
                                 command=lambda: ButtPress(ws, ListOfPointers, LOP, 4), width=ButtonWidth,
                                 justify=CENTER, padx=10)
BreakfastButton.grid(column=0, row=4)

# Chicken Button.  This button selects chicken recipes
ChickenButton = Tkinter.Button(leftframe, text="Chicken",
                               command=lambda: ButtPress(ws, ListOfPointers, LOP, 5), width=ButtonWidth,
                               justify=CENTER, padx=10)
ChickenButton.grid(column=0, row=5)

# Condiments Button.  This button selects condiments recipes
CondimentsButton = Tkinter.Button(leftframe, text="Condiments",
                                  command=lambda: ButtPress(ws, ListOfPointers, LOP, 6), width=ButtonWidth,
                                  justify=CENTER, padx=10)
CondimentsButton.grid(column=0, row=6)

# Cookie Button.  This button selects cookie recipes
CookieButton = Tkinter.Button(leftframe, text="Cookies",
                              command=lambda: ButtPress(ws, ListOfPointers, LOP, 7), width=ButtonWidth,
                              justify=CENTER, padx=10)
CookieButton.grid(column=0, row=7)

# Dessert Button.  This button selects dessert recipes
DessertButton = Tkinter.Button(leftframe, text="Dessert",
                               command=lambda: ButtPress(ws, ListOfPointers, LOP, 8), width=ButtonWidth,
                               justify=CENTER, padx=10)
DessertButton.grid(column=0, row=8)

# Drinks Button.  This button selects drink recipes
DrinkButton = Tkinter.Button(leftframe, text="Drinks",
                             command=lambda: ButtPress(ws, ListOfPointers, LOP, 10), width=ButtonWidth,
                             justify=CENTER, padx=10)
DrinkButton.grid(column=0, row=9)

# Eggs Button.  This button selects egg recipes
EggButton = Tkinter.Button(leftframe, text="Eggs",
                           command=lambda: ButtPress(ws, ListOfPointers, LOP, 11), width=ButtonWidth,
                           justify=CENTER, padx=10)
EggButton.grid(column=0, row=10)

# Fish Button.  This button selects fish recipes
FishButton = Tkinter.Button(leftframe, text="Fish",
                            command=lambda: ButtPress(ws, ListOfPointers, LOP, 12), width=ButtonWidth,
                            justify=CENTER, padx=10)
FishButton.grid(column=0, row=11)

# Indian Food Button.  This button selects Indian food recipes
IndianFoodButton = Tkinter.Button(leftframe, text="Indian Food",
                                  command=lambda: ButtPress(ws, ListOfPointers, LOP, 14), width=ButtonWidth,
                                  justify=CENTER, padx=10)
IndianFoodButton.grid(column=0, row=12)

# Instant Pot Button.  This button selects Instant Pot recipes
InstantPotButton = Tkinter.Button(leftframe, text="Instant Pot",
                                  command=lambda: ButtPress(ws, ListOfPointers, LOP, 15), width=ButtonWidth,
                                  justify=CENTER, padx=10)
InstantPotButton.grid(column=0, row=13)

# Mexican food Button.  This button selects Mexican food recipes
MexicanFoodButton = Tkinter.Button(leftframe, text="Mexican food",
                                   command=lambda: ButtPress(ws, ListOfPointers, LOP, 17), width=ButtonWidth,
                                   justify=CENTER, padx=10)
MexicanFoodButton.grid(column=0, row=14)

# Middle Eastern food Button.  This button selects Middle Eastern food recipes
MiddleEasternFoodButton = Tkinter.Button(leftframe, text="Middle Eastern food",
                                         command=lambda: ButtPress(ws, ListOfPointers, LOP, 18), width=ButtonWidth,
                                         justify=CENTER, padx=10)
MiddleEasternFoodButton.grid(column=0, row=15)

# Miscellaneous food Button.  This button selects miscellaneous food recipes
MiscFoodButton = Tkinter.Button(leftframe, text="Miscellaneous food",
                                command=lambda: ButtPress(ws, ListOfPointers, LOP, 19), width=ButtonWidth,
                                justify=CENTER, padx=10)
MiscFoodButton.grid(column=0, row=16)

# Pasta Button.  This button selects pasta recipes
PastaButton = Tkinter.Button(leftframe, text="Pasta",
                             command=lambda: ButtPress(ws, ListOfPointers, LOP, 21), width=ButtonWidth,
                             justify=CENTER, padx=10)
PastaButton.grid(column=0, row=17)

# Pork Button.  This button selects pork recipes
PorkButton = Tkinter.Button(leftframe, text="Pork",
                            command=lambda: ButtPress(ws, ListOfPointers, LOP, 22), width=ButtonWidth,
                            justify=CENTER, padx=10)
PorkButton.grid(column=0, row=18)

# Potato Button.  This button selects potato recipes
PotatoButton = Tkinter.Button(leftframe, text="Potato",
                              command=lambda: ButtPress(ws, ListOfPointers, LOP, 23), width=ButtonWidth,
                              justify=CENTER, padx=10)
PotatoButton.grid(column=0, row=19)

# Rice Button.  This button selects rice and risotto recipes
RiceButton = Tkinter.Button(leftframe, text="Rice/Risotto",
                            command=lambda: ButtPress(ws, ListOfPointers, LOP, 24), width=ButtonWidth,
                            justify=CENTER, padx=10)
RiceButton.grid(column=0, row=20)

# Salad Button.  This button selects salad recipes
SaladButton = Tkinter.Button(leftframe, text="Salad",
                             command=lambda: ButtPress(ws, ListOfPointers, LOP, 25), width=ButtonWidth,
                             justify=CENTER, padx=10)
SaladButton.grid(column=0, row=21)

# Sandwich Button.  This button selects sandwich recipes
SandwichButton = Tkinter.Button(leftframe, text="Sandwich",
                                command=lambda: ButtPress(ws, ListOfPointers, LOP, 27), width=ButtonWidth,
                                justify=CENTER, padx=10)
SandwichButton.grid(column=0, row=22)

# Seafood Button.  This button selects seafood recipes
SeafoodButton = Tkinter.Button(leftframe, text="Seafood",
                               command=lambda: ButtPress(ws, ListOfPointers, LOP, 29), width=ButtonWidth,
                               justify=CENTER, padx=10)
SeafoodButton.grid(column=0, row=23)

# Soup Button.  This button selects soup recipes
SoupButton = Tkinter.Button(leftframe, text="Soup",
                            command=lambda: ButtPress(ws, ListOfPointers, LOP, 30), width=ButtonWidth,
                            justify=CENTER, padx=10)
SoupButton.grid(column=0, row=24)

# Stuffing Button.  This button selects stuffing recipes
StuffingButton = Tkinter.Button(leftframe, text="Stuffing",
                                command=lambda: ButtPress(ws, ListOfPointers, LOP, 31), width=ButtonWidth,
                                justify=CENTER, padx=10)
StuffingButton.grid(column=0, row=25)

# Turkey Button.  This button selects turkey recipes
TurkeyButton = Tkinter.Button(leftframe, text="Turkey",
                              command=lambda: ButtPress(ws, ListOfPointers, LOP, 32), width=ButtonWidth,
                              justify=CENTER, padx=10)
TurkeyButton.grid(column=0, row=26)

# Vegetables Button.  This button selects vegetable recipes
VeggiesButton = Tkinter.Button(leftframe, text="Vegetables",
                               command=lambda: ButtPress(ws, ListOfPointers, LOP, 33),
                               width=ButtonWidth, justify=CENTER, padx=10)
VeggiesButton.grid(column=0, row=27)

# Quit Button.  This wraps everything up and quits the app.
QuitButton = Tkinter.Button(leftframe, text="Quit", command=QuitApp, width=ButtonWidth,
                            justify=CENTER, padx=10)
QuitButton.grid(column=0, row=28)

# Define a listbox to display the chosen sublist.  The listbox has a maximum height so lists that exceed the
# height will be continued in an additional overflow frame and in some cases, there will be a second
# overflow frame
Mainlb = tk.Listbox(rightframe, height=64, width=50)  # Define the main listbox widget
Mainlb.bind('<Double-1>', go)  # Bind the mouse double-click to this listbox
Mainlb.grid(row=0, column=1)  # Place the listbox in the grid

# Define a listbox to display sublist overflows
Overflowframelb = tk.Listbox(rightframe, height=64, width=50)
Overflowframelb.bind('<Double-1>', go1)
Overflowframelb.grid(row=0, column=2)

# Define a 2nd listbox to display sublist overflows
Overflowframelb1 = tk.Listbox(rightframe, height=64, width=50)
Overflowframelb1.bind('<Double-1>', go2)
Overflowframelb1.grid(row=0, column=3)

# Random Sublist Selection Button.  After a sublist is chosen, randomly select a recipe from within
RandomSubListSelectionButton = Tkinter.Button(leftframe, text="Random Selection",
                                              command=RandSelect, width=ButtonWidth, justify=CENTER,
                                              padx=10, pady=10)
RandomSubListSelectionButton.grid(column=0, row=29)

# Random Entree List Selection Button.  After a sublist is chosen, randomly select a recipe from within
EntreeSurpriseButton = Tkinter.Button(leftframe, text="Entree Surprise",
                                      command=SurpriseMe, width=ButtonWidth, justify=CENTER,
                                      padx=10, pady=10)
EntreeSurpriseButton.grid(column=0, row=30)

# Non-dairy ice cream selection
NonDairyIceCreamButton = Tkinter.Button(leftframe, text="Non-Dairy Ice Cream",
                                        command=lambda: NonDairyIceCreamSelect(wb), width=ButtonWidth,
                                        justify=CENTER, padx=10, pady=10)
NonDairyIceCreamButton.grid(column=0, row=31)

# Creating Edit box to show selected option
SelectedOption = Label(rightframe, text='Recipe Selection', height=4, width=50, wraplength=384)
SelectedOption.grid(row=0, column=4)

wb = load_workbook(filename="RecipeList.xlsx")  # Load recipe list which is an EXCEL file
wb.active = 0  # Activate sheet 1 with the recipes
ws = wb.active

ListOfPointers = []  # These are the pointers to the recipe sublist rows.  Start with an empty
# list
SubList = []  # This will be a selected recipe sublist
Index = 0  # Initialize the index that selects the recipe within a sublist

# List that contains the length of each sublist.  Once sublists are created, the len function can
# be used to determine list lengths
LengthList = []

# Instantiate a RecipeList class object
RecipeList = RecipeLists(ws, ListOfPointers, SubList, LengthList, Index)

ListOfPointers = RecipeList.SubListPointer()  # Extract the row pointers
LOP = RecipeList.ListLengths()  # Determine # of recipes in each sublist
EntreeList = RecipeList.Exclusions()  # Compile an entree list
# for x in range(0,len(EntreeList)):
# print(EntreeList[x])


# The condition if __name__ == '__main__' is used in a Python program to execute the code
# inside the if statement only when the program is executed directly by the Python
# interpreter. When the code in the file is imported as a module the code inside the if
# statement is not executed.
if __name__ == "__main__":
    root.mainloop()  # lets Tkinter start running the application
