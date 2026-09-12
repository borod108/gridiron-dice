#-----------------------------------------------------------------------------
# Name:        Executive
# Purpose:     Read stats from a webpage and create worksheet
# Revison      1.0
# Author:      Rick
# Created:     02/18/2020
# Copyright:   (c) Rick 2020
#-----------------------------------------------------------------------------

from Tkinter import *
from openpyxl import *  #Import Excel Library

import os               #Import os and sys libraries for file management
import sys


import TableExtraction      #Table Extraction Class
import Tkinter              #All of the widgets that we will need
import Tkinter as tk

global PAC12URL_Entry
global PAC12Int_Entry 

global Rushing_Stats        #Rushing statistics table
global StatTables    
global Table_IDs            #Allows separation of different stat categories
global Table_Index          #Points to a particular stat table
global Team_Stats           #Team statistics table
global Passing_Stats        #Passing statistics table    
global Receiving_Stats      #Receiving statistics table
global Defensive_Stats      #Individual defensive statistics table
global Punting_Stats        #Punting statistics table
global Field_Goal_Stats     #Field Goal statistics table
global Kickoff_Stats        #Kickoff statistics table
global Punt_Return_Stats    #Punt return statistics table
global Kick_Return_Stats    #Kick return statistics table
global Scoring_Stats        #Scoring statistics table
global Game_Results         #Game Results table
global Blocked_Kick_Stats   #Blocked kick table
global Blocked_Punt_Stats   #Blocked punt table
global URL_Entry            #URL Entry Field
global IntURL               #URL Entry
global P12lbSelection       #Pac-12 Listbox Selection       
global TeamStatURL          #Selected team's stat page URL
global TeamThatWasSelected  #Identifies the selected team
global IntNames
global IntData
global Pac12ConferenceFactor
global wsStats
global wsStats


Table_Index = 0 #Initialize

#Default entry in case none is specified.  Need to troubleshoot
URL_Entry = "https://utahstateaggies.com/sports/football/stats/2019"
IntURL = ""

#Dictionary definition.  Table_IDs identifies the table index that Pandas uses
#to extract the different tables that are part of the stat webpage e.g. Table
#0 is the Team Statistics table.  The conference factor is a cheesy way of passing an object
#to a called class
Table_IDs = {'Team_Stats': 0, 'Rushing_Stats': 1, 'Passing_Stats' : 2,  'Receiving_Stats' : 3, 
                    'Defensive_Stats' : 4, 'Punting_Stats' : 5, 'FieldGoal_Stats' : 6, 'Kickoff_Stats' : 7, 
                    'Punt_Return_Stats' : 8, 'Kickoff_Return_Stats' : 9, 'Scoring_Stats' : 10, 'Game_Results' : 11, 
                    'Table12' : 12, 'Blocked_Kicks' : 13, 'Blocked_Punts' : 14, 'Int_Names' : 15, 'Int_Stats' : 16, 
                    'ConferenceFactor' : 5.0} 
    
#Dictionary definition.  Table_Row_Lengths are the number of rows in each table and are initialized here
#but will be set by a method in the TableExtraction class
Table_Row_Lengths = {'Team_Stats': 55, 'Rushing_Stats': 10,  'Passing_Stats' : 5, 'Receiving_Stats' : 15, 
                                    'Defensive_Stats' : 60, 'Punting_Stats' : 5, 'FieldGoal_Stats' : 5, 'Kickoff_Stats' : 5, 
                                    'Punt_Return_Stats' : 5, 'Kickoff_Return_Stats' : 5, 'Scoring_Stats' : 20, 
                                    'Game_Results' : 15, 'Blocked_Kicks' : 60, 'Blocked_Punts' : 60, 'Int_Names' : 60} 

#These are the worksheet starting points (rows) for each of the statistics categories
wsStartingPoints = {'Rushing_Stats': 2, 'Passing_Stats' : 15, 'Receiving_Stats' : 19, 'Kicking_Stats' : 36, 
                               'Punting_Stats' : 38, 'DefensiveTeam_Stats' : 46, 'KR_Stats' : 52, 'PR_Stats' : 55, 
                               'INT_Stats' : 58, 'OFumbles_Stats' : 67, 'Fumble_Recoveries' : 70, 'Team_Stats' : 91, 
                               'Tackle_Stats' : 94, 'LastRow' : 150} 

    
#-----------------------------------------------------------------------------
# Function Name:    CreateStatsWorksheet
# Purpose:          Creates, formats and populates stat file
# Author:           Rick Burney
# Created:          02/25/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def CreateStatsWorksheet():
  
    from openpyxl import Workbook   #Excel library
    import FormatStats                         #FormatStats class, does most of the work
    import StatsWorksheet                   #StatsWorksheet class, sets up the worksheet
    import Tkinter                               #Python widget library 
    import tkMessageBox                    #MessageBox widget
    
    global Blocked_Kick_Stats   #Blocked kick table    
    global Defensive_Stats        #Individual defensive statistics table
    global Field_Goal_Stats       #Field Goal statistics table
    global Game_Results          #Game Results table
    global Kick_Return_Stats    #Kick return statistics table
    global Kickoff_Stats            #Kickoff statistics table
    global Passing_Stats           #Passing statistics table    
    global Punt_Return_Stats    #Punt return statistics table
    global Punting_Stats           #Punting statistics table
    global Receiving_Stats        #Receiving statistics table
    global Rushing_Stats           #Rushing statistics table
    global Scoring_Stats            #Scoring statistics table
    global StatTables                 #List of the stat tables, actual table pointers in the list    
    global Table_IDs                     #List of the Table IDs
    global Table_Index                 #The actual table that is indexed from StatTables by the 
                                                   #Table ID
    global Table_Row_Lengths      #The number of rows in the extracted table    
    global Team_Stats                   #Team statistics table
    global TeamThatWasSelected
    global Table12
    global IntNames
    global IntData
    
    
    ContinueWithWorkSheet= NewWorksheet.get()     #Read check button
    if (ContinueWithWorkSheet == 0):
        tkMessageBox.showinfo\
            ("Warning", "Unless Checkbox is set, can't create a new worksheet")
        return
    
    
    NumberOfRushingTableColumns = 11  #For column headings in rushing table
     
#Instantiate a stats worksheet class object and create framework for worksheet
    wsStats = StatsWorksheet.StatsWorksheet(TeamThatWasSelected, 
                                        Table_Row_Lengths, wsStartingPoints)
    Test = wsStats.CreateWorksheetStructure()

#Now populate the worksheet with real stats.  Make sure that we can reference
#the correct worksheet, workbook and filename
    SWS = wsStats.ws                                                #Connect to worksheet and workbook                        
    SWB = wsStats.wb
    StatFileName = wsStats.FileName #Connect to correct file
    Table14 = []                                #Table 14 will remain blank but needs to be included in
                                                       #the Stat Table
    
#Form list of stat tables
    StatTables = [Team_Stats, Rushing_Stats, Passing_Stats, Receiving_Stats, 
                  Defensive_Stats, Punting_Stats, Field_Goal_Stats, Kickoff_Stats, 
                  Punt_Return_Stats, Kick_Return_Stats, Scoring_Stats, Game_Results, Table12, 
                  Blocked_Kick_Stats, Table14, IntNames, IntData] 
    StatTableLengths = []                                                           #Initialize list of table lengths
    
