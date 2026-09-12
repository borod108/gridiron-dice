from __future__ import division         #Division in this version of Python 
                                        #(2.7) only produces integer results.
                                        #This library solves this problem
from openpyxl.styles import Font        #Excel library for formatting the font
from openpyxl.styles import Alignment   #Excel library for aligning cells
from openpyxl import Workbook           #Workbook methods from Excel library 
import os                               #Libriaries for file management
import sys                              #Operating system library
import math                             #Math library

global Pac12ConferenceFactor

#****************************************************************************
#Method:   FormatStats
#Purpose:  This class contains all of the methods and objects needed to format 
#          all of the stats and write them to the worksheet
# Inputs:  Extracted Stats, Wroksheet, Workbook, Filename, Stat Table Lengths, 
#          Table_IDs, starting points
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/03/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
class FormatStats():

    def __init__(self, StatTables,SWS, SWB, StatFileName, Table_Row_Lengths, 
                 Table_IDs, wsStartingPoints):
        
        global Pac12ConferenceFactor
        
#Create objects that are visible within this class        
        self.StatTables = StatTables     
        self.wsStats = SWS
        self.wbStats = SWB
        self.StatFileName = StatFileName
        self.Table_Row_Lengths = Table_Row_Lengths
        self.Table_IDs = Table_IDs                  #Unique ID assigned to
                                                    #each stat table
        self.wsStartingPoints = wsStartingPoints
        self.TeamStatTable = []
        self.SacksByOpponent = 0
        self.TeamPassingAttempts = 500
        self.TeamRushingAttempts = 400
        self.PATs = ""
        self.PATPercentage = 100
        self.MaxRow = 0                 #Generally used for placekicking where multiple kickers
                                                   #were used and you are trying to find the kicker who had
                                                   #the most attempts
        self.PlaceKicker= ""
        self.Punter = ""
        self.FirstNumber = self.SecondNumber = self.ThirdNumber = 0
        self.AttemptsAgainst = self.CompletionsAgainst = self.InterceptionsBy = 0
        
        self.FumbleMultiplier = 10000   #Fumbles are computed in parts per 10k
        self.KickReturner = ""                 #Initialize the kick returner's name
        self.IntNameTable = []               #Initialize Interception name list
        self.IntDataTable = []                 #Initialize interception data list
        self.IntYardageTable = []           #Initialize interception yardage table-used for average
        self.FintNameList= []                 #Formatted int name list [First Name Last Name]
        self.FRNameList = []                                #Formatted fumble recovery list names
        self.NumberOfInterceptingPlayers = 0     #Initialize numbers of players who had ints
        self.GamesPlayed = 12                            #Initialize number of games played
        self.InjuryImpactStartingPoint = 133
        

#****************************************************************************
#Method:   CreateIntTable
#Purpose: Python kind of sucks for multi-dimensioned arrays.  You have to sync multiple
#              lists to get a 2nd dimension.  Oh well.  This method looks at the INT column in
#              IntData and selects a row of data for a new table if the row, column intersection
#              is > 0.  In other words, if a player had an INT, that player's data is placed in a new
#              table
#  Input:     IntNameTable, IntDataTable, NumRows             
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/20/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def CreateIntTable(self, IntNameTable, IntDataTable, NumRows):

#If a player had an INT, add this row to the new INT Table.  May have to use Table ID 4 for 
#names and IntDataTable for data
        IntColumn = 6                       #Column for # of Ints for a player
        YardageColumn = 7               #Int return yardage column for a player
        NameColumn = 1                  #Column with the name of a player who had at least 1 Int

        for i in range(NumRows):                                 #Go through the list of defensive players
            if IntDataTable.iloc[i, IntColumn] > 0:           #If a player had at least 1 Int  
                Ints = IntDataTable.iloc[i,IntColumn]                       #append Name, # of Ints and 
                IntYardage = IntDataTable.iloc[i,YardageColumn]    #yardage in Int Table
                self.IntDataTable.append(Ints)
                self.IntYardageTable.append(IntYardage)
                self.IntNameTable.append(IntNameTable[i])
                
#Create a formatted Int List to allow writing to the stats worksheet
        self.FintNameList = self.FPNForaList(self.IntNameTable, len(self.IntNameTable))
        self.NumberOfInterceptingPlayers = len(self.IntNameTable)


#****************************************************************************
#Method:   ExtractGamesPlayed
#****************************************************************************
    def ExtractGamesPlayed(self):
        PassingTable =  self.StatTables[self.Table_IDs['Passing_Stats']]
        NumRows = self.Table_Row_Lengths['Passing_Stats'] + 1
        self.GamesPlayed = PassingTable.iloc[NumRows, 2]
        
        

#****************************************************************************
#Method:   DefensiveTeamStatsFormat
#Purpose:  This method formats the defensive team stats into the worksheet
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/20/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def DefensiveTeamStatsFormat(self):

#Isolate defensive team stats
        DefensiveTeamStatsTable =  self.StatTables[self.Table_IDs['Team_Stats']]
        
#Extract defensive rushing yards per attempt and write to worksheet
        TableRow = 12
        TableColumn = 2
        wsColumn = 3
        DRushYdsPerAttempt = DefensiveTeamStatsTable.iloc[TableRow, TableColumn]
        
#Convert string to a float and write to worksheet
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'],
                          column = wsColumn).value = float(DRushYdsPerAttempt)  
        
#Make sure the cell is not bold
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'], 
                          column = wsColumn).font = Font(bold=False)
        
#Extract defense against the pass completion % and write to worksheet
        TableRow = 17
        DAgainstThePassCompPercentage = DefensiveTeamStatsTable.iloc[TableRow, 
                                                                     TableColumn]
        
#Call StringConversion(), Code 5 but understand that a string is passed in lieu of a Stat Table
#Extract passes attempted + completed against the team's D and INTs by the team's D
        Code = 5
        self.StringConversion(DAgainstThePassCompPercentage, 0, 0, Code) 
        self.AttemptsAgainst = int(self.FirstNumber)
        self.CompletionsAgainst = int(self.SecondNumber)
        self.InterceptionsBy =  int(self.ThirdNumber)
        CompletionPercentageAgainst = round(100 * self.CompletionsAgainst / \
                                            self.AttemptsAgainst, 1)
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'] + 1,
                          column = wsColumn).value = CompletionPercentageAgainst 

#Make sure the cell is not bold
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'] + 1, 
                          column = wsColumn).font = Font(bold=False)
        
        
#Extract yards per catch and write to worksheet.  First, must extract the total passing yards
#against the team.  Then divide by the previously computed Completions Against.  Write to 
#ws.  Total passing yards against is found in row 21 of the table
        TotalPassingYardsAgainstRow = 21        
        TotalPassingYardsAgainst = \
            int(DefensiveTeamStatsTable.iloc[TotalPassingYardsAgainstRow, TableColumn])
        YardsPerCatchAgainst = round(TotalPassingYardsAgainst / self.CompletionsAgainst, 1)
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'] + 2,
                          column = wsColumn).value = YardsPerCatchAgainst 

#Make sure the cell is not bold
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'] + 2, 
                          column = wsColumn).font = Font(bold=False)

#Compute defensive sacks by extracting sacks from Col 1 of the Team table and using the
#already computed self.AttemptsAgainst
        TableRow = 51
        TableColumn = 1
        Code = 6
        wsColumn = 6
        SacksByTheDefense =  DefensiveTeamStatsTable.iloc[TableRow, TableColumn]
        self.StringConversion(SacksByTheDefense, 0, 0, Code)
        DSacks = int(self.FirstNumber)
        DSackPercentage = round((100*DSacks/ self.AttemptsAgainst), 2)
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'] + 1,
                          column = wsColumn).value = DSackPercentage 

#Make sure the cell is not bold
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'] + 1, 
                          column = wsColumn).font = Font(bold=False)

#Punt and kick block information will have to be done manually. For now, we will just write 0
#by the opponent
        TableRow = 38       #Data about punts and kicks are not used at this time
        TableColumn = 2
        Code = 6
        wsColumn = 8    #Worksheet column for punt block stats.  Kick block stats are two 
                                   #columns to the left
                                   
        OpponentsPunts =  DefensiveTeamStatsTable.iloc[TableRow, TableColumn]
        self.StringConversion(OpponentsPunts, 0, 0, Code)
        OPunts = int(self.FirstNumber)
        
#Write zero to the punt block and kick block stats.  Consider changing this to 1 (%)
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'],
                          column = wsColumn).value = 0 
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'],
                          column = wsColumn - 2).value = 0 

#Make sure the cells are not bold
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'], 
                          column = wsColumn).font = Font(bold=False)
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'] + 1, 
                          column = wsColumn - 2).font = Font(bold=False)

#Compute Int % using self.InterceptionsBy and self.AttemptsAgainst

        wsColumn = 10   #Worksheet column for the team stats for interception percentage
        
#Int % is computed by dividing the number of team interceptions by the number of passes
#attempted against the team's defense
        IntPercentage = round((100*self.InterceptionsBy/ self.AttemptsAgainst), 2)
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'] ,
                          column = wsColumn).value = IntPercentage 

#Make sure the cell is not bold
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'] , 
                          column = wsColumn).font = Font(bold=False)

#Compute probability that defense will recover a fumble.            
        TableRow = 50                                                           #Location in team stats where             
        TableColumn = 2                                                        #fumble data is located
        wsColumn = 10                                           #Where in the ws this data will be written
        Code = 7            #This code tells StringConversion() how to extract the fumble data

#Extract the fumble data from the Team Stats table and then extract the number of fumbles        
        NumFum =  DefensiveTeamStatsTable.iloc[TableRow, TableColumn]
        self.StringConversion(NumFum, 0, 0, Code)
        FumblesRecoveredByTheD = int(self.SecondNumber) #Convert string to integer
        
        TableRow = 11       #Extract the # of rushing attempts against this defense
        TableColumn = 2
        RushingAttemptsAgainst = int(DefensiveTeamStatsTable.iloc[TableRow, TableColumn])
        
