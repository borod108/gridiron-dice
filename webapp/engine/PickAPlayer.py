#****************************************************************************
#Class:   PickAPlayer
#Purpose:  Used primarily during the compilation of defensive stats, this 
#          could be expanded in future revision to handle all of the searching  
#          and loading of stats in the team worksheets
# Inputs:       wsDefense-Defensive stats worksheet, PlayCount-Used to determine who gets
#                  assigned tackles, PassAttempts-# of pass attempts against the defense, 
#                  Completions-# of completions against the defense, NonTacklingPlays-
#                  PlayCount-NonTacklingPlays = Plays where a tackle is registered, SackCount-
#                  Total sacks by the defense
# Outputs:    Used to search through a cumulative probability list to determine which 
#                  offensive player touches the ball or which defensive player gets a tackle or sack
# Author:           Rick Burney
# Created:          Sometime in 2017
# Copyright:        (c) Rick 2017
#****************************************************************************
class PickAPlayer:
    
    import openpyxl
    

#****************************************************************************
#Method:   __init
#Purpose:  The constructor for this class.  The defensive stats worksheet is
#          passed in along with the playcount (for a team, number of pass  
#          attempts, number of completions, number of non-tackling plays and
#          the number of sacks
# Author:           Rick Burney
# Created:          Sometime in 2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def __init__(self,wsDefense,PlayCount,PassAttempts,Completions,
                 NonTacklingPlays,SackCount):

        self.wsDefense = wsDefense       #Defensive stats worksheet
        self.ws = wsDefense                   #Acknowledges the fact that this is the stats worksheet  
                                                          #for a team that contains offensive and defensive stats
        self.PlayCount = PlayCount               #Number of plays run against the defense. 
        self.PassAttempts = PassAttempts    #No. of pass attempts and
        self.Completions = Completions       #completions against the defense

#Not sure why we need to add 1 to the number of tackles but it works
        self.TotalNumberOfTackles = PlayCount - NonTacklingPlays + 1
        
        self.SackCount = SackCount      #Sack count constructor
        self.SackerList = []                     #Initialized lists of sackers
        self.NumberOfSacksList = []      #Since Python doesn't allow multi-dimensional lists, 
        self.TacklerList = []                    #combine single-dimensional lists with a common 
        self.NumberofTacklesList = []    #index       
        self.RunnersPosition = 0            #Initialize the requested data row that will return the 
                                                          #location of the running backs position group
        self.QBsPosition = 0                   #Initialize the requested data row that will return the 
                                                          #location of the QBs position group
        self.ReceiversPosition = 0           #Initialize the requested data row that will return the
                                                          #location of the receivers position group
        self.KickersPosition = 0              #Initialize the requested data row that will return the 
                                                          #location of the kickers position group 
        self.DStatsPosition = 0               #Initialize the requested data row that will return the 
                                                          #location of the Defensive team stats
        self.KRsPosition = 0                   #Initialize the requested data row that will return the 
                                                          #location of kickoff  returners stats
        self.INTsPosition = 0                  #Initialize the requested data row that will return the 
                                                          #location of interceptions and related stats
        self.OFumblesLostPosition = 0   #Initialize the requested data row that will return the 
                                                          #location of offensive fumbles and lost
                                        
        self.FumbleRecoveriesPosition = 0   #Initialize the requested data row that will return
                                                                #the location of the list of defensive players who
                                                                #can recover a fumble
        self.TeamStatsPosition = 0               #Initialize the requested data row that will return 
                                                                #the location of team stats such as penalties per 
                                                                #game and conference factor
        self.TacklesPosition = 0                   #Initialize the requested data row that will return 
                                                               #the location of tackle stats.  Also the row where
                                                               #sack stats are found
        self.Offset = 1                      #Offset to the row position where the data really is located
        self.PuntersOffset = 3           #Offset relative to the "Kickers" row
        self.DPCompPercOffset = 2   #Offset that points to row with pass defense completion 
                                                    #percentage
        self.DPYACOffset = 2       #Offset that points to row with pass defense yards after catch
        self.PROffset = 2                   #Offset that points to row with punt returner's statistics
        self.OFumblesLostOffset = 0 #Offset that points to row with offense's lost fumble 
                                                    #statistics                                   

        self.SacksStartRow = self.TacklesStartRow = 93  #Nominal position
        self.InjuryImpactsPosition = 130                        #Nominal position
        self.X = 0                                                           #Placeholder
                                                 