#Instantiate a formatted stats class object and call format executive
    FormattedStats = FormatStats.FormatStats(StatTables, SWS, SWB, 
                StatFileName,Table_Row_Lengths, Table_IDs, wsStartingPoints)
    Test = FormattedStats.FormatStatsExec()                                             

    
#-----------------------------------------------------------------------------
# Function Name:    ExtractStats
# Purpose:          Extract specific stats tables from the html file
# Author:           Rick Burney
# Created:          02/19/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def ExtractStats():

    import Tkinter 
    import tkMessageBox
    

    global Table_Index          #Points to a particular stat table
    global Team_Stats           #Team statistics table
    global Rushing_Stats        #Rushing statistics table
    global Passing_Stats        #Passing statistics table    
    global Receiving_Stats      #Receiving statistics table
    global Defensive_Stats      #Individual defensive statistics table
    global Punting_Stats        #Punting statistics table
    global Field_Goal_Stats     #Field Goal statistics table
    global Kickoff_Stats        #Kickoff statistics table
    global Punt_Return_Stats    #Punt return statistics table
    global Kick_Return_Stats    #Kick return statistics table
    global Scoring_Stats        #Scoring statistics table
    global Game_Results         #Game Results table
    global Blocked_Kick_Stats   #Blocked kick table    
    global URL_Entry                 #URL Entry 
    global IntURL                   #URL Entry 
    global P12lbSelection
    global TeamStatURL
    global Table12
    global IntNames
    global IntData
    global wsStats
    global wsStats
    
    ContinueWithWorkSheet= NewWorksheet.get()     #Read check button
    if (ContinueWithWorkSheet == 0):
        tkMessageBox.showinfo\
            ("Warning", "Unless Checkbox is set, can't create a new worksheet")
        return
    
    NumTables = 20  #Constant until can find a way to programmatically 
                    #determine number of tables
                    
#Also haven't found a way to cycle through tables and determine row numbers so
#will do this sequentially.

#Test code, normally commented out
    #TestMatrix = TableExtraction.TableExtraction(Table_IDs, Table_Index, URL_Entry, IntURL)
    #TestResult = TestMatrix.Print_Table_IDs()

#Extract team stats and # of rows    
    Table_Index = Table_IDs['Team_Stats']
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                    Table_Index, URL_Entry, IntURL)
    TRLM = TableRowLengthMatrix.DetermineTableRowLengths()
    NumberOfTeamStatTableRows = TableRowLengthMatrix.NumberOfRows
    Table_Row_Lengths['Team_Stats'] = NumberOfTeamStatTableRows
    Team_Stats = TableRowLengthMatrix.dfs[Table_Index]
    
    
#Extract rushing stats and # of rows - 2 since the last 2 rows are team stats    
    Table_Index = Table_IDs['Rushing_Stats']
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                    Table_Index, URL_Entry, IntURL)
    TRLM = TableRowLengthMatrix.DetermineTableRowLengths()
    NumberOfRushingTableRows = TableRowLengthMatrix.NumberOfRows
    Table_Row_Lengths['Rushing_Stats'] = NumberOfRushingTableRows - 2
    Rushing_Stats = TableRowLengthMatrix.dfs[Table_Index]
    #******Need to search for rows with 'NaN'

#Extract passing stats and # of rows  - 2  
    Table_Index = Table_IDs['Passing_Stats']
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                    Table_Index, URL_Entry, IntURL)
    TRLM = TableRowLengthMatrix.DetermineTableRowLengths()
    NumberOfPassingStatTableRows = TableRowLengthMatrix.NumberOfRows
    Table_Row_Lengths['Passing_Stats'] = NumberOfPassingStatTableRows - 2
    Passing_Stats = TableRowLengthMatrix.dfs[Table_Index]
    
#Extract receiving stats and # of rows  - 2  
    Table_Index = Table_IDs['Receiving_Stats']
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                Table_Index, URL_Entry, IntURL)
    TRLM = TableRowLengthMatrix.DetermineTableRowLengths()
    NumberOfReceivingStatTableRows = TableRowLengthMatrix.NumberOfRows
    Table_Row_Lengths['Receiving_Stats'] = NumberOfReceivingStatTableRows - 2
    Receiving_Stats = TableRowLengthMatrix.dfs[Table_Index]

#Extract receiving stats and # of rows  - 2  
    Table_Index = Table_IDs['Defensive_Stats']
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                    Table_Index, URL_Entry, IntURL) 
    TRLM = TableRowLengthMatrix.DetermineTableRowLengths()
    NumberOfDefensiveStatTableRows = TableRowLengthMatrix.NumberOfRows
    Table_Row_Lengths['Defensive_Stats'] = NumberOfDefensiveStatTableRows - 2
    Defensive_Stats = TableRowLengthMatrix.dfs[Table_Index]
    

#Extract punting stats and # of rows  - 2  
    Table_Index = Table_IDs['Punting_Stats']
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                    Table_Index, URL_Entry, IntURL)
    TRLM = TableRowLengthMatrix.DetermineTableRowLengths()
    NumberOfPuntingStatTableRows = TableRowLengthMatrix.NumberOfRows
    Table_Row_Lengths['Punting_Stats'] = NumberOfPuntingStatTableRows - 2
    Punting_Stats = TableRowLengthMatrix.dfs[Table_Index]
    

#Extract field goal stats and # of rows  - 2  
    Table_Index = Table_IDs['FieldGoal_Stats']
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                    Table_Index, URL_Entry, IntURL)
    TRLM = TableRowLengthMatrix.DetermineTableRowLengths()
    NumberOfFieldGoalStatTableRows = TableRowLengthMatrix.NumberOfRows
    Table_Row_Lengths['FieldGoal_Stats'] = NumberOfFieldGoalStatTableRows - 2
    Field_Goal_Stats = TableRowLengthMatrix.dfs[Table_Index]
    

#Extract kickoff stats and # of rows  - 2  
    Table_Index = Table_IDs['Kickoff_Stats']
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                    Table_Index, URL_Entry, IntURL)
    TRLM = TableRowLengthMatrix.DetermineTableRowLengths()
    NumberOfKickoffStatTableRows = TableRowLengthMatrix.NumberOfRows
    Table_Row_Lengths['Kickoff_Stats'] = NumberOfKickoffStatTableRows - 2
    Kickoff_Stats = TableRowLengthMatrix.dfs[Table_Index]
    

#Extract punt return stats and # of rows  - 2  
    Table_Index = Table_IDs['Punt_Return_Stats']
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                    Table_Index, URL_Entry, IntURL)
    TRLM = TableRowLengthMatrix.DetermineTableRowLengths()
    NumberOfPuntReturnStatTableRows = TableRowLengthMatrix.NumberOfRows
    Table_Row_Lengths['Punt_Return_Stats'] = NumberOfPuntReturnStatTableRows - 2
    Punt_Return_Stats = TableRowLengthMatrix.dfs[Table_Index]
    