#Compute the probability of this defense recovering a fumble on any particular play (Run,
#pass completion or sack).  Probability is expressed in parts per 10,000.  Write this value to
#the worksheet
        PDFumbleRecovery = round((self.FumbleMultiplier * FumblesRecoveredByTheD)/\
                                 (RushingAttemptsAgainst + self.CompletionsAgainst + DSacks), 1)
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats']  + 1,
                          column = wsColumn).value = PDFumbleRecovery 

#Make sure the cell is not bold
        self.wsStats.cell(row = self.wsStartingPoints['DefensiveTeam_Stats'] + 1 , 
                          column = wsColumn).font = Font(bold=False)
              
        self.wbStats.save(filename = self.StatFileName) #Save file     
        
    

#****************************************************************************
#Method:   FormatPlayerName
#Purpose:  This method takes the player name format found in a stat table and
#          reformats into a <First Name, Last Name> format
# Inputs:  Specific stat table, last row 
# Outputs: Formatted player name
# Author:           Rick Burney
# Created:          03/03/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def FormatPlayerName(self,StatTable,EndRow):

#Some tables don't include the players number and a different approach must be
#used to format the player name.
        
#Find the name by matching the player's number with the number embedded in the
#unformatted name, extract the name before the embedded number, then find the
#comma and move the last name after the first name
        x = StatTable.iloc[0, 0]    #Test to see if 1st row has a NaN
        
#If NaN in row, use the following technique to format the name.  If there isn't a NaN in the first row, then 
#the if statement returns a false and the names are processed as expected
        if math.isnan(x):
            for i in range(EndRow):                                         #Cycle through the rows
                PlayerName = StatTable.iloc[i, 1]                       #Read the player name
                CommaPosition = PlayerName.find(",")              #Look for a comma
                LastName = PlayerName[0 : CommaPosition]    #Extract last name
                
#Extract First name and put them together
                FirstName = PlayerName[CommaPosition + 2 : len(PlayerName)]
                PlayerName = FirstName + " " + LastName
                CommaPosition = PlayerName.find(",")              #Look for 2nd comma
                PlayerName = PlayerName[0 : CommaPosition] #Keep name to left of comma
                StatTable.loc[i, "Player"] = PlayerName
                
        else:                                       #The else condition means there was a NaN found in the 1st Row
            for i in range(EndRow):
                x = StatTable.iloc[i, 0]    #Test for a row with a NaN
                if math.isnan(x):            #If found delete row if NaN is found
                    
                    self.Table_Row_Lengths['Rushing_Stats'] -= 1    #Decrement number of rows 
                
#Otherwise, swap first and last name positions
                else:    
                    PlayerNumber = str(int(StatTable.iloc[i, 0]))           #Extract the player # 
                    PlayerName = StatTable.iloc[i, 1]                           #Extract player name string              
                    NumberIndex = PlayerName.find(PlayerNumber)   #Match the # in the string
                    PlayerName = PlayerName[0 : NumberIndex - 1]  #Extract the player name
                    CommaPosition = PlayerName.find(",")                  #Reverse the position of the
                    LastName = PlayerName[0 : CommaPosition]        #first and last name
                    
                    FirstName = PlayerName[CommaPosition + 2 : NumberIndex]
                    PlayerName = FirstName + " " + LastName
                    StatTable.loc[i, "Player"] = PlayerName         #Rewrite the corrected player's
                                                                                       #name into the Stat Table and
        return StatTable    #Return the updated Stat Table to the calling program
       

#****************************************************************************
#Method:   FormatSinglePlayerName
#Puropose: Very similar to FormatPlayerName() but only takes in one player rather a list of 
#                 players.  YES, I should write this functionality into FormatPlayerName() but I am
#                 not selling this app on the open market and I don't expect to have dozens of
#                 software engineers critiquing me at a code review telling me that I did not 
#                 use proper coding technique.  It is easier this way and I really don't care what
#                 you think
# Inputs:  Player's name that needs re-arranging, last row 
# Outputs: Formatted player name
# Author:           Rick Burney
# Created:          03/03/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def FormatSinglePlayerName(self,PlayerName, StartingPoint,wsColumn):

        SecondSpaceIndex = self.find_nth(PlayerName, " ", 2)    #Look for 2nd occurence of " "
        CommaPosition = PlayerName.find(",")                          #Find the comma

#Last name comes 1st which we don't want,  First name is after the comma.  Extract 1st and
#last names and swap positions
        LastName = PlayerName[0 : CommaPosition]                                    #Extract last name                   
        FirstName = PlayerName[CommaPosition + 2 : SecondSpaceIndex]   #Extact 1st name 
        PlayerName = FirstName + " " + LastName                                       #Put name together                                                                 
        self.wsStats.cell(row = StartingPoint, 
                          column = wsColumn).value = PlayerName #Write to worksheet, left-justify 
        self.wsStats.cell(row=StartingPoint,                   
            column=wsColumn).alignment = Alignment(horizontal='left', vertical='center')
 
        self.wbStats.save(filename = self.StatFileName) #Save file     
        return PlayerName                                           #Return corrected player name
    

#****************************************************************************
#Method:   find_nth
#Puropose: Can't take credit for this one.  Stole it from the Internet.  This method finds the
#                 nth occurrence of a substring within a string
# Inputs:    A needle in a haystack.  You figure it out. 
# Outputs: The index of the nth occurrence
# Author:           Beats me
#****************************************************************************
    def find_nth(self,haystack, needle, n):
        start = haystack.find(needle)           #First occurrence of what you are looking for
        while start >= 0 and n > 1:                                     #Now find the nth occurrence
            start = haystack.find(needle, start+len(needle))    #Keep looking until n = 1
            n -= 1                                                                  
        return start


#****************************************************************************
#Method:   FormatPenaltyStats
#Puropose: Writes the penalties per game 
# Inputs:    Games played, Team Stats Table 
# Outputs: Penalties per game
# Author:   Rick Burney
# Created:          03/29/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def FormatPenaltyStats(self):

#Extract the penalties string from the team stats table
        strPenalties = self.TeamStatTable.iloc[43, 1]
        wsColumn = 2                                                #Worksheet column for penalties/game
        Code = 6                                #Tells method how to extract penalties from the string
        
        self.StringConversion(strPenalties, 0, 0, Code)       #Extract penalties from the string
        NumPenalties = int(self.FirstNumber)                                            #Convert to integer
        PenaltiesPerGame = round(NumPenalties / self.GamesPlayed, 1)   #Compute penalties
        self.wsStats.cell(row = self.wsStartingPoints['Team_Stats'] + 1,      #per game and 
                          column = wsColumn).value = PenaltiesPerGame         #Write to worksheet 
        self.wsStats.cell(row = self.wsStartingPoints['Team_Stats'] + 1, 
                          column = wsColumn).font = Font(bold=False)            #Unbold
        
#Conference factor is also written is this group
        wsColumn = 3                                                                            #Worksheet column
        self.wsStats.cell(row = self.wsStartingPoints['Team_Stats'] + 1,                       #Write to 
                          column = wsColumn).value = self.Table_IDs['ConferenceFactor']  #WS and
        self.wsStats.cell(row = self.wsStartingPoints['Team_Stats'] + 1,                       #unbold                      
                          column = wsColumn).font = Font(bold=False)  
        self.wbStats.save(filename = self.StatFileName)                                               #Save file     


#****************************************************************************
#Method:   FormatStatsExec
#Purpose:  This method sequences through the formatting of each stat group
# Inputs:  Extracted Stats, Stat Table Lengths, worksheet handle
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/03/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def FormatStatsExec(self):
        
#Team stats are needed by multiple methods
#Isolate team stats
        self.TeamStatTable =  self.StatTables[self.Table_IDs['Team_Stats']]
        
#Extract sacks by opponents.  It will start off as a string but end up as an integer.  
#That integer will be visible throughout this class.  Use iloc[] to find the position of the
#number of sacks by the opponent (these are team stats) in the team stat data frame
        Sacks = self.TeamStatTable.iloc[51, 2]  
        
#Look for a delimiter that can be used to separate the number of sacks from the sack
#yardage
        SacksIndex = Sacks.find('-')                    
        self.SacksByOpponent = int(Sacks[0 : SacksIndex])
        
#Extract team passing attempts and convert to an integer.  It will be visible
#to the entire class.  Passing attempts are the first string to the left of the first hypen.
        Attempts = self.TeamStatTable.iloc[17, 1]   #Extract passing attempts by the team
        AttemptsIndex = Attempts.find('-')
        self.TeamPassingAttempts = int(Attempts[0 : AttemptsIndex]) #Convert to an integer
        
#Extract team rushing attempts and convert to an integer.  It will be visible
#to the entire class
        Attempts = self.TeamStatTable.iloc[11, 1]       #Extract rusing attempts by the team   
        self.TeamRushingAttempts = int(Attempts)    #Convert to an integer. Make visible
        
#Extract PATs from the scoring table and make visibile to the entire class.  Code = 0 is used 
#to extract two #s, separated by a hyphen and then compute the % by dividing the 2nd # by 
#the first # and multiplying the quotient by 100.  0 / 0 is replaced by 0.  
        Code = 0
        PATColumn = 5 
        ScoringTable = self.StatTables[self.Table_IDs['Scoring_Stats']]
        self.PATs = round(self.StringConversion(ScoringTable, 
                                            self.Table_Row_Lengths['Scoring_Stats'], PATColumn, Code), 1)

        self.RushingStatsFormat()               #Format rushing stats
        self.PassingStatsFormat()               #Format passing stats
        self.ReceivingStatsFormat()             #Format receiving stats
        self.KickOffStatsFormat()               #Format kickoff stats
        self.PlaceKickingStatsFormat()      #Format PK stats
        self.PuntingStatsFormat()               #Format Punting stats
        self.DefensiveTeamStatsFormat()   #Format defensive team stats
        self.KickReturnStatsFormat()        #Format kick return stats
        self.PuntReturnStatsFormat()        #Format punt return stats
        self.IntStatsFormat()                       #Format Interception stats
        self.OFumblesStatsFormat()      #Format offensive fumbles lost stat
        self.FumbleRecoveryList()       #Write the Fumble Recovery List to the worksheet
        self.ExtractGamesPlayed()       #Extract games played
        self.FormatPenaltyStats()
        self.FormatTackleStats()
        self.FormatSackStats()
        self.WriteInjuryImpacts()
     

