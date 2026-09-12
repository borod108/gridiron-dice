from ScoreboardClass import *
import GameManager
import LogPlays
#import MDArray  #Delete on Oct 28, 2021
import numpy
import openpyxl
import Penalty
import random
import ResultofthePlay
import TestTurtleGraphics   #Draw the ball position on the football field
import Tkinter
import Tkinter
import tkMessageBox
import YardageTable


#****************************************************************************
#Method:   Play
#Purpose:  This class contains all of the methods and objects to execute a 
#          non-kicking play.  The methods include the play call, pre-snap 
#          penalty test, play result, interception processing, fumble 
#          processing, penalty processing, change of possession processing and
#          game maintenance
# Inputs:  GM - Game Management Dictionary
#          PlayerStats - Player Stats Dictionary
#          GameOptions - Dictionary that holds the state of various check 
#                        buttons
#          TeamStats - Team Stats Dictionary
#          Parent - Parent frame for display of play call and result
# Outputs: Executed play and updated game maintenance
#
# Author:           Rick Burney
#
# Created:          7/9/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
class Play():
    
    def __init__(self,GM,PlayerStats,GameOptions,TeamStats,
                 Parent,GrandParent,Kicking):
        
        import PickAPlayer
        
        self.GM = GM
        self.PlayerStats = PlayerStats
        self.GameOptions = GameOptions
        self.TeamStats = TeamStats
        self.Dstats = []
        self.Play = []
        self.Parent = Parent
        self.GrandParent = GrandParent
        self.PassLength = ""
        
#PenaltyList[0] = Penalty Called 
#PenaltyList[1] = Presnap penalty flag, 0 if no presnap, 1 if presnap
#PenaltyList[2] = Automatic First Down Flag, 0 if not, 1 if so
#PenaltyList[3] = Loss of down flag, 0 if no LOD, 1 if LOD
#PenaltyList[4] = Penalty yardage, negative if on offense
#PenaltyList[5] = After the play flag, 0 if no, 1 if yes
        self.PenaltyList = ["",0,0,0,0,0,0]
        self.AcceptedPenaltyFlag = 0
        

# Result List contains everything that happened after a play is run:
#     ResultList[0] is the play type Run or Pass
#     ResultList[1] is, if a pass, whether the pass is short, mid, or long
#     ResultList[2] is, if a pass, the result of a pass (sack, complete, 
#        incomplete or int
#     ResultList[3] are the yards gained or lost on the play  

        self.ResultList = ["","","",0]

        
        
# Fumble Result is a list:
#     FumbleResult[0] is the fumble flag, 0 if no fumble lost, 1 if not
#     FumbleResult[1] is the fumble return yardage
#     FumbleResult[2] is the yardline to which the fumble is returned.  This
#                     will be handled by the Game Manager
#     FumbleResult[3] is the name of the player who recovered the fumble  
        self.FumbleResult = [0,0,0,""]
        self.IntResult = ["","",0,25,25,0]

        self.Kicking = Kicking
        self.PuntResult = []            #Make part of self.Kicking
        self.KickBlockFlag = 0          #Make part of self.Kicking

        self.KickFlag = 0       #Indicates that the play was some sort of kick
        
        #self.GM['TDFlag'] = 0     #Touchdown flag
        self.SafetyFlag = 0
        #self.DTDFlag = 0    #If set, the defense has scored a TD
        self.ScoreFlag = 0  #Any score occurred when set
        
        self.NewYardLine = 25   #Used to set the new yardline after the play
                                #is completely resolved
        self.TDYardage = 0  #Used to adjust the yardage for touchdowns since
                            #the play ends at the endzone

#All the messages that will be processed by DisplayManagement                            
        self.DisplayMessages = {'RunPlayExecutionMsg' : "", 
                                'PassPlayExecutionMsg' : "",
                                'IntExecutionMsg' : "", 
                                'FumbleExecutionMsg' : "", 'TDMsg' : "", 
                                'SafetyMsg' : "", 'PenaltyMsg' : "", 
                                'TimeLeftinQuarterDisplay' : "", 
                                'KickoffDisplayMsg' : "", 
                                'XPtDisplayMsg' : "", 'FGDisplayMsg' : "", 
                                'PuntDisplayMsg' : "", 
                                'TwoPointConversionDisplayMsg' : ""}
        
#Save current score and yardline in case of an accepted penalty
        self.GM['OldYardLine'] = self.GM['YardLine']  
        self.GM['OldHTS'] = self.GM['HomeTeamScore']  
        self.GM['OldVTS'] = self.GM['VisitingTeamScore']  
        
        self.TouchbackFlag = 0    
        self.GM['Touchback'] = 0    
        self.OutofBoundsKickoffFlag = 0
        self.BlockedKickResult = [0,"",0,0,0]
        self.FirstDownFlag = 0
        self.OverTimeIndicator = ""
        self.HTMDA = []             #At the start of a play, the array is  
        self.VTMDA = []             #initialized to an empty list but will be
        self.HTDMDA = []            #overwritten with the actual array that is
        self.VTDMDA = []            #passed into LogPlay.  This works because
                                    #at the end of the play, data is logged to
                                    #the row and passed back to the method
                                    #that called Play.LogPlay().  Not sure if
                                    #initializing to an empty array is even
                                    #needed but it works
        self.ActualTDYardage = 0    #These objects are strictly for the
        self.ActualTDYardLine = 0   #Turtle Graphics Display

        self.TurnoverAfterAnOffensiveDeadBallFoul = 0
        
#This is where the PickAPlayer class is used and player positions groups and
#rows are located in the appropriate worksheet
#Instantiate an offense class object and a defense class object that will   
#identify the worksheet row where the players stats are to be extracted
        RequestedORow = PickAPlayer.PickAPlayer(self.GM['Offense'],0,0,0,0,0) 
        RequestedORow.FindStats()
        RequestedDRow = PickAPlayer.PickAPlayer(self.GM['Defense'],0,0,0,0,0) 
        RequestedDRow.FindStats()
        self.KickerRow = RequestedORow.KickersPosition + RequestedORow.Offset
        self.ThirdQtrKickerRow = RequestedDRow.KickersPosition + \
            RequestedORow.Offset       
        self.PunterRow = self.KickerRow + RequestedORow.PuntersOffset
        self.ReceiversRow = RequestedORow.ReceiversPosition + \
            RequestedORow.Offset
        self.QBsRow = RequestedORow.QBsPosition + \
            RequestedORow.Offset
        self.RBsRow = RequestedORow.RunnersPosition + \
            RequestedORow.Offset
        if self.GameOptions['Blowout'] == 1:    #If blowout point to backup QB
            self.QBsRow += 1                    #row  
        self.FXKickerName = ""  #Name of the field goal/XPt kicker that may be
                                #different from the person who kicks off
        self.KickerName = ""                    #Name of the kicker is used by
                                                #multiple methods in this
                                                #class.  This is the guy who 
                                                #kicks off
        self.KickoffResult = 2  #Code to determined what happened with the 
                                #kickoff (not the return). Enumerated as 0 = 
                                #Touchback, 1 = Out of Bounds Kick, 2 = 
                               #Returned Kick, 3 = Onside Kick, 4 = Squib Kick
                               #5 = Free Kick
        self.KickLength = 65             #Default, used by LogPlay Method
        self.WhoRecoveredtheOnsideKick=0 #0 = Receiving team, 1 = Kicking team
        
#Initialize
        self.NumTBs = self.NumOOBKicks = self.NumKickoffs = self.KickYards = \
            self.NumPunts = self.PuntLength = self.LongestPunt = 0
        self.KickReturnersName = ""
        self.NumKicksReturned = 0
        self.NumPuntsReturned = 0
        self.KickReturnYardage = self.PuntReturnYardage = 0
        
        self.PunterName = ""        #Name of punter
        self.PuntResult = ""        #Can be Punt, Placement Punt or Blocked
                                    #Punt
        self.PuntReturnersName = "" #Initialize name of punt returner
        
        self.PuntLength = 0 #Either length of the punt or in the case of a 
                            #block, 0
        
        self.ThisPuntisReturned = 0 #Initialize object that flags whether a 
                                    #punt is returned or not
        self.FGResult = 0           #Result of a field goal - default is NG
        self.NumFGsMade = 0         #Num of successful FGs for each team
        self.FGA = 0                #Num of field goals attempted by each team        
        self.XPtResult = 0          #Result of an extra point - default is NG
        self.NumXPtsMade = 0        #Num of successful XPts for each team
        self.PuntFCPerc = 0             #FC % based upon the punter stats
        self.DPIOccurredInEndZone = 0
        self.ForceBlockedKick = 0
        self.QBSneak = 0            #Flag that is set when there is a QB Sneak

#****************************************************************************
#Method:    ClockRunning
#Purpose:   Sets/Resets a flag depending on whether or not the clock is 
#           running or stopped after a play
# Inputs:   GM dictionary element 'ClockRunning', 0 if stopped, 1 if running 
#           GM dictionary element TimeCode
# Outputs:  GM dictionary element 'ClockRunning'
# Author:           Rick Burney
# Created:          8/28/2018
# Copyright:        (c) Rick 2018
#****************************************************************************
    def ClockRunning(self):

        if (self.GM['TimeCode'] == 9) or (self.GM['TimeCode'] == 10) or \
           (self.GM['TimeCode'] == 15) or (self.GM['TimeCode'] == 18):
            self.GM['ClockRunning'] = 1
        else:
            self.GM['ClockRunning'] = 0
            
        
#****************************************************************************
#Method:    CompileStats
#Purpose:  
# Inputs:  
# Outputs: 
# Author:           Rick Burney
#
# Created:          8/5/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def CompileStats(self,MDA,TeamFlag,HQBName,VQBName,HBackupQBName,
                     VBackupQBName, homeTeamName, visitingTeamName,
                     FinalScore,DMDA):
        
        from openpyxl import load_workbook     #Using openpyxl Python library
        from openpyxl import Workbook
        from openpyxl.styles import Alignment
        import PickAPlayer
        
        FGHeadingRow = 18     #Heading location for field goal stats on ws
        XPtHeadingRow = 23    #Heading location for extra point stats on ws
        FinalScoreRow = 31
        FinalScoreColumn = 1
        KickHeadingRow = 18     #Heading location for kicking stats on ws

#Column where the label for kicking and returns goes     
        FGLabelColumn = XPtLabelColumn = 9
        KickoffLabelColumn = KickReturnLabelColumn = PuntReturnLabelColumn = 2   
        
        PuntHeadingRow = 24     #Heading location for punt stats on ws
                                                        
        PuntLabelColumn = 2         #Column where the label "Punts" go
        PuntReturnHeadingRow = 27   #Heading location for punt return stats on
                                    #the worksheet
        KickReturnColumn = 0        #Where to look in log for kick returns
        KickReturnHeadingRow = 20   #Heading location for kick return stats on
                                    #the worksheet
        KickReturnersNameColumn = 3 #Where to extract kick returner's name
        KickReturnYardageColumn = 2 #Where to extract kick returner's yardage
        KRTDColumn =  4             #Where to extract kick returns for a TD
        PRTDColumn = 3
        PuntReturnersNameColumn = 4 #Where to extract punt returner's name
        PuntReturnYardageColumn = 2 #Where to extract punt returner's yardage
        RushingHeadingRow = 1           #Heading locations on Ostat worksheets
        TurnoverRow = 30 
        InterceptionHeadingColumn = 2   #Heading for Ints on D worksheet
        IntHeadingRow = 31              #Subheadings for Ints on D worksheet
        InterceptionNameColumn = 1      #Heading for name of Interceptors
        IntReturnYardageColumn = 3      #Heading for int return yardage
        Pick6Column = 4                #Heading for Pick 6s
        BallCarrierHeadingColumn = 1
        NumberofCarriesColumn = 2
        NumIntsColumn = 2               #Heading for the # of Ints by a player        
        RushingYardsColumn = 3
        YPCColumn = 4
        RunLGCol = 5
        RBTDColumn = 6
        ReceiverNameColumn = 8
        ReceptionsColumn = 9
        ReceivingYardsColumn = 10
        YPCatchColumn = 11
        RcvgLGCol = 12
        RcvrTDColumn = 13
        QBNameColumn = 15
        PassAttemptColumn = 16
        CompletionsColumn = 17
        YardsColumn = 18
        QBLGCol = 19
        IntColumn = 20
        PassTDColumn = 21
        LogDataPlayTypeColumn = 0    #Array columns for log data
        LogIntIDColumn = 0           #Column where the Int identifier is found
        LogFumbleColumn = 0          #Column in the log that indicates if a 
                                     #lost fumble occurred on the play
        LogInterceptorNameColumn = 1 #Column where the name of the interceptor
                                     #is found
        LogIntYardsColumn = 2           #Column where the return yards from 
                                        #the int are found
        LogPick6Column = 3              #Column where the pick-6 flag is found
        LogReceivingYardageColumn = 3
        LogTDColumn = 4
        LogFumbleFlagColumn = 7
        LogBallCarrierColumn = 1
        LogPassResultColumn = 2
        LogBackupQBColumn = 8
        FumbleRecoverColumn = 1     #This is the column where the name of the
                                    #player who recovers a fumble (in the 
                                    #defensive log) goes
        FumbleRecoveryColumn = 6    #This is the column where the Fumble 
                                    #Recovery heading goes
        
        RecoveryYardsColumn = 2 #Where the fumble recovery return yards are in
                                #the defensive log
        
        
        HT = homeTeamName     #Used as a partial string to form Ostats and 
        VT = visitingTeamName #Dstats filenames
                                                
        homeWorksheet = homeTeamName + ".xlsx"
        visitingWorksheet = visitingTeamName  + ".xlsx"


        homeTeamStats = HT + "Stats.xlsx"       #All stats workbooks have an  
        visitingTeamStats = VT + "Stats.xlsx"   #xlsx extension
        homeTeamDStats = HT + "DStats.xlsx"
        visitingTeamDStats = VT + "DStats.xlsx"
        wbStats = Workbook()                        #Stats file
        wbDStats = Workbook()

#Load workbook based upon TeamFlag which should be self.GM['OffenseFlag'] but 
#need to watch this
        if TeamFlag == 0:
            
#wbTeam is the log file so we won't be using this because now we use arrays
            #wbTeam = load_workbook(filename = homeTeamName, data_only=True)
            
#wbDefense is the team worksheet that is used as an input to CompileStats to
#compile tackles and sacks
            wbDefense = load_workbook(filename = visitingWorksheet,
                                      data_only=True)
            #PlayCount = homeTeamPlayCount
            StatsName = homeTeamStats
            DStatsName = visitingTeamDStats
            QBName = HQBName                #ID the QB and backup
            BackupQBName = HBackupQBName
        else:
            #wbTeam= load_workbook(filename = visitingTeamName, data_only=True) 
            wbDefense = load_workbook(filename = homeWorksheet, 
                                      data_only=True)
            #PlayCount = visitingTeamPlayCount
            StatsName = visitingTeamStats
            DStatsName = homeTeamDStats
            QBName = VQBName                #ID the QB and backup
            BackupQBName = VBackupQBName

#wsDstats are the defenisve stats worksheet
        #ws = wbTeam.active          #switch to active worksheet
        wsStats = wbStats.active
        wsDefense = wbDefense.active
        wsDStats = wbDStats.active


        for row in wsStats['A1:N400']:  #clear stats sheet 
            for cell in row:
                cell.value = None
        wbStats.save(StatsName)     #write to workbook
            
           
        for row in wsStats['B1:U400']:  #Center the columns for both O and D
            for cell in row:
                cell.alignment = Alignment(horizontal="center") #worksheets  
        for row in wsDStats['B1:U400']:
            for cell in row:
                cell.alignment = Alignment(horizontal="center")  
                    
#Adjust width of the columns for both O and D worksheets
        wsStats.column_dimensions["A"].width = 20.0
        wsStats.column_dimensions["B"].width = 15.0
        wsStats.column_dimensions["C"].width = 15.0
        wsStats.column_dimensions["D"].width = 15.0
        wsStats.column_dimensions["E"].width = 5.0
        wsStats.column_dimensions["F"].width = 5.0    
        wsStats.column_dimensions["G"].width = 8.0
        wsStats.column_dimensions["H"].width = 20.0
        wsStats.column_dimensions["I"].width = 15.0
        wsStats.column_dimensions["L"].width = 8.0
        wsStats.column_dimensions["M"].width = 5.0
        wsStats.column_dimensions["N"].width = 8.0
        wsStats.column_dimensions["O"].width = 12.0
        wsStats.column_dimensions["P"].width = 10.0
        wsStats.column_dimensions["Q"].width = 15.0
        wsStats.column_dimensions["R"].width = 16.0
        wsStats.column_dimensions["U"].width = 5.0
            
        wsDStats.column_dimensions["A"].width = 20.0
        wsDStats.column_dimensions["B"].width = 15.0
        wsDStats.column_dimensions["C"].width = 15.0
        wsDStats.column_dimensions["D"].width = 20.0
        wsDStats.column_dimensions["F"].width = 20.0
        wsDStats.column_dimensions["G"].width = 15.0
        
        for row in wsStats['D1:D400']:  #Format the cells before populating
            for cell in row:
                cell.number_format = '0.0'          

        PlayType = ""
        BallCarrierList = []    #These lists are sync'ed to form multiple-
        PassCatcherList = []    #dimensioned arrays
        InterceptionList = []   #List of interceptions and fumbles that are 
        FumbleRecoveryList = [] #recorded on the defensive stats worksheet
        YardageList = []
        RunLongestGainList = []
        ReceivingLongestGainList = []
        PassingLongestGainList = []
        ReceivingYardageList = []
        NumberofCarriesList = []
        NumberOfIntsList = []
        NumberofIntYardsList = []
        NumberofPick6sList = []
        TDList = []
        ReceiverList = []
        NumberofReceptionsList = []
        NumberOfRecoveriesList = [] #List of the # of fumble recoveries for
                                    #each player on the fumble recovery list
        ReceivingTDList = []    #List of receiving TDs
        RecoveryYardsList = []  #List of the return yardage for fumble
                                #recoveries for each play on the fumble
                                #recovery list
        NewBallCarrierIndex = 0 #Index into the rushing stats array
        NewReceiverIndex = 0    #Index into the receiving stats array
        PassAttempts = 0        #Initialize passing stats
        BackupPassAttempts = 0  #Number of backup QB pass attempts
        Completions = 0         #Number of starting QB pass completions
        BackupCompletions = 0   #Number of backup QB pass completions
        PassingYards = 0        #Starting QB passing yardage
        BackupPassingYards = 0  #Backup QB passing yardage
        QBLG = 0                #Longest gain on a pass from the starting QB
        BackupQBLG = 0          #Longest gain on a pass from the backup QB
        Ints = 0                #Number of ints thrown by the starting QB
        BackupInts = 0          #Number of ints thrown by the backup QB
        PassTDs = 0             #Number of TD passes thrown by the starting QB
        BackupPassTDs = 0       #Number of TD passes thrown by the backup QB
        NonTacklingPlays = 0    #This object is used for tackle stats and
                                #indicates that there are no tackles by the  
                                #defense for TDs, Ints and fumbles
        SackCount = 0           #Initialize the number of sacks for the D
        PlayCount = 0   #The number of offensive plays for a team less the 
                        #non-tackling plays
                        
        for i in range(len(MDA)):   #MDA is the Memory Data Array that is used
                                    #to log data (in memory, not a file)
            RowData = MDA[i]                           #Line from the log data
            PlayType = RowData[LogDataPlayTypeColumn]  #Run or Pass
            
#Yards gained            
            ReceivingYardage = Yardage = RowData[LogReceivingYardageColumn] 
            
            ReceivingTD = TD = RowData[LogTDColumn]           #TD scored?
            FumbleFlag = RowData[LogFumbleFlagColumn]         #Fumble lost?
            if (TD == 1) or (FumbleFlag == 1):         #No tackles by the 
                NonTacklingPlays += 1                  #defense if there is a 
                                                       #fumble or a TD

            if PlayType == "Run":
                
               
                
                BallCarrier = RowData[LogBallCarrierColumn] #Compile rushing 
                                                            #stats
            
                if BallCarrier in BallCarrierList:  #Existing Entry
                
                    BallCarrierIndex = BallCarrierList.index(BallCarrier)
                    YardageList[BallCarrierIndex] += Yardage
                    NumberofCarriesList[BallCarrierIndex] += 1
                    RunLongestGainList[BallCarrierIndex] = \
                    max(RunLongestGainList[BallCarrierIndex],Yardage)
                    TDList[BallCarrierIndex] += TD
                else:                                   #New entry
                    BallCarrierList.append(BallCarrier)
                    YardageList.append(Yardage)
                    NumberofCarriesList.append(1)
                    RunLongestGainList.append(Yardage)
                    TDList.append(TD)
                    NewBallCarrierIndex += 1    #Try commenting this out
                    