#****************************************************************************
#Method:   BuildStatList
#Purpose:  A generalized method for building a list of stats for a particular category
#               (e.g. rushing or receiving).  The Stat List is a 2D array
#                with each column as an independent list (Name, yardage, LG, TD)
# Author:           Rick Burney
# Created:          4/11/2018
# Copyright:        (c) Rick 2018
#WHAT IS CRUCIAL HERE IS THAT ALL OBJECTS THAT ARE RETURNED TO CALLING METHOD
#MUST BE INITIALIZED IN __init__ AS CONSTRUCTORS AND THEN REFERENCED IN THIS
#METHOD USING self.
#Objects Passed In: Name - The name of the player who is in the Stat List
#                             NameList - The list of names from the Stat List
#                             Yardage - The amount of yards gained by a player
#                             YardageList - A list of yardage gained by each player in the Stat List
#                             NumberOfList - Depends on the stat category - Rushing will be the # of
#                                                      carries list, Receiving will be the # of catches list
#                             LongestGainList - The list of longest gains assigned to each player in the 
#                                                         Stat List
#                             TDList - The list of TDs scored by each player in the Stat
#                            List
#THIS METHOD IS NOT CURRENTLY USED.  DELETE AFTER 7/6/21
#****************************************************************************
    def BuildStatList(self,Name):
        
        self.X = Name #placeholder
  
 
 
 
         
#****************************************************************************
#Method:   TackleStats
#Purpose:  This method interrogates the play log for and calculates the # of
#          tackles for the defense, and then assigns those tackles to 
#          defensive players based upon the tackle stats on the defensive 
#          team's worksheet
# Author:           Rick Burney
# Created:          Sometime in 2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def TackleStats(self):
        
        import random

#Column in worksheet that is the 1st number in the cum probability range for a player e.g.
#range = 45 - 50 (in percent).  When the random number is between 45 and 50, then the
#player whose cum probabilities are within this range is selected as the tackler
        TacklesProbColumn = 5      
        TacklerColumn = 2           #Column in the worksheet has the name of the potential
                                                 #tackler
        
        for i in range(1,self.TotalNumberOfTackles):    
            
#Instantiate a class object that will allow the location of the row in the 
#defensive team's worksheet for tackle stats and probabilities
            self.FindStats()
            self.TacklesStartRow = self.TacklesPosition + self.Offset
            #TacklesStartRow = 93                        #team has been
                                                        #computed, start
                                                        #assigning tackles
            dice1 = random.randint(0,99) #Roll the dice to determine the 
                                         #tackler
           

#When the dice value is less than the cumulative tackler probability, then
#that person makes the tackle  
            while dice1 >= int(self.wsDefense.cell(row = self.TacklesStartRow,
                                            column=TacklesProbColumn).value):

                self.TacklesStartRow += 1
            #print(dice1)
            GuyMakingtheTackle = str(self.wsDefense.cell(row = self.TacklesStartRow,
                                            column=TacklerColumn).value)
            if GuyMakingtheTackle in self.TacklerList:  #Existing Entry
                
                TacklerListIndex = self.TacklerList.index(GuyMakingtheTackle)

                self.NumberofTacklesList[TacklerListIndex] += 1
            else:                                                                           #New entry, add name to list
                self.TacklerList.append(GuyMakingtheTackle)         #and equate name to # of
                self.NumberofTacklesList.append(1)                       #tackles
                
                
#****************************************************************************
#Method:   SackStats
#Purpose:  This method interrogates the play log for and calculates the # of sacks for the
#defense, and then assigns those sacks to defensive players based upon the sack stats on
#the defensive team's worksheet
# Author:           Rick Burney
# Created:          Sometime in 2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def SackStats(self):
        
        import random
        
        SackerProbColumn = 11   #The probability of any player on the D's worksheet making a
        SackerColumn = 8            #sack        
               
        for i in range(1,self.SackCount+1): #Start assigning sacks to players
        
#Instantiate a class object that will allow the location of the row in the defensive team's 
#worksheet for sack stats and probabilities
            self.FindStats()                                                                #Look for the sack stats row
            self.SacksStartRow = self.TacklesPosition + self.Offset 
            
            dice1 = random.randint(0,99)   #Randomly select a probability from 0 to 99
            
#Find the range of cumulative probabilities that encompasses the random value 
#just computed.  This will identify the defensive player who made the sack.  Keep parsing
#through the list of potential sackers until the random value is less than the player's 
#cumulative probability of making a sack
            print(dice1)
            while dice1 >= int(self.wsDefense.cell(row = self.SacksStartRow,
                                            column=SackerProbColumn).value):
                self.SacksStartRow += 1 
                
