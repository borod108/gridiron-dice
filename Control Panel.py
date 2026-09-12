#-----------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Rick
#
# Created:     05/11/2016
# Copyright:   (c) Rick 2016
# Licence:     <your licence>
#-----------------------------------------------------------------------------

from ID_Team import *   #May not be needed
from Tkinter import *
from LBwithWait_Window import * #May not be needed
from openpyxl import *
from ScoreboardClass import *
import GeneralInfoFile
import os
import TestTurtleGraphics   #Draws football field
import Tkinter
import Tkinter as tk

#Game Maintenance global objects
global down
global HomeTeamScore
global HomeTimeOuts             #Will be employed in revisions
global Quarter                  #1-4, OT
global StartoftheGameFlag       #Used by Kickoff() for change of possession
                                    #purposes
global TimeLeftinQuarter        #0 - 900 seconds.  

#Log file global objects
global homeTeamPlayCount        #Used as an index into the home team play log
global PlayCount                #Aggregate for both teams.  Does not include
                                #kickoffs, FG, punts, Xpts
                                
#Scoreboard global objects
global OverTimeIndicator    

#Team global objects
global homeTeam                 #Worksheet object
global homeTeamName
global TeamthatDoesNotHavetheBall   #Team on defense
global TeamWiththeBall          #Team on offense (worksheet object)
global TwoPointFlag             #Not used right now but may be used later
                                #to integrate CallPlay() and GoFor2()
global visitingTeam             #Worksheet object
global visitingTeamName
global visitingTeamPlayCount    #Used as an index into the visitors play log
global VisitingTeamScore
global VisitorTimeOuts          #Will be employed in revisions
global YardLine                 #ranges from 1 to 100
global YardsToGo

#Initialize variables

#Extra point variables
TwoPointFlag = 0

#Game initialization variables
homeTeam = None             #Set from listboxes
#homeTeamName = "USC"        #Default if listboxes are not used
visitingTeam = None     
#visitingTeamName = "UCLA"   

#Game management variables
down = 1
YardLine = 25   #Yard line will be next set by the kickoff
YardsToGo = 10

#Kickoff, FG and Punt variables
KickReturner = "X"
StartoftheGameFlag = 1      #Used to control possession
Startof3rdQuarterFlag = 0

#Scoreboard and logfile variables
homeTeamPlayCount = visitingTeamPlayCount = 0
HomeTimeOuts = 3        #Timeouts will be employed in the revisions
HomeTeamScore = VisitingTeamScore = 0
OverTimeIndicator = 1   #Used for the Scoreboard
PlayCount = 0
Quarter = 1
TimeLeftinQuarter = 900            #In seconds, initialize to 15 minutes
VisitorTimeOuts = 3                #Timeouts will be employed in the revisions

#Define scoreboard objects
AutoRunBox = Scoreboard()
BallOn = Scoreboard()
BallOnLabel = Scoreboard()
Down = Scoreboard()
DownLabel = Scoreboard()
HomeLabel = Scoreboard()
HomeOnOffense = Scoreboard()
HomeScore = Scoreboard()
ManualBox = Scoreboard()
Quarter = Scoreboard()
QuarterLabel = Scoreboard()
OTLabel = Scoreboard()
OverTime = Scoreboard()
PlayCalledLabel = Scoreboard()
PlayCalled = Scoreboard()
PlayResult = Scoreboard()
PlayResult1 = Scoreboard()
PlayResultLabel = Scoreboard()
TestLabel = Scoreboard()            #Good candidate to see if redundant
TimeLeftInQuarter = Scoreboard()
TimoutsLabel = Scoreboard()
TimeoutsLeft = Scoreboard()
TwoMinuteWarning = Scoreboard()
VisitorLabel = Scoreboard()
VisitorsOnOffense = Scoreboard()
VisitorsScore = Scoreboard()
YardsToGo = Scoreboard()
YardsToGoLabel = Scoreboard()



#-------------------------------------------------------------------------------
# Function Name:    HomeTeam - NOT USING
# Purpose:          Provides processing when the Choose Home Team button is 
#                   pressed.  Calls up a Listbox to allow the used to pick the
#                   home team
# Author:           Rick Burney
#
# Created:          11/9/2016
# Copyright:        (c) Rick 2016
#-------------------------------------------------------------------------------
def HomeTeam():

    global frame2
    global homeTeam
    global homeTeamName
    
    homeTeamName = "No Team Selected"
    listframe = Toplevel(frame)
    
    TeamList = ("Arizona","Arizona State","Cal","Colorado","Oregon",
                "Oregon State","Stanford","UCLA","USC","Utah","Washington",
                "Washington State") 
    homeTeamName = MyListBox(TeamList,listframe,1).returnValue()
    
    
    
    ws = ID_Team(homeTeamName)
    homeTeam = ws.Positions()
    
    
#-------------------------------------------------------------------------------
# Function Name:    SelectHomeTeam
# Purpose:          Opens up a window which allows the user to select the home
#                   team, then allows the user to kill the window
# Author:           Rick Burney
#
# Created:          3/8/2017
# Copyright:        (c) Rick 2017
#-------------------------------------------------------------------------------
def SelectHomeTeam():
    
    global frame2       #The window to be opened
    global homeTeamName #The selected value from the ListBox
    
    ListBoxGridColumn = 1
    ListBoxGridRow = 1
    OKButtonColumn = 1
    OKButtonRow = 2


#Temporary dimensions for the window, will adjust and will also tweak the
#colors
    frame2 = Frame(root, height = 600, width = 300, bg = "black")
    
    frame2.place(x=32,y=60) #window placement, also will get tweaked
    
    itemsforlistbox = ["ASU","Cal","ND","ORST","Stan","TEX","UCLA","USC",
                       "Utah","WMU","WSU"]
    
#Create the listbox, ID the handling method and place    
    Lb1 = Listbox(frame2,selectmode=SINGLE,width = 30, height = 10, 
                  font = ('times',13)) 
    Lb1.bind("<<ListboxSelect>>",HomeLBCurSelet)
    Lb1.grid(row = ListBoxGridRow, column = ListBoxGridColumn)
    
    for items in itemsforlistbox:   #Populate the listbox
        Lb1.insert(END,items)
    
    
#Window kill button.  Location will get tweaked    
    ButtonName = Tkinter.Button(frame2, text="OK",
                                command=TeamsSelected,fg="green", 
                                bg="black").grid(row = OKButtonRow, 
                                                 column = OKButtonColumn)
    
 
#-------------------------------------------------------------------------------
# Function Name:    SelectVisitingTeam
# Purpose:          Opens up a window which allows the user to select the 
#                   visiting team, then allows the user to kill the window
# Author:           Rick Burney
#
# Created:          3/9/2017
# Copyright:        (c) Rick 2017
#-------------------------------------------------------------------------------
def SelectVisitingTeam():
    
    global frame2           #The window to be opened
    global visitingTeamName #The selected value from the ListBox
    
    ListBoxGridColumn = 1
    ListBoxGridRow = 1
    OKButtonColumn = 1
    OKButtonRow = 2


#Temporary dimensions for the window, will adjust and will also tweak the
#colors
    frame2 = Frame(root, height = 600, width = 300, bg = "black")
    
    frame2.place(x=1100,y=60) #window placement, also will get tweaked
    
    itemsforlistbox = ["ASU","Cal","ND","ORST","Stan","TEX","UCLA","USC",
                       "Utah","WMU","WSU"]
    
#Create the listbox, ID the handling method and place    
    Lb1 = Listbox(frame2,selectmode=SINGLE,width = 30, height = 10, 
                  font = ('times',13)) 
    Lb1.bind("<<ListboxSelect>>",VisitingLBCurSelet)
    Lb1.grid(row = ListBoxGridRow, column = ListBoxGridColumn)
    
    for items in itemsforlistbox:   #Populate the listbox
        Lb1.insert(END,items)
    
    
#Window kill button.  Location will get tweaked    
    ButtonName = Tkinter.Button(frame2, text="OK",
                                command=TeamsSelected,fg="green", 
                                bg="black").grid(row = OKButtonRow, 
                                                 column = OKButtonColumn)
    
    
    
#-------------------------------------------------------------------------------
# Function Name:    HomeLBCurSelet
# Purpose:          Takes the selection from the Listbox and assigns it to a
#                   global variable
# Inputs:           evt - an event, in this case a selection made in the LB
# Outputs:          TeamName - A global variable with the selected team name
# Author:           Rick Burney
#
# Created:          3/9/2017
# Copyright:        (c) Rick 2017
#-------------------------------------------------------------------------------
def HomeLBCurSelet(event):
    
    global homeTeamName #The selected value from the listbox

    widget = event.widget
    selection=widget.curselection()
    value = widget.get(selection[0])
  
    homeTeamName = value
    

    
#-------------------------------------------------------------------------------
# Function Name:    VisitingLBCurSelet
# Purpose:          Takes the selection from the Listbox and assigns it to a
#                   global variable
# Inputs:           evt - an event, in this case a selection made in the LB
# Outputs:          TeamName - A global variable with the selected team name
# Author:           Rick Burney
#
# Created:          3/9/2017
# Copyright:        (c) Rick 2017
#-------------------------------------------------------------------------------
def VisitingLBCurSelet(event):
    
    global visitingTeamName #The selected value from the listbox

    widget = event.widget
    selection=widget.curselection()
    value = widget.get(selection[0])
  
    visitingTeamName = value

    

    
    

#-------------------------------------------------------------------------------
# Function Name:    TeamsSelected
# Purpose:          Will assigned selected teams to global variables and then
#                   kill the window
# Author:           Rick Burney
#
# Created:          3/8/2017
# Copyright:        (c) Rick 2017
#-------------------------------------------------------------------------------
def TeamsSelected():
    global frame2

    frame2.destroy()    #Kill the window
    
    

#-----------------------------------------------------------------------------
# Function Name:    VisitingTeam-NOT USED
# Purpose:          Provides processing when the Choose Home Team button is 
#                   pressed.  Calls up a Listbox to allow the used to pick the
#                   home team
# Author:           Rick Burney
#
# Created:          11/9/2016
# Copyright:        (c) Rick 2016
#-----------------------------------------------------------------------------
def VisitingTeam():

    global visitingTeam
    global visitingTeamName
    
    visitingTeamName = "No Team Selected"
    
    listframe = Toplevel(frame)
    TeamList = ("Arizona","Arizona State","Cal","Colorado","Oregon",
                "Oregon State","Stanford","UCLA","USC","Utah","Washington",
                "Washington State")
    visitingTeamName = MyListBox(TeamList,listframe,7).returnValue()
    ws = ID_Team(visitingTeamName)
    visitingTeam = ws.Positions()


#-----------------------------------------------------------------------------
# Function Name:    LoadTeams
# Purpose:          Based upon team name that is passed into this function
#                   load Excel spreadsheet for that team
# Author:           Rick Burney
#
# Created:          12/13/2016
# Copyright:        (c) Rick 2016
#-----------------------------------------------------------------------------
def LoadTeams(teamName):
    
    import openpyxl         #Using openpyxl Python library
    
    teamName += ".xlsx" #All team workbooks have an xlsx extension
    
    wb = load_workbook(filename = teamName, data_only=True)  #Load workbook
    
    ws = wb.active                              #switch to active worksheet 
       
    
    
    return ws



#-----------------------------------------------------------------------------
# Function Name:    CreateLog
# Purpose:          Based upon team name that is passed into this function
#                   create a log workbook/worksheet for logging plays for that
#                   team.
# Inputs:           teamName - Name of the team for which the play log will be
#                              created.  This routine will append "Log.xlsx"
#                              to create a filename
# Author:           Rick Burney
#
# Created:          12/13/2016
# Copyright:        (c) Rick 2016
#-----------------------------------------------------------------------------
def CreateLog(teamName):
    
    import openpyxl         #Using openpyxl Python library
    
    teamName += "Log.xlsx" #All team workbooks have an xlsx extension
    
    wb = Workbook()  #Create workbook
    
    ws = wb.get_active_sheet()  #Create an active worksheet 
    
    wb.save(teamName)
       
    
    
    return ws


#-----------------------------------------------------------------------------
# Function Name:    CoinToss
# Purpose:          See which team will receive the kickoff.  Ultimately want
#                   to display the team that will receive on the scoreboard
# Author:           Rick Burney
#
# Created:          12/13/2016
# Copyright:        (c) Rick 2016
#-----------------------------------------------------------------------------
def CoinToss(HomeTeam,VisitingTeam):
    
    import random

    
    global TeamthatDoesNotHavetheBall
    global TeamwiththeBall              #Team that has the ball
    global TeamWiththeBallFlag
    
#Initialize which team has the ball.  May no longer be needed
    TeamwiththeBall = HomeTeam  
    
    dice1 = random.randint(1,2) #Flip a coin
    DisplayMsg = Scoreboard()
    if dice1 == 1:
        D = DisplayMsg.ResultDisplay(0,
                                "Home Team will receive the kickoff",0,frame1)
        
        TeamWiththeBall = HomeTeam
        TeamWiththeBallFlag = 0
        TeamthatDoesNotHavetheBall = VisitingTeam
    else:
        D = DisplayMsg.ResultDisplay(0,
                            "Visiting Team will receive the kickoff",0,frame1)
        TeamwiththeBall = VisitingTeam
        TeamWiththeBallFlag = 1
        TeamthatDoesNotHavetheBall = HomeTeam

    return TeamwiththeBall