#On 6/19/18 replaced else statement with an elif to correct compiling of pass  
#attempts during punts and kickoffs
            elif PlayType == "Pass":
                PassCatcher = RowData[LogBallCarrierColumn]   #ID pass catcher
                
                PassResult = RowData[LogPassResultColumn] #Compile pass result
                
                if RowData[LogBackupQBColumn] == 0: #Was the pass thrown by 
                    PassAttempts += 1               #the 1st string or backup 
                else:                              #QB.  Use the blowout flag 
                    BackupPassAttempts += 1         #from the log to determine
            
                if PassResult == "Sack":    #Tally the number of sacks
                    SackCount += 1          #Sack yardage goes against the QB
                    BallCarrier = QBName                
                    if BallCarrier in BallCarrierList:  #Existing Entry
                    
                        BallCarrierIndex = BallCarrierList.index(BallCarrier)
                        YardageList[BallCarrierIndex] += Yardage
                        NumberofCarriesList[BallCarrierIndex] += 1
                    else:                                           #New entry
                        BallCarrierList.append(BallCarrier)
                        YardageList.append(Yardage)
                        NumberofCarriesList.append(1)
                        RunLongestGainList.append(Yardage)
                        TDList.append(TD)
                        #NewBallCarrierIndex += 1

            
                if PassResult == "Completed":   #Tally the number of 
                    if RowData[8] == 0:         #completions and passing 
                        Completions += 1        #yardage to either the 1st
                                                #string or backup QB
                                                
                        PassingYards += ReceivingYardage
                    else:
                        BackupCompletions += 1
                        BackupPassingYards += ReceivingYardage
                
                    if RowData[8] == 0:         #Same with longest pass gain
                        if PassAttempts == 1:           #and TD passes
                            QBLG = ReceivingYardage
                        else:
                            QBLG = max(QBLG,ReceivingYardage)
                        PassTDs += ReceivingTD
                    else:
                        if BackupPassAttempts == 1:
                            BackupQBLG = ReceivingYardage
                        else:
                            BackupQBLG = max(BackupQBLG,ReceivingYardage)
                        BackupPassTDs += ReceivingTD
                        
#Compile receiving stats
                    if PassCatcher in PassCatcherList:
                        PassCatcherIndex = PassCatcherList.index(PassCatcher)
                        ReceivingYardageList[PassCatcherIndex] += \
                            ReceivingYardage
                        NumberofReceptionsList[PassCatcherIndex] += 1
                        ReceivingLongestGainList[PassCatcherIndex] = \
                        max(ReceivingLongestGainList[PassCatcherIndex],
                            ReceivingYardage)
                        ReceivingTDList[PassCatcherIndex] += ReceivingTD
                    
                    else:
                        PassCatcherList.append(PassCatcher)
                        NumberofReceptionsList.append(1)
                        ReceivingYardageList.append(ReceivingYardage)
                        ReceivingTDList.append(ReceivingTD)
                        ReceivingLongestGainList.append(ReceivingYardage)
                        NewReceiverIndex += 1
                if PassResult == "Incomplete":
                    NonTacklingPlays += 1
                if PassResult == "Int": #Compile Int stats for the QBs and
                    if RowData[8] == 0: #note that an Int is registered as a
                        Ints +=1        #non-tackling play
                    else:
                        BackupInts += 1
                    NonTacklingPlays += 1
                    
            PlayCount += 1
        KickReturner = ""                       #Initialize local objects
        NumKicksReturned = NumPuntsReturned = 0
        KickReturnYardage = PuntReturnYardage = KickoffReturnForaTD = \
            LongestKR = PuntReturnForaTD = LongestPR = 0
        PuntReturner = ""
        
#HERE IS WHERE WE ARE GOING TO CREATE INT AND FUMBLE STATS FROM DMDA
        for i in range(len(DMDA)):              #Go through the INT and Fumble 
            DRowData = DMDA[i]                          #log row by row 
            KickReturnID = DRowData[KickReturnColumn]    #extract IntID
            if KickReturnID == "KR":
                KickReturner = DRowData[KickReturnersNameColumn]
                NumKicksReturned += 1
                KickReturnYardage += DRowData[KickReturnYardageColumn]
                KickoffReturnForaTD += DRowData[KRTDColumn]
                if NumKicksReturned == 1:
                    LongestKR = DRowData[KickReturnYardageColumn]
                else:
                    LongestKR = max(LongestKR,
                                    DRowData[KickReturnYardageColumn])
                
            if KickReturnID == "PR":
                PuntReturner = DRowData[PuntReturnersNameColumn]
                NumPuntsReturned += 1
                PuntReturnYardage += DRowData[PuntReturnYardageColumn]
                PuntReturnForaTD += DRowData[PRTDColumn]
                if NumPuntsReturned == 1:
                    LongestPR = DRowData[PuntReturnYardageColumn]
                else:
                    LongestPR = max(LongestPR,
                                    DRowData[PuntReturnYardageColumn])
                
            IntID = DRowData[LogIntIDColumn]    #extract IntID
            FumbleID=DRowData[LogFumbleColumn]  #Extract if a fumble occurred
                                                #on the play
            
#If an Int, extract rest of interception data
            if IntID == "Int":                  
                InterceptorName = DRowData[LogInterceptorNameColumn]    #Name
                IntReturnYards = DRowData[LogIntYardsColumn]            #Yards
                Pick6Flag = DRowData[LogPick6Column]            #Pick 6 flag
                if InterceptorName in InterceptionList:  #Existing Entry

#Update interceptions list with new interception data
                    #Existing entry
                    InterceptorIndex = InterceptionList.index(InterceptorName)
                    NumberOfIntsList[InterceptorIndex] += 1
                    NumberofIntYardsList[InterceptorIndex] += IntReturnYards
                    NumberofPick6sList[InterceptorIndex] += Pick6Flag
                    
                else:                                           #New entry
                    InterceptionList.append(InterceptorName)
                    NumberOfIntsList.append(1)
                    NumberofIntYardsList.append(IntReturnYards)
                    NumberofPick6sList.append(Pick6Flag)
            
#If a fumble, extract rest of fumble recovery data
            if FumbleID == "Fumble Recovery":
                FumbleRecoverName = DRowData[FumbleRecoverColumn]   #Name
                RecoveryReturnYards = DRowData[RecoveryYardsColumn] #Yards
                
                if FumbleRecoverName in FumbleRecoveryList:  #Existing Entry

#Update fumble recovery list with new recovery data                
                    FumbleRecoverIndex = \
                        FumbleRecoveryList.index(FumbleRecoverName)
                    NumberOfRecoveriesList[FumbleRecoverIndex] += 1
                    RecoveryYardsList[FumbleRecoverIndex] += \
                        RecoveryReturnYards
                else:                                            #New entry
                    FumbleRecoveryList.append(FumbleRecoverName) #Add to list
                    NumberOfRecoveriesList.append(1)
                    RecoveryYardsList.append(RecoveryReturnYards)
                    
#Kickoff, punt and return stats.  Use class objects to ensure that objects are
#always initialized when entering this method
        self.KickReturnersName = KickReturner
        self.KickReturnYardage = KickReturnYardage
        self.NumKicksReturned = NumKicksReturned
        self.NumPuntsReturned = NumPuntsReturned
        self.PuntReturnersName = PuntReturner
        self.PuntReturnYardage = PuntReturnYardage
                   
#Kickoff, FG and punt stats.  Parse through log and extract accordingly

        KickerName = PunterName = ""                #Initialize stats
        FGA = NumFGsMade = XPtA = NumXPtsMade = 0

        for i in range(len(MDA)):   #Parse through log
            
            RowData = MDA[i]                #Look at each line                           
            if RowData[0] == "Kickoff":     #If log row is a kickoff
                KickerName = RowData[1] #ID the guy kicking off
                if RowData[2] == 0:     #Count touchbacks
                    self.NumTBs += 1
                if RowData[2] == 1:         #Count out-of-bounds kicks
                    self.NumOOBKicks += 1
                KickoffDepth = RowData[3]
                if RowData[2] == 2:        #Count # of kicks that are returned
                    self.NumKickoffs += 1
                    self.KickYards += KickoffDepth  #Total # of kickoff yards
            if RowData[0] == "Punt":                #If log row is a punt
                PunterName = RowData[1]             #ID the punter
                PuntResult = RowData[2]             #Punt or blocked punt
                if PuntResult != "Blocked Punt":
                    self.NumPunts += 1              #Count the number of punts
                PuntLength = RowData[3]
                self.PuntLength += PuntLength
                self.LongestPunt = max(self.LongestPunt, PuntLength)

            if RowData[0] == "XPt":          #If log row is an extra point
                #KickerName = RowData[1]     #ID the kicker - NOT YET
                self.XPtResult = RowData[2]  #0 if XPT NG, 1 if XPT is good
                XPtA += 1                    #Increment the # of XPTs tried
                if self.XPtResult == 1:
                    NumXPtsMade += 1    #If XPT is good, increment # of XPTs  
            if RowData[0] == "FG":              #If log row is a field goal
                KickerName = RowData[1]     #ID the kicker
                self.FGResult = RowData[2]    #0 if FG NG, 1 if FG is good
                FGA += 1                               #Increment the number of FGs tried
                if self.FGResult == 1:
                    NumFGsMade += 1            #If FG is good, increment # of FGs  

#Write column headings
        wsStats.cell(row = RushingHeadingRow, 
                 column = BallCarrierHeadingColumn).value = "Ball Carrier"
        wsStats.cell(row = RushingHeadingRow, 
                 column = NumberofCarriesColumn).value = "Number of Carries"
        wsStats.cell(row = RushingHeadingRow, 
                 column = RushingYardsColumn).value = "Yards"
        wsStats.cell(row = RushingHeadingRow, column = YPCColumn).value = "Ave"
        wsStats.cell(row = RushingHeadingRow, column = RunLGCol).value = "LG"
        wsStats.cell(row = RushingHeadingRow, column = RBTDColumn).value = "TD"
        wsStats.cell(row = RushingHeadingRow, 
                     column = ReceiverNameColumn).value = "Receiver"
        wsStats.cell(row = RushingHeadingRow, 
                     column = ReceptionsColumn).value = "Receptions"
        wsStats.cell(row = RushingHeadingRow, 
                     column = ReceivingYardsColumn).value = "Yards"
        wsStats.cell(row = RushingHeadingRow, column = YPCatchColumn).value = "Ave"
        wsStats.cell(row = RushingHeadingRow, column = RcvgLGCol).value = "LG"
        wsStats.cell(row = RushingHeadingRow, column = RcvrTDColumn).value = "TD"
        wsStats.cell(row = RushingHeadingRow, column = QBNameColumn).value = "QB"
        wsStats.cell(row = RushingHeadingRow, 
                     column = PassAttemptColumn).value = "Attempts"
        wsStats.cell(row = RushingHeadingRow, 
                 column = CompletionsColumn).value = "Completions"
        wsStats.cell(row = RushingHeadingRow, 
                     column = YardsColumn).value = "Passing Yards"
        wsStats.cell(row = RushingHeadingRow, column = QBLGCol).value = "LG"
        wsStats.cell(row = RushingHeadingRow, column = IntColumn).value = "Int"
        wsStats.cell(row = RushingHeadingRow, column = PassTDColumn).value = "TD"
        
#Kickoff Stats Labels
        wsStats.cell(row = KickHeadingRow, column = KickoffLabelColumn).value = "Kickoffs"
        wsStats.cell(row = KickHeadingRow+1, 
                     column = KickoffLabelColumn-1).value = "Kicker"
        wsStats.cell(row = KickHeadingRow+1, 
                 column = KickoffLabelColumn).value = "# of Kickoffs"
        wsStats.cell(row = KickHeadingRow+1, 
                 column = KickoffLabelColumn+1).value = "Kickoff Ave"
        wsStats.cell(row = KickHeadingRow+1, 
                 column = KickoffLabelColumn+2).value = "# of Touchbacks"
        wsStats.cell(row = KickHeadingRow+1, 
                 column = KickoffLabelColumn+3).value = "# of OOB Kicks"
        
#Field Goal Stats Labels
        wsStats.cell(row = FGHeadingRow, column = FGLabelColumn).value = "Field Goals"
        wsStats.cell(row = FGHeadingRow+1, column = FGLabelColumn-1).value = "Kicker"
        wsStats.cell(row = FGHeadingRow+1, column = FGLabelColumn).value = "FGA"
        wsStats.cell(row = FGHeadingRow+1, column = FGLabelColumn+1).value = "FGM"
        
#Extra Point Stats Labels
        wsStats.cell(row = XPtHeadingRow, column = XPtLabelColumn).value = "Extra Points"
        wsStats.cell(row = XPtHeadingRow+1, column = XPtLabelColumn-1).value = "Kicker"
        wsStats.cell(row = XPtHeadingRow+1, column = XPtLabelColumn).value = "XPtA"
        wsStats.cell(row = XPtHeadingRow+1, column = XPtLabelColumn+1).value = "XPtM"

#Punt Stats Labels 
        wsStats.cell(row = PuntHeadingRow, column = PuntLabelColumn).value = "Punts"
        wsStats.cell(row = PuntHeadingRow+1, column = PuntLabelColumn-1).value = "Punter"
        wsStats.cell(row = PuntHeadingRow+1, 
                     column = PuntLabelColumn).value = "# of Punts"
        wsStats.cell(row = PuntHeadingRow+1, 
                     column = PuntLabelColumn+1).value = "Punt Ave"
        wsStats.cell(row = PuntHeadingRow+1, column = PuntLabelColumn+2).value = "Long"
        
#Kick Return Stats Labels
        wsStats.cell(row = KickReturnHeadingRow, 
                 column = KickReturnLabelColumn).value = "Kick Returns"
        wsStats.cell(row = KickReturnHeadingRow+1, 
                 column = KickoffLabelColumn-1).value = "Kick Returner"
        wsStats.cell(row = KickReturnHeadingRow+1, 
                 column = KickoffLabelColumn).value = "# of Kick Returns"
        wsStats.cell(row = KickReturnHeadingRow+1, 
                 column = KickoffLabelColumn+1).value = "Kick Return Ave"
        wsStats.cell(row = KickReturnHeadingRow+1, 
                 column = KickoffLabelColumn+2).value = "Kick Return TDs"
        wsStats.cell(row = KickReturnHeadingRow+1, 
                     column = KickoffLabelColumn+3).value = "Long"
              
#Punt Return Stats Labels
        wsStats.cell(row = PuntReturnHeadingRow, 
                 column = PuntReturnLabelColumn).value = "Punt Returns"
        wsStats.cell(row = PuntReturnHeadingRow+1, 
                 column = PuntReturnLabelColumn-1).value = "Punt Returner"
        wsStats.cell(row = PuntReturnHeadingRow+1, 
                 column = PuntReturnLabelColumn).value = "# of Punt Returns"
        wsStats.cell(row = PuntReturnHeadingRow+1, 
                 column = PuntReturnLabelColumn+1).value = "Punt Return Ave"
        wsStats.cell(row = PuntReturnHeadingRow+1, 
                 column = PuntReturnLabelColumn+2).value = "Punt Return TDs"
        wsStats.cell(row = PuntReturnHeadingRow+1, 
                 column = PuntReturnLabelColumn+3).value = "Long"
        
        HeadingRow = 1                   #Establish the locations where the tackle stats will go
        TacklerHeadingColumn = 1            
        NumberofTacklesHeadingColumn = 2
        SackerHeadingColumn = 4
        NumberofSacksHeadingColumn = 5
        
    #Write defensive stat column headings
        wsDStats.cell(row = HeadingRow, column = TacklerHeadingColumn).value = "Name"
        wsDStats.cell(row = HeadingRow, 
                 column = NumberofTacklesHeadingColumn).value = "Tackles"
        wsDStats.cell(row = HeadingRow, column = SackerHeadingColumn).value = "Name"
        wsDStats.cell(row = HeadingRow, 
                 column = NumberofSacksHeadingColumn).value = "Sacks"
        wsDStats.cell(row = TurnoverRow, column = InterceptionHeadingColumn).value = "Ints"
        wsDStats.cell(row = IntHeadingRow, 
                 column = InterceptionNameColumn).value = "Name"
        wsDStats.cell(row = IntHeadingRow, column = NumIntsColumn).value = "# of Ints"
        wsDStats.cell(row = IntHeadingRow, 
                 column = IntReturnYardageColumn).value = "Return Yardage"
        wsDStats.cell(row = IntHeadingRow, column = Pick6Column).value = "TDs"
        wsDStats.cell(row = TurnoverRow, 
                 column = FumbleRecoveryColumn).value = "Fumble Recoveries"
        wsDStats.cell(row = IntHeadingRow, 
                      column = FumbleRecoverColumn+4).value = "Name"
        wsDStats.cell(row = IntHeadingRow, 
                 column = FumbleRecoverColumn+5).value = "# of Fumbles"
        wsDStats.cell(row = IntHeadingRow, 
                 column = FumbleRecoverColumn+6).value = "Return Yardage"
        
#Fill cells with offensive stats.  Start with the rushing stats.  Go through the list of ball 
#carries and fill in the stats
        for i in range(0,len(BallCarrierList)):
            
#For each ball carrier, fill in the player's name, number of carries, rushing yards, average
#yards per carry (which needs to be computed), longest gain and number of TDs
            wsStats.cell(row = i+2, column = BallCarrierHeadingColumn).value = \
                    BallCarrierList[i]
            wsStats.cell(row = i+2, column = NumberofCarriesColumn).value = \
                    NumberofCarriesList[i]        
            wsStats.cell(row = i+2, column = RushingYardsColumn).value = YardageList[i]
            
#Divide the number of yards gained by the number of carries to 1 significant digit to 
#compute the average yards per carry
            wsStats.cell(row = i+2, column = YPCColumn).value = \
                    round(YardageList[i]/float(NumberofCarriesList[i]),1)
            wsStats.cell(row = i+2, 
                             column = RunLGCol).value = RunLongestGainList[i]        
            wsStats.cell(row = i+2, column = RBTDColumn).value = TDList[i]
                
#Receiving stats.  Figure out how many receivers caught balls and list their names, # of 
#receptions, receiving yards, calculate the yards per catch and write to the stats sheet,
#longest gain for each receiver, and # of receiving TDs
        for i in range(0,len(PassCatcherList)):
            wsStats.cell(row = i+2, 
                             column = ReceiverNameColumn).value = PassCatcherList[i]
            wsStats.cell(row = i+2, 
                             column = ReceptionsColumn).value = \
                    NumberofReceptionsList[i]        
            wsStats.cell(row = i+2, 
                             column = ReceivingYardsColumn).value = \
                    ReceivingYardageList[i]
            wsStats.cell(row = i+2, 
                             column = YPCatchColumn).value = \
             round(ReceivingYardageList[i]/float(NumberofReceptionsList[i]),1)
            wsStats.cell(row = i+2, 
                    column = RcvgLGCol).value = ReceivingLongestGainList[i]        
            wsStats.cell(row = i+2, 
                             column = RcvrTDColumn).value = ReceivingTDList[i]
                
                
        wsStats.cell(row = 2, column = QBNameColumn).value = QBName
        wsStats.cell(row = 2, column = PassAttemptColumn).value = PassAttempts       
        wsStats.cell(row = 2, column = CompletionsColumn).value = Completions
        wsStats.cell(row = 2, column = YardsColumn).value = PassingYards
        wsStats.cell(row = 2, column = QBLGCol).value = QBLG
        wsStats.cell(row = 2, column = IntColumn).value = Ints
        wsStats.cell(row = 2, column = PassTDColumn).value = PassTDs
        wsStats.cell(row = 3, column = QBNameColumn).value = BackupQBName
        wsStats.cell(row = 3, column = PassAttemptColumn).value = \
                BackupPassAttempts       
        wsStats.cell(row = 3, column = CompletionsColumn).value = \
                BackupCompletions
        wsStats.cell(row = 3, column = YardsColumn).value = BackupPassingYards
        wsStats.cell(row = 3, column = QBLGCol).value = BackupQBLG
        wsStats.cell(row = 3, column = IntColumn).value = BackupInts
        wsStats.cell(row = 3, column = PassTDColumn).value = BackupPassTDs
            
        NumPlays = PlayCount# - 3
        
        RushingYardsColumn = 3
        