#When dice1 is greater than equal to the indexed cum probability, we have identified who 
#made the sack.  Access the sacker's name
            Sacker = str(self.wsDefense.cell(row = self.SacksStartRow,
                                            column=SackerColumn).value)                        
            if Sacker in self.SackerList:                                        #See if the sacker has made any
                                                                                             #previous sacks in this game
                
#Create a local pointer to the sacker
                SackerListIndex = self.SackerList.index(Sacker)

#Increment the number of sacks attributed to that sacker
                self.NumberOfSacksList[SackerListIndex] += 1
            else:                                                                      #First sack of the game for this
                self.SackerList.append(Sacker)                           #sacker.  Add them to the sack
                self.NumberOfSacksList.append(1)                    #list and set the ## of sacks 
                                                                                        #attributed to the sacker to 1
                                                 

#****************************************************************************
#Method:   FindStats
#Purpose:  Goes through the stat worksheets and identifies the rows where the
#          stats for position groups begin.  This is to eliminate the hard-coding of worksheet 
#          rows as constants.
# Inputs:            ws.max_row - last row used in worksheet
# Author:           Rick Burney
# Created:          1/29/2018
# Copyright:        (c) Rick 2018
#****************************************************************************
    def FindStats(self):
        
        PositionColumn = 1                #In all cases, this is where the position group labels are  
                                                       #located on the worksheet
        QBNameColumn = 2                #Where the quarterback names are located             
        row_count = self.ws.max_row  #Determine last row used in worksheet
        
#Parse through worksheet to identify rows where the position headings are located. In most 
#cases, the player stats are located one row below the position label
        self.Offset = 1   
        
#Seach the worksheet for a particular position group.  Sometimes a position group is really a 
#group of stats like interceptions
        for i in range(1,row_count):  
            
#Position groups are "Runners" (RBs), QBs, Receivers, Kickers, Defensive team stats, Kick 
#Returners, Interceptions, Offensive fumbles lost, Fumble recoveries, team stats 
#(penalties, conference factor), tackles and injury impacts.  Look for the IDs and assign a
#row for each position group which allows indexing into the stats worksheet
            if self.ws.cell(row=i,column = PositionColumn).value == 'Runners':    #ID RB stats
                self.RunnersPosition = i
            if self.ws.cell(row=i,column = PositionColumn).value == 'QBs':           #ID QB stats
                self.QBsPosition = i
            if self.ws.cell(row=i,column=PositionColumn).value == 'Receivers':     #ID Receivers
                    self.ReceiversPosition = i                                                             #stats
            if self.ws.cell(row=i,column=PositionColumn).value == 'Kickers':      #ID kicking stats
                self.KickersPosition = i                                                                  #FG/Kickoffs
                self.PuntersOffset = 2                                              #Offset from Kickers stat row
                                
#Identifies where the defensive team stats are located on this worksheet.  #Includes rush 
#defense (yards/attempt), pass defense (completion % and yards/catch), sack %, kick 
#block %, punt block %, Int % and recovered fumble %
            if self.ws.cell(row = i,column = PositionColumn).value == \
               'Defensive Team Stats':                                                          #Label ID'ing DStats
                self.DStatsPosition = i           #Number of stats including yards/rush given up by D
                self.DPCompPercOffset = 2   #Passing completion % given up by the defense
                self.DPYACOffset = 3            #Yards per catch given up by the defense
                
#Find location of kick return stats.
            if self.ws.cell(row = i,column = PositionColumn).value == 'KRs':
                self.KRsPosition = i                                                                    #ID KR row
                self.PROffset = 4                                                                        #OD PR row      
                
#Find location of individual interception stats (# of Ints and return yardage average
            if self.ws.cell(row = i,column = PositionColumn).value == 'INTs':
                self.INTsPosition = i
                
#This is the location of the stats for the probability of a lost fumble for the offense
            if self.ws.cell(row = i,
                            column = PositionColumn).value == 'Fumble Lost':
                self.OFumblesLostPosition = i
                
#This is the location of the stats for the list of players that can recover fumbles
            if self.ws.cell(row = i,column = PositionColumn).value == 'Fumble Recoveries':
                self.FumbleRecoveriesPosition = i
                
#This is the location of the stats for team penalties/game and conference factor
            if self.ws.cell(row = i, column = PositionColumn).value == 'Teams Stats':
                self.TeamStatsPosition = i
                
#This is the location of the stats for tackle statistics and probabilities
            if self.ws.cell(row = i, column = PositionColumn).value == 'Tackles':
                self.TacklesPosition = i
                
#This is the location of the stats for injury impacts
            if self.ws.cell(row = i, column = PositionColumn).value == 'Injury Impacts':
                self.InjuryImpactsPosition = i 