#-----------------------------------------------------------------------------
# Function Name:    Positions
# Purpose:          Parse the worksheet into positions and determine relevant
#                   indices
# Author:           Rick Burney
#
# Created:          12/13/2016
# Copyright:        (c) Rick 2016
#-----------------------------------------------------------------------------
def Positions(ws):
    
    from openpyxl import load_workbook
    
    global QBsStartIndex
    global ReceiversStartIndex
    global RunnersStartIndex
    
    PositionColumn = 1
    QBNameColumn = 2
        
    row_count = ws.max_row  #Determine last row used in worksheet
        
    for i in range(1,row_count):
        if ws.cell(row=i, column = PositionColumn).value == 'Runners':
            RunnersRow = i
        
        if ws.cell(row=i, column = PositionColumn).value == 'QBs':
            QBsRow = i
        
        if ws.cell(row=i, column = PositionColumn).value == 'Receivers':
            ReceiversRow = i
        
        if ws.cell(row=i, column=PositionColumn).value == 'Kickers':
            KickersRow = i
        if ws.cell(row=i, column=PositionColumn).value == 'Dline':
            DlineRow = i
            if ws.cell(row=i, column=PositionColumn).value == 'LBs':
                LBsRow = i
            if ws.cell(row=i, column=PositionColumn).value == 'DBs':
                DBsRow = i

        #Develop ranges and indices
        #Runners Range
    RunnersRange = range(RunnersRow+1,QBsRow-1)

    NumberOfRunners = QBsRow - 2 - RunnersRow
    RunnersStartIndex = RunnersRange[0]

        #QBs Range
    QBsRange = range(QBsRow+1,ReceiversRow-1)
    NumberOfQBs = ReceiversRow - 2  - QBsRow
    QBsStartIndex = QBsRange[0]
    QBName = ws.cell(row=QBsStartIndex, column = QBNameColumn).value
    

        #Receivers Range
    ReceiversRange = range(ReceiversRow+1,KickersRow-1)
    NumberOfReceivers = KickersRow - 2 - ReceiversRow
    ReceiversStartIndex = ReceiversRange[0]
    
    return QBName


#-------------------------------------------------------------------------------
# Function Name:    StartGame
# Purpose:          Provides processing when the Start button is pressed.  
#                   This event will start the game
# Author:           Rick Burney
#
# Created:          11/09/2016
# Copyright:        (c) Rick 2016
#-------------------------------------------------------------------------------
def StartGame():
    
    import GameManager
    import GeneralInfoFile
    import LogPlays
    import openpyxl
    import TestTurtleGraphics   #Draws football field
    
    
#Game Maintenance
    global down
    global OTFlag
    global Quarter
    global Qtr
    global YardsToGo
    
#Team Information and Stats
    global HDstats          #home Team defensive stats
    global homeTeam
    global HomeTeamConferenceFactor
    global homeTeamName
    global TeamWiththeBall
    global VDstats          #vsiting team defensive stats
    global visitingTeam
    global VisitingTeamConferenceFactor
    global visitingTeamName
    
#Player Information and Stats
    global HQBName
    global VQBName
    global HTeamStats
    global VTeamStats
    
#Constants    
#Game Maintenance
    OTFlag = 0

#Player Information and Stats
    DIntPercColumn = 10
    DIntPercRow = 46
    DYPCTeamAveRow = 48

    
#Team Information and Stats
    ConferenceFactorColumn = 3
    ConferenceFactorRow = 90
    DRushTeamAveRow = 46
    DRushTeamAveColumn = 3
    DSacksPercRow = 47
    DSacksPerColumn = 6
    HTLeadingSpaces = ""
    PCTeamAveRow = 47
    PenaltyStatsColumn = 2
    DFumRecoveryColumn = 10
    DFumRecoveryRow = 47
    TeamNameLength = 11
    TeamStatsRow = 90
    VTLeadingSpaces = ""
    

    visitingTeam = LoadTeams(visitingTeamName)
    homeTeam = LoadTeams(homeTeamName)
    
    
    homeTeamLeadingSpaces = TeamNameLength - len(homeTeamName)
    for i in range(1,homeTeamLeadingSpaces):
        HTLeadingSpaces += " "
    HTLabel = HTLeadingSpaces + homeTeamName

    HomeTeamLabel = VisitorTeamLabel = Scoreboard()
    HomeTeamLabelPlacement = HomeTeamLabel.WriteLabel(frame,HTLabel,10,2,
                                                      "white","black",24,3,1,
                                                      0,"SE")

    VisitorTeamLabelPlacement = VisitorTeamLabel.WriteLabel(frame,
                                                            visitingTeamName,
                                                            9,2,"white",
                                                            "black",24,3,6,0,
                                                            "SW")
    

    x=LogPlays.ClearLog(homeTeamName,visitingTeamName)
    

#Extract defensive team stats here instead of Positions() because each team's
#defensive team stats will be processed with the opposing teams offensive 
#stats.  There are 4 defensive team stats that will be grouped into a list.
#Dstat[0] = Defensive Rushing Team Average
#Dstat[1] = Defensive Passing Completion Team Average
#Dstat[2] = Defensive Yards per Catch Team Average
#Dstat[3] = Defensive Sack percentage
#Dstat[4] = Defensive INT percentage
#Dstat[5] = Defensive fumble recovery percentage (# of fumbles recovered per
            #10,000 plays

    
#Stats come from http://www.ncaa.com/stats/football/fbs/current/team/xxx where 
#xxx is the stat being requested
#For the visiting team
    VDstats = [homeTeam.cell(row = DRushTeamAveRow,column = \
                             DRushTeamAveColumn).value,
               homeTeam.cell(row = PCTeamAveRow,column = \
                             DRushTeamAveColumn).value,
               homeTeam.cell(row = DYPCTeamAveRow,column = \
                             DRushTeamAveColumn).value,
               homeTeam.cell(row = DSacksPercRow, 
                             column = DSacksPerColumn).value,
               homeTeam.cell(row = DIntPercRow, 
                             column = DIntPercColumn).value,
               homeTeam.cell(row = DFumRecoveryRow, 
                             column = DFumRecoveryColumn).value]

    #For the visiting team
    HDstats = [visitingTeam.cell(row = DRushTeamAveRow,column = \
                                 DRushTeamAveColumn).value,
                visitingTeam.cell(row = PCTeamAveRow,column = \
                                  DRushTeamAveColumn).value,
                visitingTeam.cell(row = DYPCTeamAveRow,column = \
                                  DRushTeamAveColumn).value,
                visitingTeam.cell(row = DSacksPercRow, 
                                  column = DSacksPerColumn).value,               
                visitingTeam.cell(row = DIntPercRow, 
                             column = DIntPercColumn).value,
                visitingTeam.cell(row = DFumRecoveryRow, 
                             column = DFumRecoveryColumn).value]

    
#Extract team stats
#Tstat[0] = Team Penalty Stats - Probability per play of a penalty
#For the visiting team
    VTeamStats = [visitingTeam.cell(row = TeamStatsRow,
                                    column = PenaltyStatsColumn).value]
    HTeamStats = [homeTeam.cell(row = TeamStatsRow,
                                    column = PenaltyStatsColumn).value]
    
    
    
    
    #Parse each team into positions
    VQBName = Positions(visitingTeam)
    HQBName = Positions(homeTeam)
    
#Load conference factor for each team.  This allows for adjustment based upon
#the tram's conference so that a team with great stats in a weak conference 
#will be penalized.  There are two conference factor values, 5 and 4, with 5
#being the better conference.  The conferences that have a conference factor 
#of 5 are Big 10, PAC-12, ACC, SEC and Big-12.  The conferences that have a
#conference factor of 4 are the AAC, Mountain West, MAC, Conference USA and 
#Sun Belt
    HomeTeamConferenceFactor = homeTeam.cell(row = ConferenceFactorRow, 
                             column = ConferenceFactorColumn).value 
    VisitingTeamConferenceFactor = visitingTeam.cell(row = ConferenceFactorRow, 
                             column = ConferenceFactorColumn).value 
    
    
    PlayCalled = Scoreboard()
    TestLabel = Scoreboard()
#    PlayResultLocation = PlayResult.WriteLabel(frame1,"Game has started",
 #                                              60,2,"black","white",24,1,4,0,
  #                                             "W")
    
    TeamWiththeBall = homeTeam  #Not sure why this is needed but watch
    TeamWiththeBall = CoinToss(homeTeam,visitingTeam)   #Do the coin toss

    down = 1        #First and 10
    YardsToGo = 10
    Quarter = 1
    
    T = Scoreboard()
    Ds = T.ResultDisplay(3,"15:00",0,frame)
    
#Here is where we stored the teams playing to the general info file for 
#retrieval for the next time the simulator is run
    GeneralInfoFile.WriteGeneralInfo(homeTeamName,visitingTeamName)    
                                                
    

#-------------------------------------------------------------------------------
# Function Name:    Touchdown
# Purpose:          Common method for recording a touchdown, updating the 
#                   score and the display.  Accounts for offensive and 
#                   defensive touchdowns
# Inputs            Score  - the value to write to the scoreboard.  
#                            UpdateScore updates the score
#                   TeamFlag 0 if the Home Team has the ball, 1 if the
#                            Visitors have the ball
#                   OffensiveScoreFlag 0 if the score was on offense, 1 if the
#                            score was by the defense
#                   Message - the touchdown message
# Author:           Rick Burney
#
# Created:          1/18/2017
# Copyright:        (c) Rick 2017
#-------------------------------------------------------------------------------
def Touchdown(Score,TeamFlag,OffensiveScoreFlag,Message):
    
    global HomeTeamScore
    global VisitingTeamScore
    global TDFlag
    
    HTS = VTS = PR = Scoreboard()
    
    TDFlag = 1  #A TD was scored
    

    HomeorVisitorTeam = TeamFlag + OffensiveScoreFlag
    
    if HomeorVisitorTeam != 1:
        HomeTeamScore = HTS.UpdateScore(HomeTeamScore,Score)
        Ds = HTS.ResultDisplay(18,HomeTeamScore,0,frame)
    else:
        VisitingTeamScore = HTS.UpdateScore(VisitingTeamScore,Score)
        Ds = VTS.ResultDisplay(19,VisitingTeamScore,0,frame)
    
#    print(Message)
    Ds = PR.ResultDisplay(1,Message,0,frame1)


    
def ForceYardLine():

    import TestTurtleGraphics   #Draw the ball position on the football field

    #Game Management
    global AdjustedYardLine
    global YardLine
    global TeamWiththeBall
    
    AdjustedYardLine = 1
    YardLine = 1
    YL = Scoreboard()
    Ds = YL.ResultDisplay(7,AdjustedYardLine,0,frame)
    x = TestTurtleGraphics.PlaceBall(YardLine,TeamWiththeBallFlag)
    
    
    

#-------------------------------------------------------------------------------
# Function Name:    CallPlay
# Purpose:          Provides processing when the Call Play button is pressed
#                   (in the Manual mode).  Allows player on offense to choose
#                   run/pass/kick and then choose a specific play
# Author:           Rick Burney
#
# Created:          11/10/2016
# Copyright:        (c) Rick 2016
#-------------------------------------------------------------------------------
def CallPlay():
    
    import datetime
    import GameMaintenance
    import GameManager
    import LogPlays
    import openpyxl
    import Penalty
    import random
    import ResultofthePlay

    import sys  #This module provides access to some variables used or 
                #maintained by the interpreter and to functions that interact 
                #strongly with the interpreter.

    import TestTurtleGraphics   #Draw the ball position on the football field
    import Tkinter
    import tkMessageBox
    import YardageTable

#Game Management
    global AdjustedYardLine
    global down
    global HomeTeamScore
    global HomeTimeOuts
    global OTFlag               #When set, indicates OT in progress    
    global OTSeries
    global Quarter
    global SafetyFlag
    global TDFlag
    global TimeLeftinQuarter
    global VisitingTeamScore
    global VisitorTimeOuts 
    global YardLine
    global YardsToGo

#Player Information and Stats
    global BallCarrier
    global BallCarrierAve
    global QBsStartIndex        #Used to find where the QBs are on the ws
    global RunnersStartIndex    #Used to find where the RBs are on the ws
    global ReceiversStartIndex  #Same for the receiver
    global VDstats
    global visitingTeam
    global VisitingTeamConferenceFactor    
    global visitingTeamName
    
#Team Information and Stats
    global HDstats
    global HomeTeamConferenceFactor
    global homeTeam
    global homeTeamName
    global HTeamStats
    global TeamthatDoesNotHavetheBall
    global TeamWiththeBall
    global TeamWiththeBallFlag
    global VTeamStats
    
#Log file global objects    
    global homeTeamPlayCount        #Use to index the play log
    global PlayCount  
    global visitingTeamPlayCount
    
    
    DeferPenaltyAcceptanceDecisionFlagDuetoSpaghettiCode = 0
    TDFlag = 0
    PenaltyAcceptedFlag = 0
    OldYardsToGo = YardsToGo
    OldYardLine = YardLine
    OldDown = down

    if sys.version_info < (3,0):        #Check version of  python
            import Tkinter as tkinter
            import tkMessageBox as mbox
    else:
            import tkinter                      #Tkinter is Python's de-facto
            import tkinter.messagebox as mbox   #standard GUI (Graphical User
                                                #Interface) package
    #HomeCalls_TO = HomeCallTO.get()
    

    
    if ((Quarter == 1) or (Quarter == 3)) and (TimeLeftinQuarter == 900):
        
#The MessageBox module is used to display message boxes
#        window = tkinter.Tk()                   #Don't show the main TK Window in the
 #       window.wm_withdraw()                    #background.  This is essential