#Fill stats sheet with kicker stats
        wsStats.cell(row = KickHeadingRow+2, 
                     column = KickoffLabelColumn-1).value = KickerName
        wsStats.cell(row = KickHeadingRow+2, 
                     column = KickoffLabelColumn+2).value = self.NumTBs
        wsStats.cell(row = KickHeadingRow+2, 
                     column = KickoffLabelColumn).value = self.NumKickoffs
        wsStats.cell(row = KickHeadingRow+2, 
                     column = KickoffLabelColumn+3).value = self.NumOOBKicks
        
        if self.NumKickoffs > 0:
            KickoffAve = (float(self.KickYards) / float(self.NumKickoffs))
        else:
            KickoffAve = 0
        wsStats.cell(row = KickHeadingRow+2, 
                     column = KickoffLabelColumn+1).value = KickoffAve
    
#Fill stats sheet with kick return stats
        wsStats.cell(row = KickReturnHeadingRow+2, 
                column = KickoffLabelColumn-1).value = self.KickReturnersName
        wsStats.cell(row = KickReturnHeadingRow+2, 
                    column = KickoffLabelColumn).value = self.NumKicksReturned
        if self.NumKicksReturned > 0:
            KickReturnAve = (float(self.KickReturnYardage) / \
                             float(self.NumKicksReturned))
                             
        else:
            KickReturnAve = 0
        wsStats.cell(row = KickReturnHeadingRow+2, 
                     column = KickoffLabelColumn+1).value = KickReturnAve
        wsStats.cell(row = KickReturnHeadingRow+2, 
                     column = KickoffLabelColumn+2).value = \
                     KickoffReturnForaTD
        wsStats.cell(row = KickReturnHeadingRow+2, 
                     column = KickoffLabelColumn+3).value = LongestKR
        
#Fill stats sheet with punter stats
        wsStats.cell(row = PuntHeadingRow+2, 
                     column = PuntLabelColumn-1).value = PunterName
        wsStats.cell(row = PuntHeadingRow+2, 
                     column = PuntLabelColumn).value = self.NumPunts
        if self.NumPunts > 0:
            PuntAve = (float(self.PuntLength) / float(self.NumPunts))
        else:
            PuntAve = 0
        wsStats.cell(row = PuntHeadingRow+2, 
                     column = PuntLabelColumn+1).value = PuntAve    
        wsStats.cell(row = PuntHeadingRow+2, 
                     column = PuntLabelColumn+2).value = self.LongestPunt
        
#Fill stats sheet with punt return stats
        wsStats.cell(row = PuntReturnHeadingRow+2, 
                column = PuntLabelColumn-1).value = self.PuntReturnersName
        wsStats.cell(row = PuntReturnHeadingRow+2, 
                    column = PuntLabelColumn).value = self.NumPuntsReturned
        if self.NumPuntsReturned > 0:
            PuntReturnAve = (float(self.PuntReturnYardage) / \
                             float(self.NumPuntsReturned))
                             
        else:
            PuntReturnAve = 0
        wsStats.cell(row = PuntReturnHeadingRow+2, 
                     column = PuntLabelColumn+1).value = PuntReturnAve
        wsStats.cell(row = PuntReturnHeadingRow+2, 
                     column = PuntLabelColumn+2).value = \
                     PuntReturnForaTD
        wsStats.cell(row = PuntReturnHeadingRow+2, 
                     column = PuntLabelColumn+3).value = LongestPR
        
#Fill stats sheet with field goal stats
        wsStats.cell(row = FGHeadingRow+2, 
                     column = FGLabelColumn-1).value = KickerName
        wsStats.cell(row = FGHeadingRow+2, 
                     column = FGLabelColumn).value = FGA
        wsStats.cell(row = FGHeadingRow+2, 
                     column = FGLabelColumn+1).value = NumFGsMade
        
#Fill stats sheet with extra point stats
        wsStats.cell(row = XPtHeadingRow+2, 
                     column = XPtLabelColumn-1).value = KickerName
        wsStats.cell(row = XPtHeadingRow+2, 
                     column = XPtLabelColumn).value = XPtA
        wsStats.cell(row = XPtHeadingRow+2, 
                     column = XPtLabelColumn+1).value = NumXPtsMade
        
#Compile defensive stats by counting the # of plays in which defensive tackles
#could occur and then use the tackle percentages of the defense to compute
#the # of tackles assigned to each player.  Use the PickAPlayer class to
#create the tackles array (Tackler, # of Tackles)
        Tackler = PickAPlayer.PickAPlayer(wsDefense,PlayCount,PassAttempts,
                                      Completions,NonTacklingPlays,SackCount)      
        Tackler.TackleStats()
        Sacker = PickAPlayer.PickAPlayer(wsDefense,PlayCount,PassAttempts,
                                      Completions,NonTacklingPlays,SackCount)      
        Sacker.SackStats()
        for i in range(0,len(Tackler.TacklerList)):
            wsDStats.cell(row = HeadingRow + i + 1, 
                     column = TacklerHeadingColumn).value = \
            Tackler.TacklerList[i]    
            wsDStats.cell(row = HeadingRow + i + 1, 
                     column = NumberofTacklesHeadingColumn).value = \
            Tackler.NumberofTacklesList[i] 
        for i in range(0,len(Sacker.SackerList)):           #Write sack stats to worksheet
            wsDStats.cell(row = HeadingRow + i + 1, 
                     column = SackerHeadingColumn).value = \
            Sacker.SackerList[i]  
            wsDStats.cell(row = HeadingRow + i + 1, 
                     column = NumberofSacksHeadingColumn).value = \
                     Sacker.NumberOfSacksList[i] 
        for i in range(0,len(InterceptionList)):                #Write int stats to worksheet
            wsDStats.cell(row = IntHeadingRow + i + 1, 
                          column = InterceptionNameColumn).value = \
                InterceptionList[i]
            wsDStats.cell(row = IntHeadingRow + i + 1, 
                          column = NumIntsColumn).value = NumberOfIntsList[i]
            wsDStats.cell(row = IntHeadingRow + i + 1, 
                          column = IntReturnYardageColumn).value = \
                NumberofIntYardsList[i] 
            wsDStats.cell(row = IntHeadingRow + i + 1, column = \
                          Pick6Column).value = NumberofPick6sList[i] 
        for i in range(0,len(FumbleRecoveryList)):                          #Write fumble recovery stats
            wsDStats.cell(row = IntHeadingRow + i + 1,                  
                          column = FumbleRecoverColumn+4).value = \
                FumbleRecoveryList[i]
            wsDStats.cell(row = IntHeadingRow + i + 1, 
                          column = FumbleRecoverColumn+5).value = \
                NumberOfRecoveriesList[i]
            wsDStats.cell(row = IntHeadingRow + i + 1, 
                          column = FumbleRecoverColumn+6).value = \
                RecoveryYardsList[i]
 

#Here is where we are going to write the final score into row 30, column 1
        wsStats.cell(row = FinalScoreRow, column = FinalScoreColumn).value = \
            "Final Score" 
        wsStats.cell(row = FinalScoreRow + 1, 
                     column = FinalScoreColumn).value = FinalScore 

        wbStats.save(StatsName)                 #Write the stats to the files
        wbDStats.save(DStatsName)
        self.NumKickoffs = 0        #Reset this so as not to contaminate the
        self.KickYards = 0          #results of the 2nd team to compile stats
        self.NumPunts = 0
        self.PuntLength = 0
        self.LongestPunt = 0
        self.NumTBs = self.NumOOBKicks = 0
        

#****************************************************************************
#Method:   CoP
#Purpose:  This method implements the Change of Possession (CoP) after a 
#          number of events but not after a penalty is accepted
# Inputs:  self.AcceptedPenaltyFlag - No CoP after an unsuccessful 4th don 
#                                     conversion and revert to the previous
#                                     4th down state
#          self.GM['TDFlag'] - CoP after a TD for now but will be after  
#                              the XPt or 2-Point Conversion, once implemented
#          self.Kicking[] - Not Yet Implemented but contains various flags 
#                           after some sort of kick is made

#          self.IntResult[5] - Int Flag that results in a CoP
#          self.FumbleResult[0] - Fumble flag that results in a CoP       
# Outputs: CoP
#          
# Author:           Rick Burney
#
# Created:          7/17/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def CoP(self):

#If there is no accepted penalty or a turnover after an offensive dead ball foul               
        if (self.AcceptedPenaltyFlag == 0) or (self.TurnoverAfterAnOffensiveDeadBallFoul == 1):
            
            TeamGivingUpTheBall = self.GM['Offense']
            self.GM['Offense'] = self.GM['Defense']
            self.GM['Defense'] = TeamGivingUpTheBall
            self.GM['Down'] = 1                                    #1st and 10
            self.GM['YTG'] = 10
            if self.GM['TDFlag'] == 1:
                self.GM['Down'] = 1                                #1st and 10
                self.GM['YTG'] = 10
                              
                self.GM['AdjustedYardLine'] = \
                    self.YardLineAdjust(self.GM['YardLine'])
            if self.GM['Touchback'] == 1:
                self.GM['YardLine'] = 80    
             
#Adjust the yardline
            if self.GM['YardLine'] > 50:                  
                self.GM['YardLine'] = self.GM['AdjustedYardLine']
                
            else:
                self.GM['AdjustedYardLine'] = self.GM['YardLine']
                self.GM['YardLine'] = 100 - self.GM['YardLine']
                
            if self.GM['OffenseFlag'] == 0:
                self.GM['OffenseFlag'] = 1
            else:
                self.GM['OffenseFlag'] = 0
            if (self.FumbleResult[0] == 1) or (self.IntResult[5] == 1):
                tkMessageBox.showinfo("Debug Message", str(self.GM['YardLine']))
                
#Else there is an accepted penalty.  The else appears to be a debug statement
        else:
            print("Accepted Penalty Flag is set")
            
        self.GM['CoPFlag'] = 0          #Reset the CoP flag
        self.OnOffenseIndication()    #Indicate which team has the ball 
        
                


#****************************************************************************
#Method:    DisplayManagement
#Purpose:  This method updates the play called, play result, score, timekeeping, down, yards to go, 
#                yardline and other indicators on the scoreboard.   The ResultDisplay method in  the 
#                Scoreboard Class is called
# Inputs:  self.GM['YardLine'] - Line of scrimmage after the play 
#              self.GM['Down'] - Down prior to the play
#              self.GM['YTG'] - Yards to Go prior to the play
#              self.GM['TimeLeftinQuarter'] - Time left in the quarter prior to the play
#              self.GM['Quarter'] - Quarter, prior to the play
#              self.GM['HomeTeamScore'] - Home Team score prior to the play
#              self.GM['VisitingTeamScore'] - Visiting Team score prior to the play
#              self.GM['TDFlag'] - Tells this routine to display the TD message
#              self.PenaltyList[5] - Tells this routine to check the accepted penalty flag
#          self.AcceptedPenaltyFlag - Tells this routine to use the penalty 
#                                     message
#          self.IntResult[5] - Int flag, tells this routine to use the Int msg
#          self.FumbleResult[0] - Fumble flag, use fumble message
# Outputs: Various outputs to the Scoreboard
#          
# Author:           Rick Burney
#
# Created:          7/12/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def DisplayManagement(self):
        
        DisplayMessage = Scoreboard()   #Declare a Scoreboard Class object

        if self.PenaltyList[5] == 0:                   #If there is no penalty
            if self.GM['SafetyFlag'] == 1:             #If a safety occurred
                
#Display message on the Scoreboard that a safety occurred
                DM = DisplayMessage.ResultDisplay(1,
                        self.DisplayMessages['SafetyMsg'],0,self.Parent)
        
#If no safety or fumble occurred and the play was a run
            elif (self.ResultList[0] == "Run") and \
                 (self.FumbleResult[0] == 0):

#If no touchdown was scored and a conversion on downs occurred, display a
#conversion on downs message
                if (self.GM['ConversionOnDowns'] == 1) and (self.GM['TDFlag'] \
                                                            == 0):
                    self.DisplayMessages['RunPlayExecutionMsg'] += \
                    " - Conversion on Downs" 
                    
#If a first down occurs but no TD display a first down message
                if (self.FirstDownFlag == 1) and (self.GM['TDFlag'] == 0):
                    self.DisplayMessages['RunPlayExecutionMsg'] += \
                        " - First Down"
                DM = DisplayMessage.ResultDisplay(1,
                                self.DisplayMessages['RunPlayExecutionMsg'],
                                                  0,self.Parent)

#If the play was a pass and there was no INT, fumble or safety
            elif (self.ResultList[0] == "Pass") and (self.IntResult[5] == 0) \
                 and (self.FumbleResult[0] == 0) and \
                 (self.GM['SafetyFlag'] == 0):
                
#If a conversion on downs occurred and there was no TD, then display a 
#conversion on downs message
                if (self.GM['ConversionOnDowns'] == 1) and (self.GM['TDFlag'] == 0):
                        self.DisplayMessages['PassPlayExecutionMsg'] += " - Conversion on Downs"  
                    
#If a first down occurs but no TD display a first down message
                if (self.FirstDownFlag == 1) and (self.GM['TDFlag'] == 0):
                    self.DisplayMessages['PassPlayExecutionMsg'] += " - First Down"

#Display result of the pass play                    
                DM = DisplayMessage.ResultDisplay(1,
                                                  self.DisplayMessages['PassPlayExecutionMsg'],0,self.Parent)
                
#If the pass was intercepted, display the result                                       
            elif self.IntResult[5] == 1:
                DM = DisplayMessage.ResultDisplay(1,
                                self.DisplayMessages['IntExecutionMsg'],
                                                   0,self.Parent)
            elif self.FumbleResult[0] == 1:
                DM = DisplayMessage.ResultDisplay(1,
                                self.DisplayMessages['FumbleExecutionMsg'],
                                                   0,self.Parent)
                
        else:
            if self.GM['UntimedDownFlag'] == 1:
                self.DisplayMessages['PenaltyMsg'] += \
                " - There will be an untimed down"
            DM = DisplayMessage.ResultDisplay(1,
                            self.DisplayMessages['PenaltyMsg'],0,self.Parent)
                
#If this is a kickoff, output "Kickoff" to the Play Type field and
#then output kickoff result result to the Play Result field
        if self.Kicking['KickFlag'] == 1:
            if self.Kicking['KickoffFlag'] == 1:
                DM = DisplayMessage.ResultDisplay(24,"Kickoff",0,self.Parent)
                DM = DisplayMessage.ResultDisplay(1,
                            self.DisplayMessages['KickoffDisplayMsg'],0,
                            self.Parent)
                self.Kicking['KickoffFlag'] = 0 #Then reset kickoff flag
                
#If this is an extra point, output "Extra Point" to the Play Type field and
#then output extra point result to the Play Result field
            if self.Kicking['XPtFlag'] == 1:
                DM = DisplayMessage.ResultDisplay(24,"Extra Point",0,
                                                  self.Parent)
                DM = DisplayMessage.ResultDisplay(1,
                            self.DisplayMessages['XPtDisplayMsg'],0,
                            self.Parent)

#If this is a field goal, output "Field Goal" to the Play Type field and
#then output field goal result to the Play Result field
            if self.Kicking['FGFlag'] == 1:
                DM = DisplayMessage.ResultDisplay(24,"Field Goal",0,
                                                  self.Parent)
                DM = DisplayMessage.ResultDisplay(1,
                            self.DisplayMessages['FGDisplayMsg'],0,
                            self.Parent)
                #self.Kicking['FGFlag'] = 0      #Reset field goal flag

#If this is an punt, output "Punt" to the Play Type field and
#then output punt result to the Play Result field
            if self.Kicking['PuntFlag'] == 1:
                
                DM = DisplayMessage.ResultDisplay(24,"Punt",0,
                                                  self.Parent)
                DM = DisplayMessage.ResultDisplay(1,
                            self.DisplayMessages['PuntDisplayMsg'],0,
                            self.Parent)
                #self.Kicking['PuntFlag'] = 0   #Commented out on 5/31/18 b/c
                                                #seems to be redundant (reset
                                                #in ControlPanel.Punt1)
                                                
            if self.Kicking['TwoPointConvFlag'] == 1:
                
                DM = DisplayMessage.ResultDisplay(24,
                                            "Two Point Conversion Attempt",0,
                                            self.Parent)
                DM = DisplayMessage.ResultDisplay(1,
                    self.DisplayMessages['TwoPointConversionDisplayMsg'],0,
                    self.Parent)
                self.Kicking['TwoPointConvFlag'] = 0
            
#Update the Scoreboard         
        if self.GM['TDFlag'] == 0:
            DM = DisplayMessage.ResultDisplay(5,self.GM['Down'],0,
                                          self.GrandParent)
            if (self.GM['YardLine'] + self.GM['YTG']) < 100:
                DM = DisplayMessage.ResultDisplay(6,self.GM['YTG'],0,
                                              self.GrandParent)
            else:
                DM = DisplayMessage.ResultDisplay(6,"Goal",0,
                                              self.GrandParent)
            
            DM = DisplayMessage.ResultDisplay(7,self.GM['AdjustedYardLine'],0,
                                          self.GrandParent)
        elif self.AcceptedPenaltyFlag == 0:
            DM = DisplayMessage.ResultDisplay(5,"",0,self.GrandParent)
            DM = DisplayMessage.ResultDisplay(6,"",0,self.GrandParent)            
            DM = DisplayMessage.ResultDisplay(7,"",0,self.GrandParent)
            
        DM = DisplayMessage.ResultDisplay(18,self.GM['HomeTeamScore'],0,
                                          self.GrandParent)
        DM = DisplayMessage.ResultDisplay(19,self.GM['VisitingTeamScore'],0,
                                          self.GrandParent)
        
        DM = DisplayMessage.ResultDisplay(3,
                        self.DisplayMessages['TimeLeftinQuarterDisplay'],0,
                        self.GrandParent)
        DM = DisplayMessage.ResultDisplay(4,self.GM['Quarter'],0,
                                          self.GrandParent)



#Reset Flags            
        
        self.GM['ConversionOnDowns'] = 0 
            

#****************************************************************************
#Method:    ExtraPoint
#Purpose: To execute the point after touchdown (PAT) 
# Inputs:  
# Outputs: 
# Author:           Rick Burney
#
# Created:          7/27/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def ExtraPoint(self):

        KickerNameCol = 2           #Where to find the name of the kicker
        
#Extract Kicker's Name            
        self.FXKickerName = self.GM['Offense'].cell(row=self.KickerRow,
                                        column = KickerNameCol).value

        if self.GM['TDFlag'] == 0: #No TD scored so attempts to press the Xtra 
                             #Point button will be ignored
    
            tkMessageBox.\
                showinfo("Error", "No TD Scored. Don't press this button")
            return None
      
#No extra point after the 2nd series in OT        
        if self.GM['OTCounter'] >= 3:   
            tkMessageBox.\
                showinfo("Error", 
                         "After the 2nd OT, teams must go for 2 after a TD")
            return None

#In the event that a TD is scored on the last play of the game, the user is 
#asked if an extra point kick is desired
        if (self.GM['Quarter'] == 5):
            result = tkMessageBox.askyesno("Python",
                                    "Would you like to kick the extra point?")
            if result == "no":
                return

#Constants
        FGYardsAdder = 17 #kick is from 7 yards back from the LOS and the 
                          #the goalposts are 10 yards into the endzone
        PATCol = 7
        
#Access stats
        PercXPTGood = self.GM['Offense'].cell(row=self.KickerRow,column = \
                                              PATCol).value
        XPtTest = random.randint(0,99)                      #Test to see 
                                                            #if kick is good
        self.Kicking['KickFlag'] = 1

        if XPtTest <= PercXPTGood:      #If kick is good
            self.XPtResult = 1          #Used for logging
            self.Kicking['XPtFlag'] = 1
            self.DisplayMessages['XPtDisplayMsg'] = "Extra Point is Good"      
            self.Score()

        else: 
            self.XPtResult = 0          #Used for logging            
            self.Kicking['XPtFlag'] = 1
            self.DisplayMessages['XPtDisplayMsg'] = "Extra Point is No Good" 
            