#Extract kick return stats and # of rows  - 2  
    Table_Index = Table_IDs['Kickoff_Return_Stats']
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                    Table_Index, URL_Entry, IntURL)
    TRLM = TableRowLengthMatrix.DetermineTableRowLengths()
    NumberOfKickReturnStatTableRows = TableRowLengthMatrix.NumberOfRows
    Table_Row_Lengths['Kickoff_Return_Stats'] = NumberOfKickReturnStatTableRows - 2
    Kick_Return_Stats = TableRowLengthMatrix.dfs[Table_Index]
   

#Extract scoring stats (really want to just get PATs) and # of rows  - 2  
    Table_Index = Table_IDs['Scoring_Stats']
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                    Table_Index, URL_Entry, IntURL)
    TRLM = TableRowLengthMatrix.DetermineTableRowLengths()
    NumberOfScoringStatTableRows = TableRowLengthMatrix.NumberOfRows
    Table_Row_Lengths['Scoring_Stats'] = NumberOfScoringStatTableRows - 2
    Scoring_Stats = TableRowLengthMatrix.dfs[Table_Index]
   

#Extract game results to extract number of games played.  Last row should be
#ignored and the number of rows - 1 are the number of games played
    Table_Index = Table_IDs['Game_Results']
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                    Table_Index, URL_Entry, IntURL)
    TRLM = TableRowLengthMatrix.DetermineTableRowLengths()
    NumberOfGameResultsTableRows = TableRowLengthMatrix.NumberOfRows
    Table_Row_Lengths['Game_Results'] = NumberOfGameResultsTableRows - 1
    Game_Results = TableRowLengthMatrix.dfs[Table_Index]
    
    Table12 = []
   
#Extract blocked kicks
    Table_Index = Table_IDs['Blocked_Kicks']                                            #Choose table
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,  #Extract table
                                                    Table_Index, URL_Entry, IntURL)
    TRLM = TableRowLengthMatrix.DetermineTableRowLengths()          #Lose team rows
    BlockedKicksTableRows = TableRowLengthMatrix.NumberOfRows
    Table_Row_Lengths['Blocked_Kicks'] = BlockedKicksTableRows
    Blocked_Kick_Stats = TableRowLengthMatrix.dfs[Table_Index]
   
#Extract blocked punts
    Table_Index = Table_IDs['Blocked_Punts']
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                    Table_Index, URL_Entry, IntURL)
    TRLM = TableRowLengthMatrix.DetermineTableRowLengths()
    BlockedPuntsTableRows = TableRowLengthMatrix.NumberOfRows
    Table_Row_Lengths['Blocked_Punts'] = BlockedPuntsTableRows
    Blocked_Punt_Stats = TableRowLengthMatrix.dfs[Table_Index] 

#Extract Ints, names and yardage using a different webpage from the rest of the stats.  
#Create two objects.  A table with the defensive player names and a 1:1 table with the 
#defensive data from which the Int data may be extracted.
    Table_Index = 8                                               #First object
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                    Table_Index, URL_Entry, IntURL)
    TRLM = TableRowLengthMatrix.DetermineIntTableRowLengths()

    IntTableRows = TableRowLengthMatrix.NumberOfRows  #This will work for both objects    
    Table_Row_Lengths['Int_Names'] = IntTableRows
    IntNames = TableRowLengthMatrix.idfs[Table_Index]
    Table_Index = 9                                                   #2nd object
    TableRowLengthMatrix = TableExtraction.TableExtraction(Table_IDs,
                                                    Table_Index, URL_Entry, IntURL)
    IntData = TableRowLengthMatrix.idfs[Table_Index]
    
    tkMessageBox.showinfo("Done", "Stats Extracted From html file")

    
#-----------------------------------------------------------------------------
# Function Name:    ExtractURLs
# Purpose:          Extract URLs from selected team string
# Inputs:            Team selected from the listbox
# Author:           Rick Burney
# Created:          04/11/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def ExtractURLs(Teams, TeamName, lb, TeamStatURL):

    import Tkinter 
    import tkMessageBox
    
    global IntURL            #URL Entry for interception stats
    global URL_Entry       #URL Entry for all other stats
   
    for team in range(len(Teams)):                     #For all of the teams in this conference
        IndividualTeam = Teams[team]                #Extract the team name & URL
        
#Look for the tab delimiter to extract team stat URL        
        Tab_Index = IndividualTeam.find('\t')           
        
#Look for % sign that separates team stats from int stats        
        PercentIndex = IndividualTeam.find('%') 
        
#Extract team stats and Int stats URLs with next 3 statements
        TeamName.append(IndividualTeam[0:Tab_Index] )                      
        TeamStatURL.append(IndividualTeam[Tab_Index+1:  PercentIndex])                          
        IntStatURL.append(IndividualTeam[PercentIndex + 1 : len(IndividualTeam)])
        
        lb.insert('end', TeamName[team])                                   #Add team names to listbox
    TSU = [TeamStatURL, IntStatURL]
    return TSU  
 

 

#-----------------------------------------------------------------------------
# Function Name:    American_Selection
# Purpose:          Defines the behavior of the American Listbox.  Function that prints the  
#                         listbox selection in the label field.  This function is invoked when the  
#                         American Selection button is pressed.  Note American=American Athletic
#                         Conference
# Author:           Rick Burney
# Created:          05/28/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def American_Selection():
    
    global URL_Entry                      #Selected team's stat page URL
    global IntURL                           #Selected team's interception page URL 
    global ACClbSelection              #Selection from this listbox
    global ACCTSU

#String representing the team that was selected from the LB
    global TeamThatWasSelected   
    global Table_IDs                        #ID for each table from the stat page        
    
    
    AmericanT = AmericanTSU[0]
    AmericanInt = AmericanTSU[1]
    Table_IDs['ConferenceFactor'] = 4.9   #Conference factor for this particular conference
    
#This retrieves the listbox item # of the selected item.  It is a tuple in the form of
#(item #, column #) (Columns to account for multi-column listboxes).  To extract the item #,
#read that index, you would use AmericanlbSelection[0]
    AmericanlbSelection = Americanlb.curselection()  

#The listbox index (AmericanlbSelection[0]) is used to address a list of URLs such that the 
#URLs corresponding to the selected team from the listbox are assigned to URL_Entry and 
#IntURL, respectively.  URL_Entry is the URL for the selected team's stats.
    URL_Entry = AmericanT[AmericanlbSelection[0]]  
    IntURL = AmericanInt[AmericanlbSelection[0]]         #Int Stats come from a different page

#This object is the acronym that is used throughout for the team that is selected
    TeamThatWasSelected = Americanlb.get(Americanlb.curselection())  
    
 
#-----------------------------------------------------------------------------
# Function Name:    ACC_Selection
# Purpose:          Defines the behavior of the ACC Listbox.  Function that prints the listbox 
#                         selection in the label field.  This function is invoked when the ACC 
#                         Selection button is pressed.
# Author:           Rick Burney
# Created:          04/16/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def ACC_Selection():
    
    global URL_Entry                      #Selected team's stat page URL
    global IntURL                           #Selected team's interception page URL 
    global ACClbSelection              #Selection from this listbox
    global ACCTSU