#****************************************************************************
#Method:   FormatSackStats
#Purpose:  This method takes the Defensive Stats Table, extracts sack stats and writes to
#                the worksheet
# Inputs:    Defensive Stats Table
# Outputs: Sacks
# Author:           Rick Burney
# Created:          03/31/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def FormatSackStats(self):

#Extract D Table and get rid of team rows.  First, extract the defensive stats table        
        DefensivePlayersTable =  self.StatTables[self.Table_IDs['Defensive_Stats']]
        
#Determine the number of rows in the table
        NumRows = self.Table_Row_Lengths['Defensive_Stats']
        
#Get rid of any team rows and adjust the number of rows accordingly
        modDTable = self.ModifyTable(DefensivePlayersTable, NumRows)

        PlayerTableColumn = 1   #Column in the table that lists the player's names
        NamewsColumn = 8
        SackColumn = 7
        
#Extract only those players who had sacks using a similar method as used for players with
#Ints.  Code it inline rather than calling the Int method because there are too many subtle
#differences
        SackTable = []
        PlayersWhoHadSacksTable = []
        NumberOfPlayersWhoHadSacks = 0
        for i in range(NumRows):
            if modDTable.iloc[i, SackColumn]  != "0-0":
                PlayersWhoHadSacksTable.append(modDTable.iloc[i, PlayerTableColumn])
                SackTable.append(modDTable.iloc[i, SackColumn])
                NumberOfPlayersWhoHadSacks += 1
        for i in range(NumberOfPlayersWhoHadSacks): 
            Sacker = PlayersWhoHadSacksTable[i]
            if Sacker.find("Team") != -1:
                del PlayersWhoHadSacksTable[i]
                NumberOfPlayersWhoHadSacks -= 1           
        SackNameList = self.FPNForaList(PlayersWhoHadSacksTable, 
                                        NumberOfPlayersWhoHadSacks)
        SackwsColumn = 9
        Code = 6
        NumSacks = []
        TotalTeamSacks = 0                        #Calculate total team sacks
        for i in range(NumberOfPlayersWhoHadSacks):                                   
            self.wsStats.cell(row = self.wsStartingPoints['Tackle_Stats']  + i,             #Write names
                              column = NamewsColumn).value = SackNameList[i] 
            self.wsStats.cell(row=self.wsStartingPoints['Tackle_Stats']  + i,               #Left-justify 
                column=NamewsColumn).alignment = Alignment(horizontal='left', 
                                                            vertical='center')
            self.StringConversion(SackTable[i] , 0, 0, Code)
            NumSacks.append(self.FirstNumber)
            self.wsStats.cell(row = self.wsStartingPoints['Tackle_Stats']  + i,             #Write sacks
                              column = SackwsColumn).value = float(NumSacks[i])  
            TotalTeamSacks += self.wsStats.cell(row = self.wsStartingPoints['Tackle_Stats'] + i, 
                          column = SackwsColumn).value      

        CPColumn = 10                                                                        #Write cum probabilities
        self.WriteComputeCPs(self.wsStartingPoints['Tackle_Stats'],    #to the worksheet
                             NumberOfPlayersWhoHadSacks, CPColumn, TotalTeamSacks)
        self.wbStats.save(filename = self.StatFileName)                                 #Save file
        
        self.InjuryImpactStartingPoint = self.wsStartingPoints['Tackle_Stats'] + NumRows + 5


#****************************************************************************
#Method:   FormatTackleStats
#Purpose:  This method takes the Defensive Stats Table, extracts tackles stats and writes to
#                the worksheet
# Inputs:    Defensive Stats Table
# Outputs: Tackles
# Author:           Rick Burney
# Created:          03/30/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def FormatTackleStats(self):

#Extract D Table and get rid of team rows        
        DefensivePlayersTable =  self.StatTables[self.Table_IDs['Defensive_Stats']]
        NumRows = self.Table_Row_Lengths['Defensive_Stats']
        modDTable = self.ModifyTable(DefensivePlayersTable, NumRows)
        PlayerTableColumn = 1
        NamewsColumn = 2
        
#Call the Name formatting method
        for i in range(NumRows):
            self.FormatSinglePlayerName(modDTable.iloc[i, PlayerTableColumn], 
                                        self.wsStartingPoints['Tackle_Stats' ] + i, NamewsColumn)
            
#Write the # of tackles to the worksheet
        TackleColumn = 5
        wsColumn = 3
        self.WriteAve(modDTable, self.wsStartingPoints['Tackle_Stats'], NumRows, 
                      wsColumn, TackleColumn)
        TotalTeamTackles = 0                        #Calculate total team tackles
        for i in range(NumRows):
            TotalTeamTackles += self.wsStats.cell(row = self.wsStartingPoints['Tackle_Stats'] + i, 
                          column = wsColumn).value      
        CPColumn = 4                                                                        #Write cum probabilities
        self.WriteComputeCPs(self.wsStartingPoints['Tackle_Stats'],    #to the worksheet
                             NumRows, CPColumn, TotalTeamTackles)
        

#****************************************************************************
#Method:   FPNForaList
#Purpose:  This method formats a list of player names
# Inputs:    List of player names to be formatted, length of list
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/03/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def FPNForaList(self,PNList,NumRows):
     
#Team stats are needed by multiple methods
#Isolate team stats
        FormattedPlayerNameList = []               #Start with a blank list for the formatted names
        for i in range(NumRows):                                     #Go through the list that is passed in
            CommaPosition = self.find_nth(PNList[i],",",1)          #Look for the 1st comma
            SecondSpacePosition = self.find_nth(PNList[i]," ",2)  #Look for the 2nd space 
            
            FirstName = PNList[i][CommaPosition + 2 : SecondSpacePosition]  #Extract 1st name
            LastName = PNList[i][0 : CommaPosition]                                       #Extract last name
            FormattedPlayerNameList.append(FirstName + " " + LastName) #Put names together
        return FormattedPlayerNameList                                                   #Return name list


#****************************************************************************
#Method:   FumbleRecoveryList
#Purpose:  This method takes the 1st 18 players of the Defensive Stats Table (Listed 
#               chronologically by most tackles) and writes them to the Fumble Recovery List in
#               the worksheet.  This is a slight departure from the way that Simulator has worked
#               in the past
# Inputs:   Defensive Stats Table
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/28/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def FumbleRecoveryList(self):
     
#List of players will come from the Defensive Stats Table.  Extract the table
        DefensivePlayersTable =  self.StatTables[self.Table_IDs['Defensive_Stats']]
        
        NumPlayers = 18     #18 players who can recover a program
        TableColumn = 1     #Names are in column 1 of the Defensive Stats Table
        
#Players who can recover fumbles are written to column 2 of the stats sheet        
        wsColumn = 2  
        
#Create the fumble recover list that will be written to the stats sheet
        FumbleRecoveryList = DefensivePlayersTable.iloc[0 : NumPlayers, TableColumn]
        self.FRNameList = self.FPNForaList(FumbleRecoveryList, NumPlayers)
        for i in range(NumPlayers):
            self.wsStats.cell(row = self.wsStartingPoints['Fumble_Recoveries'] + i,
                              column = wsColumn).value = self.FRNameList[i] 
            self.wsStats.cell(row=self.wsStartingPoints['Fumble_Recoveries']  + i,    #Left-justify 
                column=wsColumn).alignment = Alignment(horizontal='left', 
                                                            vertical='center')
    

        self.wbStats.save(filename = self.StatFileName) #Save file     
 

#****************************************************************************
#Method:   IntStatsFormat
#Purpose:  This one is tricky.  It is not obvious where the Int yardage comes from so have to
#either extract it (if possible) from the Defensive Stats Table (ID 4) or find another web site
# Inputs:    Not yet sure
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/23/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def IntStatsFormat(self):

#Isolate Int Names Table
        #IntNameTable =  self.StatTables[self.Table_IDs['Int_Names']]    #Extract Int Tables
        DNameTable = []
        IntNameTable = self.StatTables[self.Table_IDs['Defensive_Stats']]
        IntDataTable = self.StatTables[self.Table_IDs['Int_Stats']]
        NumRows = self.Table_Row_Lengths['Int_Names'] - 4     #Changed from '-3' on 9/15/20
        
        ModIntNameTable = self.ModifyTable(IntNameTable, NumRows)
        for i in range(NumRows):
            DNameTable.append(ModIntNameTable.iloc[i, 1])
         
        ModIntDataTable = self.ModifyTable(IntDataTable, NumRows)
        self.CreateIntTable(DNameTable, ModIntDataTable, NumRows)   #Extract Int Stats
        
#Write interception data to worksheet.Worry about the CPs after
        IntNameColumn = 2
        IntNumColumn = 3
        IntAveColumn = 6
        TotalTeamInts = 0
        for i in range(self.NumberOfInterceptingPlayers):                                   #Go thru list
            self.wsStats.cell(row = self.wsStartingPoints['INT_Stats']  + i,               #Write names
                              column = IntNameColumn).value = self.FintNameList[i] 
            
#Left justify            
            self.wsStats.cell(row=self.wsStartingPoints['INT_Stats']  + i,                    
                column=IntNameColumn).alignment = Alignment(horizontal='left', vertical='center')
            
            self.wsStats.cell(row = self.wsStartingPoints['INT_Stats']  + i,           #Write # of Ints
                              column = IntNumColumn).value = self.IntDataTable[i]
            TotalTeamInts += self.IntDataTable[i]                                            #Add to total
            IntAve = round(self.IntYardageTable[i]/self.IntDataTable[i],0)         #Compute Int
            self.wsStats.cell(row = self.wsStartingPoints['INT_Stats']  + i,           #return yardage
                              column = IntAveColumn).value = IntAve                      #ave and write 