#Test to see if Extra Point is blocked
            self.BlockedKickResult = \
                ResultofthePlay.KickBlock(self.GM['Defense'],80,1) 
    
            if self.BlockedKickResult[0] == 1:
                Message = self.BlockedKickResult[1]
                self.GM['TDFlag'] = self.BlockedKickResult[3]
                
                if self.GM['TDFlag'] == 1:             #Blocked kick returned for TD 
                    self.Score()
                self.DisplayMessages['XPtDisplayMsg'] = Message 
                
        self.GM['TDFlag'] = 0   #Xtra pt concluded, reset TD flag         

        
#****************************************************************************
#Method:    FieldGoal
#Purpose:   This method kicks a field goal and determines the result  
# Author:           Rick Burney
#
# Created:          7/31/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def FieldGoal(self):
        
        if self.GM['TDFlag'] == 1: #You can't kick a field goal after a TD in place of an xtra pt    
            tkMessageBox.\
                showinfo("Error", "TD Scored. press the Extra Point or the Go For 2 button")
            return None
                
#Kicking stats are from www.footballdb.com/college-football/stats/index.html            
        FGYardsAdder = 17              #kick is from 7 yards back from the LOS and the goalposts
                                                     #are 10 yards into the endzone
        TentoNineteenCol = 8           #Relevant stats - Field goal stats are divided into ranges
        TwentytoTwentyNineCol = 9  #10-19 yards, 20-29 yards, 30-39 years, 40-49 yards
        ThirtytoThirtyNineCol = 10    #50-55 yards.  These yards are after the 17 yard adder is
        FortytoFortyNineCol = 11       #applied
        FiftytoFiftyFiveCol = 12          #"Col" refers to the worksheet column holding these stats
        PlayType = 4                          #PlayType is used by the log method (not yet a class)
        KickerNameCol = 2                #Where to find the name of the kicker
        
#Initialize                                    
        FGFlag = 0          #Flag to indicate if FG was good.  1 = Good
        PercFGGood = 1  #Initialization, will actually obtain average from the worksheet
        
        self.Kicking['KickFlag'] = 1 #If you are in this method, you are kicking a field goal  so   
        self.Kicking['FGFlag'] = 1    #set both of these flags

#Extract FG averages based upon the LOS.  Remember the 17 yard adder    
        if self.GM['YardLine'] >= 98:
            PercFGGood = self.GM['Offense'].cell(row=self.KickerRow,
                                                 column = TentoNineteenCol).value
        elif self.GM['YardLine'] >= 88:
            PercFGGood = self.GM['Offense'].cell(row=self.KickerRow,
                                        column = TwentytoTwentyNineCol).value
        elif self.GM['YardLine'] >= 78:
            PercFGGood = self.GM['Offense'].cell(row=self.KickerRow,
                                        column = ThirtytoThirtyNineCol).value
        elif self.GM['YardLine'] >= 68:
            PercFGGood = self.GM['Offense'].cell(row=self.KickerRow,
                                        column = FortytoFortyNineCol).value
        elif self.GM['YardLine'] >= 62:
            PercFGGood = self.GM['Offense'].cell(row=self.KickerRow,
                                        column = FiftytoFiftyFiveCol).value
            
#This next code prevents FGs from over 57 yards.  May want to change this to 60 yards
        elif self.GM['YardLine'] < 60:
            tkMessageBox.showinfo("Not Close Enough for a FG", "Push another button!")
            
            self.Kicking['KickFlag'] = 0 #Essentially negates the button push because the FG 
            self.Kicking['FGFlag'] = 0    #yardline is too far                             
            return                               #Too far for a FG, put up message saying so, then return
        else:                                      
            PercFGGood = 0  #Not sure if the else condition is ever met

#Extract Kicker's Name            
        self.FXKickerName = self.GM['Offense'].cell(row=self.KickerRow,
                                        column = KickerNameCol).value
        
        FGTest = random.randint(0,99)  #Random # from 0 thru 99 to see if FG is good
        
        if FGTest <= PercFGGood:                                                               #FG is good, display 
            
            self.DisplayMessages['FGDisplayMsg'] = " Field Goal is Good from " \
            + str(100-self.GM['YardLine'] + FGYardsAdder) + " yards by " + self.FXKickerName
            self.FGResult = 1
            self.GM['ConversionFlag'] = 1
            
            self.Score()            #Register the score
            self.GM['CoPFlag'] = 0  #No CoP until the kickoff
            
#Otherwise, the FG is no good.  Display this
        else:
            self.FGResult = 0
            
            self.DisplayMessages['FGDisplayMsg'] = "Field Goal by " + \
                self.FXKickerName + " is no good"


            
#Since the FG was NG, test to see if Field Goal is blocked
            self.BlockedKickResult = \
                            ResultofthePlay.KickBlock(self.GM['Defense'],
                                                      self.GM['YardLine'] - 7,
                                                      self.ForceBlockedKick) 
                
#If FG was blocked, display msg
            if self.BlockedKickResult[0] == 1: 
                self.GM['YardLine'] = self.BlockedKickResult[2]
                self.GM['AdjustedYardLine'] = \
                    self.YardLineAdjust(self.GM['YardLine'])     
                
                self.DisplayMessages['FGDisplayMsg'] = \
                    self.BlockedKickResult[1] # + " ball winds up on the " + \
                    #str(self.BlockedKickResult[2]) + " yardline"
                
#Unless blocked FG was returned for a TD, there is a COP.  The assignment to 
#the TDFlag is probably superfluous but leaving it in doesn't hurt anything
                self.GM['TDFlag'] = self.BlockedKickResult[3]
                self.GM['CoPFlag'] = 1 
                
#Test to see if bocked kick returned for TD               
                if self.BlockedKickResult[3] == 1:                    
                    self.GM['TDFlag'] = self.GM['DTDFlag'] = 1  #Set flags
                    self.GM['CoPFlag'] = 0                      #No CoP yet              
                    self.DisplayMessages['FGDisplayMsg'] = \
                        self.BlockedKickResult[1] + \
                        " returned for a Touchdown"     #Display message                    
                    self.Score()                        #Update score
                    
#FG was not blocked but was NG.  If ball was snapped from inside the D's 20
#yardline place the ball at the 20.  Otherwise, ball is placed from where the
#ball was snapped (verified this). 
            else: 
                if self.GM['YardLine'] > 80:                    
                    self.DisplayMessages['FGDisplayMsg'] += \
        " - Ball was snapped inside the 20, will be placed at the 20 yardline" 
                    
                    self.GM['YardLine'] = 80            
                    self.GM['AdjustedYardLine'] = 20    
                    self.GM['CoPFlag'] = 1              
                else:
                    self.GM['YardLine'] -= 0    #New Yardline is from where
                                                #the ball was snapped
                                                #change made 2/10/2018
                                                        
                    self.GM['AdjustedYardLine'] = \
                        self.YardLineAdjust(self.GM['YardLine'])     
                    self.GM['CoPFlag'] = 1                        
                                                                 
                    
            #self.GameManagement()
            if self.GM['CoPFlag'] == 1:
                
                self.CoP()



#****************************************************************************
#Method:   FumbleProcessing
#Purpose:  This method is called after a running play, a completed pass play
#          or a QB sack.  A fumble test is made based upon offensive and 
#          defensive team stats and if a fumble occurs, a flag is set, the 
#          return yardage is computed, the yardline is not adjusted and the 
#          player who recovered the fumble is identified
# Inputs:  self.GM['Offense'] - Who has the ball, prior to a fumble  
#          self.GM['Defense'] - Who is on defense, prior to a fumble
#          self.GM['YardLine'] - Not used by the Fumble Test method 
#          self.Dstats - defensive stats for fumble recovery
# Outputs: self.FumbleResult[0] - FumbleFlag = 0 if no fumble lost, 1 if 
#                                 fumble lost by offense
#          self.FumbleResult[1] - Fumble return yardage
#          self.FumbleResult[2] - Yardline - currently not used by Fumble meth
#          self.FumbleResult[3] - Name of the player that recovered the fumble          
# Author:           Rick Burney
# Created:          7/9/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def FumbleProcessing(self):

#See if a fumble occurred?        
        self.FumbleResult = ResultofthePlay.Fumble(self.GM['Offense'], self.GM['Defense'],
                                       self.GM['YardLine'],self.Dstats, self.GameOptions['ForcePlay']) 

        if self.FumbleResult[0] == 1:   #Lost fumble occurs
            
#Test to see if a penalty occurred on the play
            self.PenaltyList[0] = ""
            self.PenaltyList[1] = self.PenaltyList[2] = self.PenaltyList[3] = self.PenaltyList[4] =\
                self.PenaltyList[5] = self.PenaltyList[6] = 0 
         
        if self.GameOptions['QBTakesaKnee'] == 1:   #Not allowing fumbles when QBs take a 
            self.FumbleResult[0] == 0                         #knee
        if self.FumbleResult[0] == 1:                         #There was a fumble lost so register the
            OriginalLOS = self.GM['YardLine']              # original LOS
            
#Determine the yardline where the fumble was lost. 
            YardlineWhereFumbleOccurred = self.GM['YardLine'] + self.ResultList[3]  
            
#Adjust if yardline where ball is recovered is on defenses' side of the 50 yardline           
            AdjustedYardlineWhereFumbleOccurred = \
                    self.YardLineAdjust(YardlineWhereFumbleOccurred)

#Fumble lost in the endzone, declare a touchback
            if YardlineWhereFumbleOccurred > 99:
                self.DisplayMessages['FumbleExecutionMsg'] = \
                    "Fumble by " + GameManager.BallCarrier + \
                    " in the endzone, recovered by " + self.FumbleResult[3] \
                    + " resulting in a Touchback"
                self.GM['Touchback'] = 1                #Touchback and change of possession
                self.GM['Down'] = 1                         #After CoP, 1st and 10 
                self.GM['YTG'] = 10
                self.GM['YardLine'] = 80                #Ball goes to the 20 yard line
                self.GM['AdjustedYardLine'] = 20
                self.GM['CoPFlag'] = 1                       #CoP 
                self.GM['TDFlag'] = 0   #Not sure why but make sure the TD flag is reset
                
#Absolutely no idea why this line is here but it works so WTF
                AdjustedYardlineWhereFumbleOccurred = \
                        self.YardLineAdjust(YardlineWhereFumbleOccurred)

            else:                                      #Fumble but no touchback
                self.Score()                        #Was fumble returned for a TD?  
                if self.GM['TDFlag'] == 0:  # Determine what happened
                    
                    AdjustedYardlineWhereFumbleOccurred = \
                        self.YardLineAdjust(YardlineWhereFumbleOccurred)
                    self.GM['YardLine'] = YardlineWhereFumbleOccurred - \
                        self.FumbleResult[1]

                    self.DisplayMessages['FumbleExecutionMsg'] = \
                    "Fumble by " + GameManager.BallCarrier + " at the " + \
                    str(AdjustedYardlineWhereFumbleOccurred) + \
                    " yardline and recovered by " + self.FumbleResult[3] \
                    + " and returned " + str(self.FumbleResult[1]) + " yards"
                    self.GM['AdjustedYardLine'] = \
                        self.YardLineAdjust(self.GM['YardLine'])
                    
                    self.GM['CoPFlag'] = 1  #Ball changes possession except if 
                                                #returned for TD
                    
                else:
                    self.FumbleResult[1] = min(self.GM['YardLine'],
                                               abs(self.FumbleResult[1]))
                    self.DisplayMessages['FumbleExecutionMsg'] = \
                    "Fumble by " + GameManager.BallCarrier + \
                    " recovered by " + self.FumbleResult[3] \
                    + " and returned " + str(self.FumbleResult[1]) + \
                    " yards for a Touchdown!"
                    self.GM['YardLine'] = 0
                    self.GM['TurnoverTD'] = 1
            DebugMessage = "Original LOS = " + str(OriginalLOS) + '\n'
            DebugMessage += "Yards Gained = " + str(self.ResultList[3]) + '\n'
            DebugMessage += "YL Where Fumble Occurred = " + \
                str(YardlineWhereFumbleOccurred) + '\n'
            DebugMessage += "AYL Where Fumble Occurred = " + \
                str(AdjustedYardlineWhereFumbleOccurred) + '\n'
            DebugMessage += "Return Yards = " + \
                str(self.FumbleResult[1]) + '\n'
            DebugMessage += "YL after fumble return = " + \
                str(self.GM['YardLine']) + '\n'
            tkMessageBox.showinfo("Fumble Debug Message", DebugMessage)
 

#****************************************************************************
#Method:   GameManagement
#Purpose:  This method updates the down, yards to go, time left in the
#          quarter, quarter, and the score after the play has been completely
#          resolved (penalties, turnovers, scores and change of possession.
#          The yardline update is handled separately because the user needs
#          to know what happened on a play prior to deciding to accept a 
#          penalty.  Will need to introduce the concept of "old yardline," 
#          "old adjusted yardline," "old down," and "old yards to go" so that
#          the game management state prior to the play can be preserved 
#          (primary for accepting penalties but also, for timeouts)
# Author:           Rick Burney
# Created:          7/12/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def GameManagement(self):

        DeadBallFlag = 0                #Initialize dead ball penalty flag
        
#****************************************************************************************
#PRE-SNAP PENALTY PROCESSING
        if self.PenaltyList[1] == 1:  #Pre-snap Penalty   
           
#Assess penalty yardage.  The yardline was already updated in another routine.
#YES, THIS IS AWKWARD AND SHOULD BE FIXED.  If the penalty was on the offense
#self.ResultList is a negative number so need to add it to the yards to go.
#Consequently, the -= to negate the negative number
            self.GM['YTG'] -= self.ResultList[3] 
            if self.GM['YTG'] <= 0:                 #Does a presnap penalty on
                self.GM['Down'] = 1     #the defense result in a first down.
                self.FirstDownFlag = 1  #If so, reset the down to 1, set the 
                self.GM['YTG'] = 10     #1st down flag, and reset YTG to 10
#****************************************************************************************
                
#****************************************************************************************
#NORMAL GAME MANAGEMENT PROCESSING WHEN THERE IS NO ACCEPTED PENALTY
        elif self.AcceptedPenaltyFlag == 0:     #If no accepted penalty
            if self.Kicking['KickFlag'] == 0:   #Non-kicking play
                self.GM['Down'] += 1                    #Update down and YTG
                self.GM['YTG'] -= self.ResultList[3]
            else:                                       #Kicking play always
                self.GM['Down'] = 1 #results in a 1st and 10 but if XPt or FG
                self.GM['YTG'] = 10 #there is a kickoff that follows
            if self.GM['YTG'] <= 0:                 #First down, reset down
                self.GM['Down'] = 1
                self.FirstDownFlag = 1  #Set flag, set YTG to 10
                self.GM['YTG'] = 10

#NEED A TEST FOR A TD SO IF A TD IS SCORED ON A 4TH DOWN TRY, WE DON'T GET A
#CONVERSION ON DOWNS MESSAGE AND WE DON'T GET A CoP
            if self.GM['Down'] == 5: 
                if self.GM['TDFlag'] == 0:  #As long as a TD was not scored
                    self.GM['Down'] = 1    #Turnover on downs, call CoP method
                
                    self.GM['ConversionOnDowns'] = 1    #Conversion on downs
                    self.GM['CoPFlag'] = 1              #Change of possession
            self.PenaltyList[5] = 0         #Reset Penalty Flag                
 
#****************************************************************************************
#****************************************************************************************
#PROCESSING AFTER AN ACCEPTED PENALTY
        else:                               #Penalty accepted
#*****DEFENSIVE PASS INTERFERENCE*****            
#If DPI, figure out how to assess yardage.  If incomplete take the greater of
#the spot of the foul and 15 yards.  If completed, by virtue of the user 
#accepting the penalty, 15 yards will be assessed.  Compute length of pass.  
#YardsonthePlay is passed in so should be local
            if self.PenaltyList[0] == "Pass Interference on the Defense":
                if self.ResultList[2] == "Incomplete":  
                    if self.PassLength == "Short":              #Determine
                        YardsonthePlay = random.randint(0,10)   #placement    
                    elif self.PassLength == "Mid":              #spot of the          
                        YardsonthePlay = random.randint(10,20)  #foul
                    elif self.PassLength == "MidLong":
                        YardsonthePlay = random.randint(15,25)
                    else:
                        YardsonthePlay = random.randint(20,40)                        
                else:
                    YardsonthePlay = self.ResultList[3] #Otherwise, the pass
                                                        #was completed and the
                                                        #ball will be placed
                                                        #based upon the yards
                                                        #gained.
                                                        
                SpotWhereDPIOccurred = YardsonthePlay + self.GM['YardLine']
                if SpotWhereDPIOccurred > 99:
                    self.DPIOccurredInEndZone = 1 #Determine is DPI occurred 
                else:                             #in endzone
                    self.DPIOccurredInEndZone = 0
                                                        
#If yardage is > 15 yards or if the pass is intercepted (int will be negated)
#the penalty yardage will be 15 yards against the defense
                if (self.ResultList[2] == "Int") or (YardsonthePlay > 15):         
                    self.PenaltyList[4] = 15     
                else:                                       #which means 
                    self.PenaltyList[4] = YardsonthePlay    #decline penalty    
                 
#Half the difference to the goal line
            self.HalftheDifferenceTest()    

#*****DEAD BALL FOUL PENALTY*****            
            if self.PenaltyList[6] == 1:    #Dead ball foul.  Don't assess if a TD is scored or if on 
                                                        #4th down
                if self.GM['TDFlag'] == 0:
                    
#Penalty assessed at end of the play AND SHOULD BE AT THE END-OF-PLAY YARDLINE
                    self.GM['OldYardLine'] = self.GM['YardLine']
                    self.HalftheDifferenceTest()                    
                    if self.PenaltyList[4] < 0:                                             #On Offense
                        self.GM['YTG'] = self.GM['YTG'] - self.ResultList[3]  #1st down check
                        if self.GM['YTG'] <= 0:
                            self.GM['Down'] = 1 #1st down, remains 1st and 10
                            self.GM['YTG'] = 10
                        else:
                            self.GM['Down'] += 1                          #Otherwise, advance down                         
                            self.GM['YTG'] -= self.PenaltyList[4]   #Adjust YTG
                        
                    else:                               #On defense
                        self.GM['Down'] = 1 #1st and 10
                        self.GM['YTG'] = 10

#This else code should be removed and tested - appears to step on previous code                    
            else:                            
                self.GM['YTG'] -= self.PenaltyList[4]   #Apply Penalty Yardage
            
                if (self.GM['YTG'] <= 0) or (self.PenaltyList[2] == 1): #1st 
                    self.GM['Down'] = 1                                #down
                    self.FirstDownFlag = 1
                    self.GM['YTG'] = 10
            if self.PenaltyList[3] == 1:    #Loss of down
                self.GM['Down'] += 1   
                
#Adjust yardline based on the penalty yardage, update AYL
            self.GM['YardLine'] = self.GM['OldYardLine'] + self.PenaltyList[4]  
            
            self.GM['AdjustedYardLine'] = \
               self.YardLineAdjust(self.GM['YardLine'])
            if self.DPIOccurredInEndZone == 1:                   
                self.GM['YardLine'] = 97            #Ball placed at defense's
                self.GM['AdjustedYardLine'] = 3 #three yardline
#Reset turnover flags   
            if self.TurnoverAfterAnOffensiveDeadBallFoul == 0:
                self.FumbleResult[0] = self.IntResult[5] = \
                    self.GM['CoPFlag'] = 0 
            else:
                self.FumbleResult[0] = self.IntResult[5] = 0
                
#We are not allowing offensive dead ball fouls on turnovers.  No idea what
#happens during an defensive dead ball foul on turnovers but will have to deal
#with that at some point - includes facemask penalties
                self.PenaltyList[6] = 0                      
                                
#This allows reverting to the old score if a TD is scored but is negated by a
#penalty
            self.GM['HomeTeamScore'] = self.GM['OldHTS']
            self.GM['VisitingTeamScore'] = self.GM['OldVTS']
            
#Remember to reset the TD and conversion flags or TDs will happen on the 
#next play
            self.GM['TDFlag'] = self.GM['DTDFlag'] \
                = self.GM['ConversionFlag'] = 0 
            