#String representing the team that was selected from the LB
    global TeamThatWasSelected   
    global Table_IDs                        #ID for each table from the stat page        
    
    
    ACCT = ACCTSU[0]
    ACCInt = ACCTSU[1]
    Table_IDs['ConferenceFactor'] = 5.0   #Conference factor for this particular conference
    
#This retrieves the listbox item # of the selected item.  It is a tuple in the form of
#(item #, column #) (Columns to account for multi-column listboxes).  To extract the item #,
#read that index, you would use ACClbSelection[0]
    ACClbSelection = ACClb.curselection()  

#The listbox index (ACClbSelection[0]) is used to address a list of URLs such that the URLs
#corresponding to the selected team from the listbox are assigned to URL_Entry and IntURL,
#respectively.  URL_Entry is the URL for the selected team's stats.
    URL_Entry = ACCT[ACClbSelection[0]]  
    IntURL = ACCInt[ACClbSelection[0]]                     #Int Stats come from a different page

#This object is the acronym that is used throughout for the team that is selected
    TeamThatWasSelected = ACClb.get(ACClb.curselection())  
 

#-----------------------------------------------------------------------------
# Function Name:    Big_10_Selection
# Purpose:          Defines the behavior of the Big-10 Listbox.  Function that prints the listbox 
#                         selection in the label field.  This function is invoked when the Big-10
#                         Selection button is pressed.
# Author:           Rick Burney
# Created:          05/3/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def Big_10_Selection():
    
    global URL_Entry                      #Selected team's stat page URL
    global IntURL                           #Selected team's interception page URL 
    global Big_10lbSelection          #Selection from this listbox
    global Big_10TSU

#String representing the team that was selected from the LB
    global TeamThatWasSelected   
    global Table_IDs                        #ID for each table from the stat page        
    
    
    Big_10T = Big_10TSU[0]
    Big_10Int = Big_10TSU[1]
    Table_IDs['ConferenceFactor'] = 5.0   #Conference factor for this particular conference
    
#This retrieves the listbox item # of the selected item.  It is a tuple in the form of
#(item #, column #) (Columns to account for multi-column listboxes).  To extract the item #,
#read that index, you would use Big_10lbSelection[0]
    Big_10lbSelection = Big_10lb.curselection()  

#The listbox index (Big_10lbSelection[0]) is used to address a list of URLs such that the URLs
#corresponding to the selected team from the listbox are assigned to URL_Entry and IntURL,
#respectively.  URL_Entry is the URL for the selected team's stats.
    URL_Entry = Big_10T[Big_10lbSelection[0]]  
    IntURL = Big_10Int[Big_10lbSelection[0]]                   #Int Stats come from a different page

#This object is the acronym that is used throughout for the team that is selected
    TeamThatWasSelected = Big_10lb.get(Big_10lb.curselection())  
    

#-----------------------------------------------------------------------------
# Function Name:    Big_12_Selection
# Purpose:          Defines the behavior of the Big-12 Listbox.  Function that prints the listbox 
#                         selection in the label field.  This function is invoked when the Big-12 
#                         Selection button is pressed.
# Author:           Rick Burney
# Created:          04/30/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def Big_12_Selection():
    
    global URL_Entry                      #Selected team's stat page URL
    global IntURL                           #Selected team's interception page URL 
    global Big_12lbSelection          #Selection from this listbox
    global Big_12TSU

#String representing the team that was selected from the LB
    global TeamThatWasSelected   
    global Table_IDs                        #ID for each table from the stat page        
    
    
    Big_12T = Big_12TSU[0]
    Big_12Int = Big_12TSU[1]
    Table_IDs['ConferenceFactor'] = 5.0   #Conference factor for this particular conference
    
#This retrieves the listbox item # of the selected item.  It is a tuple in the form of
#(item #, column #) (Columns to account for multi-column listboxes).  To extract the item #,
#read that index, you would use Big_12lbSelection[0]
    Big_12lbSelection = Big_12lb.curselection()  

#The listbox index (Big_12lbSelection[0]) is used to address a list of URLs such that the URLs
#corresponding to the selected team from the listbox are assigned to URL_Entry and IntURL,
#respectively.  URL_Entry is the URL for the selected team's stats.
    URL_Entry = Big_12T[Big_12lbSelection[0]]  
    IntURL = Big_12Int[Big_12lbSelection[0]]                   #Int Stats come from a different page

#This object is the acronym that is used throughout for the team that is selected
    TeamThatWasSelected = Big_12lb.get(Big_12lb.curselection())  
 

#-----------------------------------------------------------------------------
# Function Name:    CUSA_Selection
# Purpose:          Defines the behavior of the C-USA Listbox.  Function that prints the listbox 
#                         selection in the label field.  This function is invoked when the C-USA 
#                         Selection button is pressed.
# Author:           Rick Burney
# Created:          04/30/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def CUSA_Selection():
    
    global URL_Entry                      #Selected team's stat page URL
    global IntURL                           #Selected team's interception page URL 
    global CUSAlbSelection          #Selection from this listbox
    global CUSATSU

#String representing the team that was selected from the LB
    global TeamThatWasSelected   
    global Table_IDs                        #ID for each table from the stat page        
    
    
    CUSAT = CUSATSU[0]
    CUSAInt = CUSATSU[1]
    Table_IDs['ConferenceFactor'] = 4.5   #Conference factor for this particular conference
    
#This retrieves the listbox item # of the selected item.  It is a tuple in the form of
#(item #, column #) (Columns to account for multi-column listboxes).  To extract the item #,
#read that index, you would use CUSAlbSelection[0]
    CUSAlbSelection = CUSAlb.curselection()  

#The listbox index (CUSAlbSelection[0]) is used to address a list of URLs such that the URLs
#corresponding to the selected team from the listbox are assigned to URL_Entry and IntURL,
#respectively.  URL_Entry is the URL for the selected team's stats.
    URL_Entry = CUSAT[CUSAlbSelection[0]]  
    IntURL = CUSAInt[CUSAlbSelection[0]]                   #Int Stats come from a different page

#This object is the acronym that is used throughout for the team that is selected
    TeamThatWasSelected = CUSAlb.get(CUSAlb.curselection())  


#-----------------------------------------------------------------------------
# Function Name:    FCS_Selection
# Purpose:          Defines the behavior of the FCS Listbox.  Function that prints the 
#                       listbox selection in the label field.  This function is invoked when the 
#                       FCS Selection button is pressed.
# Author:           Rick Burney
# Created:          04/23/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def FCS_Selection():
    
    global URL_Entry                      #Selected team's stat page URL
    global IntURL                           #Selected team's interception page URL 
    global FCSlbSelection               #Selection from this listbox
    global FCSTSU

#String representing the team that was selected from the LB
    global TeamThatWasSelected   
    global Table_IDs                        #ID for each table from the stat page        
        
    FCST = FCSTSU[0]
    FCSInt = FCSTSU[1]
    Table_IDs['ConferenceFactor'] = 4.2   #Conference factor for this particular conference
    