#Write CPs
        CPColumn = 4
        self.WriteComputeCPs(self.wsStartingPoints['INT_Stats'], 
                             self.NumberOfInterceptingPlayers, CPColumn, TotalTeamInts)


        self.wbStats.save(filename = self.StatFileName) #Save file     
        

#****************************************************************************
#Method:   KickOffStatsFormat
#Purpose:  This method formats the passing stats into the worksheet
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/12/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def KickOffStatsFormat(self):

#Isolate Kickoff Table
        KickoffTable =  self.StatTables[self.Table_IDs['Kickoff_Stats']]
        NumRows = 1 #For kickoffs we only want 1 person
        
        modKickOffTable = self.ModifyTable(KickoffTable, NumRows)
        
#Format the kickoff guy's name.  
        FormattedKickoffTable = self.FormatPlayerName(modKickOffTable, NumRows)
        
#Write kickoff stats to worksheet
#Write the Player Names noting that there will always be only one kicker.    Note the key 
#name difference in StartingPoints[]
        NameColumn = 1
        TableColumn = 1
        NumberOfKickers = 1
        
        self.WriteName(FormattedKickoffTable, 
            self.wsStartingPoints['Kicking_Stats'], NumberOfKickers, NameColumn, TableColumn)
     
#Next step is to extract the # of kickoffs from the Stat Table and write this number to the 
#worksheet.  Use WriteAve() to write this value because it simply reads the value from the 
#table and then writes the value to the worksheet without alteration
        TableColumn = 2
        KOColumn = 3
        self.WriteAve(FormattedKickoffTable, self.wsStartingPoints['Kicking_Stats'], NumRows, 
                      KOColumn, TableColumn)
     
#Using the same methodology as the # of kickoffs, use WriteAve() to extract and write the
#yards/kickoff to the worksheet
        TableColumn = 4
        NumColumn = 4
        self.WriteAve(FormattedKickoffTable, self.wsStartingPoints['Kicking_Stats'], NumRows, 
                      NumColumn, TableColumn)
     
#Use WriteAve() to write the touchback and out-of-bounds kickoff percentage.  But 
#WriteRatio() uses two numbers from the StatTable.  So we have to extract these numbers
#from the StatTable, make the computation and then set the percentage flag
        TBTableColumn = 5
        OOBTableColumn = 6
        TBwsColumn = 5
        OOBwsColumn = 6
        self.WriteAve(FormattedKickoffTable, self.wsStartingPoints['Kicking_Stats'], NumRows, 
                      TBwsColumn, TBTableColumn)
        self.WriteAve(FormattedKickoffTable, self.wsStartingPoints['Kicking_Stats'], NumRows, 
                      OOBwsColumn, OOBTableColumn)
        

#****************************************************************************
#Method:   KickReturnStatsFormat
#Purpose:  This method formats the kick return stats into the worksheet
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/22/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def KickReturnStatsFormat(self):

#Isolate Kickoff Return Table
        KickReturnTable =  self.StatTables[self.Table_IDs['Kickoff_Return_Stats']]
        NumRows = self.Table_Row_Lengths['Kickoff_Return_Stats']
        modKickReturnTable = self.ModifyTable(KickReturnTable, NumRows)

#Format the player names so it looks like English.  
        FormattedKickReturnTable = self.FormatPlayerName(modKickReturnTable, NumRows)
        KRColumn = 2
        Code = 4
        wsColumn = 2
        self.KickReturner = self.StringConversion(FormattedKickReturnTable, 
                                        self.Table_Row_Lengths['Kickoff_Return_Stats'], KRColumn, Code)
        self.wsStats.cell(row = self.wsStartingPoints['KR_Stats'], 
                          column = wsColumn).value = self.KickReturner        #Write KR's name to WS 

#Write # of returns, average per return and longest return for the designated kick returner        
        self.wsStats.cell(row = self.wsStartingPoints['KR_Stats'], column = \
                          wsColumn + 1).value = int(FormattedKickReturnTable.iloc[self.MaxRow , 
                                                                                  KRColumn]) 
        self.wsStats.cell(row = self.wsStartingPoints['KR_Stats'], column = \
                          wsColumn + 2).value = round(FormattedKickReturnTable.iloc[self.MaxRow , 
                                                                                  KRColumn + 2], 1) 
        self.wsStats.cell(row = self.wsStartingPoints['KR_Stats'], column = \
                          wsColumn + 3).value = int(FormattedKickReturnTable.iloc[self.MaxRow , 
                                                                                  KRColumn + 4]) 
        
        self.wbStats.save(filename = self.StatFileName)                      #Save file     
        

#****************************************************************************
#Method:   ModifyTable
#Purpose:  This method uses Table_Row_Length to truncate the # of rows
# Inputs:  A stat table, index of the last row desired
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/03/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def ModifyTable(self,StatTable,EndRow):

#Creating a copy prevents a hidden chaining error so even though I have no idea what that 
#means, any time that the table is sliced (rows or columns are deleted, make a copy        
        ModTable = StatTable.iloc[0 : EndRow,:].copy()        
        return ModTable
       

#****************************************************************************
#Method:   OFumblesStatsFormat
#Purpose:  This method formats the defensive team stats into the worksheet
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/20/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def OFumblesStatsFormat(self):

#Isolate defensive team stats
        OFumblesStatsTable =  self.StatTables[self.Table_IDs['Team_Stats']]

#Compute probability that offense will lose a fumble.          
        TableRow = 50       #Row in Team Stats Table for fumbles lost for O and D
        TableColumn = 1    #Offense column for fumbles lost
        wsColumn = 2        #Worksheet column for offensive fumbles lost
        Code = 7                #Tells method how to extract fumbles lost from total fumbles
        
        NumFum =  OFumblesStatsTable.iloc[TableRow, TableColumn]   #Extract fumbles
        
        self.StringConversion(NumFum, 0, 0, Code)       #Extract fumbles lost and assign it to an
        FumblesLostByTheO = int(self.SecondNumber)  #object  
        
        TableRow = 11    #These next 2 objects are for extracting the number of rushing 
        TableColumn = 1 #attempts by the offense
        
#The probability that the offense loses a fumble is the number of fumbles lost divided by the
#quantity RushingAttemptsBy + PassCompletionsBy + SacksofYourQB
        RushingAttemptsBy = int(OFumblesStatsTable.iloc[TableRow, TableColumn])
        TableRow = 17
        OFumbleString = OFumblesStatsTable.iloc[TableRow, TableColumn]
        
#Call StringConversion(), Code 5 but understand that a string is passed in lieu of a Stat Table
#Extract passes completed  
        Code = 5
        self.StringConversion(OFumbleString, 0, 0, Code) 
        self.CompletionsBy = int(self.SecondNumber)        

#FumbleMultiplier takes into account that fumbles are computed in parts per 10k        
        POFumbleLoss = round((self.FumbleMultiplier * FumblesLostByTheO)/\
                                 (RushingAttemptsBy + self.CompletionsBy + self.SacksByOpponent), 1)
        self.wsStats.cell(row = self.wsStartingPoints['OFumbles_Stats'] ,
                          column = wsColumn).value = POFumbleLoss 

#Make sure the cell is not bold
        self.wsStats.cell(row = self.wsStartingPoints['OFumbles_Stats'], 
                          column = wsColumn).font = Font(bold=False)
        self.wbStats.save(filename = self.StatFileName)                      #Save file     


#****************************************************************************
#Method:   PassingStatsFormat
#Purpose:  This method formats the passing stats into the worksheet
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/12/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def PassingStatsFormat(self):

#Isolate passing table
        PassingTable =  self.StatTables[self.Table_IDs['Passing_Stats']]
        NumRows = self.Table_Row_Lengths['Passing_Stats'] 
        modPassingTable = self.ModifyTable(PassingTable, NumRows)

#Format the player names so it looks like English.  
        FormattedPassingTable = self.FormatPlayerName(modPassingTable, 
                                                        NumRows)
        #FormattedPassingTable = \
            #FormattedPassingTable.\
            #iloc[0 : self.Table_Row_Lengths['Passing_Stats'] - 1].copy()
        FormattedPassingTable = \
            FormattedPassingTable.\
            iloc[0 : NumRows ].copy()
        
#Choose first two rows for passing.  MAY HAVE TO EDIT THIS MANUALLY
        NumRows = 2 
        FormattedPassingTable = FormattedPassingTable.iloc[0 : NumRows].copy()

#Delete unwanted columns 
        FormattedingPassingTable = FormattedPassingTable.drop(['GP', 'Rating', 
                            'COMP', 'YDS', 'TD', 'Long', 'AVG/G'], axis = 1)
        
#Write passing stats to worksheet
#Write the Player Names noting that there will always be only two QBs
        NameColumn = 2
        TableColumn = 1
        NumberOfQBs = 2
        self.WriteName(FormattedingPassingTable, 
                        self.wsStartingPoints['Passing_Stats'], NumberOfQBs, 
                        NameColumn, TableColumn)
        
     
#Next step is to write % completion and format to one decimal point
        TableColumn = 4
        CPColumn = 3
        self.WritePercentage(FormattedingPassingTable, NumRows, TableColumn, 
                             CPColumn, self.wsStartingPoints['Passing_Stats'])
        
#Write INT %
        DividendColumn = 3
        DivisorColumn = 2
        PercentageFlag = 1
        SigDigits = 4
        INTColumn = 4
        SimpleRatio = 0
        self.WriteRatio(FormattedingPassingTable, self.wsStartingPoints['Passing_Stats'], 
                        NumRows, DividendColumn, DivisorColumn, PercentageFlag, SigDigits, 
                        INTColumn, SimpleRatio)
       
#Write player availability but this is not used
        AvailabilityColumn = 5
        TableColumn = 5                                                 #Not using this right now.                  
        self.WriteAvailability(FormattedingPassingTable, 
            self.wsStartingPoints['Passing_Stats'], NumRows, AvailabilityColumn, TableColumn)
       