#A constant reminder that dead ball fouls are automatic and there is no option
#to accept or decline
            if self.PenaltyList[6] == 0:
                self.DisplayMessages['PenaltyMsg'] = "Penalty accepted - " \
                + str(abs(self.PenaltyList[4])) + " yards assessed" 
            else:
                self.DisplayMessages['PenaltyMsg'] = "Dead ball foul - " \
                + str(self.ResultList[3]) + " yards gained on the play " + \
                str(abs(self.PenaltyList[4])) + \
                " yards assessed after the play, " + self.PenaltyList[0]
                        
 #Assign Time Codes
        if self.PenaltyList[5] == 0:                   #No penalty

            if self.GameOptions['SpiketheBall'] == 1:  #12 is the TimeCode for 
                self.GM['TimeCode'] = 12               #spiking the ball                
            elif self.ResultList[2] == "Incomplete":   #0 is the TimeCode for 
                self.GM['TimeCode'] = 0                #an incomplete pass 
                
#1 is the TimeCode for a TD but the TDFlag is kept set for the extra point to
#prevent inadvertant presses of the Extra Point button
            elif (self.GM['TDFlag']) == 1 and (self.Kicking['XPtFlag'] == 0):
                self.GM['TimeCode'] = 1
                
#Hurry up offense time codes but does not apply to field goals or extra points
            elif self.GameOptions['Hup'] == 1 and \
                 (self.Kicking['FGFlag'] == 0) and \
                 (self.Kicking['XPtFlag'] == 0):  
                self.GM['TimeCode'] = 6 
            elif self.FirstDownFlag == 1:    #9 is the TimeCode for a 1st down
                self.GM['TimeCode'] = 9
            elif self.GameOptions['QBTakesaKnee'] == 1:  #QB takes a knee
                self.GM['TimeCode'] = 18
            elif (self.GM['ConversionOnDowns'] == 1): #Unsuccessful 4th down 
                self.GM['TimeCode'] = 8               #attempt
            elif (self.TouchbackFlag == 1) or \
                 (self.OutofBoundsKickoffFlag == 1): #Touchback on a kick or
                self.GM['TimeCode'] = 13             #kick out of bounds
            elif (self.TouchbackFlag == 0) and \
                 (self.OutofBoundsKickoffFlag == 0) and \
                 (self.Kicking['KickoffFlag'] == 1):          #Normal kickoff
                self.GM['TimeCode'] = 8
            elif (self.Kicking['KickoffFlag'] == 0) and \
                 (self.Kicking['FGFlag'] == 1):             #Field Goal
                self.GM['TimeCode'] = 11
            elif (self.Kicking['XPtFlag'] == 1):     #Extra Point
                self.GM['TimeCode'] = 16             #No time elapses for Xpts
            elif (self.Kicking['PuntFlag'] == 1):     #Extra Point
                self.GM['TimeCode'] = 7             #Punt
            elif self.GM['CoPFlag'] == 1:   #Use kickoff time code for a CoP
                self.GM['TimeCode'] = 8
            else:
                self.GM['TimeCode'] = 15    #15 is the TimeCode for all else

#Presnap Penalty        
        if (self.PenaltyList[1] == 1) and (self.PenaltyList[5] == 1): 
            self.GM['TimeCode'] = 16   
                
#Regular penalty
        if (self.PenaltyList[1] == 0) and (self.PenaltyList[5] == 1): 
            self.GM['TimeCode'] = 17 
        if (self.PenaltyList[0] == "Delay of Game by the Offense") and \
           (self.GM['ClockRunning'] == 1):
            self.GM['TimeCode'] = 19
       
#Update time left in the quarter and the quarter, as long as it is not OT       
        if self.GM['OTFlag'] == 0:
            
            self.GM['OldTimeLeftInQuarter'] = self.GM['TimeLeftinQuarter']             
 
#Extract updated time list based upon the time code
            TimeList = ResultofthePlay.UpdateTime1(self.GM['TimeCode'],
                                                self.GM['TimeLeftinQuarter'],
                                                self.GM['Quarter'],
                                                self.GM['UntimedDownFlag'],
                                                self.PenaltyList,
                                                self.GM['TDFlag'])

#The time list consists of two elements.  The 1st element is the time left in
#the quarter, the 2nd element is the quarter
            self.GM['TimeLeftinQuarter'] = TimeList[0]  
            self.GM['Quarter'] = TimeList[1]

#----------------------------Debug Code---------------------------
            #if (self.GameOptions['ForcePlay'] == 1):    #Force time to end of
                #self.GM['TimeLeftinQuarter'] =  10      #2nd quarter
                #self.GM['Quarter'] = 2 
#----------------------------Debug Code---------------------------

        else:                                                    #OT
            self.GM['TimeLeftinQuarter'] = 900  #Reset clock to 15 minutes although there is no 
                                                                    #timekeeping in OT
            
#Extract timelist again.  If during regular time, this should not affect anything and the
#untimed down flag should not be changed.  If in OT, then TimeList is given an assignment 
#for the 1st play of OT
            TimeList = [900,0,0]            
        self.GM['UntimedDownFlag'] = TimeList[2]    #Note if there is to be an an untimed down

#This is the string that is displayed on the scoreboard for timekeeping
        MinutesLeftInQuarter = str(int(self.GM['TimeLeftinQuarter'] / 60))
        SecondsLeftInQuarter = str(int(self.GM['TimeLeftinQuarter'] % 60))
        
#Add a leading '0' to seconds if seconds are < 10
        if int(SecondsLeftInQuarter) < 10:
            SecondsLeftInQuarter = "0" + SecondsLeftInQuarter
            
#Display time left in the quarter on the scoreboard              
        self.DisplayMessages['TimeLeftinQuarterDisplay'] = \
            MinutesLeftInQuarter+":"+SecondsLeftInQuarter
         
#Test for end of game.  Need to include TDFlag here so if the last play of the game is a TD 
#and the score is tied, an untimed extra point will occur.
        if self.GM['OTFlag'] == 0:
            if (self.GM['Quarter'] == 5) and (self.GM['HomeTeamScore'] != \
                                          self.GM['VisitingTeamScore']):
                tkMessageBox.showinfo("Game Over.","Press OK to Quit") 
            
            elif self.GM['TDFlag'] == 0:   #Enter OT but only if a TD was not scored on the last 
                                                         #play of game

                if (self.GM['Quarter'] == 5) and (self.GM['HomeTeamScore'] == \
                                              self.GM['VisitingTeamScore']): 
                    self.GM['OTFlag'] = 1                                        #Now in OT
                    self.GM['OffenseFlag'] = random.randint(0,1)    #See who gets the ball first
                    if self.GM['OffenseFlag'] == 0:                
 
#Display OT instructions to the user.  NEED TO SERIOUSLY REVISIT THIS BECAUSE THERE ARE
#                                                         BUGS
                        Message = "In Overtime.  Press Call Play button to start the first series. " \
                            + self.TeamStats['homeTeamName'] + \
                    " will get the ball first.  On all subsequent possessions, start the possession by pressing the OT Button"
                        self.GM['Offense'] = self.TeamStats['homeTeam']
                        self.GM['Defense'] = self.TeamStats['visitingTeam']
                    else:
                        Message = "In Overtime.  Press Call Play button to start the first series. " \
                            + self.TeamStats['visitingTeamName'] + \
                    " will get the ball first.  On all subsequent possessions, start the possession by pressing the OT Button"
                        self.GM['Offense'] = self.TeamStats['visitingTeam']
                        self.GM['Defense'] = self.TeamStats['homeTeam']
                    tkMessageBox.showinfo("OverTime!!",Message)
                    
                    self.GM['YardLine'] = 75                #Ball starts from defense's 25 yardline                     
                    self.GM['AdjustedYardLine'] = 25    
                    self.TGraphics()                             #Update the graphics
                    self.GM['Down'] = 1                       #First and 10
                    self.GM['YTG'] = 10
                    self.OverTimeIndicator = str(self.GM['OTSeries'])   #Indicate that we are in OT
                    OverTime = Scoreboard()                                      #Open up an OT class object
                    OTSB = OverTime.WriteLabel(self.GrandParent,
                                               self.OverTimeIndicator,2,2,
                                               "white","black",24,6,9,0,"")                        
                    self.GM['Quarter'] = "OT"                               #Officially in OT
                    self.OnOffenseIndication()                              #Indicate who has the ball 1st

#Indicates on the Scoreboard if the time left in the 2nd or 4th quarter is less than 2 minutes
        if ((self.GM['Quarter'] == 2) or (self.GM['Quarter'] == 4)) and \
                   (self.GM['TimeLeftinQuarter'] <= 120):
            
#Open up a Scoreboard class object so that the "within 2 minutes" indicater can be 
#illuminated.  Red if within 2 minutes, black if not
            TMW = Scoreboard()                                                                 
            TMWIndicatorLabel = TMW.WriteLabel(self.GrandParent,"",1,1,
                                               "white","red",12,7,9,0,"W") 
        else:
            TMW = Scoreboard()
            TMWIndicatorLabel = TMW.WriteLabel(self.GrandParent,"",1,1,
                                               "white","black",12,7,9,0,"W")

#See if play that just executed ended with the clock running or stopped
        self.ClockRunning()   
  
            
#****************************************************************************
#Method:    GoForTwoPoints
#Purpose:  Executes the 2-point conversion  
# Inputs:  
# Outputs:  Result of the 2-point conversion
# Author:           Rick Burney
# Created:          8/5/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def GoForTwoPoints(self):
        
        Perc2PtConversionGood = 42  #Average for all FBS.  No idea where this came from
        
        TwoPtTest = random.randint(0,99)    #Test to see if conversion is good
        self.Kicking['KickFlag'] = 1                 #Not technically a kick but is an "after-TD" play
        self.Kicking['TwoPointConvFlag'] = 1  #This is a 2-point conversion attempt

#Display whether the 2-pont conversion was good or not and if good, update the score
        if TwoPtTest <= Perc2PtConversionGood:                  
            self.DisplayMessages['TwoPointConversionDisplayMsg'] = \
                "Two Point Conversion is Good"      
            self.Score()
        else:
            self.DisplayMessages['TwoPointConversionDisplayMsg'] = \
                "Two Point Conversion is No Good"      

#2 pt attempt concluded, reset TD flag.  Other flags will be reset once Play Class is 
#re-entered
            self.GM['TDFlag'] = 0    
            
               
#****************************************************************************
#Method:   HalftheDifferenceTest
#Purpose:  This method determines if, for a penalty, the yards assessed are reduced by 1/2 
#                the distance to the goalline
# Inputs:    Original line of scrimmage, normally assessed penalty yardage
# Outputs:  Adjusted penalty yardage
# Author:           Rick Burney
# Created:          8/10/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def HalftheDifferenceTest(self):

#Test to see if the original LOS + the penalty yardage times 2 will result in either the ball 
#being placed in the opponents endzone if a defensive penalty or in the offense's endzone if 
#an offensive penalty.  If so, the new LOS after the penalty yardage is assessed is 
#half-the-distance to the endzone.
        if self.GM['OldYardLine'] + (2*self.PenaltyList[4]) > 99:                   
            self.PenaltyList[4] = int(round((100 - self.GM['OldYardLine'])/2,0))                                   
        if self.GM['OldYardLine'] + (2*self.PenaltyList[4]) < 1:               
            self.PenaltyList[4] = -int(round(self.GM['OldYardLine']/2,0))


#****************************************************************************
#Method:   IntProcessing
#Purpose:  This method is called after a running play, an interception.  It 
#               calls ResultofthePlay.Int
# Inputs:  self.GM['Defense'] - Who is on defense, prior to the Int
#          GameManager.PassLength - Defines a pass as short, mid or long. 
#                                   ResultofthePlay.Int figures out where the
#                                   pass was intercepted
#          self.GM['YardLine'] - LOS prior to the interception
# Outputs: self.IntResult[0] - Indicates whether a Pick-6 or TB occurred 
#          self.IntResult[1] - The name of the player that made the int
#          self.IntResult[2] - Int return yardage
#          self.IntResult[3] - Yardline where the ball ended up
#          self.IntResult[4] - Where the ball was intercepted 
#          self.IntResult[5] - Int Flag
# Author:           Rick Burney
# Created:          7/13/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def IntProcessing(self):
        
        if self.GameOptions['ForcePlay'] == 1:  #Forces a condition during an int
            force = 1                          
        else:
            force = 0

#Int has occurred, determine where intercepted and if returned, to where
        self.IntResult = ResultofthePlay.Int(self.GM['Defense'],GameManager.PassLength,
                                        self.GM['YardLine'],force)      
        if self.IntResult[5] == 1:                                  #Set int flag and initialize penalty list
            self.PenaltyList[0] = ""
            self.PenaltyList[1] = self.PenaltyList[2] = self.PenaltyList[3] = self.PenaltyList[4] =\
                self.PenaltyList[5] = self.PenaltyList[6] = 0 

        OriginalLOS = self.GM['YardLine']                     #Retain original LOS in case of a penalty        
        YardlineWhereIntOccurred = self.IntResult[4]    #Yardline where the int occurred
        
#Test to see if Int resulted in a touchback and if so, display on the scoreboard
        if self.IntResult[4] > 99:                      
            self.DisplayMessages['IntExecutionMsg'] = \
                "Pass intercepted by " + self.IntResult[1] + \
                " in the endzone resulting in a Touchback"
            self.GM['Touchback'] = 1                                #Set TB flag
            self.GM['Down'] = 1                                        #Reset to 1st and 10, place ball on 
            self.GM['YTG'] = 10                                        #the 20 and set the Change of 
            self.GM['YardLine'] = 80                                 #Possession flag
            self.GM['AdjustedYardLine'] = 20
            self.GM['CoPFlag'] = 1 
            
#Not sure if this next line is needed for touchbacks but it is generally needed to accurately
#account for the yardline after the return (Yardlines go from 1-50, then back down to 1)
            AdjustedYardlineWhereIntOccurred = self.YardLineAdjust(YardlineWhereIntOccurred)
                           
        else:                                       #Not a touchback
            self.Score()                          #See if there was a Pick-6.  Either way, display the Int 
            if self.GM['TDFlag'] == 0:   #Msg
 
#Definitely need next statement because now we will calculate the new yardline after the
#Int return
                AdjustedYardlineWhereIntOccurred = \
                    self.YardLineAdjust(YardlineWhereIntOccurred)
                
#Determine the yardline to where the Int was returned using IntResult[2] and do adjustments
                self.GM['YardLine'] = YardlineWhereIntOccurred - self.IntResult[2]   
                self.DisplayMessages['IntExecutionMsg'] = "Pass intercepted by " + \
                    self.IntResult[1] + " at the " + str(AdjustedYardlineWhereIntOccurred) + \
                    " yardline and returned " + str(self.IntResult[2]) + " yards"

#Set new yardline and enter this into the Game Management data structure                
                self.GM['AdjustedYardLine'] = self.YardLineAdjust(self.GM['YardLine'])
                self.GM['CoPFlag'] = 1                       #Only CoP if not
                                                             #a Pick-6

            else:
                
                AdjustedYardlineWhereIntOccurred = \
                    self.YardLineAdjust(YardlineWhereIntOccurred)

                self.DisplayMessages['IntExecutionMsg'] = \
                    "Pass Intercepted by " + self.IntResult[1] + " at the " \
                    + str(AdjustedYardlineWhereIntOccurred) + \
                    " yardline and returned " + str(self.IntResult[2]) + \
                    " yards for a TD"
                self.GM['TurnoverTD'] = 1   
                self.GM['YardLine'] = self.GM['AdjustedYardLine'] = 0
                
        DebugMessage = "Original LOS = " + str(OriginalLOS) + '\n'
        DebugMessage += "Int Occurred at = " + str(YardlineWhereIntOccurred) \
            + '\n'
        DebugMessage += "AYL where Int Occurred = " + \
            str(AdjustedYardlineWhereIntOccurred) + '\n'
        DebugMessage += "Return Yardage = " + str(self.IntResult[2]) + '\n'
        DebugMessage += "New YardLine = " + str(self.GM['YardLine']) + '\n'
        DebugMessage += "New AYL = " + str(self.GM['AdjustedYardLine']) + '\n'
            
        tkMessageBox.showinfo("Int Debug Message", DebugMessage)
        





#****************************************************************************
#Method:    Kickoff
# Author:           Rick Burney
#
# Created:          7/20/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def Kickoff(self):
        DisplayMessage = Scoreboard()   #Create a Scoreboard Object                
        
        NumKickoffsRow = 36 #Kicker stat locations in the worksheet
        NumKickoffsCol = 3
        KickoffAveCol = 4
        TouchbacksCol = 5
        OutofBoundsKicksCol = 6         
        KickOffFactor = 15              #1-sigma for the length of the kickoff
        self.Kicking['KickFlag'] = 1    #Means that this is a kicking play        
        KickoffDepth = 65               #Default, will be set by this method
        
#Test for start of the 3rd quarter
        if (self.GM['Quarter'] == 3) and \
           (self.GM['TimeLeftinQuarter'] == 900):
            self.Kicking['Startofthe3rdQuarter'] = 1
            self.GM['HomeTimeouts'] = self.GM['VisitorTimeouts'] = 3
            DM = DisplayMessage.ResultDisplay(20,"3",0,self.GrandParent)
            DM = DisplayMessage.ResultDisplay(21,"3",0,self.GrandParent)
        else:
            self.Kicking['Startofthe3rdQuarter'] = 0
            


#Determine the yardline where the kick will be made.        
        if self.Kicking['FreeKick'] == 0:
            KickOffFromthe = 35 #Constant unless there is a penalty or a safety
        else:                   #Free kick which means a safety occurred
            KickOffFromthe = 20
            self.KickerRow = self.ThirdQtrKickerRow #Treat this as a turnover
        self.GM['AdjustedYardLine'] = KickOffFromthe
        
#Determine who kicks off to who.  If the kickoff follows a defensive
#touchdown, the a CoP must be performed.  Kickoff team is the offense, 
#receiving team is the defense with the OffenseFlag consistent with the 
#offense.  Prior to the return, a CoP is called and the offense and defense 
#flip with the offense flag remaining consistent with the offense
        if self.GM['DTDFlag'] == 1:
            
            self.CoP()
            self.GM['DTDFlag'] = 0
            self.GM['ConversionFlag'] = 0   #Part of debug to see if error
                                            #msg about pushing kickoff or 
                                            #extra point occurs
            
#It's complicated.  At the start of the game, the kickoff team is the offense,
#until after the kickoff when a CoP() occurs.  It follows that the receiving
#team is the defense at the start of the game.  This reverses at the start of
#the 3rd quarter.  Then, the team that received the kickoff at the start of 
#the game (defense) becomes the kickoff team for the start of the 3rd quarter.
#At the start of the 3rd quarter, the receiving team is the kickoff team from
#the start of the game.
        if self.Kicking['StartoftheGame'] == 1:                            #If this is the start of the game
            KickoffTeam = self.GM['Offense']                                           #Kickoff team is offense    
            self.Kicking['ThirdQuarterKickoffTeam'] = self.GM['Defense'] #Flip this for 3rd quarter
            self.Kicking['ThirdQuarterTeamReceivingtheKick'] = \
                self.GM['Offense']  
            if self.GM['OffenseFlag'] == 0:                     #Set the ThirdQuarterOffenseFlag
                self.GM['ThirdQuarterOffenseFlag'] = 1
            else:
                self.GM['ThirdQuarterOffenseFlag'] = 0
            self.Kicking['ThirdQuarterKickoffRow'] = \
                    self.ThirdQtrKickerRow            
        else:                                           
            KickoffTeam = self.GM['Offense']    #At all other times, the kickoff team is offense
    
        if self.Kicking['Startofthe3rdQuarter'] == 1:                       #On the 1st kickoff of the 3rd
            KickoffTeam = self.Kicking['ThirdQuarterKickoffTeam']   #qtr, set the kickoff team
            self.KickerRow = self.Kicking['ThirdQuarterKickoffRow'] #Determine where to get stats
            
            self.GM['HomeTimeouts'] = self.GM['VisitorTimeouts'] = 3    #Reset timeouts
            self.GM['Offense'] = \
                self.Kicking['ThirdQuarterKickoffTeam']                             #Set the offense flag
            self.GM['OffenseFlag'] = \
                self.GM['ThirdQuarterOffenseFlag']      #Set the 3rd qtr offense flag
            self.GM['Defense'] = \
                self.Kicking['ThirdQuarterTeamReceivingtheKick']    #Set the Defense flag
            
        if self.GM['TurnoverTD'] == 1:                      #Have KickerRow point to team that just  
            self.KickerRow = self.ThirdQtrKickerRow   #scored a turnover TD and then reset the 
            self.GM['TurnoverTD'] = 0                         #turnover flag 
            