#This retrieves the listbox item # of the selected item.  It is a tuple in the form of
#(item #, column #) (Columns to account for multi-column listboxes).  To extract the item #,
#read that index, you would use FCSlbSelection[0]
    FCSlbSelection = FCSlb.curselection()  

#The listbox index (FCSlbSelection[0]) is used to address a list of URLs such that the URLs
#corresponding to the selected team from the listbox are assigned to URL_Entry and IntURL,
#respectively.  URL_Entry is the URL for the selected team's stats.
    URL_Entry = FCST[FCSlbSelection[0]]  
    IntURL = FCSInt[FCSlbSelection[0]]                     #Int Stats come from a different page

#This object is the acronym that is used throughout for the team that is selected
    TeamThatWasSelected = FCSlb.get(FCSlb.curselection())  


#-----------------------------------------------------------------------------
# Function Name:    MAC_Selection
# Purpose:          Defines the behavior of the MAC Listbox.  Function that prints the 
#                       listbox selection in the label field.  This function is invoked when the 
#                       MAC Selection button is pressed.
# Author:           Rick Burney
# Created:          04/12/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def MAC_Selection():
    
    global URL_Entry                      #Selected team's stat page URL
    global IntURL                           #Selected team's interception page URL 
    global MAClbSelection               #Selection from this listbox
    global MACTSU

#String representing the team that was selected from the LB
    global TeamThatWasSelected   
    global Table_IDs                        #ID for each table from the stat page        
        
    MACT = MACTSU[0]
    MACInt = MACTSU[1]
    Table_IDs['ConferenceFactor'] = 4.6   #Conference factor for this particular conference
    
#This retrieves the listbox item # of the selected item.  It is a tuple in the form of
#(item #, column #) (Columns to account for multi-column listboxes).  To extract the item #,
#read that index, you would use MAClbSelection[0]
    MAClbSelection = MAClb.curselection()  

#The listbox index (MWlbSelection[0]) is used to address a list of URLs such that the URLs
#corresponding to the selected team from the listbox are assigned to URL_Entry and IntURL,
#respectively.  URL_Entry is the URL for the selected team's stats.
    URL_Entry = MACT[MAClbSelection[0]]  
    IntURL = MACInt[MAClbSelection[0]]                     #Int Stats come from a different page

#This object is the acronym that is used throughout for the team that is selected
    TeamThatWasSelected = MAClb.get(MAClb.curselection())  
 

#-----------------------------------------------------------------------------
# Function Name:    Mountain_West_Selection
# Purpose:          Defines the behavior of the Mountain West Listbox.  Function that prints the 
#                       listbox selection in the label field.  This function is invoked when the 
#                       Mountain West Selection button is pressed.
# Author:           Rick Burney
# Created:          04/12/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def Mountain_West_Selection():
    
    global URL_Entry                      #Selected team's stat page URL
    global IntURL                           #Selected team's interception page URL 
    global MWlbSelection               #Selection from this listbox
    global MWTSU

#String representing the team that was selected from the LB
    global TeamThatWasSelected   
    global Table_IDs                        #ID for each table from the stat page        
    
    
    MWT = MWTSU[0]
    MWInt = MWTSU[1]
    Table_IDs['ConferenceFactor'] = 4.7   #Conference factor for this particular conference
    
#This retrieves the listbox item # of the selected item.  It is a tuple in the form of
#(item #, column #) (Columns to account for multi-column listboxes).  To extract the item #,
#read that index, you would use MWlbSelection[0]
    MWlbSelection = MWlb.curselection()  

#The listbox index (MWlbSelection[0]) is used to address a list of URLs such that the URLs
#corresponding to the selected team from the listbox are assigned to URL_Entry and IntURL,
#respectively.  URL_Entry is the URL for the selected team's stats.
    URL_Entry = MWT[MWlbSelection[0]]  
    IntURL = MWInt[MWlbSelection[0]]                     #Int Stats come from a different page

#This object is the acronym that is used throughout for the team that is selected
    TeamThatWasSelected = MWlb.get(MWlb.curselection())  
    

#-----------------------------------------------------------------------------
# Function Name:    Pac_12Selection
# Purpose:          Defines the behavior of the Pac-12 Listbox.  Function that prints the listbox 
#                       selection in the label field.  This function is invoked when the Pac-12 
#                       Selection button is pressed.
# Author:           Rick Burney
# Created:          02/19/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def Pac_12Selection():
    
    global URL_Entry                      #Selected team's stat page URL
    global IntURL                           #Selected team's interception page URL 
    global P12lbSelection               #Selection from this listbox
    global P12TSU

#String representing the team that was selected from the LB
    global TeamThatWasSelected   
    global Table_IDs                        #ID for each table from the stat page        
    
    
    P12T = P12TSU[0]
    P12Int = P12TSU[1]
    Table_IDs['ConferenceFactor'] = 5.0   #Conference factor for this particular conference
    
#This retrieves the listbox item # of the selected item.  It is a tuple in the form of
#(item #, column #) (Columns to account for multi-column listboxes).  To extract the item #,
#read that index, you would use P12lbSelection[0]
    P12lbSelection = P12lb.curselection()  

#The listbox index (P12lbSelection[0]) is used to address a list of URLs such that the URLs
#corresponding to the selected team from the listbox are assigned to URL_Entry and IntURL,
#respectively.  URL_Entry is the URL for the selected team's stats.
    URL_Entry = P12T[P12lbSelection[0]]  
    IntURL = P12Int[P12lbSelection[0]]                     #Int Stats come from a different page

#This object is the acronym that is used throughout for the team that is selected
    TeamThatWasSelected = P12lb.get(P12lb.curselection())   
                                                                      
    
#-----------------------------------------------------------------------------
# Function Name:    QuitApp
# Purpose:               Exits the App
# Author:                 Rick Burney
# Created:                02/19/2020
# Copyright:            (c) Rick 2020
#-----------------------------------------------------------------------------
def QuitApp():
    
    import Tkinter  #Needed to be able to destroy all widgets      
    root.destroy()    #Quit the application 
    

#-----------------------------------------------------------------------------
# Function Name:    SECSelection
# Purpose:          Defines the behavior of the SEC Listbox.  Function that prints the listbox 
#                       selection in the label field.  This function is invoked when the SEC Selection 
#                       Button is pressed.
# Author:           Rick Burney
# Created:          04/10/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def SECSelection():
    
    global IntURL                           #Selected team's interception page URL 
    global SEClbSelection               #Selection from this listbox
    global SECTSU
    global URL_Entry                      #Selected team's stat page URL

#String representing the team that was selected from the LB
    global TeamThatWasSelected   
    global Table_IDs                        #ID for each table from the stat page        
    
    SECT = SECTSU[0]
    SECInt = SECTSU[1]
    Table_IDs['ConferenceFactor'] = 5.0   #Conference factor for this particular conference
    
#This retrieves the listbox item # of the selected item.  It is a tuple in the form of
#(item #, column #) (Columns to account for multi-column listboxes).  To extract the item #,
#read that index, you would useSEClbSelection[0]
    SEClbSelection = SEClb.curselection()  