#        mbox.showinfo('Wrong Button Pressed!','Press the Kickoff Button')
        EM = Scoreboard()
        Ds = EM.ErrorMessage("Wrong Button Pressed",
                             "Press the Kickoff Button")
        return None    
    
    SafetyFlag = 0
    TouchdownFlag = 0   #Used to signify a TD has been scored
    IntFlag = 0
    FumbleFlag = 0
    FirstDownFlag = 0
    ForcePenaltyFlag = 0
    Unsuccessful4thDownConversionFlag = 0
    
    RunCentric = RunOriented.get()
    PassCentric = PassOriented.get()
    Hup = HurryUp.get()
    SpiketheBall = Spike.get()
    HailMary = HailMaryPass.get()
    FEOQ2 = ForceEndOfQ2.get()
    FYL = ForceYL.get()
    FP = ForcePenalty.get()
    FTD= ForceTD.get()
    QBTaK = QBTakesaKnee.get()
    ZY = ZeroYDs.get()
    FFum = ForceFumble.get()
   
    
    if FEOQ2 == 1:          #Even though the variable implies Q2, this was
        Quarter = 2             #changed to Q4 to faciilitate the testing of
        TimeLeftinQuarter = 60  #OT
    if FYL == 1:
        FFum = 1
        
    if (PassCentric == 1) and (RunCentric == 1): #These can't be set at the 
        RunOriented.set(0)                       #same time so reset both
        PassOriented.set(0)                       #if this occurs and message
                                                #the user
        PassCentric = RunCentric = 0

        tkMessageBox.showinfo("Dummy","Both Run and Pass Oriented Checkboxes \
        can't be checked at the same time so both were unchecked")
    
    
    
#Call play
    x = GameManager.PlayCall(TeamWiththeBall,down, YardsToGo,
                             RunnersStartIndex,ReceiversStartIndex,RunCentric,
                             PassCentric,Hup,SpiketheBall,YardLine,HailMary,FP)
    

    
    #Format play call information into a displayable string
    xStr = str(x)
    TestLabel = Scoreboard()
    PR = Scoreboard()
    if QBTaK == 1:
        xStr = "Quarterback Takes a Knee"
    
    #Write play call information to the scoreboard    
    PlayResultLocation = TestLabel.WriteLabel(frame1,xStr,60,2,"black",
                                              "white",24,1,4,0,"W")
    
    
    if GameManager.PlayType == "Run":
        GameManager.PassLength = ""


#    Dstats = HDstats        
    if TeamWiththeBallFlag == 0:
        Dstats = HDstats
        ConferenceFactorAdder = HomeTeamConferenceFactor - \
            VisitingTeamConferenceFactor
        ConferenceFactorMultiplier = float(HomeTeamConferenceFactor)/\
            float(VisitingTeamConferenceFactor)
    else:
        Dstats = VDstats
        ConferenceFactorAdder = VisitingTeamConferenceFactor - \
            HomeTeamConferenceFactor
            
        ConferenceFactorMultiplier = float(VisitingTeamConferenceFactor)/\
            float(HomeTeamConferenceFactor)

# Result List contains everything that happened:
#     ResultList[0] is the play type Run or Pass
#     ResultList[1] is, if a pass, whether the pass is short, mid, or long
#     ResultList[2] is, if a pass, the result of a pass (sack, complete, 
#        incomplete or int
#     ResultList[3] are the yards gained or lost on the play
    ResultList = ResultofthePlay.ResultofthePlay(TeamWiththeBall,
                                            GameManager.PlayType,
                                            GameManager.PassLength,
                                            QBsStartIndex,Dstats,
                                            GameManager.BallCarrierAve,
                                            SpiketheBall,HailMary,YardLine,
                                            ConferenceFactorAdder,
                                            ConferenceFactorMultiplier)
    if FTD == 1:
        ResultList[3] = 99

    if FP == 1:
        ForcePenaltyFlag = 1

    #See if a penalty occurred
    PenaltyList = Penalty.Penalty(HTeamStats[0],VTeamStats[0],
                                  TeamWiththeBallFlag,GameManager.PlayType,
                                  ResultList[3],ResultList[2],
                                  ForcePenaltyFlag,GameManager.PassLength)
    
    if QBTaK == 1:              #QB takes a knee
        ResultList[0] = "Run"
        ResultList[3] = -1
#        PenaltyList[5] = 0
        
        
    if (PenaltyList[5] == 1):     #presnap infraction
        if PenaltyList[1] == 1:
            PenaltyMessage = "Pre-Snap Infraction   " + PenaltyList[0]
            tkMessageBox.showinfo("Penalty",PenaltyMessage)

#Play does not happen so yards gained is 0. This takes care of YL, AYL and YTG
            if YardLine + (2*PenaltyList[4]) > 99:                   
                PenaltyList[4] = int(round((100 - YardLine)/2,0))                    
            if YardLine + (2*PenaltyList[4]) < 1:               
                PenaltyList[4] = -int(round(YardLine/2,0)) 
                
            ResultList[3] = 0                           #PenaltyList[4] 
            YardsToGo -= PenaltyList[4]
            YardLine += PenaltyList[4]
                

                                
            down -= 1   #Trick on pre-snap penalties to keep the down the same
                        #Subtract 1 and let the increment down instruction
                        #restore the down
            if YardsToGo <= 0:
                down = 0          #First down - set to zero because down will
                FirstDownFlag = 1 #be incremented by 1 fuirther in this
                YardsToGo = 10    #function
            
        else:
            DeferPenaltyAcceptanceDecisionFlagDuetoSpaghettiCode = 1            

#Test to see if INT
    if ResultList[2] == "Int":
        IntFlag = 1
        IntResult = ResultofthePlay.Int(TeamthatDoesNotHavetheBall,
                                        GameManager.PassLength,YardLine)
#IntResult is a multi-type list
    # IntResult[0] indicates whether a Pick-6 or touchback occurred
    # IntResult[1] is the name of the player that intercepted
    # IntResult[2] is the return yardage
    # IntResult[3] is the yard line (display use only, TBs and TDs are already
    #     tested.  In this case, YardLine will always need to be subtracted
    #     from 100
    #Adjust YardLine to account for change of possession
        YardLine = IntResult[3]

        
        if YardLine > 50:
            AdjustedYardLine = 100 - YardLine
        else:
            AdjustedYardLine = YardLine
        ResultStr = "Pass Intercepted by " + IntResult[1]
        if IntResult[0] == "Pick 6":
            IntMessage = "Check to see if Pick 6 was logged as a TD"
            tkMessageBox.showinfo("Pick-6",IntMessage)
            
            TouchdownFlag = 1
            IntReturnStr = str(IntResult[2]+IntResult[3])
            ResultStr = ResultStr + " returned "+ IntReturnStr + \
                " yards for a touchdown"
            Touchdown(6,TeamWiththeBallFlag,1,ResultStr)
        elif IntResult[0] == "Touchback":
            AdjustedYardLine = 20
            ResultStr += " for a touchback.  Ball goes to the 20"
        else:
            ResultStr = ResultStr + " Returned " + str(IntResult[2]) + \
                " yards to the " + str(AdjustedYardLine) + " yardline"
            
#Write INT result to the scoreboard
        PR = Scoreboard()
        Ds = PR.ResultDisplay(1,ResultStr,0,frame1)
        
#Implement OTFlag
        if (OTFlag == 0):
            Teams = GameManager.ChangeOfPossession(TeamWiththeBall,
                                           TeamthatDoesNotHavetheBall,
                                           YardLine,AdjustedYardLine,
                                           TeamWiththeBallFlag)
    
            TimeCode = 8                                #10-20 secs for CofP
            TeamWiththeBall = Teams[0]
            TeamthatDoesNotHavetheBall = Teams[1]
            down = Teams[2]
            YardsToGo = Teams[3]
            TeamWiththeBallFlag = Teams[6]
            YardLine = Teams[4]
        
            OnOffenseIndication(TeamWiththeBallFlag)
            ResetAllCheckBoxes()
       
        
    else:

#Advance the down and update yards to go    
        down += 1 
        YardsToGo = GameMaintenance.UpdateYTG(down,YardsToGo,ResultList)

            
        if YardsToGo <= 0:
            down = 1        #First down
            FirstDownFlag = 1
            YardsToGo = 10


        
        if ZY == 1:
            ResultList[3] = 0
            YardsToGo = 10
        YardLine += ResultList[3]   #Update yardline with yards gained
        
        
#Adjust yardline if the ball is past the 50 yardline
        if YardLine > 50:
            AdjustedYardLine = YardageTable.YardlineAdjust(YardLine)

#Will use this for a yardline marker display
            if TeamWiththeBallFlag == 0:    
                BallPositionFlag = 1
            else:
                BallPositionFlag = 0
        else:
            AdjustedYardLine = YardLine

        if (YardLine <= 0) and (PenaltyList[1] == 0):   #Safety
            ResultStr = "Safety.  2 Points to the defense"
            SafetyFlag = 1
            Touchdown(2,TeamWiththeBallFlag,1,ResultStr)
            
            print("Safety")
            
#Determine if either a TD or a 2-pt conversion has occurred
#        elif AdjustedYardLine <= 0:
        elif YardLine >= 100:
            
            if TwoPointFlag == 0:
                PointsScored = 6
                TouchdownFlag = 1
            else:
                PointsScored = 2
                print("2-Point Conversion Successful")
            
#Calculate length of TD e.g. if ball is on the opponents 2 yard line and the
#yardage is 3 yards, display that the ball carrier went 2 yards for the TD
            ResultList[3] += AdjustedYardLine
            AdjustedYardLine = 0
            ScoreUp = Scoreboard()
            HTS = VTS = Scoreboard()
        
#Not sure why we are not using the Display method in the Scoreboard class so
#at some point, need to fix this but this is how the 6 points from a TD gets
#updated on the scoreboard
            
            yds = str(ResultList[3])
            
            ResultStr = "Touchdown!!!!  " + yds + " yard " + ResultList[0] + \
                " " + GameManager.BallCarrier
            Touchdown(6,TeamWiththeBallFlag,0,ResultStr)
            
        
#Format play result based upon the type of play            
        if ResultList[0] == "Run":
            ResultStr = "Run:          "
            ResultStr += "Yards Gained = "
            ResultStr += str(ResultList[3])
            
        else:
            ResultStr = "Pass:          " + ResultList[2]
            if ResultList[2] == "Completed":
                ResultStr += "     Yards = "
                ResultStr += str(ResultList[3])
            if ResultList[2] == "Sack":
                ResultStr += " Loss of "
                ResultStr += str(ResultList[3])
                ResultStr += "  Yards"
                
        if TouchdownFlag == 1:  #Display T, who scored and how many yards
        
            yds = str(ResultList[3])
            if ResultList[3] <= 0:         #To diagnose source of negative TDs
                print(ResultList)
            ResultStr = "Touchdown!!!!  " + yds + " yard " + ResultList[0] + \
                " " + GameManager.BallCarrier
    
        
        

#Update time but first, determine TimeCode by priority to determine if cases
# Priority 1 - Spike the ball
# Priority 2 - Incomplete Pass, TD, Timeout, Out of bounds under 2 minutes
# Priority 3 - Hurry Up
# Priority 4 - First Down
# Priority 5 - Out of bounds
# Priority 6 - If none of the above
    
    if SpiketheBall == 1:
        TimeCode = 12                #12 is the TimeCode for spiking the ball
    elif ResultList == "Incomplete":
        TimeCode = 0                 #0 is the TimeCode for an incomplete pass
    elif TouchdownFlag == 1:
        TimeCode = 1                 #1 is the TimeCode for a touchdown
    elif Hup == 1:
        TimeCode = 6                 #6 is the TimeCode for a hurry up offense
    elif FirstDownFlag == 1:
        TimeCode = 9
    else:
        TimeCode = 15                #15 is the TimeCode for none of the above

    if (PenaltyList[1] == 1) and (PenaltyList[5] == 1): #Presnap penalty
        TimeCode = 16                                  #No time elapsed
    if (PenaltyList[1] == 0) and (PenaltyList[5] == 1): #Presnap penalty
        TimeCode = 17                                  #For simplicity, this
                                                       #will be 10 seconds


        
    

#This is after an unsuccessful 4th down conversion.  Change possession
    if (down > 4) and (OTFlag == 0):
        
        Teams = GameManager.ChangeOfPossession(TeamWiththeBall,
                                               TeamthatDoesNotHavetheBall,
                                               YardLine,AdjustedYardLine,
                                               TeamWiththeBallFlag)
        Unsuccessful4thDownConversionFlag = 1
        TimeCode = 8
        TeamWiththeBall = Teams[0]
        TeamthatDoesNotHavetheBall = Teams[1]
        down = Teams[2]
        YardsToGo = Teams[3]
        YardLine = Teams[4]
        AdjustedYardLine = Teams[5]
        TeamWiththeBallFlag = Teams[6]
        OnOffenseIndication(TeamWiththeBallFlag)
        ResultStr += " Change of Possession"
        ResetAllCheckBoxes()