#Write sack percentage.  This is the probability that the QB will be sacked
#and uses sacks given up from the team stats (under opponents sacks.  First,
#we need to extract the sacks from the team stats.  Also need to make ATT
#visible to entire class
        PercentageFlag = 1
        SigDigits = 4
        SPColumn = 6
        SimpleRatio = 1
        self.WriteRatio(FormattedingPassingTable, self.wsStartingPoints['Passing_Stats'], 
                        NumRows, self.SacksByOpponent, self.TeamPassingAttempts, 
                        PercentageFlag, SigDigits, SPColumn, SimpleRatio)
    
#Set flags to determine if offense is Run-Oriented or Pass-Oriented.  The
#team rushing attempts and the team passing attempts are used to make this
#determination
        ROColumn = 12
        POColumn = 10
        self.RushingOrPassingOffense(self.wsStartingPoints['Passing_Stats'], ROColumn, 
                                     POColumn)


#****************************************************************************
#Method:   PlaceKickingStatsFormat
#Purpose:  This method formats the placekicking stats (field goal and extra point %) and
#                writes to the worksheet
# Inputs:    Field Goal Stat Table, PAT % that has been extracted from the Scoring Table
# Outputs: Extra Point %, 
# Author:           Rick Burney
# Created:          03/16/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def PlaceKickingStatsFormat(self):

#Isolate Placekicking Table
        FieldGoalTable =  self.StatTables[self.Table_IDs['FieldGoal_Stats']]
        
#Figure out who is the placekicker.  Field goals and extra points may be two separate kickers
        FGColumn = 2
        Code = 2            #Code is used to convert strings into numerical stats.  See
                                   #StringConversion() method
        PATColumn = 7
        self.PlaceKicker = self.StringConversion(FieldGoalTable, 
                                              self.Table_Row_Lengths['FieldGoal_Stats'], FGColumn, Code)

#Format kicker's name (e.g. first name, then last name)        
        PlayerName = self.FormatSinglePlayerName(self.PlaceKicker, 
                                                 self.wsStartingPoints['Kicking_Stats'], FGColumn)
        self.wsStats.cell(row = self.wsStartingPoints['Kicking_Stats'], 
                          column = PATColumn).value = self.PATs             #Write PAT % to WS 
        
#Now write FG % stats starting with the 0-19 yard range, which means the ball is snapped 
#from either the 1 or 2 yard line.  If this string is '0-0, it means that a FG was never tried
#from this close in so make it is like an extra point and use self.PATs.  StringConversion, 
#Code 1
        FG20_29Column = 4
        Code = 1
        wsColumn = 8
        R0_19 = self.StringConversion(FieldGoalTable, self.MaxRow, FG20_29Column, Code)
        self.wsStats.cell(row = self.wsStartingPoints['Kicking_Stats'], 
                          column = wsColumn).value = round(R0_19,1)       #Write 0-19 Yd FG Range 

#Now write FG % stats starting with the 20-29 yard range 
        FG20_29Column = 5
        Code = 3
        wsColumn = 9
        R20_29 = self.StringConversion(FieldGoalTable, self.MaxRow, FG20_29Column, Code)
        self.wsStats.cell(row = self.wsStartingPoints['Kicking_Stats'], 
                          column = wsColumn).value = round(R20_29,1)   #Write 20-29 Yd FG Range 

#Now write FG % stats starting with the 30-39 yard range 
        FG30_39Column = 6
        Code = 3
        wsColumn = 10
        R30_39 = self.StringConversion(FieldGoalTable, self.MaxRow, FG30_39Column, Code)
        self.wsStats.cell(row = self.wsStartingPoints['Kicking_Stats'], 
                          column = wsColumn).value = round(R30_39,1)   #Write 30-39 Yd FG Range 

#Now write FG % stats starting with the 40-49 yard range 
        FG40_49Column = 7
        Code = 3
        wsColumn = 11
        R40_49 = self.StringConversion(FieldGoalTable, self.MaxRow, FG40_49Column, Code)
        self.wsStats.cell(row = self.wsStartingPoints['Kicking_Stats'], 
                          column = wsColumn).value = round(R40_49,1)   #Write 40-49 Yd FG Range 

#Now write FG % stats starting with the 50-55 yard range 
        FG50_55Column = 8
        Code = 3
        wsColumn = 12
        R50_55 = self.StringConversion(FieldGoalTable, self.MaxRow, FG50_55Column, Code)
        self.wsStats.cell(row = self.wsStartingPoints['Kicking_Stats'], 
                          column = wsColumn).value = round(R50_55,1)   #Write 50-55 Yd FG Range              
        self.wbStats.save(filename = self.StatFileName)                      #Save file     
        

#****************************************************************************
#Method:   PuntReturnStatsFormat
#Purpose:  This method formats the punt return stats into the worksheet
# Outputs: Formatted punt return stats written to the worksheet
# Author:           Rick Burney
# Created:          03/22/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def PuntReturnStatsFormat(self):

#Isolate Punt Return Table
        PuntReturnTable =  self.StatTables[self.Table_IDs['Punt_Return_Stats']]
        NumRows = self.Table_Row_Lengths['Punt_Return_Stats']                       # of rows
        modPuntReturnTable = self.ModifyTable(PuntReturnTable, NumRows) #Lose team stats

#Format the player names so it looks like English.  We only want one punt returner so parse
#through the punt returner stats (using Code 4 and calling StringConversion() to choose the
#player with the most returns
        FormattedPuntReturnTable = self.FormatPlayerName(modPuntReturnTable, NumRows)
        PRColumn = 2
        Code = 4          
        wsColumn = 2
        self.PuntReturner = self.StringConversion(FormattedPuntReturnTable, NumRows, 
                                                  PRColumn, Code)

        self.wsStats.cell(row = self.wsStartingPoints['PR_Stats'], column = wsColumn).value =\
            self.PuntReturner 
        self.wsStats.cell(row = self.wsStartingPoints['PR_Stats'], column = wsColumn + 2).value\
            = round(float(FormattedPuntReturnTable.iloc[self.MaxRow, PRColumn + 2]), 1)
        self.wsStats.cell(row = self.wsStartingPoints['PR_Stats'], column = \
                          wsColumn + 3).value = int(FormattedPuntReturnTable.iloc[self.MaxRow , 
                                                                                  PRColumn + 4]) 
        
        self.wbStats.save(filename = self.StatFileName)     
        
     
#****************************************************************************
#Method:   PuntingStatsFormat
#Purpose:  This method formats the punting stats and
#                writes to the worksheet
# Inputs:    Punting Stat Table
# Outputs: Punting stats
# Author:           Rick Burney
# Created:          03/19/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def PuntingStatsFormat(self):
    
#Isolate Punting Table and get rid of team total rows
        PuntingTable =  self.StatTables[self.Table_IDs['Punting_Stats']]
        NumRows = self.Table_Row_Lengths['Punting_Stats']
        modPuntingTable = self.ModifyTable(PuntingTable, NumRows)    
    
        PuntColumn = 2  #Figure out who is the punter    
        Code = 4
        wsColumn = 2
        self.Punter = self.StringConversion(modPuntingTable, 
                                              self.Table_Row_Lengths['Punting_Stats'], PuntColumn, Code)
        PlayerName = self.FormatSinglePlayerName(self.Punter, 
                                                 self.wsStartingPoints['Punting_Stats'], PuntColumn)
        self.wsStats.cell(row = self.wsStartingPoints['Punting_Stats'], 
                          column = wsColumn).value = PlayerName           #Write Punter's Name to ws 
     
        TableColumn = 4 #Extract and write the yards/punt to the worksheet
        AveColumn = 4
        self.wsStats.cell(row = self.wsStartingPoints['Punting_Stats'], 
          column = AveColumn).value = round(modPuntingTable.iloc[self.MaxRow , 
                                                                 TableColumn], 1)
     
        TableColumn = 5 #Extract and write the longest punt to the worksheet
        LongColumn = 5
        self.wsStats.cell(row = self.wsStartingPoints['Punting_Stats'], 
          column = LongColumn).value = modPuntingTable.iloc[self.MaxRow, TableColumn]
     
#Extract both the # of fair catches and the # of punts and compute the FC percentage
        NumFCColumn = 7
        NumPuntsColumn = 2
        FCPColumn = 6        
        NumPunts = modPuntingTable.iloc[self.MaxRow, NumPuntsColumn] #Extract # of punts
        NumFCs = modPuntingTable.iloc[self.MaxRow, NumFCColumn]        #Extract # of FCs
        FCPercentage = round((100*NumFCs / NumPunts), 0)                       #Compute FC %
        self.wsStats.cell(row = self.wsStartingPoints['Punting_Stats'], 
                          column = FCPColumn).value = FCPercentage      #Write FC % to worksheet    
        self.wbStats.save(filename = self.StatFileName)                     #Save file                
      

#****************************************************************************
#Method:   ReceivingStatsFormat
#Purpose:  This method formats the receiving stats into the worksheet
#Inputs:     Stat tables, table row lengths, table IDs
# Outputs: Formatted receiving stats
# Author:           Rick Burney
# Created:          03/03/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def ReceivingStatsFormat(self):

#Isolate receiving table and delete team rows (designated with NaN for player
#numbers.  If necessary, swap the first and last names of the players.
        ReceivingTable =  self.StatTables[self.Table_IDs['Receiving_Stats']]    #Extract stats
        NumRows = self.Table_Row_Lengths['Receiving_Stats'] - 1              #Compute # of rows
        
#Delete the team rows from the table
        modReceivingTable = self.ModifyTable(ReceivingTable, NumRows)
        
#Swap last and first names if necessary
        FormattedReceivingTable = self.FormatPlayerName(modReceivingTable,
                                                        NumRows)

#Next statement prevents a warning.  That's it, no other reason for it.
        FormattedReceivingTable = \
            FormattedReceivingTable.\
            iloc[0 : self.Table_Row_Lengths['Receiving_Stats'] - 1].copy()