#The listbox index (SEClbSelection[0]) is used to address a list of URLs such that the URLs
#corresponding to the selected team from the listbox are assigned to URL_Entry and IntURL,
#respectively.  URL_Entry is the URL for the selected team's stats.
    URL_Entry = SECT[SEClbSelection[0]]  
    IntURL = SECInt[SEClbSelection[0]]                     #Int Stats come from a different page

#This object is the acronym that is used throughout for the team that is selected
    TeamThatWasSelected = SEClb.get(SEClb.curselection())   
    

#-----------------------------------------------------------------------------
# Function Name:    SunSelection
# Purpose:          Defines the behavior of the Sun Belt Listbox.  Function that prints the  
#                       listbox selection in the label field.  This function is invoked when the Sun 
#                       Belt Selection Button is pressed.
# Author:           Rick Burney
# Created:          06/3/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def SunSelection():
    
    global IntURL                           #Selected team's interception page URL 
    global SunlbSelection               #Selection from this listbox
    global SunTSU
    global URL_Entry                      #Selected team's stat page URL

#String representing the team that was selected from the LB
    global TeamThatWasSelected   
    global Table_IDs                        #ID for each table from the stat page        
    
    SunT = SunTSU[0]
    SunInt = SunTSU[1]
    Table_IDs['ConferenceFactor'] = 4.4   #Conference factor for this particular conference
    
#This retrieves the listbox item # of the selected item.  It is a tuple in the form of
#(item #, column #) (Columns to account for multi-column listboxes).  To extract the item #,
#read that index, you would use SunlbSelection[0]
    SunlbSelection = Sunlb.curselection()  

#The listbox index (SunlbSelection[0]) is used to address a list of URLs such that the URLs
#corresponding to the selected team from the listbox are assigned to URL_Entry and IntURL,
#respectively.  URL_Entry is the URL for the selected team's stats.
    URL_Entry = SunT[SunlbSelection[0]]  
    IntURL = SunInt[SunlbSelection[0]]                     #Int Stats come from a different page

#This object is the acronym that is used throughout for the team that is selected
    TeamThatWasSelected = Sunlb.get(Sunlb.curselection())   
    

#-----------------------------------------------------------------------------
# Function Name:   IndSelection
# Purpose:          Defines the behavior of the Independent Listbox.  Function that prints the 
#                       listbox selection in the label field.  This function is invoked when the 
#                       Independent Selection Button is pressed.
# Author:           Rick Burney
# Created:          04/27/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def IndSelection():
    
    global IntURL                           #Selected team's interception page URL 
    global IndlbSelection               #Selection from this listbox
    global IndTSU
    global URL_Entry                      #Selected team's stat page URL

#String representing the team that was selected from the LB
    global TeamThatWasSelected   
    global Table_IDs                        #ID for each table from the stat page        
    
    IndT = IndTSU[0]
    IndInt = IndTSU[1]
    Table_IDs['ConferenceFactor'] = 5.0   #Conference factor for this particular conference
    
#This retrieves the listbox item # of the selected item.  It is a tuple in the form of
#(item #, column #) (Columns to account for multi-column listboxes).  To extract the item #,
#read that index, you would useIndlbSelection[0]
    IndlbSelection = Indlb.curselection()  

#The listbox index (IndlbSelection[0]) is used to address a list of URLs such that the URLs
#corresponding to the selected team from the listbox are assigned to URL_Entry and IntURL,
#respectively.  URL_Entry is the URL for the selected team's stats.
    URL_Entry = IndT[IndlbSelection[0]]  
    IntURL = IndInt[IndlbSelection[0]]                     #Int Stats come from a different page

#This object is the acronym that is used throughout for the team that is selected
    TeamThatWasSelected = Indlb.get(Indlb.curselection())   
    

#-----------------------------------------------------------------------------
# Function Name:   IndSelection
# Purpose:          Defines the behavior of the Independent Listbox.  Function that prints the 
#                       listbox selection in the label field.  This function is invoked when the 
#                       Independent Selection Button is pressed.
# Author:           Rick Burney
# Created:          04/27/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def IndSelection():
    
    global IntURL                           #Selected team's interception page URL 
    global IndlbSelection               #Selection from this listbox
    global IndTSU
    global URL_Entry                      #Selected team's stat page URL

#String representing the team that was selected from the LB
    global TeamThatWasSelected   
    global Table_IDs                        #ID for each table from the stat page        
    
    IndT = IndTSU[0]
    IndInt = IndTSU[1]
    Table_IDs['ConferenceFactor'] = 5.0   #Conference factor for this particular conference
    
#This retrieves the listbox item # of the selected item.  It is a tuple in the form of
#(item #, column #) (Columns to account for multi-column listboxes).  To extract the item #,
#read that index, you would useIndlbSelection[0]
    IndlbSelection = Indlb.curselection()  

#The listbox index (IndlbSelection[0]) is used to address a list of URLs such that the URLs
#corresponding to the selected team from the listbox are assigned to URL_Entry and IntURL,
#respectively.  URL_Entry is the URL for the selected team's stats.
    URL_Entry = IndT[IndlbSelection[0]]  
    IntURL = IndInt[IndlbSelection[0]]                     #Int Stats come from a different page

#This object is the acronym that is used throughout for the team that is selected
    TeamThatWasSelected = Indlb.get(Indlb.curselection())
    
#-----------------------------------------------------------------------------
# Function Name: ReWriteStatsButton
# Purpose:            Calls the ReWriteStats class to update stats (updated CPs for example)
# Author:             Rick Burney
# Created:            02/25/2020
# Copyright:        (c) Rick 2020
#-----------------------------------------------------------------------------
def ReWriteStatsButton():

    import FormatStats          #Classes that will be needed
    import StatsWorksheet
    import openpyxl             #Excel library for Python
    import ReWriteStats                         #Class that does the rewrites
    from openpyxl import Workbook     #Workbook methods from Excel library 

    global TeamThatWasSelected          #Listbox selection
 
 #Need two workbooks.  Read the selected team's stat file into the first workbook.  Copy
 #them into the 2nd workbook (may not be necessary). make the changes desired and then
 #write the entire workbook to the original file.  Ultimately, want to use one workbook
 
    FileName = TeamThatWasSelected + ".xlsx"    #Filename for Excel worksheet   
    wb = openpyxl.load_workbook(FileName)       #Load file into first workbook    
    wb1 = Workbook()                                          #Create a 2nd workbook
    ws = wb.active                                                #Refer to the active worksheet for both
    ws1 = wb1.active                                            #workbooks
    ws.title = TeamThatWasSelected                     #Change title of worksheet to team name  
    ws1.title = TeamThatWasSelected                   #for both workbooks  
    for i in range(180):                                        #Read first wb and copy into 2nd wb
        for j in range(13):
            ws1.cell(row = i+1, column = j+1).value = ws.cell(row = i+1, column = j+1).value

#Instantiate a RewriteStats class object,  pass in the ws and call the executive    
    ReWrittenStats = ReWriteStats.ReWriteStats(ws1, wb1, FileName)          
    Test = ReWrittenStats.ReWriteStatsExec()                
            
        
#***************************MAIN LOOP****************************************

#Program starts here
root = Tkinter.Tk(  )

#Have the display grab the focus
#os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of \
#process "Python" to true' ''')