#Test for a fumble
    if (TouchdownFlag == 0) and (QBTaK == 0):
        if (ResultList[0] == "Run") or (ResultList[2] == "Completed") or \
           (ResultList[2] == "Sack"):
            FumbleResult = ResultofthePlay.Fumble(TeamWiththeBall,
                                                  TeamthatDoesNotHavetheBall,
                                                  YardLine,Dstats)
            FumbleFlag = FumbleResult[0]
            FumbleRecoverer = FumbleResult[3]
            if (FFum == 1):
                FumbleFlag = 1
            
            if  FumbleFlag == 1:
                TimeCode = 8
                YardLine = FumbleResult[2]  #This is where the fumble occurred
                                            #not the original LOS
                                            
                FumbleReturn = FumbleResult[1]
                YardLine -= FumbleReturn
                if FFum == 1:
                    YardLine = 0
                
                if YardLine > 50:
                    AdjustedYardLine = 100 - YardLine
                else:
                    AdjustedYardLine = YardLine
                AdjustedYardLineStr = str(AdjustedYardLine)
                FumbleReturnStr = str(FumbleReturn)
                ResultStr = "Fumble Recoved by " + FumbleRecoverer + \
                    " returned "
                if YardLine <= 0:
                    FumbleReturnStr = str(FumbleReturn+YardLine)
                    ResultStr +=  FumbleReturnStr + " yards for a touchdown"
                    Touchdown(6,TeamWiththeBallFlag,1,ResultStr)
                else:
                    ResultStr += FumbleReturnStr + " yards to the "
                    ResultStr += AdjustedYardLineStr + " yard line"
                if OTFlag == 0:
                    Teams = GameManager.ChangeOfPossession(TeamWiththeBall,
                                                TeamthatDoesNotHavetheBall,
                                                YardLine,AdjustedYardLine,
                                                TeamWiththeBallFlag)
                    
                    TeamWiththeBall = Teams[0]
                    TeamthatDoesNotHavetheBall = Teams[1]
                    YardLine = Teams[4]
                    down = Teams[2]
                    YardsToGo = Teams[3]
                    TeamWiththeBallFlag = Teams[6]
                    OnOffenseIndication(TeamWiththeBallFlag) 
                    ResetAllCheckBoxes()
                    print("Line 1174",YardLine,AdjustedYardLine,TeamWiththeBall,
                              TeamthatDoesNotHavetheBall,TeamWiththeBallFlag)
                    
                    
    if OTFlag == 0:
        TimeList = ResultofthePlay.UpdateTime1(TimeCode,TimeLeftinQuarter,
                                               Quarter)
    
    
        TimeLeftinQuarter = TimeList[0]
        Quarter = TimeList[1]
    else:
        TimeLeftinQuarter = 900

    if ((Quarter == 2) or (Quarter == 4)) and (TimeLeftinQuarter <= 120):
        TMW = Scoreboard()
        TMWIndicatorLabel = TMW.WriteLabel(frame,"",1,1,"white",
                                                        "red",12,7,9,0,"W") 
    else:
        TMW = Scoreboard()
        TMWIndicatorLabel = TMW.WriteLabel(frame,"",1,1,"white",
                                                        "black",12,7,9,0,"W") 


#Test for end of game.  NEED TO CHANGE QUARTER TO "OT" SO THAT WE DON'T KEEP
#SENDING THE OT MESSAGE.  OR, SET AN OTFLAG AND AT THE END OF CALLPLAY, CALL A
#NEW FUNCTION THAT ASSESSES THE OT STATUS
    if (Quarter == 5) and (HomeTeamScore != VisitingTeamScore):
        EM = Scoreboard()
        Ds = EM.ErrorMessage("Game Over.","Press OK to Quit")   #Game Over
    if (Quarter == 5) and (HomeTeamScore == VisitingTeamScore):
        TeamWiththeBallFlag = random.randint(0,1)
        if TeamWiththeBallFlag == 0:
            Message = homeTeamName + " will get the ball first.  Press OT Button to Start OT"
            TeamWiththeBall = homeTeam
            TeamthatDoesNotHavetheBall = visitingTeam
        else:
            Message = visitingTeamName + " will get the ball first.  Press OT Button to Start OT"
            TeamWiththeBall = visitingTeam
            TeamthatDoesNotHavetheBall = homeTeam
        tkMessageBox.showinfo("OverTime!!",Message)
        OTFlag = 1
        OTSeries = 0
        Quarter = "OT"
        Q = Scoreboard()
        P = Scoreboard()
        PR = Scoreboard()
        T = Scoreboard()
        Ds = Q.ResultDisplay(4,Quarter,0,frame) 
        Ds = PR.ResultDisplay(1,"We are going to Overtime",0,frame1)
        Ds = P.ResultDisplay(24,"",0,frame1)
        Ds = T.ResultDisplay(3,"",0,frame)
        
        
        return


    if (PenaltyList[1] == 1) and (PenaltyList[5] == 1): #If pre-snap penalty, 
        ResultStr = PenaltyList[0]                     #show it on message

    if DeferPenaltyAcceptanceDecisionFlagDuetoSpaghettiCode == 1:
            
        Ds = PR.ResultDisplay(1,ResultStr,0,frame1)
        Accept = tkMessageBox.askyesno("Penalty. Do you wish to accept?",
                          PenaltyList[0])
        if Accept:
            
#if penalty is accepted and the result of the play is a touchdown in any way, 
#take the touchdown off the board by passing a 6 to the touchdown function.  
#Use TouchdownFlag to detect touchdown
            PenaltyAcceptedFlag = 1

#Revert to the previous down unless the penalty is applied to the end of the 
#play and there was a safety                
            if (PenaltyList[6] == 0) or (SafetyFlag == 1):     
                down = OldDown                  
            else:
                OldYardLine = YardLine
                OldYardsToGo = YardsToGo                
            if PenaltyList[2] == 1: #Penalty is on the D and results in an
                down = 1            #automatic 1st down
            if PenaltyList[3] != 0: #Unless the penalty results in the loss of
                down += 1           #a down, go back to the original down
                
#Half the difference to the goal line
            if OldYardLine + (2*PenaltyList[4]) > 99:                   
                PenaltyList[4] = int(round((100 - OldYardLine)/2,0))                    
            if OldYardLine + (2*PenaltyList[4]) < 1:               
                PenaltyList[4] = -int(round(OldYardLine/2,0)) 
            if TouchdownFlag == 1:
                Touchdown(-6,TeamWiththeBallFlag,0,ResultStr) 
            if SafetyFlag == 1:    
                Touchdown(-2,TeamWiththeBallFlag ^ 1,0,ResultStr) 
                SafetyFlag = 0
               
            YardLine = PenaltyList[4] + OldYardLine     #Update YL,YTG and AYL
            YardsToGo = OldYardsToGo - PenaltyList[4] 
                
            if ((down == 1) and (PenaltyList[6] == 1) and \
                (PenaltyList[4] < 0)) or PenaltyList[2] == 1:
                YardsToGo = 10
            if YardsToGo <= 0:
                down = 1        #First down
                YardsToGo = 10  
            if YardLine > 50:
                AdjustedYardLine = 100 - YardLine
            else:
                AdjustedYardLine = YardLine
            print("Line 1338",OldYardLine,OldYardsToGo,YardLine,YardsToGo,AdjustedYardLine)
            
#Penalty accepted, negate any interception or lost fumble
# and revert the possession back to the offense - see if we can handle penalties on 4th down
            if (IntFlag == 1) or (FumbleFlag == 1) or ((down == 4) and \
                                                       (PenaltyList[4] > 0)):    
                Teams = GameManager.ChangeOfPossession(TeamWiththeBall,
                                            TeamthatDoesNotHavetheBall,
                                            YardLine,AdjustedYardLine,
                                            TeamWiththeBallFlag)
                TeamWiththeBallFlag = TeamWiththeBallFlag ^ 1
                
                TeamWiththeBall = Teams[0]
                TeamthatDoesNotHavetheBall = Teams[1]
                OnOffenseIndication(TeamWiththeBallFlag)
                if ((down == 4) and (PenaltyList[4] > 0)):
                    YardsToGo = 10
                
        else:
            PenaltyList[5] = 0
            PenaltyAcceptedFlag = 0
    

#Define scoreboard objects
    T = Scoreboard()
    D = Scoreboard()
    Y = Scoreboard()
    YL = Scoreboard()
    Q = Scoreboard()
    YardsToGoStr = str(YardsToGo)
    
#Update down, yards to go, yardline, time left in the quarter and, if the end
#of the quarter, advance the quarter, on the scoreboard
    Ds = D.ResultDisplay(5,down,0,frame)
    
    if (YardLine >=90) and (down == 1):
        YardsToGo = 100 - YardLine
        YardsToGoStr = str(YardsToGo)
    if (TouchdownFlag == 1) and (PenaltyAcceptedFlag == 0):
        DS = Y.ResultDisplay(6,"",0,frame)
        Ds = YL.ResultDisplay(7,"",0,frame)
    else:
        Ds = Y.ResultDisplay(6,YardsToGoStr,0,frame)
        Ds = YL.ResultDisplay(7,AdjustedYardLine,0,frame)
    Ds = T.ResultDisplay(3,ResultofthePlay.TimeLeftinQuarterDisplay,0,frame)
    Ds = Q.ResultDisplay(4,Quarter,0,frame)    
    

    

#Write play result to the scoreboard
    if SafetyFlag == 1:
        ResultStr = "Safety. 2 points to the defense"        
    Ds = PR.ResultDisplay(1,ResultStr,0,frame1)
    
#The following is a stupid little trick to compensate for the spaghetti code
#that CallPlay has become.  Because INTs result in a change of possession and
#the change of possession has already occurred, INTs get logged to the wrong
#team.  So a local variable that flags who is on offense is created and is
#inverted using the old exclusive-or trick when the INT (and ultimately, the 
#fumble flag) is set.  Will get fixed in Revision 2.0
    TWTBF = TeamWiththeBallFlag
    if (IntFlag == 1) or (FumbleFlag == 1) or \
               (Unsuccessful4thDownConversionFlag == 1):
        BallCarrier = ""
        TWTBF =  TeamWiththeBallFlag ^ 1
        TouchdownFlag = 0

    
    PlayCount += 1

    if PenaltyList[5] == 0:
        if TWTBF == 0:
            homeTeamPlayCount += 1
        else:
            visitingTeamPlayCount += 1
            
        if ResultList[0] == "Run":
            PlayType = 0
        else:
            PlayType = 1
        x=LogPlays.PlayLog(homeTeamName,visitingTeamName,TWTBF,
                       homeTeamPlayCount,visitingTeamPlayCount,PlayType,
                       GameManager.BallCarrier,ResultList[2],ResultList[3],
                       TouchdownFlag,IntFlag,FumbleFlag,YardLine,
                       ResultofthePlay.TimeLeftinQuarterDisplay)


#Always write an EOF to the next line of the log
        x=LogPlays.PlayLog(homeTeamName,visitingTeamName,TWTBF,
                       homeTeamPlayCount+1,visitingTeamPlayCount+1,"EOF",
                       "","","",0,0,0,YardLine,
                       ResultofthePlay.TimeLeftinQuarterDisplay)
    x = TestTurtleGraphics.PlaceBall(YardLine,TeamWiththeBallFlag)

    Spike.set(0)        #These checkboxes get cleared after every play
    HailMaryPass.set(0)
    
    
   

#-------------------------------------------------------------------------------
# Function Name:    ResetAllCheckBoxes
# Purpose:          Resets all checkbodes
# Author:           Rick Burney
# Created:          3/20/2017
# Copyright:        (c) Rick 2017
#-------------------------------------------------------------------------------
def ResetAllCheckBoxes():
    
    import Tkinter
    import tkMessageBox
        
    Squib.set(0)    #Reset kickoff checkboxes
    Onside.set(0)
    FK.set(0)
    PlacementPunt.set(0)    #Reset punt checkboxes
    RunOriented.set(0)      #Reset play call checkboxes
    PassOriented.set(0)
    HurryUp.set(0)
    Spike.set(0)
    HailMaryPass.set(0)



#-------------------------------------------------------------------------------
# Function Name:    OnOffenseIndication
# Purpose:          Calls display routine that will illuminate the "On Offense"
#                   indicator for either the home or visiting team as indicated
#                   by TeamWiththeBallFlag
# Inputs            TeamWiththeBallFlag    0 - Home team, 1 - Visiting Team
# Author:           Rick Burney
# Created:          1/21/2017
# Copyright:        (c) Rick 2017
#-------------------------------------------------------------------------------
def OnOffenseIndication(TeamWiththeBallFlag):
    
    OOI = Scoreboard()
    if TeamWiththeBallFlag == 0:
        Ds = OOI.ResultDisplay(25,"green",0,frame)
        Ds = OOI.ResultDisplay(26,"black",0,frame)
    else:
        Ds = OOI.ResultDisplay(25,"black",0,frame)
        Ds = OOI.ResultDisplay(26,"green",0,frame)
        
        

#-------------------------------------------------------------------------------
# Function Name:    OTSetup
# Purpose:          Sets up and runs multiple series of OT.  OT follows the 
#                   following sequence.  The first OT consists of Series 1 and 
#                   2, with 1 team on offense on Series 1 and the other team  
#                   on offense on Series 2.  For Series 3, the team on offense 
#                   on Series 2 is on offense and then the team on offense on 
#                   Series 1 will be on offense for Series 4.  This
#                   alternating pattern will continue but after every even-
#                   numbered series, the score will be evaluated and if the
#                   score is no longer ties, the team with more points wins 
#                   and the game is over.  Each team starts from the opposing
#                   team's 25.  After the 2nd OT (Series 1-4), all TDs will be
#                   followed by a 2-point conversion, no Xtra points.  Only 
#                   globals will be passed to and from this function.
# Author:           Rick Burney
# Created:          3/22/2017
# Copyright:        (c) Rick 2017
#-------------------------------------------------------------------------------
def OTSetup():

    import GameManager
    import sys
    import TestTurtleGraphics   #Draw the ball position on the football field
    import Tkinter
    import tkMessageBox