#Fetch the kicker's stats and compute percentages.  Note that on 12/7/18, the
#ability to distinguish between separate people kicking off vs FG/XPts was
#made by choosing the name two columns to the left of the # of kickoffs column
#Will have to fix each of the worksheets.
        NumKickoffs = KickoffTeam.cell(row=self.KickerRow,
                                           column = NumKickoffsCol).value
        self.KickerName = KickoffTeam.cell(row=self.KickerRow,
                                           column = NumKickoffsCol-2).value
        KickoffAve = round(KickoffTeam.cell(row=self.KickerRow,
                                            column = KickoffAveCol).value,0)
        Touchbacks = KickoffTeam.cell(row=self.KickerRow,
                                          column = TouchbacksCol).value
        OutofBoundsKicks = KickoffTeam.cell(row=self.KickerRow,
                                        column = OutofBoundsKicksCol).value
        PercTB = int(round(100*Touchbacks/NumKickoffs,0))
        PercOB = int(round((100*float(OutofBoundsKicks))/NumKickoffs,0))
        
#Test to see if the kick results in a touchback
        FirstKickoffTest = random.randint(0,99)
        
        if (FirstKickoffTest <= PercTB) and (self.Kicking['SquibKick'] == 0) \
               and (self.Kicking['OnsideKick'] == 0) and \
               (self.Kicking['FreeKick'] == 0):
            self.DisplayMessages['KickoffDisplayMsg'] = "Touchback"
            self.TouchbackFlag = 1
            self.GM['AdjustedYardLine'] = 25
            self.GM['YardLine'] = 75     
            self.KickoffResult = 0
        
#Test to see if the kick goes out of bounds. Squib, onside and free kicks by
#definition do not go out of bounds.  Also, if touchback, this code is not
#tested
        elif (FirstKickoffTest <= (PercTB + PercOB)) and \
             (self.Kicking['SquibKick'] == 0) \
             and (self.Kicking['OnsideKick'] == 0) and \
             (self.Kicking['FreeKick'] == 0):
            self.DisplayMessages['KickoffDisplayMsg'] = \
                "Kick Went Out of Bounds"                   #Display message
            self.OutofBoundsKickoffFlag = 1                 #and set flag
            self.GM['AdjustedYardLine'] = 35    #Ball goes to the 35 
            self.GM['YardLine'] = 65  
            self.KickoffResult = 1
            
#This should never happen, a hold over from a previous version.  We have
#already tested to make sure that this was not a free kick.  Delete after
#12/2/2017
            if self.Kicking['FreeKick'] == 1:
                self.GM['AdjustedYardLine'] = self.GM['YardLine'] = 50
                
                self.KickoffResult = 5                  #Free kick                
                                       
#Otherwise, the kick will be returned.  Determine how deep is the kick
        else:
            if (self.Kicking['SquibKick'] == 0) and \
               (self.Kicking['OnsideKick'] == 0):
                KickoffDepth = \
                    random.randint(int(KickoffAve-KickoffAve/KickOffFactor),
                                    int(KickoffAve+KickoffAve/KickOffFactor))
            elif self.Kicking['OnsideKick'] == 1:
                KickoffDepth = random.randint(10,15)
                self.KickoffResult = 3                  #Onside kick                
            else:
                KickoffDepth = random.randint(20,50)    #Squib Kicks won't be 
                                                                #returned 
            self.GM['YardLine'] = KickOffFromthe + KickoffDepth
            
            self.GM['AdjustedYardLine'] = \
                            self.YardLineAdjust(self.GM['YardLine'])

            self.DisplayMessages['KickoffDisplayMsg'] = \
                "Kickoff to the " + str(self.GM['AdjustedYardLine']) + \
                " Yardline, "
            
#Pre-Rev 3, made a test to check what happens if the kick does not cross the 
# 50 yardline.  Don't think we have to do this but leave this comment here 
#just in case

#What is different in Rev 3 is that the onside kick recovery is done before 
#CoP if the kicking team recovers, there is no CoP so have to work that if 
#statement into the logic.  Also, set a flag for LogPlay()
        if self.Kicking['OnsideKick'] == 1:
            
            self.ResultList[3] = 0  #There is no return            
            OnsideKickRecoveryFlag=ResultofthePlay.WhoRecoverstheOnsideKick()
            self.WhoRecoveredtheOnsideKick = OnsideKickRecoveryFlag
            
            if OnsideKickRecoveryFlag == 0:
           
                self.DisplayMessages['KickoffDisplayMsg'] = \
                    "Onside Kick to the " + str(self.GM['AdjustedYardLine']) \
                    + " yardline.  Recovered by receiving team"
                self.CoP()    
            else:
                self.DisplayMessages['KickoffDisplayMsg'] = \
                    "Onside Kick to the " + str(self.GM['AdjustedYardLine']) \
                    + " yardline.  Recovered by kicking team"

        else:
            
            self.CoP()  #After the kick and before the return, if any, 
                        #there is a CoP
                     
        if self.Kicking['SquibKick'] == 1:  #Squib kick, no return
            self.ResultList[3] = 0   
            self.KickoffResult = 4                  #Squib kick                
            
            self.DisplayMessages['KickoffDisplayMsg'] = "Squib Kick to the " \
                + str(self.GM['AdjustedYardLine']) + " yardline.  No return"
        self.OnOffenseIndication()
        if (self.Kicking['SquibKick'] == 0) and \
           (self.Kicking['OnsideKick'] == 0) and (self.TouchbackFlag == 0) \
           and (self.OutofBoundsKickoffFlag == 0):
            self.KickReturn()
        self.KickLength = KickoffDepth    
        self.Kicking['StartoftheGame'] = 0 #Don't need this flag anymore        
            
            
            
#****************************************************************************
#Method:    KickReturn
#Purpose:  
# Inputs:  
# Outputs: 
# Author:           Rick Burney
#
# Created:          7/26/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def KickReturn(self):
        
#Determine length of kickoff return
        self.ResultList[3] = YardageTable.KickReturn(self.GM['Offense'])

#Apply the kickoff return yardage and update AYL
        self.Score()

        self.GM['YardLine'] += self.ResultList[3]
       
        self.GM['AdjustedYardLine'] = \
            self.YardLineAdjust(self.GM['YardLine'])
        
#Form kickoff return message for appending to the kickoff message
        Message = str(self.ResultList[3]) + "    " + str(self.GM['YardLine'])
        
#Test for a kickoff return for a TD
        if self.GM['TDFlag'] == 0:        
            self.DisplayMessages['KickoffDisplayMsg'] += " Returned " + \
                str(self.ResultList[3]) + " yards to the " + \
                str(self.GM['AdjustedYardLine']) + " Yardline by " + \
                YardageTable.KickReturner
        else:
            self.DisplayMessages['KickoffDisplayMsg'] += " Returned " + \
                str(self.ResultList[3]) + " yards for a Touchdown by " + \
                YardageTable.KickReturner


#****************************************************************************
#Method:    LogPlay
#Purpose:  
# Inputs:  
# Outputs: 
# Author:           Rick Burney
#
# Created:          8/5/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def LogPlay(self,HTMDA,VTMDA,HTDMDA,VTDMDA):
        
#Deal with the fact that fumbles, Int and turnovers on downs result in a CoP
#before the play is logged.  Need a way to assign the offensive result to the
#pre-CoP offense and the defensive result to the ppuntre-CoP defense
        
#Need a way to increment homeTeamPlayCount and visitingTeamPlayCount - use 
#self.TeamStats['PreCoPOffenseFlag']
        self.HTMDA = HTMDA    #Log Arrays in Memory that are appended on each 
        self.VTMDA = VTMDA    #play depending on who has the ball
        self.HTDMDA = HTDMDA  #Same for defensive logging 
        self.VTDMDA = VTDMDA  
        
        
#Only do the PreCoP "who is on offense check" if the play is not a kickoff 
#Necessary because for the 1st kickoff of the game, 
#PreCoPOffenseFlag is not yet defined.  PreCoPOffenseFlag is checked to update 
#the correct play count prior to a CoP.  Kickoffs will be handled as an else
#statement.  If this is not a kick of any kind, log non-kicking play
        if (self.Kicking['KickoffFlag'] == 0) and \
           (self.Kicking['PuntFlag'] == 0) and (self.Kicking['FGFlag'] == 0) \
           and (self.Kicking['XPtFlag'] == 0):                           
            if self.TeamStats['PreCoPOffenseFlag'] == 0:     
                self.GM['homeTeamPlayCount'] += 1           
            else:
                self.GM['visitingTeamPlayCount'] += 1 
                
            if self.ResultList[0] == "Run":   #Is the Play Type a run or pass
                PlayType = 0                            
            else:
                PlayType = 1
            if self.Kicking['KickoffFlag'] == 1:        #This code is stupid
                self.ResultList == "Kickoff"        #It is inside the not a 
                                              #kickoff loop -REMOVE ON 8/29/18

#Pick-6, don't log TD            
            if (self.GM['TDFlag'] == 1) and (self.IntResult[5] == 0):
                LogTDFlag = 1
            else:
                LogTDFlag = 0
            
#Build up a single row in the log
            RowData =  [self.ResultList[0]]         #Play type 
            RowData.append(GameManager.BallCarrier) #Ball carrier
            RowData.append(self.ResultList[2])      #Result of the pass
            RowData.append(self.ResultList[3])      #Yardage
            RowData.append(LogTDFlag)               #TD
            RowData.append(self.GM['Quarter'])              #Quarter
            RowData.append(self.GM['TimeLeftinQuarter'])    #Time left in qtr
            RowData.append(self.FumbleResult[0])            #Fumble flag 
            RowData.append(self.GameOptions['Blowout'])     #Is the blowout 
                                                            #flag set? 
                                                        
            if self.AcceptedPenaltyFlag == 0:                #If no accepted 
                if self.TeamStats['PreCoPOffenseFlag'] == 0: #penalty, see who 
                                                             #has the ball
                    self.HTMDA.append(RowData)               #Append row data 
                else:                                        #as appropriate                                           
                    self.VTMDA.append(RowData)               
                
#Add interception info to defensive memory data array.  Need a special case 
#for a turnover that results in a TD. If there was an interception create row 
#list with the 1st entry being the name of the player with the int
                if self.IntResult[5] == 1:       
                    DRowData = ["Int"]                  #ID D-log as an INT
                    DRowData.append(self.IntResult[1])  #Log name of player
                                                        #who made the INT

#Add return yardage to row. Add if this is a pick-6                                                
                    DRowData.append(self.IntResult[2])  
                    DRowData.append(self.GM['TDFlag'])  

#Depending on who has the ball.Append the int data to the D log as appropriate                
                    if self.TeamStats['PreCoPOffenseFlag'] == 0:  
                        self.VTDMDA.append(DRowData)                                                                                                              
                    else:                               
                        self.HTDMDA.append(DRowData)             
                
                if self.FumbleResult[0] == 1:       #Log fumble recovery stats
                    DRowData = ["Fumble Recovery"]  #ID log entry as a fumble
                                                    #recovery
#Append name of player who recovered the fumble                                               
                    DRowData.append(self.FumbleResult[3]) 

#Add rtn yardage to row
                    DRowData.append(self.FumbleResult[1])  
                    
#Depending on who has the ball. Append the fumble data to the D log as 
#appropriate
                    if self.TeamStats['PreCoPOffenseFlag'] == 0:  
                        self.VTDMDA.append(DRowData)                                                                                                        
                    else:                               
                        self.HTDMDA.append(DRowData)             
        else:                                           #Kickoff, punt, FG or                                           
            if self.GM['OffenseFlag'] == 0:             #Xpt but we are not                  
                self.GM['homeTeamPlayCount'] += 1       #considering it a play           
            else:                                        
                self.GM['visitingTeamPlayCount'] += 1
            
            if self.Kicking['KickoffFlag'] == 1:        #Type of kick is a 
                                                        #kickoff
                
#Build up a single row in the log
                RowData =  ["Kickoff"]  #Identifies this play as a kickoff 
            
#Add if kickoff is a touchback, onside kick, squib kick, out of bounds or a 
#returned kick
                RowData.append(self.KickerName)
                RowData.append(self.KickoffResult) #Log enumerated kick result
            
#Only log data for kickoffs that are returned.  This includes free kick
                if (self.KickoffResult == 2) or (self.KickoffResult == 5):
                    DRowData = ["KR"]              
                    DRowData.append(1)
                    DRowData.append(self.ResultList[3])
                    DRowData.append(YardageTable.KickReturner)
                    DRowData.append(self.GM['TDFlag'])
                    if self.GM['OffenseFlag'] == 1: 
                        self.HTDMDA.append(DRowData) 
                    else:                                                                                                            
                        self.VTDMDA.append(DRowData) 
                
                RowData.append(self.KickLength) #Log length of kick if 
                                                #returned
            
#Log which team recovered if there was an onside kick            
                RowData.append(self.WhoRecoveredtheOnsideKick)                                    
                RowData.append(self.GM['Quarter'])              #Quarter
                RowData.append(self.GM['TimeLeftinQuarter']) #Time left in qtr
            
                RowData.append(0)                   #Unused field for kickoffs
                RowData.append(0)                   #Unused field for kickoffs
            
                if self.GM['OffenseFlag'] == 1: #Add kickoff data to log  
                                            
                    self.HTMDA.append(RowData)    
                else:                                                                                                            
                    self.VTMDA.append(RowData)
            elif self.Kicking['PuntFlag'] == 1: #Type of kick is a punt

#Build up a single row in the log
                RowData = ["Punt"]
                RowData.append(self.PunterName)
                RowData.append(self.PuntResult) 
                RowData.append(self.PuntLength) 
                RowData.append(0)                                    
                RowData.append(self.GM['Quarter'])              #Quarter
                RowData.append(self.GM['TimeLeftinQuarter']) #Time left in qtr
            
                RowData.append(0)                   #Unused field for punts
                RowData.append(0)                   #Unused field for punts
                if self.ThisPuntisReturned == 1:    #Punt is returned, log rtn
                    DRowData = ["PR"]                               #ID as a punt return
                    DRowData.append(1)                            #Not sure why
                    DRowData.append(self.ResultList[3])     #Log return yardage
                    DRowData.append(self.GM['TDFlag'])
                    
#Log who returned the punt
                    DRowData.append(YardageTable.PuntReturner)
                    if self.GM['OffenseFlag'] == 1: 
                        self.HTDMDA.append(DRowData) 
                    else:                                                                                                            
                        self.VTDMDA.append(DRowData) 
                if self.GM['OffenseFlag'] == 1:  
                                            
                    self.HTMDA.append(RowData)    
                else:                                                                                                            
                    self.VTMDA.append(RowData)
            elif self.Kicking['FGFlag'] == 1:   #Type of kick is a field goal

#Build up a single row in the log for a field goal
                RowData = ["FG"]                 #IDs this row as a field goal
                RowData.append(self.FXKickerName) #Who kicked the field goal
                RowData.append(self.FGResult)   #Result of the field goal 
                RowData.append(0)               #Unused field for field goals 
                RowData.append(0)                   #Unused field                                    
                RowData.append(self.GM['Quarter'])              #Quarter
                RowData.append(self.GM['TimeLeftinQuarter']) #Time left in qtr
            
                RowData.append(0)                   #Unused field for FGs
                RowData.append(0)                   #Unused field for FGs
                
#Here is a weird one.  The OffenseFlag, which indicates if the home or 
#visiting has possession is flipped at different times depending if the FG was
#good or NG.  If NG, FieldGoal() toggles this flag so the CoP is already 
#occurred prior to logging the data.  If the field goal is good, CoP does not
#occur until after the ensuing kickoff.  So here is the truth table
#OffensiveFlag  Field Goal Result   HT or VT log
#       0               0                VT     0
#       0               1                HT     1
#       1               0                HT     1
#       1               1                VT     0
#Classic Exclusive-OR
                WhereLogged = self.GM['OffenseFlag'] ^ self.FGResult

                if WhereLogged:                 #Append to home team log                                              
                    self.HTMDA.append(RowData)    
                else:                           #Append to visiting team log                                                                                                           
                    self.VTMDA.append(RowData)
            elif self.Kicking['XPtFlag'] == 1:   #Type of kick is a field goal
                   
#Build up a single row in the log for extra points.  Need to fix auto row 
#location to correctly identify the kicker, then remove the comment for the
#kicker identification
                RowData = ["XPt"]
                RowData.append(self.FXKickerName) #Who kicked the extra point
                
                RowData.append(self.XPtResult)  #Log whether XPt is good or NG    
                RowData.append(0)               #Unused field for XPts 
                RowData.append(0)                   #Unused field for XPts                                    
                RowData.append(self.GM['Quarter'])              #Quarter
                RowData.append(self.GM['TimeLeftinQuarter']) #Time left in qtr
            
                RowData.append(0)                   #Unused field for XPts
                RowData.append(0)                   #Unused field for XPts
                if self.GM['OffenseFlag'] == 0:                                              
                    self.HTMDA.append(RowData)    
                else:                                                                                                            
                    self.VTMDA.append(RowData)
           
                    
                
#-------------------------------------------------------------------------------
# Function Name:    OnOffenseIndication
# Purpose:          Calls display routine that will illuminate the "On 
#                   Offense" indicator for either the home or visiting team as 
#                   indicated by self.GM['OffenseFlag']
# Inputs            self.GM['OffenseFlag']    0 - Home team, 1 - Visiting Team
# Author:           Rick Burney
# Created:          7/19/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
    def OnOffenseIndication(self):
        
        OOI = Scoreboard()              #Instantiate a Scoreboard() object
        if self.GM['OffenseFlag'] == 0:                             #If home
            Ds = OOI.ResultDisplay(25,"green",0,self.GrandParent)   #team has
            Ds = OOI.ResultDisplay(26,"black",0,self.GrandParent)   #the ball
        else:
            Ds = OOI.ResultDisplay(25,"black",0,self.GrandParent)
            Ds = OOI.ResultDisplay(26,"green",0,self.GrandParent)


#****************************************************************************
#Method:    OTManagement
#Purpose:   Game manager during OT.  
# Author:           Rick Burney
# Created:          8/10/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def OTManagement(self):

#If a full OT series has been played, increment the series count by 1       
        if (self.GM['OTPossession'] % 2) == 0:
            self.GM['OTSeries']  += 1
        self.OverTimeIndicator = str(self.GM['OTSeries'])   
        OverTime = Scoreboard()                              
        OTSB = OverTime.WriteLabel(self.GrandParent,
                                self.OverTimeIndicator,2,2,
                                               "white","black",24,6,9,0,"")

        self.GM['OTPossession'] += 1
        self.GM['YardLine'] = 75            #Ball starts from defense's 25 
        self.GM['AdjustedYardLine'] = 25    #yardline
        self.TGraphics()
        self.GM['Down'] = 1
        self.GM['YTG'] = 10
        if self.GM['OTPossession'] > 2:
            self.GM['OTPossession'] = 1


        if (self.GM['OTPossession'] + self.GM['OTSeries']) % 2 == 1:
            
            self.CoP()
            self.GM['YardLine'] = 75            #Ball starts from defense's 25 
            self.GM['AdjustedYardLine'] = 25    #yardline

        else:    
            #Not tied, game is over
            if self.GM['HomeTeamScore'] != self.GM['VisitingTeamScore']:                    
                tkMessageBox.showinfo("Game Over","Press Quit")

        self.OverTimeIndicator = str(self.GM['OTSeries'])
        OverTime = Scoreboard()
        
#Illuminate the OT indicator on the scoreboard to show that we are in OT
        OTSB = OverTime.WriteLabel(self.GrandParent,self.OverTimeIndicator,2,
                                   2,"white","black",24,6,9,0,"")
        
#The only reason for call DisplayManagement() in OT is so that we don't try 
#for an extra point after the 2nd OT series and if some presses the Xpt button
#an error message will be displayed and that is the function of 
#DisplayManagement()
        self.DisplayManagement()
        self.TGraphics()


#****************************************************************************
#Method:    PenaltyProcessing
#Purpose:  
# Inputs:  
# Outputs: 
# Author:           Rick Burney
#
# Created:          7/20/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def PenaltyProcessing(self):
        
        
        
        PlayResultMessage = ""
        PenaltyMessage = self.PenaltyList[0] +'\n'  #Start of the penalty msg
        