#Draw control panel, using grid geometry to place widgets
QuitButtonRow = 8
ReWriteStatsButtonRow = 7
root.geometry("1400x700")              #Original size was 1350 x 600, will increase size as we 
                                                        #add listboxes
root.configure(background='grey')   #Set main window background to grey

frame = Frame(root, height =  2000, width = 600, bg = 'grey')
frame.grid_rowconfigure(QuitButtonRow, weight=1)                    #Allows the Quit button to
frame.pack(fill=BOTH, expand=1)                                   #move to the bottom of the frame

#BUTTONS                           
#Extract Stats Button.  This starts the major part of this as stats are extracted from the web
#page and put into tables
ES = Tkinter.Button(frame,  text="Extract Stats", 
                    command=ExtractStats).grid(row = 1, column = 0)

#Quit Button.  This wraps everything up and quits the app
QB = Tkinter.Button(frame, text="Quit",command=QuitApp).grid(row = QuitButtonRow, 
                                                             column = 0)

#ReWriteStats Button.  This allows cum probabilities to be recomputed upon a change to 
#the worksheet
RWS = Tkinter.Button(frame, text="ReWrite Stats",
                command=ReWriteStatsButton).grid(row = ReWriteStatsButtonRow, column = 0)


#***************START American (AAC) TEAM CODE**********************************
# Open function to open the file "American Team Stats.txt" (same directory) in append 
#mode and read file.  TeamName a list of team name acronyms that populate the list  box 
#for this conference
TeamName = []       #Start with empty lists                   
TeamStatURL = []    #List of associated team stat URLs for each team in the conference
IntStatURL = []         #list of associated Int stat URLs for each team in the conference

#Open the URL file for this conference and read into a list for subsequent parsing
AmericanFile = open("American Team Stats.txt","r")  
Teams = AmericanFile.readlines()                          

#Define the functionality of the American Selection button
b1 = tk.Button(frame, text='American', width=15, height=2,             
               command=American_Selection).grid(row = 0, column = 1)  

#There is a text file with a list of team name acronyms and their associated cumulative stats
#file and a separate file to extract interception stats since the cum stats file does not have
#INT yardage
Americanlb = tk.Listbox(frame, height = 12)                        #Create and position a listbox
Americanlb.grid(row = 1, column = 1)           
AmericanTSU = ExtractURLs(Teams, TeamName, Americanlb, TeamStatURL)
#***************END American (AAC) TEAM CODE**********************************


#***************START ACC TEAM CODE**********************************
# Open function to open the file "ACC Team Stats.txt" (same directory) in append 
#mode and read file.  TeamName a list of team name acronyms that populate the list  box 
#for this conference
TeamName = []                   
TeamStatURL = []    #List of associated team stat URLs for each team in the conference
IntStatURL = []         #list of associated Int stat URLs for each team in the conference

#Open the URL file for this conference and read into a list for subsequent parsing
ACCFile = open("ACC Team Stats.txt","r")  
Teams = ACCFile.readlines()                          

#Define the functionality of the ACC Selection button
b1 = tk.Button(frame, text='ACC', width=15, height=2,             
               command=ACC_Selection).grid(row = 0, column = 2)  

ACClb = tk.Listbox(frame, height = 12)                                   #Create and position a listbox
ACClb.grid(row = 1, column = 2) 

#From the file that lists the URLs associated with each team's cumulative stats for this 
#conference, populate the listbox with the conference teams and their associated URLs for
#stats
ACCTSU = ExtractURLs(Teams, TeamName, ACClb, TeamStatURL)
#***************END ACC TEAM CODE**********************************


#***************START Big-10 TEAM CODE**********************************
# Open function to open the file "Big-10 Team Stats.txt" (same directory) in append 
#mode and read file.  TeamName a list of team name acronyms that populate the list box
#for this conference
TeamName = []                   
TeamStatURL = []    #List of associated team stat URLs for each team in the conference
IntStatURL = []         #list of associated Int stat URLs for each team in the conference

#Open the URL file for this conference and read into a list for subsequent parsing
Big_10File = open("Big-10 Team Stats.txt","r")  
Teams = Big_10File.readlines()                          

#Define the functionality of the Big-10 Selection button
b1 = tk.Button(frame, text='Big-10', width=15, height=2,             
               command=Big_10_Selection).grid(row = 0, column = 3)  

Big_10lb = tk.Listbox(frame, height = 12)                            #Create and position a listbox
Big_10lb.grid(row = 1, column =  3)           
Big_10TSU = ExtractURLs(Teams, TeamName, Big_10lb, TeamStatURL)
#***************END Big-10 TEAM CODE**********************************


#***************START Big-12 TEAM CODE**********************************
# Open function to open the file "Big-12 Team Stats.txt" (same directory) in append 
#mode and read file.  TeamName a list of team name acronyms that populate the list  box 
#for this conference
TeamName = []                   
TeamStatURL = []    #List of associated team stat URLs for each team in the conference
IntStatURL = []         #list of associated Int stat URLs for each team in the conference

#Open the URL file for this conference and read into a list for subsequent parsing
Big_12File = open("Big-12 Team Stats.txt","r")  
Teams = Big_12File.readlines()                          

#Define the functionality of the Big-12 Selection button
b1 = tk.Button(frame, text='Big-12', width=15, height=2,             
               command=Big_12_Selection).grid(row = 0, column = 4)  

Big_12lb = tk.Listbox(frame, height = 12)                                #Create and position a listbox
Big_12lb.grid(row = 1, column = 4)           
Big_12TSU = ExtractURLs(Teams, TeamName, Big_12lb, TeamStatURL)
#***************END Big-12 TEAM CODE**********************************


#***************START C-USA TEAM CODE**********************************
# Open function to open the file "C-USA Team Stats.txt" (same directory) in append 
#mode and read file.  TeamName a list of team name acronyms that populate the list  box 
#for this conference
TeamName = []                   
TeamStatURL = []    #List of associated team stat URLs for each team in the conference
IntStatURL = []         #list of associated Int stat URLs for each team in the conference

#Open the URL file for this conference and read into a list for subsequent parsing
CUSAFile = open("C-USA Team Stats.txt","r")  
Teams = CUSAFile.readlines()                          

#Define the functionality of the Big-12 Selection button
b1 = tk.Button(frame, text='C-USA', width=15, height=2,             
               command=CUSA_Selection).grid(row = 0, column = 5)  

CUSAlb = tk.Listbox(frame, height = 12)                                   #Create and position a listbox
CUSAlb.grid(row = 1, column = 5)           
CUSATSU = ExtractURLs(Teams, TeamName, CUSAlb, TeamStatURL)
#***************END C-USA TEAM CODE**********************************


#***************START FCS TEAM CODE**********************************
# Open function to open the file "FCS Team Stats.txt" (same directory) in append 
#mode and read file.  TeamName is a list of team name acronyms that populate the list  box 
#for this conference
TeamName = []       #List of team name acronymns                  
TeamStatURL = []    #List of associated team stat URLs for each team in the conference
IntStatURL = []         #list of associated Int stat URLs for each team in the conference