#Game Management Global Objects
    global AdjustedYardLine
    global down
    global HomeTeamScore
    global OTFlag           #When set, indicates OT in progress
    global OTSeries
    global Quarter
    global VisitingTeamScore
    global YardsToGo
    global YardLine
    global TDFlag
    
#Scoreboard global objects
    global OverTimeIndicator
    
#Team Global Objects
    global homeTeamName
    global TeamWiththeBall
    global TeamWiththeBallFlag
    global TeamthatDoesNotHavetheBall
    global visitingTeamName
    
    YardLine = 75           #Ball starts from defense's 25 yardline
    AdjustedYardLine = 25
    down = 1
    YardsToGo = 10

    OTSeries += 1

#Define scoreboard objects
    OverTime = Scoreboard()
    T = Scoreboard()
    D = Scoreboard()
    Y = Scoreboard()
    YL = Scoreboard()
    Q = Scoreboard()
    YardsToGoStr = str(YardsToGo)
    Ds = D.ResultDisplay(5,down,0,frame)            #Update scoreboard
    Ds = Y.ResultDisplay(6,YardsToGoStr,0,frame)
    Ds = YL.ResultDisplay(7,AdjustedYardLine,0,frame)
#Test to see what happens next
#First see if this is an odd OTSeries whixch means an even OTSeries just
#completed
    OddSeries = OTSeries % 2
    OverTimeIndicator = int(float((OTSeries+1)/2))
    OverTimeStr = str(OverTimeIndicator)
    
    if OddSeries == 1: #Odd series, next test to see if score is tied
        
        
        if HomeTeamScore != VisitingTeamScore:  #Not tied, game is over
            
            tkMessageBox.showinfo("Game Over","Press Quit")

#Now implement the OT rules of possession.  #CoP on even series only
    else:
        
        Teams = GameManager.ChangeOfPossession(TeamWiththeBall,
                                            TeamthatDoesNotHavetheBall,
                                            YardLine,AdjustedYardLine,
                                            TeamWiththeBallFlag)        
        TeamWiththeBall = Teams[0]
        TeamthatDoesNotHavetheBall = Teams[1]
        TeamWiththeBallFlag = Teams[6]
           
    OnOffenseIndication(TeamWiththeBallFlag)
    x = TestTurtleGraphics.PlaceBall(YardLine,TeamWiththeBallFlag)
    OTSB = OverTime.WriteLabel(frame,OverTimeStr,2,2,"white","black",24,6,9,
                               0,"")
    
        
    return None
    



#-----------------------------------------------------------------------------
# Function Name:    Kickoff
# Purpose:          Determines length of kickoff, calls kickoff return method
#                   and passes results for display
# Author:           Rick Burney
# Created:          1/3/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
def Kickoff():
    import GameManager
    import LogPlays
    import openpyxl
    import random
    import ResultofthePlay
    import TestTurtleGraphics
    import Tkinter
    import tkMessageBox
    import YardageTable

#log file global objects    
    global homeTeamPlayCount
    global PlayCount 
    global visitingTeamPlayCount
    
#Game Management global objects
    global AdjustedYardLine
    global down
    global HomeTeamScore
    global HomeTimeOuts
    global Quarter
    global SafetyFlag
    global StartoftheGameFlag
    global TDFlag
    global TimeLeftinQuarter
    global VisitingTeamScore
    global VisitorTimeOuts 
    global YardLine
    global YardsToGo
    
#Scoreboard global objects
    global TimeLeftinQuarterDisplay
     
#Team and player global objects
    global homeTeamName
    global KickReturner
    global StartKickoffTeam
    global TeamthatDoesNotHavetheBall
    global TeamWiththeBall
    global TeamWiththeBallFlag
    global ThirdQuarterKickoffTeam
    global ThirdQuarterTeamReceivingtheKick
    global ThirdQuarterTeamWiththeBallFlag
    global visitingTeamName
             
    
    
    NumKickoffsRow = 36
    NumKickoffsCol = 3
    KickoffAveCol = 4
    TouchbacksCol = 5
    OutofBoundsKicksCol = 6
    PlayType = 2            #For logging purposes
    KickReturnFlag = 0      #Is set only when there is an actual return
    
    TDFlag = 0
    
    
    if (Quarter == 3) and (TimeLeftinQuarter == 900):
        Startofthe3rdQuarterFlag = 1
        HomeTimeOuts = VisitorTimeOuts = 3
        #Here is where we write the number of timeouts to the Scoreboard
    else:
        Startofthe3rdQuarterFlag = 0

        
    TouchbackFlag = 0   #Indicates if a touchback has occurred on the kickoff
    TouchdownFlag = 0
    SquibKick = Squib.get()
    OnsideKick = Onside.get()
    FreeKick = FK.get()
    
    NumKickCBsChecked = SquibKick + OnsideKick + FreeKick   #Stupid little
                                                            #trick to see if
                                                            #more than 1 CB is
                                                            #checked
    
    if NumKickCBsChecked > 1: #If more than 1 CB is checked, reset all and
        Squib.set(0)          #notify the user
        Onside.set(0)                       
        FK.set(0)
        SquibKick = OnsideKick = FreeKick = 0

        tkMessageBox.showinfo("Dummy","Only one of the kicking checkboxes \
        can be checked at once so all were reset and ignored")
    
    
    
    KickOffFactor = 15  #Effectively, the standard deviation for a kickoff
    if FreeKick == 0:
        KickOffFromthe = 35 #Constant unless there is a penalty or a safety
    else:
        KickOffFromthe = 20
    AdjustedYardLine = KickOffFromthe

#Determine who kicks off to who.  Also, at the start of the game (and also, at
#the start of the 3rd quarter, there is no "change of possession."  For all
#other kickoffs there is a change of possession
    if StartoftheGameFlag == 1:
        KickoffTeam = TeamthatDoesNotHavetheBall
        ThirdQuarterKickoffTeam = TeamWiththeBall
        ThirdQuarterTeamReceivingtheKick = TeamthatDoesNotHavetheBall
        print(ThirdQuarterKickoffTeam,ThirdQuarterTeamReceivingtheKick,
              TeamthatDoesNotHavetheBall)
        if TeamWiththeBallFlag == 0:
            ThirdQuarterTeamWiththeBallFlag = 1
        else:
            ThirdQuarterTeamWiththeBallFlag = 0
        
    else:
        KickoffTeam = TeamWiththeBall
    
    if Startofthe3rdQuarterFlag == 1:
        print(ThirdQuarterKickoffTeam,ThirdQuarterTeamReceivingtheKick,
              TeamthatDoesNotHavetheBall)
        KickoffTeam = ThirdQuarterKickoffTeam
        TeamWiththeBall = ThirdQuarterTeamReceivingtheKick
        TeamWiththeBallFlag = ThirdQuarterTeamWiththeBallFlag
        TeamthatDoesNotHavetheBall = KickoffTeam
         
        
        
    if (StartoftheGameFlag == 0) and (Startofthe3rdQuarterFlag == 0):
        Teams = GameManager.ChangeOfPossession(TeamWiththeBall,
                                               TeamthatDoesNotHavetheBall,
                                               YardLine,AdjustedYardLine,
                                               TeamWiththeBallFlag)
        TeamWiththeBall = Teams[0]
        TeamthatDoesNotHavetheBall = Teams[1]
        down = Teams[2]
        YardsToGo = Teams[3]
        TeamWiththeBallFlag = Teams[6]
        
    
#Fetch the kicker's stats and compute percentages
    NumKickoffs = KickoffTeam.cell(row=NumKickoffsRow,
                                   column = NumKickoffsCol).value
    KickoffAve = round(KickoffTeam.cell(row=NumKickoffsRow,
                                        column = KickoffAveCol).value,0)
    Touchbacks = KickoffTeam.cell(row=NumKickoffsRow,
                                  column = TouchbacksCol).value
    OutofBoundsKicks = KickoffTeam.cell(row=NumKickoffsRow,
                                        column = OutofBoundsKicksCol).value
    PercTB = int(round(100*Touchbacks/NumKickoffs,0))
    PercOB = int(round((100*float(OutofBoundsKicks))/NumKickoffs,0))
    
#Test to see if the kick results in a touchback
    FirstKickoffTest = random.randint(1,100)
    YL = KO = D = YTG = HTS = VTS = Scoreboard()
    OutofBoundsKickoffFlag = 0
    if (FirstKickoffTest <= PercTB) and (SquibKick == 0) and \
       (OnsideKick == 0) and (FreeKick == 0):
        KickoffResult = "Touchback"
        TouchbackFlag = 1
        AdjustedYardLine = YardLine = 25    #Touchbacks put the ball on the 25
        
        Ds = YL.ResultDisplay(7,AdjustedYardLine,0,frame)
        
        Ds = KO.ResultDisplay(8,KickoffResult,0,frame1)

#Test to see if the kick goes out of bounds
    elif (FirstKickoffTest <= (PercTB + PercOB)) and (SquibKick == 0) and \
         (OnsideKick == 0):
        OutofBoundsKickoffFlag = 1
        KickoffResult = "Kick Went Out of Bounds"
        AdjustedYardLine = 35
        if FreeKick == 0:
            AdjustedYardLine = YardLine = 35        #Ball goes on the 35 and
                                                    #counts as a penalty
        else:
            AdjustedYardLine = YardLine = 50
        
        
        Ds = YL.ResultDisplay(7,AdjustedYardLine,0,frame)
        
        Ds = KO.ResultDisplay(8,KickoffResult,0,frame1)

#Otherwise, the kick will be returned
    else:
        
#Determine how deep is the kick
        if (SquibKick == 0) and (OnsideKick == 0):
            KickoffYards = \
                random.randint(int(KickoffAve-KickoffAve/KickOffFactor),
                                    int(KickoffAve+KickoffAve/KickOffFactor))
        elif OnsideKick == 1:
            KickoffYards = random.randint(10,15)
        else:
            KickoffYards = random.randint(20,50)    #Squib Kicks won't be 
                                                    #returned 
        KickTo = KickOffFromthe + KickoffYards
#        KickTo = 35 + KickoffYards
        
#Will need to deal with kicks that don't cross the 50 (onside kicks).  In any
#event, kickoff occurs and then the kickoff results in either a touchback or 
#a kickoff return
        if KickTo > 50:
            AdjustedKickTo = YardageTable.YardlineAdjust(KickTo)
        else:
            AdjustedKickTo = KickTo
        AdjustedKickToStr = str(AdjustedKickTo)
        KickoffResult = "Kickoff to the " + AdjustedKickToStr + ", "
        KickReturnResult = YardageTable.KickReturn(TeamWiththeBall)
        if SquibKick == 1:
            KickReturnResult = 0    #For squib kicks, overwrite return w/ 0
            KickoffResult = "Squib Kick to the " + AdjustedKickToStr + \
                " yardline.  No return"

            TouchbackFlag = 1   #Use a touchback timecode
        if OnsideKick == 1:
            KickReturnResult = 0    #For squib kicks, overwrite return w/ 0
            OnsideKickRecoveryFlag=ResultofthePlay.WhoRecoverstheOnsideKick()
            if OnsideKickRecoveryFlag == 0:

#Need logic to determine who recovers onside kick.  By definition there is a 
#change in possession so if the kicking team recovers there needs to be a 2nd
#change in possession
            
                KickoffResult = "Onside Kick to the " + AdjustedKickToStr + \
                    " yardline.  Recovered by receiving team"
            else:
                KickoffResult = "Onside Kick to the " + AdjustedKickToStr + \
                    " yardline.  Recovered by kicking team"
                Teams = GameManager.ChangeOfPossession(TeamWiththeBall,
                                                TeamthatDoesNotHavetheBall,
                                                YardLine,AdjustedYardLine,
                                                TeamWiththeBallFlag)
                TeamWiththeBall = Teams[0]
                TeamthatDoesNotHavetheBall = Teams[1]
        #        YardLine = Teams[4]
         #       AdjustedYardLine = Teams[5]
                down = Teams[2]
                YardsToGo = Teams[3]
                TeamWiththeBallFlag = Teams[6]
                
                
            TouchbackFlag = 1   #use a touchback timecode

        KickReturnResultStr = str(KickReturnResult) #Prepare for display
        
        if (SquibKick == 0) and (OnsideKick == 0):
            KickoffResult += " Return of " + KickReturnResultStr + \
                " yards to the "
            KickReturnFlag = 1
        
#Need formatting if kickoff is returned from the endzone
        KickReturnTo = AdjustedKickTo + KickReturnResult    #KO rtned to where
        YardLine = KickReturnTo
        
#Test for a kick return for a TD
        if KickReturnTo >= 100:                             #KO rtned for a TD
            LengthofReturnStr = str(100 - AdjustedKickTo)
            KickoffResult = KickoffResult[:-27]             #Format TD message
            TouchdownFlag = 1
            KickoffResult += "TD!  Kickoff Returned " + LengthofReturnStr + \
                " yards by " + YardageTable.KickReturner

#Update score            
            Touchdown(6,TeamWiththeBallFlag,0,KickoffResult)
            Y = YL = Scoreboard()
            DS = Y.ResultDisplay(6,"",0,frame)  #Blank displays
            Ds = YL.ResultDisplay(7,"",0,frame)

#Adjust for kickoffs that are returned past the 50 yard line            
        else:
            if KickReturnTo > 50:
                KickReturnTo = YardageTable.YardlineAdjust(KickReturnTo)
        
            AdjustedYardLine = KickReturnTo
            AdjustedYardLineStr = str(AdjustedYardLine)
            