#Form a message detailing the play result so the user can know what happened
#before making a decision to accept or decline a penalty
        if (self.ResultList[0] == "Run") and (self.FumbleResult[0] == 0):
            PlayResultMessage = str(self.ResultList[3]) + " yd gain on the play"
            if self.GM['ConversionOnDowns'] == 1:
                PlayResultMessage += " - Conversion on Downs"  
            
        elif (self.ResultList[0] == "Pass") and (self.IntResult[5] == 0) and \
             (self.FumbleResult[0] == 0):
            

            PlayResultMessage = self.ResultList[2] + "," + \
                str(self.ResultList[3]) + " yd gain on the play"
            if self.GM['ConversionOnDowns'] == 1:
                PlayResultMessage += " - Conversion on Downs"  
            
        elif self.FumbleResult[0] == 1:
            PlayResultMessage = self.DisplayMessages['FumbleExecutionMsg']
            
        elif self.IntResult[5] == 1:
            PlayResultMessage = self.DisplayMessages['IntExecutionMsg']
            
        if self.GM['TDFlag'] == 1:
            PlayResultMessage += " - TD"
            
        PenaltyMessage += PlayResultMessage
        
#Need to prevent offensive dead ball fouls from negating a turnover.  Rather,
#we assess the penalty at the end of the play in favor of the defense.
        TurnoverFlag = self.FumbleResult[0] or self.IntResult[5]    #Turnover
                                                                    #occurred
                                                                    
#Detect that a turnover occurred and there was a penalty and it was on the 
#offense and it was a dead ball foul
        self.TurnoverAfterAnOffensiveDeadBallFoul = TurnoverFlag and \
            (self.PenaltyList[4] < 0) and (self.PenaltyList[5] == 1) and \
            (self.PenaltyList[6] == 1)
        
#If condition is true, allow the CoP and ignore the dead ball foul
        if self.TurnoverAfterAnOffensiveDeadBallFoul == 1:  
            self.GM['CoPFlag'] = 1                          
        
#For Dead Ball fouls, automatically accept the penalty, otherwise
#Use a message box to inform the user of what type of penalty occurred, was it
#on the offense or defense and the play result.  The user then can make an 
#informed decision to accept or decline the penalty.  If a dead ball foul
#occurs, the penalty is automatically accepted
        if self.PenaltyList[6] == 0:        #Not a dead ball foul
            DisplayMessage = Scoreboard()   #Blank Play Result from previous 
                                            #play on display.  
            
            DM = DisplayMessage.ResultDisplay(1,"",0,self.Parent)
            Accept = tkMessageBox.askyesno("Penalty. Do you wish to accept?",
                          PenaltyMessage)
        else:
            Accept = 1                  #Dead ball foul is accepted
        
        if Accept:
            
#if penalty is accepted, set a flag.  GameManagement will handle the replay of
#the down
            self.AcceptedPenaltyFlag = 1 
       

#****************************************************************************
#Method:   PlayCall
#Purpose:  This method calls a play by calling the GameManager.PlayCall 
#          function and displays the play that was called on the display
# Inputs:  Who has the ball
#          down 
#          Yards to Go 
#          Running Back's Start Index (on the teams stat worksheet)
#          Receiver's Start Index
#          RunCentric - Either the team has a run-oriented offense or the 
#                       conditions are such that the user favors running the
#                       ball
#          PassCentric - Either the team has a pass-oriented offense or the 
#                       conditions are such that the user favors passing the
#                       ball
#          Hup - The user has chosen to run a hurry-up offense
#          SpiketheBall - the user directs the QB to spike the ball to stop
#                         the clock
#          YardLine - self-explanatory, used by the play caller to choose a 
#                     play.  Ranges from 1-99, another function adjusts for 
#                     when the ball is in opposing territory
#          HailMary - the user elects to throw a Hail Mary pass
#          ForcePenalty - Used for diagnostic purposes only, forces a penalty
#                         to be called
#          Blowout - Can be set by either the home or visiting team but forces
#                    2nd and 3rd team players to be used by the team that is
#                    ahead
#          Parent - Parent frame for display of play call and result
# Outputs: A play call is chosen based upon the aforementioned inputs, display 
#           of the play that was called
# Author:           Rick Burney
#
# Created:          7/9/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def PlayCall(self):
        
        import GameManager  #This is where most of the work of calling a play
                            #is done.  Future revisions will convert this to
                            #a class
                           
#Call the play.  Pass to GameManager who is on offense, down, YTG, starting
#locations of RBs, QBs, Receivers, Run/Pass-Centric, Hurry Up offense, QB
#spikes the ball, Yardline (1-99), HailMary Pass, Force Penalty flag (debug)
#and if backup players are being used

        self.Play = GameManager.PlayCall(self.GM['Offense'],self.GM['Down'], 
                self.GM['YTG'],self.RBsRow,
                self.ReceiversRow,self.GameOptions['RunCentric'],
                self.GameOptions['PassCentric'],self.GameOptions['Hup'],
                self.GameOptions['SpiketheBall'],self.GM['YardLine'],
                self.GameOptions['HailMary'],self.GameOptions['ForcePenalty'],
                self.GameOptions['Blowout'])
        if self.Play.find("Sneak") != -1:       
            self.QBSneak = 1


        DisplayPlayCall = Scoreboard()              #Display the play called  
        DisplayStr = str(self.Play)                 #on the scoreboard
        if self.GameOptions['QBTakesaKnee'] == 1:   #Special rules for QBTaK 
            DisplayStr = "QB Takes a Knee"

#Display the play that is called using the standardized display methods in 
#the Scoreboard class
        DPC = DisplayPlayCall.ResultDisplay(24,DisplayStr,0,self.Parent)
        
        if GameManager.PlayType == "Run":   #If a pass, want to know the 
            self.PassLength = ""            #general length of the pass
        else:
            self.PassLength = GameManager.PassLength
        
        
        

#****************************************************************************
#Method:   PlayResult
#Purpose:  This method runs the play and returns one of a number of results.  
#          If the play is a run, the run is executed, the yardage is computed,
#          and either a fumble occurred or it did not.  If the play is a pass,
#          then either the pass is incomplete, completed, intercepted or a 
#          sack occurred.  If incomplete, proceed to penalty processing.  If
#          completed, the yardage is computed, a TD test is made and then a 
#          test for a fumble is made.  If the pass is intercepted, the return 
#          yardage is computed and a TD test (pick-6) is made.  Then a penalty 
#          test is made.  If a sack is registered, the sack yardage is 
#          computed and a fumble test is made.  If there is a lost fumble, the 
#          fumble return yardage is computed and a TD-test is made.
# Author:           Rick Burney
#
# Created:          7/9/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def PlayResult(self):
        

#Non-kicking play, extract D-stats.  Include conference factor.  So we are
#clear, HomeDStats is really the visitor stats that was assigned in 
#ControlPanel.StartGame.  This is where the cross-assignment takes place and
#it is an unfortunate holdover from Rev 1.  So, the HomeDStats are really the
#visitor Dstats and VisitorDStats are really the home Dstats.  Got that?
        self.Kicking['KickFlag'] = 0                                                       
        if self.GM['OffenseFlag'] == 0:                 
            self.Dstats = self.TeamStats['HomeDStats']
            
#Some stats use the conference factor as an adder/subtractor, other stats use
#it as a multiplier/dividor
            ConferenceFactorAdder = self.TeamStats['HTCF'] - \
                self.TeamStats['VTCF']
            ConferenceFactorMultiplier = float(self.TeamStats['HTCF'])/\
                float(self.TeamStats['VTCF'])
        else:
            self.Dstats = self.TeamStats['VisitorDStats']
            ConferenceFactorAdder = self.TeamStats['VTCF'] - \
                self.TeamStats['HTCF']            
            ConferenceFactorMultiplier = float(self.TeamStats['VTCF'])/\
            float(self.TeamStats['HTCF'])

#Run the play
        self.ResultList = ResultofthePlay.ResultofthePlay(self.GM['Offense'],
            GameManager.PlayType,self.PassLength,self.QBsRow,
            self.Dstats,GameManager.BallCarrierAve,
            self.GameOptions['SpiketheBall'],self.GameOptions['HailMary'],
            self.GM['YardLine'],ConferenceFactorAdder,
            ConferenceFactorMultiplier, self.GameOptions['Blowout'],
            self.GM['Defense'])
#****************FORCE PLAY DEBUG CODE - REMOVE WHEN DEBUGGED****************
        #if self.GameOptions['ForcePlay'] == 1:       
            #self.ResultList[3]= 40  
            #print(self.IntResult[5])
#****************FORCE PLAY DEBUG CODE - REMOVE WHEN DEBUGGED****************
           
        if self.QBSneak == 1:                              #Limit QB Sneak   
            self.ResultList[3] = min(self.ResultList[3],1) #yards to 1 yard max
            
       
        if self.ResultList[3] >= 0: #This becomes part of the display message
            GainLoss = "gain"
        else:
            GainLoss = "loss"
            
        if self.ResultList[0] == "Run":       #Run the play, test for a fumble
            self.FumbleProcessing()

            
            if self.FumbleResult[0] == 0:   #As long as there was no fumble
                self.SafetyTest("2081")           #Was there a safety?
                self.Score()                #Was there a TD scored?  
            if self.GM['TDFlag'] == 0:                   
                self.DisplayMessages['RunPlayExecutionMsg'] = \
                GameManager.BallCarrier + " " + str(self.ResultList[3]) + \
                " yard " + GainLoss
            else:
                self.DisplayMessages['RunPlayExecutionMsg'] = \
                GameManager.BallCarrier + " runs " + str(self.ResultList[3]) \
                + " yards for a touchdown! "
                
            
        else:                                       #Pass, figure out what
            if self.ResultList[2] == "Incomplete":  #happened on the pass
                self.ResultList[3] = 0
                self.DisplayMessages['PassPlayExecutionMsg'] = "Pass to " +\
                    GameManager.BallCarrier + " is incomplete"
            elif self.ResultList[2] == "Completed":
                self.FumbleProcessing()                     #See if there was 
                                              #a fumble after the completion
                if self.FumbleResult[0] == 0:  #As long as there was no fumble
                    #self.SafetyTest()                   #Was there a safety?
                    self.Score()                        #TD?
                if self.GM['TDFlag'] == 0:
                    self.DisplayMessages['PassPlayExecutionMsg'] = "Pass to "\
                     + GameManager.BallCarrier + " from " + \
                    ResultofthePlay.QBName + " is completed for a "+ \
                    GainLoss + " of " + str(self.ResultList[3]) + " yards"
                    
#TD Pass!
                else:
                    self.DisplayMessages['PassPlayExecutionMsg'] = "Pass to "\
                                         + GameManager.BallCarrier + " from "\
                                         + ResultofthePlay.QBName + \
                                         " is completed for a "+ \
                                         str(self.ResultList[3]) + \
                                         " yard Touchdown"                    
            elif self.ResultList[2] == "Int":
                self.DisplayMessages['PassPlayExecutionMsg'] = "Pass from " +\
                    ResultofthePlay.QBName + " is intercepted"                
                self.IntProcessing()                                                #Interception
            elif self.ResultList[2] == "Sack":                                #Sack.  Display sack message
                self.DisplayMessages['PassPlayExecutionMsg'] = \
                    ResultofthePlay.QBName + " is sacked for a loss of " + str(-self.ResultList[3]) \
                    + " yards"
                self.SafetyTest("2128")                   #Was there a safety?
                self.Score()                                     #Was there a TD scored?  
                if self.GM['SafetyFlag'] == 0:          #If no safety, was there a fumble on the sack
                    self.FumbleProcessing()              #Safeties and fumbles are mutually exclusive

#QB takes a knee, -1 yard. considered a run play, ball carrier is the QB              
        if self.GameOptions['QBTakesaKnee'] == 1:                
            self.DisplayMessages['RunPlayExecutionMsg'] = "QB Takes a Knee"    
            self.ResultList[0] = "Run"                                                                               
            self.ResultList[3] = -1 
            self.ResultList[2] = ""
            GameManager.BallCarrier = ResultofthePlay.QBName
            
 #We are declaring that there is no Joe Pisarcik programmed into a QB taking a knee.  Can't
 #fumble when taking a knee
            self.FumbleResult[0] = 0    


#****************************************************************************
#Method:   PreSnapPenaltyTest
#Purpose:  This method uses the penalties per game stats for each team and tests to see if a
#                penalty will occur on the subsequent play.  A 2nd test is conducted to see if the 
#                penalty, if it will occur, is a pre-snap penalty.  If a penalty occurs, a Penalty Flag 
#                will be set.  If the penalty is pre-snap, a message box is presented to the user, 
#                the penalty yardage is assessed, the scoreboard is updated and the         
#          method returns to user control for the next play.  If the penalty
#          is post-snap, the play execution will continue and by virtue of the
#          penalty flag, the user is given the option to accept or decline the
#          penalty based upon the result of the play
# Inputs:  
# Outputs:  
# Author:           Rick Burney
#
# Created:          7/9/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def PreSnapPenaltyTest(self):

#Test for a penalty and a pre-snap penalty.  Note: some penalties such as PI
#require the length of the pass, yards gained and pass result but the play has
#not yet been run.  Penalty will have to be revised to allow a re-entrant call
#into Penalty after the result of the play has been fully defined. 
        self.PenaltyList = \
            Penalty.Penalty(self.TeamStats['HomePenaltiesPerGame'],
                                    self.TeamStats['VisitorPenaltiesPerGame'],
                            self.GM['OffenseFlag'],GameManager.PlayType,0,"",
                            self.GameOptions['ForcePenalty'],
                            self.PassLength)                
        
        if (self.GM['Down'] == 4) and self.PenaltyList[6] == 1:
            self.PenaltyList[5] = 0
            self.PenaltyList[6] = 0
            
#Can't have a penalty when the QB takes a knee            
        if self.GameOptions['QBTakesaKnee'] == 1:
            self.PenaltyList[1] = self.PenaltyList[5] = 0   
        
        if self.PenaltyList[1] == 1:                    #Presnap penalty
            
                                                           
            #Half the difference to the goal line
            self.HalftheDifferenceTest()

            self.ResultList[3] = self.PenaltyList[4]    #Assess yardage
            self.UpdateYardLine()                       #Move the ball
            self.GameManagement()                       #Update YTG & time
            DisplayPreSnapPenalty = Scoreboard()  #Display the PreSnap Penalty  
            
            DPSP = DisplayPreSnapPenalty.ResultDisplay(24,self.PenaltyList[0],
                                                       0,self.Parent)
            DisplayMessage = Scoreboard()   #Blank Play Result from previous 
                                            #play on display
            
            DM = DisplayMessage.ResultDisplay(1,"",0,self.Parent)
        return self.PenaltyList


#****************************************************************************
#Method:            Punt
# Author:           Rick Burney
#
# Created:          8/3/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def Punt(self):
        
        self.Kicking['PuntFlag'] = 1 #Set punt flag
        self.Kicking['KickFlag'] = 1     #Set kick flag
        
        CoffinCornerCap = 45      #Max length that a placement punt can travel
        
        CoffinCornerPuntSigma = 12  #Placement punt length standard deviation
        CoffinCornerBackOff = 5     #Target, trying to place the ball around
                                    #the 5 yardline
        PunterAveColumn = 4
        PunterLongColumn = 5
        PunterFCPercColumn = 6
        PuntLengthVariance = 10 #Estimated punt average standard deviation, 
                                #regular punt average, not placement punt ave
        PuntNameColumn = 2                        
        YardageTable.FCFlag = 0 #Initialize flags
        ReturnFlag = 0          #Used to determine if PuntReturn is called

        self.PuntFCPerc = int(round(self.GM['Offense'].cell(row=self.PunterRow,
                                         column = PunterFCPercColumn).value,0))
#extract punt averages from the team file
        PuntAve = int(round(self.GM['Offense'].cell(row=self.PunterRow,
                                         column = PunterAveColumn).value,0))
        PuntLong = int(round(self.GM['Offense'].cell(row=self.PunterRow,
                                         column = PunterLongColumn).value,0))
        
#this is somewhat of a misnomer.  ~10% of all punts are shanks and this sets
#the upper bound on a shank punt.  The minimum shank punt is something like
#15 yards
        Punter = self.GM['Offense'].cell(row=self.PunterRow,
                                         column = PuntNameColumn).value
        self.PunterName = Punter
        PuntLengthUpperMin = max(PuntAve - PuntLengthVariance , 20)
        
#Test for blocked punt.  The last argument is a forced block punt which for
#now will be set to zero but if we need it, we will create an FBP variable
#that we can use to force a block.
#BlockedPuntResult[0] = Punt block flag, 0 if no block, 1 if block
#BlockedPuntResult[1] = Punt block Message
#BlockedPuntResult[2] = YardLine where ball ends up
#BlockedPuntResult[3] = TD flag, 0 blocked punt not returned for a TD
#BlockedPuntResult[4] = AYL of where the ball ends up
#Test to see if a punt is block and construct the result list as defined
#above
        BlockedPuntResult = ResultofthePlay.PuntBlock(self.GM['Defense'],
                                                  self.GM['YardLine'],0)
        
        if BlockedPuntResult[0] == 1:
            self.PuntLength = 0
            self.PuntResult = "Blocked Punt"
            self.GM['YardLine'] = 5         #Absolutely no idea what this is
            if BlockedPuntResult[3] == 1:   #Punt block returned for a TD
                self.GM['CoPFlag'] = 0                   
                
                self.DisplayMessages['PuntDisplayMsg'] = BlockedPuntResult[1]
                    
                self.BlockedKickResult[3] = self.BlockedKickResult[0] = \
                    self.GM['TDFlag'] = self.GM['DTDFlag'] = 1
                self.Score()
            else:
                self.GM['CoPFlag'] = 1  
                self.GM['YardLine'] = BlockedPuntResult[2]
                self.GM['AdjustedYardLine'] = BlockedPuntResult[4]
                self.DisplayMessages['PuntDisplayMsg'] = BlockedPuntResult[1]\
                    + " returned to the " + \
                    str(BlockedPuntResult[4]) + " yardline"
                
        else:   #No block
            
            if self.Kicking['PlacementPunt'] == 0:           #Normal punt
                self.PuntResult = "Punt"
                
#The logic here is that 10# of punts are shanks, 80% are normal within a 
#gaussian distribution and 10% are boomers
                ReturnFlag = 1
                PuntLengthTest = random.randint(1,10)   
                if PuntLengthTest == 1:                                 
                    PuntLength = random.randint(15,PuntLengthUpperMin)
                elif PuntLengthTest <= 9:
                    PuntLength = int(round(numpy.random.normal(PuntAve,5),0))
                    
                else:
                    PuntLength = random.randint(PuntAve + PuntLengthVariance,
                                            PuntLong + PuntLengthVariance)
                    
            else:   #Placement punt that is capped
                self.PuntResult = "Placement Punt"                
                PuntSigma = random.randint(-CoffinCornerPuntSigma-\
                                           CoffinCornerBackOff,
                                           CoffinCornerPuntSigma)
                
#The idea is that the coffin corner punt lands near the endzone +/- some sigma
#but is capped to a max number so you are not doing placement punts from your
#own 5 yardline
#                PuntLength = min(100 - self.GM['YardLine'] + \
 #                                PuntSigma,CoffinCornerCap)
                PuntLength = random.randint(30,55)
                
#Seeing lots of punts wind up at the 4 yardline due to the CoffinCornerCap.
#Overriding the above code and will try out the code just above.  The idea is 
#that a placement punt will be made from th 50 yardline at its farthest and 
#will travel between 30 and 55 yards.  Will take some stats.
                
                ReturnFlag = 0
            self.PuntLength = PuntLength
            self.GM['YardLine'] += PuntLength

          

            self.GM['AdjustedYardLine'] = \
                self.YardLineAdjust(self.GM['YardLine'])        
            self.DisplayMessages['PuntDisplayMsg'] = "Punt by " + Punter + \
                " travels " + str(PuntLength) + " yards to the " + \
                str(self.GM['AdjustedYardLine']) + " yardline"
            if PuntLength < 30:
                ReturnFlag = 0
                self.DisplayMessages['PuntDisplayMsg'] += " No Return"
                self.GM['TimeCode'] = 11               
            elif (self.GM['YardLine'] >= 95) and (self.GM['YardLine'] <= 99):
                ReturnFlag = 0
                self.DisplayMessages['PuntDisplayMsg'] += " No Return"
                self.GM['TimeCode'] = 11               
                
            elif self.GM['YardLine'] > 99:
                PuntLength -= (self.GM['YardLine'] - 100)   #Calculate the 
                                                            #distance to the
                                                            #endzone
                self.PuntLength = PuntLength    #Adjust length if touchback
                self.GM['YardLine'] = 80
                self.DisplayMessages['PuntDisplayMsg'] = "Punt by " + Punter \
                    + " travels " + str(PuntLength) + \
                    " yards into the endzone for a touchback"  
                
            
                self.GM['AdjustedYardLine'] = \
                    self.YardLineAdjust(self.GM['YardLine'])
                ReturnFlag = 0
                self.GM['TimeCode'] = 11               
            self.GM['CoPFlag'] = 1
        if self.GM['CoPFlag'] == 1: #Change of Poseession after a punt with            
            self.CoP()              #no return         
        if ReturnFlag == 1:     #But if there is a return, call the PuntReturn
            self.PuntReturn()   #method
                