#Delete unwanted columns.  In retrospect, this wasn't necessary
        FormattedReceivingTable = FormattedReceivingTable.drop(['GP', 'YDS', 'TD', 'Long', 
                                                'AVG/G'], axis = 1)
        NameColumn = 2                                                  #Worksheet name column
        TableColumn = 1                                                  #Table column with the player's name
        self.WriteName(FormattedReceivingTable,              #Write receiver names to worksheet
                        self.wsStartingPoints['Receiving_Stats'], 
                        self.Table_Row_Lengths['Receiving_Stats'] - 1, NameColumn, TableColumn)
       
#Write the number of receptions
        ReceptionsColumn = 4                                #For some reason, this column is after YPC 
        TableColumn = 2                                                       #Stat table column        
        self.WriteTouches(FormattedReceivingTable,              #Write number of receptions to ws 
                        self.wsStartingPoints['Receiving_Stats'], 
                        self.Table_Row_Lengths['Receiving_Stats'] - 1, ReceptionsColumn, 
                        TableColumn)
        YPCColumn = 3
        TableColumn = 3
        self.WriteAve(FormattedReceivingTable,                  #Write the yards per catch (YPC)
                        self.wsStartingPoints['Receiving_Stats'], 
                        self.Table_Row_Lengths['Receiving_Stats'] - 1, YPCColumn, TableColumn)
       
#Write player availability
        AvailabilityColumn = 5
        self.WriteAvailability(FormattedReceivingTable, self.wsStartingPoints['Receiving_Stats'], 
                self.Table_Row_Lengths['Receiving_Stats'] - 1, AvailabilityColumn, TableColumn)
        
#Write adjusted receptions based upon availability
        AdjustedTouchesColumn = 6
        TouchesColumn = 4
        self.WriteAdjustedTouches(FormattedReceivingTable, 
                        self.wsStartingPoints['Receiving_Stats'], 
                        self.Table_Row_Lengths['Receiving_Stats'] - 1, 
                        AdjustedTouchesColumn, TableColumn, TouchesColumn, AvailabilityColumn)
        
#Write cumulative probabilities.  First, calculates the total number of receptions for the team
        CPColumn = 7
        TeamTouches=self.WriteTotals(self.wsStartingPoints['Receiving_Stats'], 
                         self.Table_Row_Lengths['Receiving_Stats'] - 1, AdjustedTouchesColumn)
        self.WriteComputeCPs(self.wsStartingPoints['Receiving_Stats'], 
                        self.Table_Row_Lengths['Receiving_Stats'] - 1, CPColumn, TeamTouches)
        
#Write player positions (speculatively)
        PPColumn = 9
        StatCode = 1                                                                             #Receiving Stats        
        self.WritePlayerPosition(self.wsStartingPoints['Receiving_Stats'], #Write to worksheet
                        self.Table_Row_Lengths['Receiving_Stats'] - 1,           #The called method 
                        PPColumn, StatCode)                                                 #does the write
        
#Write blowout cumulative probabilities (speculatively, will correct using ReWriteStats class)
        BCPColumn = 10                      #BCP1
        BFColumn = 12                        #Backup factor.  Either 1 or 0
        StatCode = 1                            #For receivers
        
        self.WriteBackupComputeCPs(self.wsStartingPoints['Receiving_Stats'], 
                        self.Table_Row_Lengths['Receiving_Stats'] - 1, 
                        BCPColumn, BFColumn, StatCode)
               
        
#****************************************************************************
#Method:   RushingOrPassingOffense
#Purpose:  This method ratios the # of team rushing attempts and the # of team passing 
#               attempts and sets flags for either a Run-Oriented team, a Pass-Oriented Team or 
#               Balanced
# Inputs:   Starting row for these stats, Run-Oriented ws column, Pass-Oriented ws column
# Outputs: Pass-Oriented or Run-Oriented flags (Can't both be 1)
# Author:           Rick Burney
# Created:          03/13/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def RushingOrPassingOffense(self, StartingPoint, ROColumn, POColumn):

#Thresholds.  Passing Attempts / (Passing Attempts + Rushing Attempts)
        RunOrientedThreshold = 0.4
        PassOrientedThreshold = 0.6

#Compute the ratio        
        RunOrPass = self.TeamPassingAttempts / (self.TeamPassingAttempts + \
                                           self.TeamRushingAttempts)
        RunOriented = PassOriented = 0                              #Most teams are neither
        if RunOrPass < RunOrientedThreshold:    #If true, then set Run-Oriented flag
            RunOriented = 1
            PassOriented = 0                                    #Can't both be 1
        elif RunOrPass > PassOrientedThreshold:   #If true, then set Pass-Oriented flag
            RunOriented = 0
            PassOriented = 1
            
#Write RunOriented, PassOriented flags to the worksheet and save file
        self.wsStats.cell(row = StartingPoint, column = ROColumn).value = RunOriented 
        self.wsStats.cell(row = StartingPoint, column = POColumn).value = PassOriented    
        self.wbStats.save(filename = self.StatFileName)     



#****************************************************************************
#Method:   RushingStatsFormat
#Purpose:  This method formats the rushing stats into the worksheet
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/03/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def RushingStatsFormat(self):

#Isolate rushing table and identify non-player entries by player #s that are NaN by using 
#Table_Row_Lengths
        RushingTable =  self.StatTables[self.Table_IDs['Rushing_Stats']]
        NumRows = self.Table_Row_Lengths['Rushing_Stats'] - 1
        modRushingTable = self.ModifyTable(RushingTable, NumRows)

#Format the player names so it looks like English.  But it gets complicated.
#Players are identified by their number and sometimes, the stat row is for the
#team and therefore, there is no player number, rather, a NaN.  The called
#method identifies those rows with a NaN for the number and adjusts the valid
#number of rows.  But there is still one too many rows so the # of rows is 
#decremented by one.  A new table is created with only players with numbers 
#included in the stat table
        FormattedRushingTable = self.FormatPlayerName(modRushingTable, 
                                                        NumRows)
        FormattedRushingTable = \
            FormattedRushingTable.\
            iloc[0 : self.Table_Row_Lengths['Rushing_Stats'] - 1].copy()

#Delete unwanted columns and make a copy for some reason
        FormattedRushingTable = FormattedRushingTable.drop(['GP', 'Gain', 
                            'Loss', 'Net', 'TD', 'Long', 'AVG/G'], axis = 1)

#Write rushing stats to worksheet
#Write the Player Names
        NameColumn = 2  #Worksheet name column
        TableColumn = 1 #Table column with the player's name
        
        self.WriteName(FormattedRushingTable,                   #Call the Name formatting method 
                        self.wsStartingPoints['Rushing_Stats'], 
                        self.Table_Row_Lengths['Rushing_Stats'] - 1, 
                        NameColumn, TableColumn)
       
        TouchesColumn = 3   #Write the number of carries
        TableColumn = 2
        self.WriteTouches(FormattedRushingTable, 
                        self.wsStartingPoints['Rushing_Stats'], 
                        self.Table_Row_Lengths['Rushing_Stats'] - 1, 
                        TouchesColumn, TableColumn)
       
        AveColumn = 4       #Write the rushing averages
        TableColumn = 3
                        
#This next line takes the minimum of two methods of calculating the number of players who
#ran the ball to avoid indexing errors
        NumRows = min(NumRows, self.Table_Row_Lengths['Rushing_Stats'] - 1)
        self.WriteAve(FormattedRushingTable, 
                        self.wsStartingPoints['Rushing_Stats'], 
                        NumRows, 
                        AveColumn, TableColumn)
       
#Write player availability
        AvailabilityColumn = 5
        self.WriteAvailability(FormattedRushingTable, 
                        self.wsStartingPoints['Rushing_Stats'], 
                        self.Table_Row_Lengths['Rushing_Stats'] - 1, 
                        AvailabilityColumn, TableColumn)
        
#Write adjusted touches based upon availability
        AdjustedTouchesColumn = 6
        TouchesColumn = 3
        self.WriteAdjustedTouches(FormattedRushingTable, 
                        self.wsStartingPoints['Rushing_Stats'], 
                        self.Table_Row_Lengths['Rushing_Stats'] - 1, 
                        AdjustedTouchesColumn, TableColumn, TouchesColumn, 
                        AvailabilityColumn)
        
#Write cumulative probabilities.  First, calculates the total number of
#carries for the team
        CPColumn = 7
        TeamTouches = self.WriteTotals(self.wsStartingPoints['Rushing_Stats'], 
                         self.Table_Row_Lengths['Rushing_Stats'] - 1, 
                         AdjustedTouchesColumn)
        self.WriteComputeCPs(self.wsStartingPoints['Rushing_Stats'], 
                        self.Table_Row_Lengths['Rushing_Stats'] - 1, CPColumn, 
                        TeamTouches)
        
#Write player positions (speculatively)
        PPColumn = 9
        StatCode = 0    #Rushing Stats
        
        self.WritePlayerPosition(self.wsStartingPoints['Rushing_Stats'], 
                        self.Table_Row_Lengths['Rushing_Stats'] - 1, PPColumn, 
                        StatCode)
        
#Write blowout cumulative probabilities (speculatively)
        BCPColumn = 10
        BFColumn = 12
        StatCode = 0
        self.WriteBackupComputeCPs(self.wsStartingPoints['Rushing_Stats'], 
                        self.Table_Row_Lengths['Rushing_Stats'] - 1,BCPColumn, 
                        BFColumn, StatCode)


#****************************************************************************
#Method:   StringConversion
#Purpose:  Based upon a code that is passed in, this method performs a variety of string
#               extraction and conversion functions, and various math operations based upon the
#               code
# Inputs:   StatTable, NumRows, Table column, Code  Code = 0 is used to extract two #s,
#               separated by a hyphen and then compute the % by dividing the 2nd # by the first
#               # and multiplying the quotient by 100.  0 / 0 is replaced by 0.  
#               Code = 1 is similar to Code 0 but 0 / 0 is assigned a value of 100 %. 
# Outputs: Returns the output of the designated math operation such as a computed %
# Author:           Rick Burney
# Created:          03/17/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def StringConversion(self, StatTable, NumRows, TableColumn, Code):