#Display yardline to where kickoff was returned and update time
            if (SquibKick == 0) and (OnsideKick == 0):
                KickoffResult += AdjustedYardLineStr + " by " + \
                    YardageTable.KickReturner
            Ds = KO.ResultDisplay(8,KickoffResult,0,frame1)
        
            Ds = YL.ResultDisplay(7,AdjustedYardLine,0,frame)
            
    if (TouchbackFlag == 1) or (OutofBoundsKickoffFlag == 1):
        TimeCode = 13
    else:
        TimeCode = 8

    TimeList = ResultofthePlay.UpdateTime1(TimeCode,TimeLeftinQuarter,Quarter)
        
   # TimeList = ResultofthePlay.UpdateTime("", 0,TimeLeftinQuarter,
    #                                               0,TouchbackFlag,1,Quarter)
    
    TimeLeftinQuarter = TimeList[0]
    Quarter = TimeList[1]

    PC = Scoreboard()                               #Display that it is a 
    Ds = PC.ResultDisplay(24,"Kickoff",0,frame1)    #Kickoff
  
    T = Scoreboard()
    Ds = T.ResultDisplay(3,ResultofthePlay.TimeLeftinQuarterDisplay,0,frame)
    Q = Scoreboard()
    Ds = Q.ResultDisplay(4,Quarter,0,frame)    
    


    down = 1 
    YardsToGo = 10
    YardsToGoStr = str(YardsToGo)
    Ds = D.ResultDisplay(5,down,0,frame)
    Ds = YTG.ResultDisplay(6,YardsToGoStr,0,frame)
    
#This flag is used to indicate whether the kickoff is the one to start the 
#game or a kickoff after a score.  
    StartoftheGameFlag = 0  
    OnOffenseIndication(TeamWiththeBallFlag)

    PlayCount += 1
#    if TeamWiththeBallFlag == 0:
 #       homeTeamPlayCount += 1
  #  else:
   #     visitingTeamPlayCount += 1
    x = TestTurtleGraphics.PlaceBall(YardLine,TeamWiththeBallFlag)
    
#    if KickReturnFlag == 1:
 #       x=LogPlays.PlayLog(homeTeamName,visitingTeamName,TeamWiththeBallFlag,
  #                     homeTeamPlayCount,visitingTeamPlayCount,PlayType,
   #                    YardageTable.KickReturner,"",KickReturnResult,
    #                   TouchdownFlag,0,0,YardLine)

#Always write an EOF to the next line of the log
     #   x=LogPlays.PlayLog(homeTeamName,visitingTeamName,TeamWiththeBallFlag,
      #                 homeTeamPlayCount+1,visitingTeamPlayCount+1,"EOF",
       #                "","","",0,0,0,YardLine)
       
    ResetAllCheckBoxes()
    SafetyFlag = 0
    
    return None

#-----------------------------------------------------------------------------
# Function Name:    FG
# Purpose:          Receives the yardline from the calling program and 
#                   determines if the kick is good or not
# Author:           Rick Burney
# Created:          1/3/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
def FG():
    import GameManager
    import LogPlays
    import openpyxl
    import random
    import ResultofthePlay
    import TestTurtleGraphics
    import Tkinter
    import tkMessageBox
    import YardageTable

#Game Maintenance global objects    
    global AdjustedYardLine
    global down
    global HomeTeamScore
    global OTFlag           #Used to prevent a CoP in OT
    global Quarter
    global TimeLeftinQuarter
    global VisitingTeamScore
    global YardLine
    global YardsToGo
    
#Log file global objects
    global homeTeamPlayCount
    global PlayCount 
    global visitingTeamPlayCount
    
#Scoreboard global objects
    global TimeLeftinQuarterDisplay
    
#Team and player global objects
    global homeTeamName
    global TeamthatDoesNotHavetheBall   #Team on Defense
    global TeamWiththeBall              #Team kicking the FG
    global TeamWiththeBallFlag          # 0=Home Team, 1 = Visitors
    global visitingTeamName
    
#Kicking stats are from www.footballdb.com/college-football/stats/index.html
    
    FGYardsAdder = 17   #kick is from 7 yards back from the LOS and the 
                        #the goalposts are 10 yards into the endzone
    KickerRow = 36              #Worksheet constants that ID the kicker and
    TentoNineteenCol = 8        #relevant stats
    TwentytoTwentyNineCol = 9
    ThirtytoThirtyNineCol = 10
    FortytoFortyNineCol = 11
    FiftytoFiftyFiveCol = 12
    PlayType = 4
    
    FGFlag = 0      #Flag to indicate if FG was good.  1 = Good
    PercFGGood = 1  #Initialization, will actually obtain average from the 
                    #worksheet
    if YardLine < 50:
        AdjustedYardLine = YardageTable.YardlineAdjust(YardLine)

#Extract FG averages based upon the LOS    
    if AdjustedYardLine <= 2:
        PercFGGood = TeamWiththeBall.cell(row=KickerRow,
                                          column = TentoNineteenCol).value
    elif AdjustedYardLine <= 12:
        PercFGGood = TeamWiththeBall.cell(row=KickerRow,
                                        column = TwentytoTwentyNineCol).value
    elif AdjustedYardLine <= 22:
        PercFGGood = TeamWiththeBall.cell(row=KickerRow,
                                        column = ThirtytoThirtyNineCol).value
    elif AdjustedYardLine <= 32:
        PercFGGood = TeamWiththeBall.cell(row=KickerRow,
                                        column = FortytoFortyNineCol).value
    elif AdjustedYardLine <= 38:
        PercFGGood = TeamWiththeBall.cell(row=KickerRow,
                                        column = FiftytoFiftyFiveCol).value
    elif AdjustedYardLine > 46:
        tkMessageBox.showinfo("Not Close Enough for a FG",
                              "Push another button!")
        return
    else:
        PercFGGood = 0
    
    FGTest = random.randint(1,100)  #See if FG is good
    HTS = VTS = FG = Scoreboard()
    FGYardsStr = str(AdjustedYardLine+FGYardsAdder)
    if FGTest <= PercFGGood:

        ScoreUp = HTS = VTS = Scoreboard()  #FG is good, update the score
        if TeamWiththeBallFlag == 0:
            HomeTeamScore = ScoreUp.UpdateScore(HomeTeamScore,3)
            Ds = HTS.ResultDisplay(18,HomeTeamScore,0,frame)
        else:
            VisitingTeamScore = ScoreUp.UpdateScore(VisitingTeamScore,3)
            Ds = VTS.ResultDisplay(19,VisitingTeamScore,0,frame)
 
        Message = "Field Goal is good from " + FGYardsStr + " Yards"
        Ds = FG.ResultDisplay(9,Message,0,frame1)
    else:
        #Test for blocked kick
        BlockedKickResult = \
            ResultofthePlay.KickBlock(TeamthatDoesNotHavetheBall,YardLine,0)
        if BlockedKickResult[0] == 1:
            Message = BlockedKickResult[1]
            YardLine = BlockedKickResult[2]
            AdjustedYardLine = BlockedKickResult[4]
            TDFlag = BlockedKickResult[3]
            if TDFlag == 1:                     #Blocked kick returned for TD
                
                Message = "Field Goal Blocked.  Returned for a TD" #TD message
                #Ds = FG.ResultDisplay(9,Message,0,frame1)
                
#Change possession so the TD gets applied to the team that blocked the kick
                if OTFlag == 0:
                    Teams = GameManager.ChangeOfPossession(TeamWiththeBall,
                                                TeamthatDoesNotHavetheBall,
                                                YardLine,AdjustedYardLine,
                                                TeamWiththeBallFlag)
                    TeamWiththeBall = Teams[0]
                    TeamthatDoesNotHavetheBall = Teams[1]
                    ResetAllCheckBoxes()                
                
                
                    Touchdown(6,TeamWiththeBallFlag,1,Message) #Call TD method 
                                                             #for 6 points
                
                    return

        else:
            Message = "Field Goal missed from " + FGYardsStr + " Yards"
        
            if (YardLine > 80):                     #FG NG, if ball was kicked
                YardLine = 80                       #from inside the 20, the
                AdjustedYardLine = 20               #ball goes to the 20 and
                                                    #results in a change of 
                                                    #possession
        Ds = FG.ResultDisplay(9,Message,0,frame1)
            
        if OTFlag == 0:     
            Teams = GameManager.ChangeOfPossession(TeamWiththeBall,
                                               TeamthatDoesNotHavetheBall,
                                               YardLine,AdjustedYardLine,
                                               TeamWiththeBallFlag)
            TeamWiththeBall = Teams[0]
            TeamthatDoesNotHavetheBall = Teams[1]
            YardLine = Teams[4]
            AdjustedYardLine = Teams[5]
        
            down = Teams[2]
            YardsToGo = Teams[3]
            TeamWiththeBallFlag = Teams[6]
            OnOffenseIndication(TeamWiththeBallFlag)
        YardsToGoStr = str(YardsToGo)
        D = YTG = Scoreboard()
        Ds = D.ResultDisplay(5,down,0,frame)
        Ds = YTG.ResultDisplay(6,YardsToGoStr,0,frame)
        YL = Scoreboard()
        
        Ds = YL.ResultDisplay(7,AdjustedYardLine,0,frame)
        x = TestTurtleGraphics.PlaceBall(YardLine,TeamWiththeBallFlag)
        ResetAllCheckBoxes()
        
        
    TimeCode = 11    
    
    TimeList = ResultofthePlay.UpdateTime1(TimeCode,TimeLeftinQuarter,Quarter)
        

#    TimeList = ResultofthePlay.UpdateTime("", 0,TimeLeftinQuarter,0,
 #                                                  1,0,Quarter)
    
    TimeLeftinQuarter = TimeList[0]
    Quarter = TimeList[1]

    T = Scoreboard()
    Ds = T.ResultDisplay(3,ResultofthePlay.TimeLeftinQuarterDisplay,0,frame)

    PC = Scoreboard()                                       #Display that it 
    Ds = PC.ResultDisplay(24,"Field Goal Attempt",0,frame1)  #is a FG
    Q = Scoreboard()
    Ds = Q.ResultDisplay(4,Quarter,0,frame)    
 
    PlayCount += 1
#    if TeamWiththeBallFlag == 0:
 #       homeTeamPlayCount += 1
  #  else:
   #     visitingTeamPlayCount += 1
#    x=LogPlays.PlayLog(homeTeamName,visitingTeamName,TeamWiththeBallFlag,
 #                      homeTeamPlayCount,visitingTeamPlayCount,PlayType,
  #                     "",Message,AdjustedYardLine+FGYardsAdder,
   #                    0,0,0,YardLine)

#Always write an EOF to the next line of the log
    #x=LogPlays.PlayLog(homeTeamName,visitingTeamName,TeamWiththeBallFlag,
     #                  homeTeamPlayCount+1,visitingTeamPlayCount+1,"EOF",
      #                 "","","",0,0,0,YardLine)
    
    
    return None


#-----------------------------------------------------------------------------
# Function Name:    XPt
# Purpose:          Determines if the extra point try is good or not
# Author:           Rick Burney
# Created:          1/3/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
def XPt():
    import openpyxl
    import random
    import Tkinter
    import tkMessageBox
    import ResultofthePlay
     
#Game maintenance global objects
    global AdjustedYardLine
    global HomeTeamScore
    global OverTimeIndicator
    global VisitingTeamScore
    global TDFlag
    
#Log file global objects
    global PlayCount 
    
#Team and Player global objects
    global TeamWiththeBall      #Offense that just scored the TD
    global TeamWiththeBallFlag  
    

    if TDFlag == 0: #No TD scored so attempts to press the Extra Point button
                    #will be ignored

        tkMessageBox.\
            showinfo("Error", "No TD Scored. Don't press this button")
        return None
    if OverTimeIndicator >= 3:
        tkMessageBox.\
            showinfo("Error", 
                     "After the 2nd OT, teams must go for 2 after a TD")
        return None
        
    
    FGYardsAdder = 17 #kick is from 7 yards back from the LOS and the 
                        #the goalposts are 10 yards into the endzone
    KickerRow = 36  #Location of Xpt stats
    PATCol = 7
    
    XPtFlag = 0 #Initialize
    
#Access stats
    PercXPTGood = TeamWiththeBall.cell(row=KickerRow,column = PATCol).value
    
  
    XPtTest = random.randint(1,100) #Test to see if kick is good
    ScoreUp = HTS = VTS = XP = Scoreboard() #Update scoreboard
    if XPtTest <= PercXPTGood:      #If kick is good

        if TeamWiththeBallFlag == 0:
            HomeTeamScore = ScoreUp.UpdateScore(HomeTeamScore,1)
            
            Ds = HTS.ResultDisplay(18,HomeTeamScore,0,frame)
        else:
            VisitingTeamScore = ScoreUp.UpdateScore(VisitingTeamScore,1)
            Ds = VTS.ResultDisplay(19,VisitingTeamScore,0,frame)
            
#Display result
        Ds = XP.ResultDisplay(10,"Extra Point is Good",0,frame1)
               
    else:                       #See if kick is blocked
        BlockedKickResult = \
            ResultofthePlay.KickBlock(TeamthatDoesNotHavetheBall,80,1) 

        if BlockedKickResult[0] == 1:
            Message = BlockedKickResult[1]
            TDFlag = BlockedKickResult[3]
            if TDFlag == 1:                     #Blocked kick returned for TD
                
                Message = "Kicked Blocked.  Returned for a 2-Point score" 
                
