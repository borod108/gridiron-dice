import Tkinter


#-----------------------------------------------------------------------------
# Class Name:    SelectTeamsPanel
# Purpose:          Presents a panel to the user that allows for the selection
#                   of teams.  Will be expanded in Rev 3 to incorporate
#                   features such as injuries and statistics updates
# Inputs            root - The parent frame
# Author:           Rick Burney
#
# Created:          6/27/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
class SelectTeamsPanel(Tkinter.Frame):
    
    def __init__(self,root):
        
        import collections  #collections allows for ordered dictionaries
        #import tkFont
        import Tkinter
        import tkMessageBox                   #Using messages boxes for debug
        from Tkinter import Frame, Tk, Button 
        from Tkinter import LEFT    #Allows left justification of  
                                    #checkbutton text

        x = 20              #Starting coordinates of the checkbuttons
        PAC12Label_x = 20   #Where to place this label
        PAC12Label_y = 20
        ystart = 45
        y = ystart
        xincrement = 250     #Horizontal pixels between checkbutton columns
        yincrement = 25     #Vertical pitch of the checkbuttons
        CheckBoxWidth = 20  #Width of the checkbuttons
        
        self.TeamSelected = "No Team Selected"
        self.HomeTeamSelected = "yyyyy"
        self.cbget = 0
        self.rbget = "z"
        self.FullNameoftheTeamSelected  = ""
        
        Independents_x = PAC12Label_x + xincrement
        Big12_x = PAC12Label_x + 2*xincrement
        MAC_x = PAC12Label_x + 3*xincrement
        PAC12RB_x = PAC12Label_x + 4*xincrement
        
        

#Allows us to use the parent window across the methods        
        self.root = root
        
#Create the panel and place over the Control Panel window
        self.Panel = Frame(self.root,  height = 600, width = 1350, 
                           bg = "black")
        self.Panel.place(x = 0, y = 0)
        
        self.variables = {} #Initialize checkbox variables
        self.ListofCheckButtons = []
        
#Button that closes the panel.  Note that using "self" in front of the command
#allows the command processing to be a method within this class.  Use self to
#access other methods in this class!!!!
        KButton = Button(self.Panel,text = "Close", 
                         command = self.KillButton)
        KButton.place(x=1200,y = 500)
       

#Button accepts the home team selection.
        AHTButton = Button(self.Panel,text = "Accept Home Team Selection", 
                           command = self.AcceptHomeTeamSelectionButton)
        AHTButton.place(x=800, y = 500)


#Create an ordered dictionary of the PAC-12 teams and their acronyms.  The
#acronyms are used to access the team worksheets
        self.PAC12Teams = [('Arizona State',"ASU"),('Arizona',"AZ"),
                               ('California',"Cal"),('Colorado',"CO"),
                               ('Oregon State',"ORST"),('Stanford',"Stan"),
                               ('UCLA',"UCLA"),('USC',"USC"),
                               ('Utah',"Utah"),('Washington State',"WSU")] 
        self.PAC12TeamsAtoZ = collections.OrderedDict(self.PAC12Teams)

#Create an ordered dictionary of the independent teams and teams from other 
#conferences (only one team per conference for now) and their acronyms.  
#The acronyms are used to access the team worksheets
        self.IndependentTeams = [('Notre Dame',"ND")] 
        self.IndependentTeamsAtoZ = \
            collections.OrderedDict(self.IndependentTeams)
        self.Big12Teams = [('Texas',"TEX")] 
        self.Big12TeamsAtoZ = \
            collections.OrderedDict(self.Big12Teams)
        self.MACTeams = [('Western Michigan',"WMU")] 
        self.MACTeamsAtoZ = \
            collections.OrderedDict(self.MACTeams)
        
#Create the PAC-12 heading.  
        PAC12Label = Tkinter.Label(self.Panel, text="PAC-12", width=10,
                                            height=1,fg="white",bg="black",
                                            font=("Helvetica bold", 
                                            16)).place(x = PAC12Label_x,
                                                       y = PAC12Label_y)
#Create the Indepedents heading.  
        IndependentLabel = Tkinter.Label(self.Panel, text="Independents", 
                                         width=15,height=1,fg="white",
                                         bg="black",font=("Helvetica bold", 
                                        16)).place(x = Independents_x,
                                                       y = PAC12Label_y)
#Create the Big-12 heading.  
        Big12Label = Tkinter.Label(self.Panel, text="Big-12", 
                                         width=15,height=1,fg="white",
                                         bg="black",font=("Helvetica bold", 
                                        16)).place(x=Big12_x,
                                                       y = PAC12Label_y)
#Create the MAC heading.  
        MACLabel = Tkinter.Label(self.Panel, text="MAC", 
                                         width=15,height=1,fg="white",
                                         bg="black",font=("Helvetica bold", 
                                        16)).place(x = MAC_x,
                                                       y = PAC12Label_y)
        