#Process Code = 0.  First, separate the dividend and divisor for each row and find the max
#divisor.  The max divisor allows for the player with the most touches/kicks to be chosen
#when there are multiple players who played the position but the simulator will use only one
        if Code == 0:
            MaxDivisor = 0
            ConvertedString = 0
            for i in range(NumRows):
                StringToBeConverted = StatTable.iloc[i, TableColumn]    #Find the hyphen
                HyphenIndex = StringToBeConverted.find("-")
                
#extract divisor and dividend
                Divisor=float(StringToBeConverted[HyphenIndex + 1 : len(StringToBeConverted)])
                
                Dividend = float(StringToBeConverted[0 : HyphenIndex]) #extract dividend
                if Divisor > MaxDivisor:                                                    #Find the row with the
                    self.MaxRow = i                                                            #max divisor, capture
                    MaxDivisor = Divisor                                                    #the dividend and 
                    MaxDividend = Dividend                                              #divisor for that row
            if MaxDivisor != 0:
                ConvertedString = 100 * (MaxDividend / MaxDivisor)
            return ConvertedString

#Process Code = 1.  First, separate the dividend and divisor for each row and find the max
#divisor
        if Code == 1:
            MaxDivisor = 0
            ConvertedString = 0 
            StringToBeConverted = StatTable.iloc[NumRows, TableColumn]    #Find the hyphen
            HyphenIndex = StringToBeConverted.find("-")
                
#extract divisor
            Divisor=float(StringToBeConverted[HyphenIndex + 1 : len(StringToBeConverted)])
                
            Dividend = float(StringToBeConverted[0 : HyphenIndex]) #extract dividend
            if MaxDivisor != 0:
                ConvertedString = 100 * (MaxDividend / MaxDivisor)
            else:
                ConvertedString = self.PATs
            return ConvertedString


#Process Code = 2.  First, separate the dividend and divisor for each row and find the max
#divisor.  For example, the overall field goal stats are a string in the form of
#"4-6" which means the kicker made 4 of 6 kicks.  So with a Code = 2, 
#need to find the hyphen and separate the kicks made vs kicks attempted, then return the 
#name of the kicker (there may be more than 1) to the calling program.  Also computed is
#the table row for that kicker so his stats may be used.  The calling program is responsible
#for all FG computations for this kicker.
        if Code == 2:                                                                               #If Code = 2
            MaxDivisor = 0                                                                         #Initialize
            ExtractededString = ""
            PlayerColumn = 1
            
#Find the kicker who had the most kicks and use that kicker            
            for i in range(NumRows):                                                    
                StringToBeExtracteded = StatTable.iloc[i, TableColumn]  #Find the hyphen
                HyphenIndex = StringToBeExtracteded.find("-")
                
#extract divisor
                Divisor=\
                    float(StringToBeExtracteded[HyphenIndex + 1 : len(StringToBeExtracteded)])
                
                Dividend = float(StringToBeExtracteded[0 : HyphenIndex]) #extract dividend
                if Divisor > MaxDivisor:                                                      #Find the row with the
                    self.MaxRow = i                                                              #max divisor, capture
                    MaxDivisor = Divisor                                                      #the dividend and 
                    MaxDividend = Dividend                                                #divisor for that row
            PlayerName = StatTable.iloc[self.MaxRow, PlayerColumn]  #ID the kicker and return
            return PlayerName                                                            #his name to the calling
                                                                                                     #program

#Process Code = 3.  First, separate the dividend and divisor for each row and find the max
#divisor.  Only difference from Code = 1 is that '0-0 is replaced by 0 instead of the PAT %
        if Code == 3:
            StringToBeConverted = StatTable.iloc[NumRows, TableColumn]    #Find the hyphen
            HyphenIndex = StringToBeConverted.find("-")
                
#extract divisor
            Divisor=float(StringToBeConverted[HyphenIndex + 1 : len(StringToBeConverted)])
                
            Dividend = float(StringToBeConverted[0 : HyphenIndex]) #extract dividend
            if Divisor != 0:                                                                  #Test for a divide-by-zero
                ConvertedString = 100 * (Dividend / Divisor)            #If not, compute the quotient
            else:
                ConvertedString = 0                                                 #If so, replace with zero
            return ConvertedString                                               #Return the computed number

#Process Code = 4.  First, separate the dividend and divisor for each row and find the max
#divisor.  Used for punters among others.  Choose the punter with the most punts
        if Code == 4:
            MaxNumberOf = 0                                 #Initialize this object
            PlayerColumn = 1                      #Punter's name is in column 1 of the Punt Stat Table
            for i in range(NumRows):                        #Go through the list of punters
                NumberOf = float(StatTable.iloc[i, 2])  #Look at the # of punts 
                if NumberOf > MaxNumberOf:            #Find the row with the # of punts max
                    self.MaxRow = i                              #value, capture the row and value
                    MaxNumberOf = NumberOf                        
            PlayerName = StatTable.iloc[self.MaxRow, PlayerColumn]  #Choose the punter with 
            return PlayerName                                                            #the max # of punts

#Process Code = 5.  Search for two different hyphens and return the three numbers that are
#on boths sides of the hyphens.  Use self. to assign values to global objects.  StatTable is 
#redefined as a string.  Used for  team stats such as passing, by and against
        if Code == 5:   
            FirstHyphenIndex = self.find_nth(StatTable, "-", 1)           #Look for 1st hyphen
            SecondHyphenIndex = self.find_nth(StatTable, "-", 2)       #Look for 2nd hyphen
            self.FirstNumber = StatTable[0 : FirstHyphenIndex]          #Extract 1st Number
            
#Extract 2nd and 3rd Numbers            
            self.SecondNumber = StatTable[FirstHyphenIndex + 1 : SecondHyphenIndex]
            self.ThirdNumber = StatTable[SecondHyphenIndex + 1 : len(StatTable)]

#Process Code = 6.  Same as Code = 5 but only one hypen
        if Code == 6:   
            FirstHyphenIndex = self.find_nth(StatTable, "-", 1)           #Look for 1st hyphen
            self.FirstNumber = StatTable[0 : FirstHyphenIndex]          #Extract 1st Number

#Process Code = 7.  Same as Code = 6 but want 2nd number
        if Code == 7:   
            FirstHyphenIndex = self.find_nth(StatTable, "-", 1)           #Look for hyphen
            
            self.SecondNumber = StatTable[FirstHyphenIndex + 1 :  len(StatTable)]
            
       
#****************************************************************************
#Method:   WriteAdjustedTouches
#Purpose:  This method adjusts the number of touches based upon the players
#               availability.  AdjustedTouches = Availability * touches
# Inputs:   Stat table, Worksheet row starting point, number of rows, worksheet
#               column, Stat Table column, Tocuhes column from the worksheet, 
#               Availability column from the worksheet
# Outputs: AdjustedTouches = Availability * touches
# Author:           Rick Burney
# Created:          03/08/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def WriteAdjustedTouches(self, FormattedTable, StartingPoint, 
                             TableRowLength, wsColumn, TableColumn, 
                             TouchesColumn, AvailabilityColumn):

#For each player, extract availability and number of touches from the 
#worksheet.  Write the adjusted number of touches to the worksheet        
        for i in range(TableRowLength):                                                   #Go through the table
            Availability = self.wsStats.cell(row = StartingPoint + i, #Read the availability flag from
              column = AvailabilityColumn).value                                       #the worksheet
            NumberOfTouches = self.wsStats.cell(row = StartingPoint + i, #Read the # of touches 
              column = TouchesColumn).value                                           #from the worksheet
            self.wsStats.cell(row = StartingPoint + i,                                      #Write # of adjusted
              column = wsColumn).value = Availability * NumberOfTouches #touches back to ws        
        self.wbStats.save(filename = self.StatFileName)                                 #Write to the file     
        
        
#****************************************************************************
#Method:   WriteAvailability
#Purpose:  This method writes whether a player is available to play.  More will be done with 
#                this later.  For now, this is set to 1 for each player
# Inputs:    Stat table, Worksheet row starting point, number of rows, worksheet column
# Outputs: Availability flag
# Author:           Rick Burney
# Created:          03/08/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def WriteAvailability(self, FormattedTable, StartingPoint, TableRowLength, 
                 wsColumn, TableColumn):

        for i in range(TableRowLength):                 #For each player, write the availability flag
            self.wsStats.cell(row = StartingPoint + i,  # to the worksheet.  Right now, that flag is
              column = wsColumn).value = 1                  #always set to 1        
        self.wbStats.save(filename = self.StatFileName) #Write file        
        
        
#****************************************************************************
#Method:   WriteAve
#Purpose:  This method writes a statistics average (could be rushing, receiving or something 
#                else and in actuality, it is just a number read from the stats table that is rewritten 
#                to the worksheet).  1 significant digit to the right of the decimal point
# Inputs:  Stat table, Worksheet row starting point, number of rows, worksheet column, table 
#              column
# Outputs: Number read from stats table that is rewritten to the worksheet 
# Author:           Rick Burney
# Created:          03/08/2020
# Copyright:       (c) Rick 2020
#****************************************************************************
    def WriteAve(self, FormattedTable, StartingPoint, TableRowLength, 
                 AveColumn, TableColumn):

#For each row in the stat table, read the designated number from the (row, column) address
        # and write this number to the appropriate cell in the worksheet
        for i in range(TableRowLength): 
            if (FormattedTable.iloc[i , TableColumn]) != u'\u221e':
                self.wsStats.cell(row = StartingPoint + i, 
              column = AveColumn).value = round(float(FormattedTable.iloc[i , 
                                                            TableColumn]),1)       
        self.wbStats.save(filename = self.StatFileName)                                         #Write to file        
       
        
#****************************************************************************
#Method:   WriteBlowoutComputeCPs
#Purpose:  This method computes the cumulative probability that a particular player will get 
#                a touch during a blowout. Different criteria are used to compute probabilities. 
#                The blowout flags are speculatively filled.  They will be adjusted manually and 
#                updated when the ReWrite Stats button is pressed
# Inputs:    Worksheet row starting point, number of rows, worksheet column, 
#                blowout flag column, stat code to distinguish b/n RBs and receivers
# Outputs: Cumulative probabilities
# Author:           Rick Burney
# Created:          03/09/2020
# Copyright:       (c) Rick 2020
#****************************************************************************
    def WriteBackupComputeCPs(self, StartingPoint, TableRowLength, BCPColumn, 
                              BFColumn, StatCode):     
                    