#Open the URL file for this conference and read into a list for subsequent parsing
FCSFile = open("FCS Team Stats.txt","r")  
Teams = FCSFile.readlines()                                               

#Define the functionality of the FCS Selection button
b1 = tk.Button(frame, text='FCS', width=15, height=2,             
               command=FCS_Selection).grid(row = 0, column = 6)  

FCSlb = tk.Listbox(frame, height = 12)                                   #Create and position a listbox
FCSlb.grid(row = 1, column = 6)           
FCSTSU = ExtractURLs(Teams, TeamName, FCSlb, TeamStatURL)
#***************END FCS TEAM CODE**********************************


#***************START MAC TEAM CODE**********************************
# Open function to open the file "MAC Team Stats.txt" (same directory) in append 
#mode and read file.  TeamName a list of team name acronyms that populate the list  box 
#for this conference
TeamName = []                   
TeamStatURL = []    #List of associated team stat URLs for each team in the conference
IntStatURL = []         #list of associated Int stat URLs for each team in the conference

#Open the URL file for this conference and read into a list for subsequent parsing
MACFile = open("MAC Team Stats.txt","r")  
Teams = MACFile.readlines()                          

#Define the functionality of the Mountain West Selection button
b1 = tk.Button(frame, text='MAC', width=15, height=2,             
               command=MAC_Selection).grid(row = 2, column = 2)  

MAClb = tk.Listbox(frame, height = 12)                                   #Create and position a listbox
MAClb.grid(row = 3, column = 2)           
MACTSU = ExtractURLs(Teams, TeamName, MAClb, TeamStatURL)
#***************END MAC TEAM CODE**********************************


#***************START MOUNTAIN WEST TEAM CODE**********************************
# Open function to open the file "Mountain West Team Stats.txt" (same directory) in append 
#mode and read file.  TeamName a list of team name acronyms that populate the list  box 
#for this conference
TeamName = []                   
TeamStatURL = []    #List of associated team stat URLs for each team in the conference
IntStatURL = []         #list of associated Int stat URLs for each team in the conference

#Open the URL file for this conference and read into a list for subsequent parsing
Pac_12File = open("Mountain West Team Stats.txt","r")  
Teams = Pac_12File.readlines()                          

#Define the functionality of the Mountain West Selection button
b1 = tk.Button(frame, text='Mountain West', width=15, height=2,             
               command=Mountain_West_Selection).grid(row = 2, column = 3)  

MWlb = tk.Listbox(frame, height = 12)                                     #Create and position a listbox
MWlb.grid(row = 3, column = 3)           
MWTSU = ExtractURLs(Teams, TeamName, MWlb, TeamStatURL)
#***************END MOUNTAIN WEST TEAM CODE**********************************


#***************START PAC-12 TEAM CODE**********************************
# Open function to open the file "Pac-12 Team Stats.txt" (same directory) in append mode 
#and read file.  TeamName a list of team name acronyms that populate the list  box for this 
#conference
TeamName = []                   
TeamStatURL = []    #List of associated team stat URLs for each team in the conference
IntStatURL = []         #list of associated Int stat URLs for each team in the conference

Pac_12File = open("Pac-12 Team Stats.txt","r")  #Open the URL file for this conference and
Teams = Pac_12File.readlines()                          #read into a list for subsequent parsing

#Define the functionality of the Pac-12 Selection button
b1 = tk.Button(frame, text='Pac-12', width=15, height=2,             
               command=Pac_12Selection).grid(row = 2, column = 4)  

P12lb = tk.Listbox(frame, height = 12)                                     #Create and position a listbox
#scrollbar = Scrollbar(P12lb, orient=VERTICAL)   #New
#P12lb.config(yscrollcommand=scrollbar.set)   #New
#scrollbar.config(command=P12lb.yview)   #New
P12lb.grid(row = 3, column = 4)    #, rowspan=4)    #,
                   #columnspan=2, sticky=N+E+S+W)    #New
#P12lb.columnconfigure(3, weight=1)   #New
#scrollbar.grid(column=3, sticky=N+S)   #New
P12TSU = ExtractURLs(Teams, TeamName, P12lb, TeamStatURL)
#***************END PAC-12 TEAM CODE**********************************


#***************START SEC-12 TEAM CODE**********************************
# Open function to open the file "Pac-12 Team Stats.txt"  
# (same directory) in append mode and read file
TeamName = []                   #Create empty lists for the team names & the
TeamStatURL = []                #associated URLs
IntStatURL = []
SEC_12File = open("SEC Team Stats.txt","r") 
Teams = SEC_12File.readlines()

#Define the functionality of the SEC Selection button
b1 = tk.Button(frame, text='SEC', width=15, height=2,             
               command=SECSelection).grid(row = 2, column = 5)  

SEClb = tk.Listbox(frame, height = 12)                                     #Create and position a listbox
SEClb.grid(row = 3, column = 5)           
SECTSU = ExtractURLs(Teams, TeamName, SEClb, TeamStatURL)

#***************END SEC-12 TEAM CODE**********************************


#***************START Independent TEAM CODE**********************************
# Open function to open the file "Independent Team Stats.txt"  
# (same directory) in append mode and read file
TeamName = []                   #Create empty lists for the team names & the
TeamStatURL = []                #associated URLs
IntStatURL = []
IndFile = open("Independent Team Stats.txt","r") 
Teams = IndFile.readlines()

#Define the functionality of the Ind Selection button
b1 = tk.Button(frame, text='Ind', width=15, height=2,             
               command=IndSelection).grid(row = 2, column = 1)  

Indlb = tk.Listbox(frame, height = 12)                                     #Create and position a listbox
Indlb.grid(row = 3, column = 1)           
IndTSU = ExtractURLs(Teams, TeamName, Indlb, TeamStatURL)

#***************END Independent TEAM CODE**********************************


#***************START Sun Belt TEAM CODE**********************************
# Open function to open the file "Sun Belt Team Stats.txt"  
# (same directory) in append mode and read file
TeamName = []                   #Create empty lists for the team names & the
TeamStatURL = []                #associated URLs
IntStatURL = []
IndFile = open("Sun Belt Team Stats.txt","r") 
Teams = IndFile.readlines()

#Define the functionality of the Sun Belt Selection button
b1 = tk.Button(frame, text='Sun Belt', width=15, height=2,             
               command=SunSelection).grid(row = 2, column = 6)  

Sunlb = tk.Listbox(frame, height = 12)                                     #Create and position a listbox
Sunlb.grid(row = 3, column = 6)           
SunTSU = ExtractURLs(Teams, TeamName, Sunlb, TeamStatURL)

#***************END Independent TEAM CODE**********************************

                                     
#Define the functionality of the CreateStatsWorkSheet button
bSWS = tk.Button(frame, text='Create Worksheet', width=15, height=2, 
               command=CreateStatsWorksheet).grid(row = 2, column = 0)


NewWorksheet = IntVar()
TimeIsShort = Tkinter.Checkbutton(frame, text="Create New Worksheet",
                                  variable = NewWorksheet ).grid(row=5, column=4, padx=0,pady=0,
                                            sticky = "")



if __name__ == "__main__":
    root.mainloop(  )