#Reversed because defense has returned a block kick for a score
                if TeamWiththeBallFlag == 1:        
                    HomeTeamScore = ScoreUp.UpdateScore(HomeTeamScore,2)
                    
                    Ds = HTS.ResultDisplay(18,HomeTeamScore,0,frame)
                else:
                    VisitingTeamScore = \
                        ScoreUp.UpdateScore(VisitingTeamScore,2)
                    Ds = VTS.ResultDisplay(19,VisitingTeamScore,0,frame)                
                
        else:
            Message = "Extra Point is No Good"
        Ds = XP.ResultDisplay(10,Message,0,frame1)
        
    PC = Scoreboard()                                    #Display that it is  
    Ds = PC.ResultDisplay(24,"Extra Point Try",0,frame1)  #an extra point
    
    PlayCount += 1
    TDFlag = 0
        
        
    return None


#-----------------------------------------------------------------------------
# Function Name:    GoFor2
# Purpose:          Determines if a 2-Point conversion is successful.  Right
#                   now, for reasons of convenience, an actual play will not 
#                   be run.  also can't find team stats so the average success
#                   rate in college football is 42 %.
#                   No player or play will be identified
# Author:           Rick Burney
# Created:          1/25/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
def GoFor2():

    import openpyxl
    import random

#Game maintenance global objects
    global HomeTeamScore
    global VisitingTeamScore

#Log file global objects
    global PlayCount
    
#Team and player global objects
    global TeamWiththeBall      #Offense that just scored the TD
    global TeamWiththeBallFlag  
    
 #   FGYardsAdder = 17 #kick is from 7 yards back from the LOS and the 
                        #the goalposts are 10 yards into the endzone

    Perc2PtConversionGood = 42  #Average for all FBS
#    PATCol = 7
    
    TwoPtFlag = 0 #Initialize 
    

    
  
    TwoPtTest = random.randint(1,100)       #Test to see if conversion is good
    ScoreUp = HTS = VTS = XP = Scoreboard() #Update scoreboard
    if TwoPtTest <= Perc2PtConversionGood:  #If good, update score, message

        if TeamWiththeBallFlag == 0:
            HomeTeamScore = ScoreUp.UpdateScore(HomeTeamScore,2)
            
            Ds = HTS.ResultDisplay(18,HomeTeamScore,0,frame)
        else:
            VisitingTeamScore = ScoreUp.UpdateScore(VisitingTeamScore,2)
            Ds = VTS.ResultDisplay(19,VisitingTeamScore,0,frame)
            
#Display result
        Ds = XP.ResultDisplay(11,"2-Point Conversion is Good",0,frame1)
               
    else:
        Ds = XP.ResultDisplay(11,"2-Point Conversion is No Good",0,frame1) #NG
       

    PC = Scoreboard()                                    #Display that it is  
    Ds = PC.ResultDisplay(24,"2-Point Try",0,frame1)  #an extra point
    
    PlayCount += 1
        
        
    
    return None

#-----------------------------------------------------------------------------
# Function Name:    Punt
# Purpose:          Determines length of punt and calls the routine to return
#                   the punt
# Author:           Rick Burney
# Created:          1/3/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
def Punt():
    import datetime
    import GameManager
    import openpyxl
    import numpy
    import random
    import ResultofthePlay
    import TestTurtleGraphics
    import Tkinter
    import tkMessageBox
    import YardageTable
    

#Game Maintenance global objects    
    global AdjustedYardLine              
    global down                         
    global HomeTeamScore                
    global Quarter
    global TimeLeftinQuarter            
    global VisitingTeamScore
    global YardLine                     #Initially, the LOS at the time of the
                                        #punt, then the location of the return
    global YardsToGo                    #location to where the punt is 

#Log file global objects    
    global PlayCount
    
#Punt related global objects
    global FCFlag      
    
#Scoreboard global objects
    global TimeLeftinQuarterDisplay     #Time that is displayed on the 
                                        #scoreboard

#Team and player global objects    
    global TeamthatDoesNotHavetheBall
    global TeamWiththeBall              #Initially, team punting the ball.
    global TeamWiththeBallFlag          #This changes at the end of the method
      
    CoffinCorner = PlacementPunt.get()
    FBP = ForceBlockedPunt.get()
    
    
    if down < 4:
        tkMessageBox.showinfo("Button Pressed Incorrectly",
                              "Punts Only Can Happen on 4th Downs")
        return
    
    CoffinCornerCap = 45
    MinCoffinCornerPunt = 15
    MaxCoffinCornerPunt = 40
    CoffinCornerPuntSigma = 12
    CoffinCornerBackOff = 5
    
    
    PunterRow = 38          #Location in team file for punter stats
    PunterAveColumn = 4
    PunterLongColumn = 5
    PuntLengthVariance = 10 #estimated punt average standard deviation
    
    YardageTable.FCFlag = 0 #Initialize flags
    PuntFlag = 0            #Used by the update time method
    
#extract punt averages from the team file
    PuntAve = int(round(TeamWiththeBall.cell(row=PunterRow,
                                         column = PunterAveColumn).value,0))
    PuntLong = int(round(TeamWiththeBall.cell(row=PunterRow,
                                         column = PunterLongColumn).value,0))
    PuntLengthUpperMin = max(PuntAve - PuntLengthVariance , 20)
    
#Punt block logic here.  Complete code through change of possession and then
#return.
#Test for blocked punt
    BlockedPuntResult = ResultofthePlay.PuntBlock(TeamthatDoesNotHavetheBall,
                                                  YardLine,FBP)

       
    if BlockedPuntResult[0] == 1:
        PuntMessage = BlockedPuntResult[1]
        YardLine = BlockedPuntResult[2]
        AdjustedYardLine = BlockedPuntResult[4]
        TDFlag = BlockedPuntResult[3]
        if TDFlag == 1:                     #Blocked kick returned for TD
            
            Message = "Punt Blocked.  Returned for a TD" #TD message
            
            Teams = GameManager.ChangeOfPossession(TeamWiththeBall,
                                            TeamthatDoesNotHavetheBall,
                                            YardLine,AdjustedYardLine,
                                            TeamWiththeBallFlag)
#            TeamWiththeBall = Teams[0]
 #           TeamthatDoesNotHavetheBall = Teams[1]
            
            
            Touchdown(6,TeamWiththeBallFlag,1,Message) #Call TD method 
                                                         #for 6 points
            Y = YL = Scoreboard()
            DS = Y.ResultDisplay(6,"",0,frame)  #Blank displays
            Ds = YL.ResultDisplay(7,"",0,frame)
            ResetAllCheckBoxes()
            
            
#Display message and change possession
        P = Scoreboard()
        Ds = P.ResultDisplay(12,PuntMessage,0,frame1)
        Teams = GameManager.ChangeOfPossession(TeamWiththeBall,
                                           TeamthatDoesNotHavetheBall,
                                           YardLine,AdjustedYardLine,
                                           TeamWiththeBallFlag)
        TeamWiththeBall = Teams[0]
        TeamthatDoesNotHavetheBall = Teams[1]
        down = Teams[2]
        YardsToGo = Teams[3]
        TeamWiththeBallFlag = Teams[6]
        OnOffenseIndication(TeamWiththeBallFlag)
    
        YardLine = Teams[4]
        AdjustedYardLine = Teams[5]
        YL = Scoreboard()
        Ds = YL.ResultDisplay(7,AdjustedYardLine,0,frame)
        ResetAllCheckBoxes()
        x = TestTurtleGraphics.PlaceBall(YardLine,TeamWiththeBallFlag)
        return None
         



#Compute length of the punt 
    if CoffinCorner == 0:
        PuntLengthTest = random.randint(1,10)
        if PuntLengthTest == 1:
            PuntLength = random.randint(15,PuntLengthUpperMin)
        elif PuntLengthTest <= 9:
            #PuntLength = random.randint(PuntAve - PuntLengthVariance,
                                    #PuntAve + PuntLengthVariance)
            PuntLength = int(round(numpy.random.normal(PuntAve,5),0))
            
        else:
            PuntLength = random.randint(PuntAve + PuntLengthVariance,
                                    PuntLong + PuntLengthVariance)
    else:
        PuntSigma = random.randint(-CoffinCornerPuntSigma-CoffinCornerBackOff,
                                   CoffinCornerPuntSigma)
        
#The idea is that the coffin corner punt lands near the endzone +/- some sigma
#but is capped to a max number so you are not doing placement punts from your
#own 5 yardline
        PuntLength = min(100 - YardLine + PuntSigma,CoffinCornerCap)
        
    YardLineBeforePunt = YardLine   #For display purposes
    YardLine += PuntLength          #Calculate where the punt lands
    
    TouchbackFlag = YardageTable.TouchbackTest(YardLine)    #Touchback?
    HTS = VTS = P = Scoreboard()
    if TouchbackFlag == 1:          #If touchback, display and ball goes to
                                    #the 20
        
        AdjustedPuntLengthStr = str(100 - YardLineBeforePunt)
        PuntMessage = "Punt of " + AdjustedPuntLengthStr + " yards for a touchback"
        Ds = P.ResultDisplay(12,PuntMessage,0,frame1)
        
        AdjustedYardLine = 20
        
    else:                               #No touchback, form the beginning of
        PuntLengthStr = str(PuntLength) #the punt display message
        PunttoYL = YardLine
     
        if YardLine > 50:
            PunttoYL=YardageTable.YardlineAdjust(YardLine)
        else:
            PunttoYL = YardLine
               
        PunttoYLStr = str(PunttoYL)
        PuntMessage = "Punt " + PuntLengthStr + " yds to  "+ PunttoYLStr + " yardline" 
               
#Some punts are not returned.  Punts that land within the receiving teams 5
#yardline are not returned.  Punts that travel less than 30 yards are not
#returned.  Coffin Corner punts are not returned but can result in a 
#touchback.  Left off here but basically, if CoffinCorner == 1, then force
#return to 0.  elif state after line 1498


        if (YardLineBeforePunt + PuntLength) >=95:
            PuntMessage += " No Return"
            TouchbackFlag = 1               #Use a touchback timecode
            PR = 0
            if YardLine > 50:
                AdjustedYardLine = YardageTable.YardlineAdjust(YardLine)
            else:
                AdjustedYardLine = YardLine
        elif PuntLength < 30:
            PuntMessage += " No Return"
            TouchbackFlag = 1               #Use a touchback timecode
            PR = 0
            if YardLine > 50:
                AdjustedYardLine = YardageTable.YardlineAdjust(YardLine)
            else:
                AdjustedYardLine = YardLine
        elif CoffinCorner == 1:
            PuntMessage += " No Return"
            TouchbackFlag = 1               #Use a touchback timecode
            PR = 0
            if YardLine > 50:
                AdjustedYardLine = YardageTable.YardlineAdjust(YardLine)
            else:
                AdjustedYardLine = YardLine


#If none of the previous conditions are true, there is a punt return        
        else:
            Force = FBP #Force just is a forced condition, not necessarily a
                        #blocked punt inspite of the name, FBP
            PuntReturnList=YardageTable.PuntReturn(TeamthatDoesNotHavetheBall,
                                                   Force)
            if YardageTable.FCFlag == 1:        #Fair catch
                FairCatchMessage = "Fair Catch"
                PuntMessage += " " + FairCatchMessage + " by " + YardageTable.PuntReturner
                if YardLine > 50:
                    AdjustedYardLine = YardageTable.YardlineAdjust(YardLine)
                else:
                    AdjustedYardLine = YardLine
            else:
                PR = PuntReturnList[0]            #Punt return yardage
                PuntReturner = PuntReturnList[1]  #Who returned the punt
                YardLine -= PR                    #Update the yardline
                if YardLine <= 0:                 #See if return goes for a TD
                    TDFlag = 1
                    TDReturn = PR + YardLine    
                    TDReturnStr = str(TDReturn)
                    PuntMessage += " - TD!!!!  Returned " + TDReturnStr + " yards by " + PuntReturner
                    Touchdown(6,TeamWiththeBallFlag,1,PuntMessage)
                else:
                    TDFlag = 0
                    if YardLine > 50:
                        AdjustedYardLine=YardageTable.YardlineAdjust(YardLine)
                    else:
                        AdjustedYardLine = YardLine
        
            
                    AdjustedYardLineStr = str(AdjustedYardLine)


                    PRStr = str(PR)

                    PuntMessage += ", RTN " + PRStr + " yds to  " + AdjustedYardLineStr + " ydline by " + PuntReturner
                    PuntFlag = 1
            
#Display message and change possession
    Ds = P.ResultDisplay(12,PuntMessage,0,frame1)
    Teams = GameManager.ChangeOfPossession(TeamWiththeBall,
                                           TeamthatDoesNotHavetheBall,
                                           YardLine,AdjustedYardLine,
                                           TeamWiththeBallFlag)
    TeamWiththeBall = Teams[0]
    TeamthatDoesNotHavetheBall = Teams[1]
    down = Teams[2]
    YardsToGo = Teams[3]
    TeamWiththeBallFlag = Teams[6]
    OnOffenseIndication(TeamWiththeBallFlag)
    
    YardLine = Teams[4]
    AdjustedYardLine = Teams[5]
    YL = Scoreboard()
    Ds = YL.ResultDisplay(7,AdjustedYardLine,0,frame)
    PC = Scoreboard()                                 #Display that it is a 
    Ds = PC.ResultDisplay(24,"Punt",0,frame1)           #Punt
    