#The following is how you loop through a dictionary.  Team is the instance.
#self.PAC12TeamsAtoZ is the ordered dictionary.  For each instance, create a
#checkbutton that is placed below the previous one.  Team is the checkbutton 
#text and is the name of the team as the for loops moves through the ordered
#dictionary.  Each pass through the loop creates a new checkbox variable that
#holds the state of the checkbox.  When the user checks or unchecks a checkbox
#a routine that retrieves the state of the appropriate checkbox is called

        for Team in self.PAC12TeamsAtoZ:
            self.variables[Team] = Tkinter.IntVar()
            Team1CheckBox = Tkinter.Checkbutton(self.Panel, text=Team,
                          variable = self.variables[Team],
                          command=self.oncheck(Team,self.PAC12TeamsAtoZ[Team]),
                          width=CheckBoxWidth,
                          justify = LEFT)
            Team1CheckBox.place(x = x, y = y)
            y += yincrement
            self.ListofCheckButtons.append(self.variables[Team])

        y = ystart          #reset y position of checkbuttons
        
#Loop through the independents although for now, there is only one team.
        for Team in self.IndependentTeamsAtoZ:
            self.variables[Team] = Tkinter.IntVar()
            Team1CheckBox = Tkinter.Checkbutton(self.Panel, text=Team,
                          variable = self.variables[Team],
                          command=self.oncheck(Team,self.IndependentTeamsAtoZ[Team]),
                          width=CheckBoxWidth,
                          justify = LEFT)
            Team1CheckBox.place(x = Independents_x, y = y)
            
            y += yincrement
            self.ListofCheckButtons.append(self.variables[Team])


        y = ystart          #reset y position of checkbuttons

        
#Loop through the Big-12 teams although for now, there is only one team.
        for Team in self.Big12TeamsAtoZ:
            self.variables[Team] = Tkinter.IntVar()
            Team1CheckBox = Tkinter.Checkbutton(self.Panel, text=Team,
                          variable = self.variables[Team],
                          command=self.oncheck(Team,self.Big12TeamsAtoZ[Team]),
                          width=CheckBoxWidth,
                          justify = LEFT)
            Team1CheckBox.place(x = Big12_x, y = y)
            
            y += yincrement
            self.ListofCheckButtons.append(self.variables[Team])

        
        y = ystart          #reset y position of checkbuttons


#Loop through the MAC teams although for now, there is only one team.
        for Team in self.MACTeamsAtoZ:
            self.variables[Team] = Tkinter.IntVar()
            Team1CheckBox = Tkinter.Checkbutton(self.Panel, text=Team,
                          variable = self.variables[Team],
                          command=self.oncheck(Team,self.MACTeamsAtoZ[Team]),
                          width=CheckBoxWidth,
                          justify = LEFT)
            Team1CheckBox.place(x = MAC_x, y = y)
            
            self.ListofCheckButtons.append(self.variables[Team])
            y += yincrement

            


#-----------------------------------------------------------------------------
# Method Name:    oncheck
# Purpose:          Depending on the checkbox that is checked or unchecked by
#                   the user, this method returns the state of that checkbox.
#                   I have no idea why the nested method, _oncheck, works but
#                   it does so I won't screw with it
# Inputs:           key - this identifies the checkbox from which which to 
#                         "get" the state
# Author:           Rick Burney
#
# Created:          6/29/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
    def oncheck(self,key,ChosenTeam):
        def _oncheck():
            
#Get the state of the selected checkbox and the team acronym that goes with
#that selection and store in class objects that can be used outside of the 
#class
            self.cbget = self.variables[key].get()    
            if self.cbget == 1:
                self.TeamSelected = ChosenTeam
                self.FullNameoftheTeamSelected = key
                
                NumberofCheckButtons = len(self.ListofCheckButtons)
                for Team in range(0,NumberofCheckButtons):
                    self.ListofCheckButtons[Team].set(0)
                self.variables[key].set(1)
        return _oncheck
        





#-----------------------------------------------------------------------------
# Method Name:    KillButton
# Purpose:          Close Button Processing.  Kills the Panel.
# Author:           Rick Burney
#
# Created:          6/28/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
    def KillButton(self):
        
        import Tkinter
        
        self.HomeTeamSelected = self.TeamSelected
        
        
        for widget in self.Panel.winfo_children():
            print widget
            widget.destroy()        
        #self.Panel.quit() #
        #self.Panel.hide()    #Kill the window
        self.Panel.destroy()    #Kill the window
        


 
    def AcceptHomeTeamSelectionButton(self):
       
        self.HomeTeamSelected = self.TeamSelected
        #print(self.FullNameoftheTeamSelected)
        LabelName = Tkinter.Label(self.Panel, text="Home Team Selected", 
                                                width=20,height=1,fg="white",
                                                bg="black",font=("Helvetica", 
                                                24))
        LabelName.place(x = 300, y = 330)
        

        LabelName = Tkinter.Label(self.Panel, 
                                  text=self.FullNameoftheTeamSelected, 
                                  width=20,height=1,fg="black",bg="white",
                                  font=("Helvetica",24))
        LabelName.place(x = 300, y = 300)
       