#****************************************************************************
#Method:    PuntReturn
#Purpose:   Determine the result of a punt return  
# Inputs:  
# Outputs: 
# Author:           Rick Burney
#
# Created:          8/5/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def PuntReturn(self):
        
        self.ThisPuntisReturned = 1 #If you are in this method, the punt is 
                                    #returned unless it isn't

        Force = 0   #This is from an earlier revision.  The routine
                    #YardageTable.PuntReturn calculates the yardage on a punt
                    #return and Force is used to influence a particular result
                    #YardageTable will ultimately be converted to a class
                    #in a future revision

#Call YardageTable.PuntReturn to determine result of the punt return.  Punt
#return results are returned in a list.  If this is a placement punt, don't
#have a return
        PuntReturnList=YardageTable.PuntReturn(self.GM['Offense'],Force,
                                               self.PuntFCPerc)

#Punt return yardage is assigned to the standard result list
        self.ResultList[3] = PuntReturnList[0] 
        if YardageTable.FCFlag == 1:            #See if there was a fair catch
            
#If so, create a fair catch message for display and set the timecode that is
#appropriate for fair catches
            self.ThisPuntisReturned = 0
            FairCatchMessage = "Fair Catch"                         
            self.DisplayMessages['PuntDisplayMsg'] += ", Fair Catch by "+ \
                PuntReturnList[1]
            self.GM['TimeCode'] = 11                   
            self.ThisPuntisReturned = 0 #Won't be logged as a return
        elif self.GM['YardLine'] <= 5:
            self.ThisPuntisReturned = 0
            
            self.DisplayMessages['PuntDisplayMsg'] += " No Return"
            self.GM['TimeCode'] = 11  
            self.ThisPuntisReturned = 0 #Won't be logged as a return            
        else:
            self.Score()
            
            self.GM['TimeCode'] = 7 
            self.GM['YardLine'] += self.ResultList[3]
            
            
            
            self.GM['AdjustedYardLine'] = \
                self.YardLineAdjust(self.GM['YardLine'])
            
#Test for a punt return for a TD
            if self.GM['TDFlag'] == 0:        
                self.DisplayMessages['PuntDisplayMsg'] += ", returned " + \
                    str(self.ResultList[3]) + " yards by  " + \
                    PuntReturnList[1]
            else:
                self.DisplayMessages['PuntDisplayMsg'] += " Returned " + \
                            str(self.ResultList[3]) + \
                            " yards for a Touchdown by " + PuntReturnList[1]
            #self.PuntReturnersName = PuntReturnList[1]
            


#****************************************************************************
#Method:    SafetyTest
#Purpose:   This method tests to see if a safety has occurred and sets a 
#           flag and a display message.
# Author:           Rick Burney
#
# Created:          8/2/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def SafetyTest(self,CallingLine):

        TempYardLine = self.GM['YardLine'] + self.ResultList[3]        
        if TempYardLine <= 0:   #Safety
            
            self.GM['SafetyFlag'] = 1
            if self.ResultList[2] == "Sack":
                GameManager.BallCarrier = ResultofthePlay.QBName
            self.DisplayMessages['SafetyMsg'] = "Safety!, " + \
                GameManager.BallCarrier + " tackled in the endzone"






#****************************************************************************
#Method:   Score
#Purpose:  This method updates the score based upon the play.  The outputs
#          will either be a TD (6 points), a Field Goal (3 points), a safety
#          (2 points), 2 point conversion (2 points) or an extra point 
#          (1 point).  The data structure that holds the score will be 
#          updated.  The Display routine will update the scoreboard
# Inputs:  GameManager.PlayType - Either Run or Pass 
#          ResultList[2] is, if a pass, the result of a pass (sack, complete, 
#                        incomplete or int
#          IntResult[5] - Int Flag - See IntResult[0]
#          IntResult[0] - "Pick6", "Touchback" on an Int, or ""
#          self.GM['YardLine'] - Depend on the result 
#          self.ResultList[3] - Yards gained on the play   
#          self.FumbleResult[0] - if 1, then play resulted in a fumble
#          self.Kicking- Not yet implemented but play was a kickoff
#          self.PuntResult - Not yet implemented but play was a punt
#          self.KickBlockFlag - Not yet implemented - may be part of Kicking
#          FG - Not yet implemented but play was a FG, part of Kicking struct
#          XPt - Not yet implemented but part of Kicking struct
#          TwoPtConversionFlag - Not yet implemented
#          self.GM['Offense'] - Who has the ball and will affect who scores 
#          self.GM['Defense'] - Who is on defense and will affect who scores
# Outputs: self.GM['HomeTeamScore']
#          self.GM['VisitingTeamScore']

# Author:           Rick Burney
#
# Created:          7/12/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def Score(self):

        Points = 0  #Initialize

        
        if self.Kicking['KickFlag'] == 0:  #Non-kicking play
            
#No int or fumble on the play
            if (self.FumbleResult[0] == 0) and (self.IntResult[5] == 0):
                TempYardLine = self.GM['YardLine'] + self.ResultList[3]
                
                if TempYardLine > 99:       #TD
                    self.GM['TDFlag'] = 1   #Set flags and points
                    Points = 6
                    self.ScoreFlag = 1
                    self.GM['DTDFlag'] = 0  #Not a defensive TD because there
                                            #there was no fumble or int
                                            
                    self.ActualTDYardage = self.ResultList[3]  #For TG Display
                    self.TDYardage = 100 - self.GM['YardLine'] #want actual  
                    self.ResultList[3] = self.TDYardage        #yardage of TD
                    
                if self.GM['SafetyFlag'] == 1:  #Safety
                    self.GM['DTDFlag'] = 1      #Set flags and points.  This 
                    Points = 2                  #is a defensive score
                    self.ScoreFlag = 1                    
            elif self.FumbleResult[0] == 1: #Fumble return 
                
#Determine to where the fumble recovery is returned 
                FumbleReturnYL = self.GM['YardLine'] + self.ResultList[3] - \
                    self.FumbleResult[1]
                if FumbleReturnYL <= 0:     #If this condition is true it is a
                    self.GM['TDFlag'] = 1   #fumble return for a TD.  Set 
                    self.GM['DTDFlag'] = 1  #flags and points and this is a 
                    Points = 6              #defensive score.  Compute actual
                    self.ScoreFlag = 1      #yardage of return for TD
                    
                    self.FumbleResult[1] = FumbleReturnYL
            elif self.IntResult[5] == 1: #Int return 
                
#Determine to where the interception is returned 
                IntReturnYL = self.IntResult[4] - self.IntResult[2]
                
                if IntReturnYL <= 0:        #If this condition is true it is a
                    self.GM['TDFlag'] = 1
                    self.GM['DTDFlag'] = 1
                    Points = 6
                    self.ScoreFlag = 1

                    self.IntResult[2] = self.IntResult[4]
      
#Kicking Play                    
        else:

            if self.Kicking['XPtFlag'] == 1:    #Extra Point                
                Points = 1
                self.ScoreFlag = 1
            if self.Kicking['TwoPointConvFlag'] == 1:    #Extra Point                
                Points = 2
                self.ScoreFlag = 1
            if self.Kicking['FGFlag'] == 1: #Field Goal
                Points = 3
                self.ScoreFlag = 1
                self.GM['DTDFlag'] = 0

#Blocked kick returned for a score               
            if (self.BlockedKickResult[0] == 1) and \
               (self.BlockedKickResult[3] == 1): 
                if self.GM['TDFlag'] == 1:
                    if self.Kicking['XPtFlag'] == 1:    #Block occurred on an 
                        Points = 2                      #extra Point try
                    else:           #Blocked field goal or punt, returned for
                        Points = 6      #a TD
                    self.ScoreFlag = 1      #Either way, a score occurred
                    self.GM['DTDFlag'] = 1  #Score is attributed to the D
                
#Score on a kickoff return.  First have to test for a kickoff.  Then determine
#where the return ended.  If the yardline where the return ended is > 99, then
#we know that it was a kickoff returned for a TD
            if self.Kicking['KickoffFlag'] == 1:
                TempYardLine = self.GM['YardLine'] + self.ResultList[3]
                if TempYardLine > 99:
                    self.GM['TDFlag'] = 1   #Kickoff returned for a TD.  Set
                    Points = 6              #the TD and Score flag, points = 6
                    self.ScoreFlag = 1
                    
#The reason we used a TempYardLine was that we need to compute the statistical
#length of the kickoff return, not what the random value of the return which
#could be greater than the statistical value.  e.g., a kickoff fielded at the
#7 yardline and a random return value of 99 yards results in a TempYardLine of
#106, which records as a kickoff return for a TD but the actual return yards
#would be recorded as 93.
                    self.TDYardage = 100 - self.GM['YardLine']
                    self.ResultList[3] = self.TDYardage
                    self.GM['DTDFlag'] = 0                  #Not sure why
                    
#Same as kickoff return and very possibly, this code can be merged with the 
#kickoff return.
            if self.Kicking['PuntFlag'] == 1:
                TempYardLine = self.GM['YardLine'] + self.ResultList[3]
                if TempYardLine > 99:
                    self.GM['TDFlag'] = 1
                    Points = 6
                    self.ScoreFlag = 1
                    self.TDYardage = 100 - self.GM['YardLine']
                    self.ResultList[3] = self.TDYardage
                    self.GM['DTDFlag'] = 0

#This is where we remember the score before the play so we can revert to it
#if a TD is scored but is negated by a penalty
        if self.ScoreFlag == 1:                            #Some sort of score     
            self.GM['OldHTS'] = self.GM['HomeTeamScore']
            self.GM['OldVTS'] = self.GM['VisitingTeamScore']

            if (self.GM['OffenseFlag'] + self.GM['DTDFlag']) == 1:  #Apply offensive
                self.GM['VisitingTeamScore'] += Points        # and defensive        
            else:                                            #points
                self.GM['HomeTeamScore'] += Points           #appropriately
            if self.GM['SafetyFlag'] == 1:          #Safety
           
                self.CoP()                  #Fix in a later rev, messes up
                                        #TG but does not result in an error
                                        
#After a TD is scored, set the conversion flag because either an extra point
#or 2-point conversion will ensue.  Don't set if there is a safety
        if ((self.GM['TDFlag'] == 1) or (self.GM['DTDFlag'] == 1)) and (Points != 2):
            self.GM['ConversionFlag'] = 1
            
            
            
#****************************************************************************
#Method:    TGraphics
#Purpose:   Common method that can be called from CallPlay, Kickoff, FG, XPt 
#           and Punt.  
# Inputs:  
# Outputs: 
# Author:           Rick Burney
#
# Created:          8/10/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def TGraphics(self):
 
 #Call graphics routine that I wrote in Rev 1.  Room for growth here  
    
        TG = TestTurtleGraphics.PlaceBall(self.GM['YardLine'], 
                                          self.GM['OffenseFlag'])

#****************************************************************************
#Method:    TimeOutProcessing
#Purpose:   Checks to see if there are any timeouts left, if so, deducts 1 
#           from the number of timeouts for the calling team and does some
#           tricky time math to gain the effect of stopping the clock, also,
#           reset # of timeouts at start of 3rd quarter.  Also, updates the
#           # of timeouts on the scoreboard
# Author:           Rick Burney
#
# Created:          8/10/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def TimeOutProcessing(self,HomeTimeOut,VisitorTimeOut):
 
        DisplayMessage = Scoreboard()   #Create a Scoreboard Object        
        HTimeoutsDisplay = VTimeoutsDisplay = ""
        TimeElapsedOnPreviousPlay = self.GM['OldTimeLeftInQuarter'] - \
                self.GM['TimeLeftinQuarter']
        
#If a timeout is called but time has expired in the quarter, then display a 
#message, do not register a time out and exit this process
        if self.GM['TimeLeftinQuarter'] == 900:
            tkMessageBox.showinfo("Error Message", 
                            "Time expired in the quarter, no timeout called")
            return
#This is arbitrary but the way timeouts will be implemented is too take the
#time of the last play, divide it by 2 and to add it back to the new time left
#in the quarter
        self.GM['TimeLeftinQuarter'] += (TimeElapsedOnPreviousPlay / 2)
        MinutesLeftInQuarter = str(int(self.GM['TimeLeftinQuarter'] / 60))
        SecondsLeftInQuarter = str(int(self.GM['TimeLeftinQuarter'] % 60))
        
#Add a leading '0' to seconds if seconds are < 10
        if int(SecondsLeftInQuarter) < 10:
            SecondsLeftInQuarter = "0" + SecondsLeftInQuarter
            
#Display time                
        self.DisplayMessages['TimeLeftinQuarterDisplay'] = \
            MinutesLeftInQuarter+":"+SecondsLeftInQuarter
         
        
        DM = DisplayMessage.ResultDisplay(3,
                        self.DisplayMessages['TimeLeftinQuarterDisplay'],0,
                        self.GrandParent)
        if HomeTimeOut == 1:
            
#Make sure there are timeouts left
            if self.GM['HomeTimeouts'] <= 0:
                tkMessageBox.showinfo("Error Message", "No Timeouts Left") 
                return
            self.GM['HomeTimeouts'] -= 1 #If so, decrement # of timeouts by 1
            
            HTimeoutsDisplay = str(self.GM['HomeTimeouts'])
            DM = DisplayMessage.ResultDisplay(20,HTimeoutsDisplay,0,
                                              self.GrandParent)
            
        if VisitorTimeOut == 1:
            
#Make sure there are timeouts left
            if self.GM['VisitorTimeouts'] <= 0:
                tkMessageBox.showinfo("Error Message", "No Timeouts Left") 
                return
            self.GM['VisitorTimeouts'] -= 1 #If so, decrement # of timeouts by 1
            
            VTimeoutsDisplay = str(self.GM['VisitorTimeouts'])
            
        
            DM = DisplayMessage.ResultDisplay(21,VTimeoutsDisplay,0,
                                          self.GrandParent)


#****************************************************************************
#Function: UpdateYardLine
#Purpose:  This method updates the yardline after any play.  The adjusted
#          yardline, which is the yardline when the offense has the ball in
#          the opponent's territory (i.e., yardline > 50) is also updated
#            
# Author:           Rick Burney
#
# Created:          7/12/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def UpdateYardLine(self):
        
        
        self.GM['YardLine'] += self.ResultList[3] #Update YL based upon result
        if self.GM['SafetyFlag'] == 1:
            self.GM['YardLine'] = 0
        if self.GM['YardLine'] > 50:              #Update AYL
            
            self.GM['AdjustedYardLine'] = 100 - self.GM['YardLine']
        else:
            self.GM['AdjustedYardLine'] = self.GM['YardLine']
   




#****************************************************************************
#Function: WriteLogFile
#Purpose:  This method takes the log data that is stored in memory for a
#          team and writes to a file
#
# Created:          9/14/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def WriteLogFile(self, MDA, LogTeamName):
        
        from openpyxl import load_workbook     #Using openpyxl Python library
        from openpyxl import Workbook
        from openpyxl.styles import Alignment
        
        wbLog = Workbook()      #Log workbook to be written to a file
        wsLog = wbLog.active    #Open worksheet
        
        LogIndex = 1    #Start at row 2 because row 1 has the column names
        LogColumn = 1   #Start at column 1 per Excel numbering convention

#Define column names        
        Column1Heading = "Play Type"
        Column2Heading = "Ball Carrier"
        Column3Heading = "Play Result"
        Column4Heading = "Yardage"
        Column5Heading = "TD"
        Column6Heading = "Quarter"
        Column7Heading = "Seconds Left in Quarter"
        Column8Heading = "Fumble"
        Column9Heading = "Blowout"
        
#Adjust width of the columns
        wsLog.column_dimensions["A"].width = 10
        wsLog.column_dimensions["B"].width = 20.0
        wsLog.column_dimensions["C"].width = 15.0
        wsLog.column_dimensions["D"].width = 7.0    
        wsLog.column_dimensions["E"].width = 5.0
        wsLog.column_dimensions["F"].width = 7.0
        wsLog.column_dimensions["G"].width = 23.0
        wsLog.column_dimensions["H"].width = 7.0    
        wsLog.column_dimensions["I"].width = 7.0    
        
#Write the column names
        wsLog.cell(row = LogIndex, column = 1).value = Column1Heading
        wsLog.cell(row = LogIndex, column = 2).value = Column2Heading
        wsLog.cell(row = LogIndex, column = 3).value = Column3Heading
        wsLog.cell(row = LogIndex, column = 4).value = Column4Heading
        wsLog.cell(row = LogIndex, column = 5).value = Column5Heading
        wsLog.cell(row = LogIndex, column = 6).value = Column6Heading
        wsLog.cell(row = LogIndex, column = 7).value = Column7Heading
        wsLog.cell(row = LogIndex, column = 8).value = Column8Heading
        wsLog.cell(row = LogIndex, column = 9).value = Column9Heading

        for row in wsLog['A1:U400']:  #Center the columns 
            for cell in row:
                cell.alignment = Alignment(horizontal="center")  


        LogIndex += 1

        for i in range(len(MDA)):   
            RowData = MDA[i]                           #Line from the log data
            for j in range(len(RowData)):
                CellData = RowData[j]
                wsLog.cell(row = LogIndex, column = LogColumn).value = \
                    CellData   
                LogColumn += 1
            LogColumn = 1
            LogIndex += 1
        wbLog.save(LogTeamName)                 #Write the stats to the files
            


#****************************************************************************
#Function: YardLineAdjust
#Purpose:  This method receives YardLine as an input and updates AYL
#          
# Author:           Rick Burney
#
# Created:          7/31/2017
# Copyright:        (c) Rick 2017
#****************************************************************************
    def YardLineAdjust(self,YL):
        
        if YL > 50:         #On opponent's side of the field
            AYL = 100 - YL
        else:
            AYL = YL
        
        return AYL

#****************************************************************************
#Function: Debug
#Purpose:  TFor now, giving this a try       
# Author:           Rick Burne7
# Created:          11/20/2018
# Copyright:        (c) Rick 2018
#****************************************************************************
#    def Debug(self):
 #       if self.GameOptions['ForcePlay'] == 1:
  #          self.GM['TimeLeftinQuarter'] = 1
   #         self.GameOptions['ForcePenalty'] = 1
    #    else:
     #       self.GameOptions['ForcePenalty'] = 0
            
#****************************************************************************
#Function: DebugAfterThePlay
#Purpose:  For now, giving this a try       
# Author:           Rick Burney
# Created:          11/20/2018
# Copyright:        (c) Rick 2018
#****************************************************************************
    def DebugAfterThePlay(self,DebugCode):
        if DebugCode == 0:
            print("Turnover after an offensive deadball penalty flag = ", 
                  self.TurnoverAfterAnOffensiveDeadBallFoul)
            print("Fumble Flag = ", self.FumbleResult[0])
            print("Interception Flag = ", self.IntResult[5])
            if self.PenaltyList[4] < 0:
                print("Offensive Penalty")
            else:
                print("Defensive Penalty")
                print("Penalty Flag should be set ", self.PenaltyList[5])
        if DebugCode == 1:                                                              
            print(self.PenaltyList[6])          #Comfirm that a dead ball foul occurred
            print (self.GM['OldYardLine'])  #This should be where the play ended but before the penalty is assessed
            print(self.PenaltyList[4])          #Confirm that the penalty is on the defense
            print(self.ResultList[3])           #Print out the yardage gained
            print(self.GM['YardLine'])      #Print yardline after the penalty is applied