#Update time, down, etc. 

    if TouchbackFlag == 1:
        TimeCode = 14
    elif YardageTable.FCFlag == 1:
        TimeCode = 14
    else:
        TimeCode = 7
    TimeList = ResultofthePlay.UpdateTime1(TimeCode,TimeLeftinQuarter,Quarter)
        
        
#    TimeList = ResultofthePlay.UpdateTime("", 0,TimeLeftinQuarter,
 #                                                  YardageTable.FCFlag,
  #                                                 TouchbackFlag,PuntFlag,
   #                                                Quarter)
    
    TimeLeftinQuarter = TimeList[0]
    Quarter = TimeList[1]

    T = Scoreboard()
    Ds = T.ResultDisplay(3,ResultofthePlay.TimeLeftinQuarterDisplay,0,frame)
    Q = Scoreboard()
    Ds = Q.ResultDisplay(4,Quarter,0,frame)    
    
    D = YTG = Scoreboard()    
    down = 1 
    YardsToGo = 10
    YardsToGoStr = str(YardsToGo)
    Ds = D.ResultDisplay(5,down,0,frame)
    Ds = YTG.ResultDisplay(6,YardsToGoStr,0,frame)
    
    PlayCount += 1
    x = TestTurtleGraphics.PlaceBall(YardLine,TeamWiththeBallFlag)
    ResetAllCheckBoxes()
    

    return None

#-----------------------------------------------------------------------------
# Function Name:    GoForIt
# Purpose:          Determines if 4th down conversion is successful
# Author:           Rick Burney
# Created:          1/3/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
def GoForIt():
    return None



#-----------------------------------------------------------------------------
# Function Name:    QuitGame
# Purpose:          Exits the simulator
# Author:           Rick Burney
#
# Created:          11/10/2016
# Copyright:        (c) Rick 2016
#-----------------------------------------------------------------------------
def QuitGame():

    import LogPlays
    import Tkinter
    import tkMessageBox
    

#Game Maintenance global objects    
    global HomeTeamScore
    global VisitingTeamScore

    
#Log file global objects    
    global homeTeamPlayCount
    global visitingTeamPlayCount

#Team Information and Stats
    global homeTeamName
    global visitingTeamName


#Since the kickoff counts as a play, there needs to be at least 2 plays for
#either team before stats can be compiled
    if (homeTeamPlayCount > 1) and (visitingTeamPlayCount > 1):
        LogPlays.CompileStats(homeTeamName,visitingTeamName,1,1,0,HQBName,
                              VQBName)
        LogPlays.CompileStats(homeTeamName,visitingTeamName,1,1,1,HQBName,
                              VQBName)
    if HomeTeamScore > VisitingTeamScore:
        WinningTeam = homeTeamName
        LosingTeam = visitingTeamName
        WinningScore = str(HomeTeamScore)
        LosingScore = str(VisitingTeamScore)
    else:
        WinningTeam = visitingTeamName
        LosingTeam = homeTeamName
        WinningScore = str(VisitingTeamScore)
        LosingScore = str(HomeTeamScore)
    
    FinalScore = WinningTeam + ": " + WinningScore + "  " + LosingTeam + ": " + LosingScore 
    tkMessageBox.showinfo("Final Score",FinalScore)

    root.destroy()




#Program starts here
root = Tkinter.Tk(  )

#Have the display grab the focus
os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of \
process "Python" to true' ''')

#Draw scoreboard
root.geometry("1350x600")
root.configure(background='black')
frame = Frame(root, height = 500, width = 1350, bg = "black")
frame1 = Frame(root, height = 175, width = 1350, bg = "black")
frame.pack()
frame1.pack()

#Define checkbox variables and initialize global variables
var = IntVar()
varm = IntVar()
autorun = IntVar()
autorun = 0
manual = IntVar()
manual = 0




#Input Widget processing and placement
ButtonName = Tkinter.Button(frame, text="Choose Home Team",
                            command=SelectHomeTeam).grid(row=1,column=1,padx=20,
                                                pady=20)
ButtonName = Tkinter.Button(frame, text="Start",command=StartGame).grid(row=1,
                            column=2,padx=20,pady=20)
ButtonName = Tkinter.Button(frame, text="Kickoff",command=Kickoff).grid(row=1,
                            column=3,padx=20,pady=20)
ButtonName = Tkinter.Button(frame, text="FG",command=FG).grid(row=1,
                            column=4,padx=20,pady=20)
ButtonName = Tkinter.Button(frame, text="XPt",command=XPt).grid(row=1,
                            column=5,padx=20,pady=20)
ButtonName = Tkinter.Button(frame, text="Go For 2",command=GoFor2).grid(row=1,
                            column=6,padx=20,pady=20)
ButtonName = Tkinter.Button(frame, text="Punt",command=Punt).grid(row=1,
                            column=7,padx=20,pady=20)
ButtonName = Tkinter.Button(frame, text="Call Play",
                            command=CallPlay).grid(row=1,column=9,padx=20,
                                                   pady=20)
ButtonName = Tkinter.Button(frame, text="Quit",command=QuitGame).grid(row=6,
                            column=7,padx=20,pady=20)
ButtonName = Tkinter.Button(frame, text="Choose Visiting Team",
                            command=SelectVisitingTeam).grid(row=1,column=10,
                                                       padx=20,pady=20)
ButtonName = Tkinter.Button(frame, text="OT",
                            command=OTSetup).grid(row=5,column=10,
                                                       padx=0,pady=0)
ButtonName = Tkinter.Button(frame, text="FYL",
                            command=ForceYardLine).grid(row=6,column=10,
                                                       padx=0,pady=0)
                                           
HomeLabelPlacement = HomeLabel.WriteLabel(frame,"          HOME",10,2,"white",
                                            "black",24,3,1,0,"SE")
HomeScorePlacement = HomeScore.WriteLabel(frame,"00",3,1,"black","white",36,4,
                                          1,2,"NE")
HomeOnOffensePlacement = HomeOnOffense.WriteLabel(frame,"",2,1,"green",
                                                  "green",8,4,2,0,"W")

TLIQPlacement = TimeLeftInQuarter.WriteLabel(frame,"00:00",6,2,"white",
                                             "black",36,3,4,0,"")
VisitorLabelPlacement = VisitorLabel.WriteLabel(frame,"VISITORS",9,2,"white",
                                                "black",24,3,6,0,"SW")
TimoutsLabelPlacement = TimoutsLabel.WriteLabel(frame,"TIMEOUTS",9,2,"white",
                                                "black",24,5,1,0,"W")
TimoutsLabelPlacement = TimoutsLabel.WriteLabel(frame,"TIMEOUTS",9,2,"white",
                                                "black",24,5,7,0,"W")
QtrLabelPlacement = QuarterLabel.WriteLabel(frame,"Qtr",4,2,"white",
                                                "black",24,4,3,0,"E")
VisitorsOnOffensePlacement = VisitorsOnOffense.WriteLabel(frame,"",2,1,
                                                          "black","grey",8,4,
                                                          6,0,"W")
VisitorsScorePlacement = VisitorsScore.WriteLabel(frame,"00",3,1,"black",
                                                    "white",36,4,6,5,"")
QuarterPlacement = Quarter.WriteLabel(frame,"1",3,1,"black","white",24,4,4,0,
                                      "")

#Place Timeout boxes
TimeoutsPlacement = TimeoutsLeft.WriteLabel(frame,"3",3,1,"white","black",24,
                                            5,1,0,"E")
TimeoutsPlacement = TimeoutsLeft.WriteLabel(frame,"3",3,1,"white","black",24,
                                            5,8,0,"E")

#Yard markers
DownLabelPlacement = DownLabel.WriteLabel(frame,"DOWN",5,1,"white","black",22,
                                          7,1,0,"")
DownLocation = Down.WriteLabel(frame,"1",2,2,"white","black",24,7,1,0,"E")
YardsToGoLocation = YardsToGo.WriteLabel(frame,"10",3,2,"white","black",24,7,
                                         4,0,"W")
YardsToGoLabelLocation = YardsToGoLabel.WriteLabel(frame,"To Go",6,2,"white",
                                                    "black",24,7,3,2,"E")
BallOnLocation = BallOn.WriteLabel(frame,"25",3,2,"white","black",24,7,6,0,
                                   "W")
BallOnLabelLocation = BallOnLabel.WriteLabel(frame,"Ball is On",9,2,"white",
                                                "black",24,7,5,0,"W")
OTL = OTLabel.WriteLabel(frame,"OverTime",9,2,"white",
                                                "black",24,6,8,0,"")
PlayResultLabelLocation = PlayResultLabel.WriteLabel(frame1,"Play Result",11,
                                                     2,"white","black",24,1,3,
                                                        0,"E")
PlayResultLocation = PlayResult.WriteLabel(frame1,"",  
                                           60,2,"black","white",24,1,4,0,"W")
PlayResult1Location = PlayResult1.WriteLabel(frame1,
                                             "",60,2,
                                             "black","white",24,4,4,5,"W")

RunOriented = IntVar()
TimeIsShort = Tkinter.Checkbutton(frame, text="Run-Oriented",
                                  variable = RunOriented ).grid(row=2,
                                            column=9, padx=0,pady=0,
                                            sticky = "")
PassOriented = IntVar()
TimeIsShort = Tkinter.Checkbutton(frame, text="Pass-Oriented",
                                  variable = PassOriented ).grid(row=2,
                                            column=10, padx=0,pady=0,
                                            sticky = "")
HurryUp = IntVar()
TimeIsShort = Tkinter.Checkbutton(frame, text="Hurry-Up",
                                  variable = HurryUp ).grid(row=3,
                                            column=9, padx=0,pady=0,
                                            sticky = "")
Spike = IntVar()
SpikeCheckBox = Tkinter.Checkbutton(frame, text="SpiketheBall",
                                  variable = Spike).grid(row=3,
                                            column=10, padx=0,pady=0,
                                            sticky = "")
Squib = IntVar()
SquibCheckBox = Tkinter.Checkbutton(frame, text="Squib Kick",
                                  variable = Squib).grid(row=2,
                                            column=3, padx=0,pady=0,
                                            sticky = "")
Onside = IntVar()
OnsideKickCheckBox = Tkinter.Checkbutton(frame, text="Onside Kick",
                                  variable = Onside).grid(row=2,
                                            column=4, padx=0,pady=0,
                                            sticky = "")
PlacementPunt = IntVar()
PlacementPuntCheckBox = Tkinter.Checkbutton(frame, text="Placement Punt",
                                  variable = PlacementPunt).grid(row=2,
                                            column=7, padx=0,pady=0,
                                            sticky = "")
FK = IntVar()
FreeKickCheckBox = Tkinter.Checkbutton(frame, text="Free Kick",
                                  variable = FK).grid(row=2,
                                            column=5, padx=0,pady=0,
                                            sticky = "")

TMW = Scoreboard()
TMWIndicatorLabel = TMW.WriteLabel(frame,"2 Min Warn",10,1,"white",
                                                "black",12,7,8,0,"W")

HailMaryPass = IntVar()
HailMaryPassCB = Tkinter.Checkbutton(frame, text="Hail Mary Pass",
                                  variable = HailMaryPass).grid(row=4,
                                            column=10, padx=0,pady=0,
                                            sticky = "")
ForceEndOfQ2 = IntVar()
ForceEndOfQ2CB = Tkinter.Checkbutton(frame, text="Force End of Q2",
                                  variable = ForceEndOfQ2).grid(row=6,
                                            column=1, padx=0,pady=0,
                                            sticky = "")
ForceYL = IntVar()
ForceYLCB = Tkinter.Checkbutton(frame, text="Force Fum/TD",
                                  variable = ForceYL).grid(row=6,
                                            column=2, padx=0,pady=0,
                                            sticky = "")
ForcePenalty = IntVar()
ForcePenaltyCB = Tkinter.Checkbutton(frame, text="Penalty",
                                  variable = ForcePenalty).grid(row=6,
                                            column=3, padx=0,pady=0,
                                            sticky = "")
ForceTD = IntVar()
ForceTDCB = Tkinter.Checkbutton(frame, text="Force TD",
                                  variable = ForceTD).grid(row=6,
                                            column=4, padx=0,pady=0,
                                            sticky = "")

ZeroYDs = IntVar()
ZeroYDsCB = Tkinter.Checkbutton(frame, text="0 YDs",
                                  variable = ZeroYDs).grid(row=6,
                                            column=5, padx=0,pady=0,
                                            sticky = "")

ForceFumble = IntVar()
ForceFumbleCB = Tkinter.Checkbutton(frame, text="Fumble",
                                  variable = ForceFumble).grid(row=6,
                                            column=6, padx=0,pady=0,
                                            sticky = "")

ForceBlockedPunt = IntVar()
ForceBlockedPuntCB = Tkinter.Checkbutton(frame, text="PBTD",
                                  variable = ForceBlockedPunt).grid(row=3,
                                            column=7, padx=0,pady=0,
                                            sticky = "")

QBTakesaKnee = IntVar()
QBTakesaKneeCB = Tkinter.Checkbutton(frame, text="Take a Knee",
                                  variable = QBTakesaKnee).grid(row=4,
                                            column=9, padx=0,pady=0,
                                            sticky = "")


TeamList = GeneralInfoFile.ReadGeneralInfo()    #Read the last 2 teams that 
                                                #played
homeTeamName = TeamList[0]
visitingTeamName = TeamList[1]
DF = TestTurtleGraphics.DrawField()             #Draw the football field


if __name__ == "__main__":
    root.mainloop(  )