#The blowout flag indicates if a player plays during a blowout.
#Speculatively, fill in the blowout flag column
        NumberOfBlowoutPlayers = 0
        if StatCode == 0:
            PlayersSittingDown = 0
        else:
            PlayersSittingDown = 3
        for i in range(TableRowLength):
            
            if i <= PlayersSittingDown:
                self.wsStats.cell(row = StartingPoint + i, 
                                  column = BFColumn).value = 0
            else:
                self.wsStats.cell(row = StartingPoint + i, 
                      column = BFColumn).value = 1
                NumberOfBlowoutPlayers += \
                        self.wsStats.cell(row = StartingPoint + i, 
                                  column = BFColumn).value
        for i in range(TableRowLength):
            BlowoutFlag = self.wsStats.cell(row = StartingPoint + i, 
                                                 column = BFColumn).value
            if i == 0:                                                                  #Set CPs for first row
                BCP1 = 0
                BCP2 = (100/NumberOfBlowoutPlayers) * BlowoutFlag
                
            else:           #Remaining rows are computed differently than 1st      
                BCP1 = BCP2
                BCP2 = BCP1 + (100/NumberOfBlowoutPlayers) * BlowoutFlag
            
#ADD ELSE CONDITION and put if statement within for statement - check other statcode for example               
#Write cum probability limits to worksheet
            self.wsStats.cell(row = StartingPoint + i, 
                              column = BCPColumn).value = round(BCP1,0)
            self.wsStats.cell(row = StartingPoint + i, 
                          column = BCPColumn+1).value  = round(BCP2 , 0)
            
        self.wbStats.save(filename = self.StatFileName)     #Write file       
               
        
#****************************************************************************
#Method:   WriteComputeCPs
#Purpose:  This method computes the cumulative probability that a particular
#          player will get a touch
# Inputs:  Worksheet row starting point, number of rows, worksheet column
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/09/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def WriteComputeCPs(self, StartingPoint, TableRowLength, CPColumn, 
                        TotalTeamTouches):

#Write the CPs for each row in this particular stat category.  Note that the
#concept of "touches" could be carries, interceptions, receptions, tackles or
#sacks
        for i in range(TableRowLength):
            AdjustedTouches = self.wsStats.cell(row = StartingPoint + i, 
              column = CPColumn-1).value
            if i == 0:
                CP1 = 0
                CP2 = ((100 * AdjustedTouches)/TotalTeamTouches)
            else:
                CP1 = CP2
                CP2 = CP1 + ((100 * AdjustedTouches)/TotalTeamTouches)
            self.wsStats.cell(row = StartingPoint + i, 
                              column = CPColumn).value = round(CP1,0)
            self.wsStats.cell(row = StartingPoint + i, 
                          column = CPColumn+1).value  = round(CP2 , 0)          
        self.wbStats.save(filename = self.StatFileName)        
        
        
#****************************************************************************
#Method:   WriteInjuryImpacts
#Purpose:  This method simply writes 0 to the 4 Injury Impact fields.  For future use
# Outputs: 0
# Author:           Rick Burney
# Created:          04/01/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def WriteInjuryImpacts(self):
       
        for i in range(4):
            self.wsStats.cell(row = self.InjuryImpactStartingPoint + i, 
             column = 3).value = 0
        
        self.wbStats.save(filename = self.StatFileName)    #Write to worksheet          
                   
        
#****************************************************************************
#Method:   WriteName
#Purpose:  This method writes a player names to the worksheet (left-justified)
# Outputs: Formatted player name
# Author:           Rick Burney
# Created:          03/03/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def WriteName(self, FormattedTable, StartingPoint, TableRowLength, 
                  wsColumn, TableColumn):
       
#Write names to worksheet, left justified        
        for i in range(TableRowLength):
            self.wsStats.cell(row = StartingPoint + i, 
             column = wsColumn).value = FormattedTable.iloc[i , TableColumn]
            self.wsStats.cell(row=StartingPoint + i, 
                column=wsColumn).alignment = Alignment(horizontal='left', 
                                                            vertical='center')            
        self.wbStats.save(filename = self.StatFileName)         #Write to file          
        
        
#****************************************************************************
#Method:   WritePercentage
#Purpose:  This method pulls a % string from a table, removes the %, converts to a float and 
#               then writes the number to the worksheet
# Inputs:   Stat table, number of rows, Table column with the string to be converted, 
#               worksheet column where the percentage will be written, Worksheet starting row
# Outputs: Percentage written to the worksheet
# Author:           Rick Burney
# Created:          03/12/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def WritePercentage(self, StatTable, NumRows, TableColumn, wsColumn, StartingPoint):

        for i in range(NumRows):                                                    #Read % string from table       
            CompletionPercentage = StatTable.iloc[i, TableColumn]
            
#Remove literal from string and convert to a float
            CP = CompletionPercentage.replace(' %','')
            CP = round(float(CP),1)
            self.wsStats.cell(row = StartingPoint + i, 
                              column = wsColumn).value = CP
            
        self.wbStats.save(filename = self.StatFileName)    #Write to worksheet        
        
        
#****************************************************************************
#Method:   WritePlayerPosition
#Purpose:  This method is the first pass at determing a player's position.
#          Possibly, a 2nd pass will be added that reads the roster to 
#          determine the position
# Inputs:  Worksheet starting row, number of rows, worksheet column, stat code
#          0 = Rushing, 1 = Receiver
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/03/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def WritePlayerPosition(self, StartingPoint, TableRowLength, wsColumn, 
                            StatCode):


#The Stat code is used as a criteria for speculating if the player is an RB, 
#QB or WR.  If 0, this is a rushing table and the following logic applies 
#Carries > 10 are 'RB', less than or equal to 10 are "WR" and YPC < 0 are QB.
#If stat code = 1, then this is a receiving table and and YPC < 5 will be RB,
#otherwise, will be 'Receiver'.  At first, their will be manual corrections to
#be made
        for i in range(TableRowLength):
            if StatCode == 0:
                if self.wsStats.cell(row = StartingPoint + i, 
                                     column = 3).value > 10:
                    self.wsStats.cell(row = StartingPoint + i, 
                                      column = wsColumn).value = "RB"
                else:
                    self.wsStats.cell(row = StartingPoint + i, 
                                            column = wsColumn).value = "WR" 
                    if self.wsStats.cell(row = StartingPoint + i,column=4).\
                       value < 0:
                        self.wsStats.cell(row = StartingPoint + i, 
                                            column = wsColumn).value = "QB" 
            else:
                if self.wsStats.cell(row = StartingPoint + i, 
                                     column = 3).value < 5:
                    self.wsStats.cell(row = StartingPoint + i, 
                                      column = wsColumn).value = "RB"
                else:
                    self.wsStats.cell(row = StartingPoint + i, 
                                        column = wsColumn).value = "Receiver" 
            
        self.wbStats.save(filename = self.StatFileName)        
        
        
#****************************************************************************
#Method:   WriteRatio
#Purpose:  This method receives a table, extracts two numbers as specified in
#          the list of arguments and divides one number by the other.  A flag
#          is passed in that is used to determine if this ratio is a
#          percentage which means the ratio will be mulitplied by 100 prior to
#          writing the ratio to the worksheet.  SimpleRatio means that the 
#          dividend and divisor columns are actually the dividend and divisor
#          and are used directly rather than pointing at columns
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/12/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def WriteRatio(self, StatTable, StartingPoint, TableRowLength, 
                   DividendColumn, DivisorColumn, PercentageFlag, SigDigits, 
                   wsColumn, SimpleRatio):

        for i in range(TableRowLength):
            if SimpleRatio == 0:
                Dividend = StatTable.iloc[i, DividendColumn] #Extract dividend
                Divisor = StatTable.iloc[i, DivisorColumn]   #Extract divisor
            else:
                Dividend = DividendColumn
                Divisor = DivisorColumn
            ratio = round(Dividend / Divisor,SigDigits)  #Compute ratio
            if PercentageFlag == 1:
                ratio *= 100
            self.wsStats.cell(row = StartingPoint + i, 
                              column = wsColumn).value = ratio

        self.wbStats.save(filename = self.StatFileName)                  
               
        
#****************************************************************************
#Method:   WriteTotals
#Purpose:  This method is given a range down a column and computes the total
# Inputs:   Worksheet row starting point, number of rows, worksheet column
# Outputs: Formatted worksheet
# Author:           Rick Burney
# Created:          03/09/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def WriteTotals(self, StartingPoint, TableRowLength, TotalsColumn):

        TotalsRow = StartingPoint + TableRowLength  #Where to write total 
        
#Compute total
        Total = 0                                       #First, initialize the total, then compute
        for i in range(TableRowLength):
            Total += self.wsStats.cell(row = StartingPoint + i, column = TotalsColumn).value
            
#Write the total 1 row below the last row in the totals column
        self.wsStats.cell(row = TotalsRow,column = TotalsColumn).value = Total
        
#Save everything in the worksheet
        self.wbStats.save(filename = self.StatFileName)        
        return(Total)                                                       #Return the computed total

        
#****************************************************************************
#Method:   WriteTouches
#Purpose:  This method writes the number of touches (could be rushing, receiving or 
#                something else). 
# Inputs:  Stat table, Worksheet row starting point, number of rows, worksheet column, table
#              column
# Outputs: Number of touches for each player
# Author:           Rick Burney
# Created:          03/08/2020
# Copyright:       (c) Rick 2020
#****************************************************************************
    def WriteTouches(self, FormattedTable, StartingPoint, TableRowLength, wsColumn, 
                     TableColumn):

#Write # of touches to worksheet        
        for i in range(TableRowLength):
            self.wsStats.cell(row = StartingPoint + i, 
              column = wsColumn).value = FormattedTable.iloc[i, TableColumn]        
        self.wbStats.save(filename = self.StatFileName)                                         #Write to file        