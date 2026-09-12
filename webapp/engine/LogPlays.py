
#-----------------------------------------------------------------------------
# Method Name:    PlayLog
# Purpose:        Writes play-by-play log to the relevant team worksheets.  A
#                 separate method will compile the log into statistics or
#                 EXCEL will do this
# Inputs:         homeTeamName - Name of the Home Team - duh
#                 visitingTeamName - Name of the Visiting Team 
#                 TeamWiththeBallFlag - 0 if home team is on offense
#                 homeTeamPlayCount - Used to index the Home Team log                 
#                 visitingTeamPlayCount - Used to index the Visiting Team log
#       The next set of inputs may or may not have content depending
#                 on the type of play - this list will grow in the future to 
#                 accommodate defensive stats
#                 PlayType 0=run, 1=pass, 2=kickoff, 3=punt, 4=field goal,
#                          5=Extra Point
#                 BallCarrier - also obvious
#                 ResultofthePass - result of the pass if there was a pass
#                 YardsGained - Yards gain on either a run, completed pass, or
#                               any type of kick
#                 TDFlag - 1 TD occurred
#                 IntFlag - 1 Pass resulted in an INT
#                 FumbleFlag - 1 Lost fumble occurred
#                 ExtraPointResult - 0 XtraPoint NG
#                 Need a flag to clear the logs
# Author:         Rick Burney
#
# Created:        1/23/2017
# Copyright:      (c) Rick 2017
#-----------------------------------------------------------------------------
def PlayLog(homeTeamName,visitingTeamName,TeamWiththeBallFlag,
            homeTeamPlayCount,visitingTeamPlayCount,PlayType,BallCarrier,
            ResultofthePass,Yardage,TDFlag,IntFlag,FumbleFlag,YardLine,
            TimeLeftinQuarterDisplay,PenaltyFlag,HomeTeamBlowout,
            VisitingTeamBlowout):
    
    import sys

    from openpyxl import load_workbook         #Using openpyxl Python library
    
    
    homeTeamName += "Log.xlsx"      #All log workbooks have an xlsx extension
    visitingTeamName += "Log.xlsx"

#Load workbooks
    wbhomeTeam= load_workbook(filename = homeTeamName, data_only=True)  
    wbvisitingTeam= load_workbook(filename = visitingTeamName, data_only=True) 
    
    if TeamWiththeBallFlag == 0:    #Determine which workbook to write the log
        wbOffense = wbhomeTeam
        TeamName = homeTeamName
        PlayCount = homeTeamPlayCount
    else:
        wbOffense = wbvisitingTeam
        TeamName = visitingTeamName
        PlayCount = visitingTeamPlayCount
    
    ws = wbOffense.active               #switch to active worksheet
    if (TDFlag == 1) and (IntFlag == 1):
        TDFlag = 0;                     #Pick-6, don't log TD
        
    
    PlayCount +=1           #Start at row 2 because there are titles on row 1

#Determine if play is a run or pass    
    if PlayType == 0:   
        ws.cell(row = PlayCount, column = 1).value = "Run"
        
#If pass, include what happened with the pass (Inc, Complete, Int, Sack)        
    if PlayType == 1:
        ws.cell(row = PlayCount, column = 1).value = "Pass"
        ws.cell(row = PlayCount, column = 3).value = ResultofthePass

#Not logging kickoffs, kicks or punts at this time        
    if PlayType == 2:
        ws.cell(row = PlayCount, column = 1).value = "Kickoff Return"
    if PlayType == 3:
        ws.cell(row = PlayCount, column = 1).value = "Punt"
    if PlayType == 4:
        ws.cell(row = PlayCount, column = 1).value = "Field Goal"
    if PlayType == 3:
        ws.cell(row = PlayCount, column = 1).value = "Extra Point"
        
#EOF allows CompileStats to know when it is at the end of the logfile
    if PlayType == "EOF":
        ws.cell(row = PlayCount, column = 1).value = PlayType
        
    ws.cell(row = PlayCount, column = 2).value = BallCarrier    
    ws.cell(row = PlayCount, column = 4).value = Yardage
    
    if TDFlag == 1:
        ws.cell(row = PlayCount, column = 5).value = "TD"

#Need to deal with fumbles - logged to offensive team before the change of 
#possession which means that logging needs to move before the Change of 
#Possession in ControlPanel
    
#General log info   

    ws.cell(row = PlayCount, column = 7).value = TimeLeftinQuarterDisplay
    ws.cell(row = PlayCount, column = 8).value = FumbleFlag

    if (TeamWiththeBallFlag == 0) and (HomeTeamBlowout == 1):
        Blowout = 1
    elif (TeamWiththeBallFlag == 1) and (VisitingTeamBlowout == 1):
        Blowout = 1
    else:
        Blowout = 0
    ws.cell(row = PlayCount, column = 9).value = Blowout
       
    
    
    wbOffense.save(TeamName)    #Write to workbook
   
    
    return ws


#-----------------------------------------------------------------------------
# Method Name:    ClearLog
# Purpose:        Clears the log worksheets for both teams
# Inputs:         homeTeamName - Name of the Home Team - duh
#                 visitingTeamName - Name of the Visiting Team 
# Author:         Rick Burney
#
# Created:        1/23/2017
# Copyright:      (c) Rick 2017
#-----------------------------------------------------------------------------
def ClearLog(homeTeamName,visitingTeamName):

    from openpyxl import load_workbook         #Using openpyxl Python library
    
    homeTeamName += "Log.xlsx"      #All log workbooks have an xlsx extension
    visitingTeamName += "Log.xlsx"

#Load workbooks
    wbhomeTeam= load_workbook(filename = homeTeamName, data_only=True)  
    wbvisitingTeam= load_workbook(filename = visitingTeamName, data_only=True) 
        
    wshomeTeam = wbhomeTeam.active               #switch to active worksheet
    wsvisitingTeam = wbvisitingTeam.active       #switch to active worksheet
   
    
    for row in wshomeTeam['A2:N400']:  #Start at Row 2 so we can have headings 
        for cell in row:
            cell.value = None
    
    for row in wsvisitingTeam['A2:N400']:   #Clear all cells for both teams
        for cell in row:
            cell.value = None
    
    
    wbhomeTeam.save(homeTeamName)
    wbvisitingTeam.save(visitingTeamName)
    
    
    return None
 
   



#-----------------------------------------------------------------------------
# Method Name:    CompileStats
# Purpose:        Writes play-by-play log to the relevant team worksheets.  A
#                 separate method will compile the log into statistics or
#                 EXCEL will do this
# Inputs:         homeTeamName - Name of the Home Team - duh
#                 visitingTeamName - Name of the Visiting Team 
#                 TeamWiththeBallFlag - 0 if home team is on offense
#                 homeTeamPlayCount - Used to index the Home Team log                 
#                 visitingTeamPlayCount - Used to index the Visiting Team log
#       The next set of inputs may or may not have content depending
#                 on the type of play - this list will grow in the future to 
#                 accommodate defensive stats
#                 PlayType 0=run, 1=pass, 2=kickoff, 3=punt, 4=field goal,
#                          5=Extra Point
#                 BallCarrier - also obvious
#                 ResultofthePass - result of the pass if there was a pass
#                 YardsGained - Yards gain on either a run, completed pass, or
#                               any type of kick
#                 TDFlag - 1 TD occurred
#                 IntFlag - 1 Pass resulted in an INT
#                 FumbleFlag - 1 Lost fumble occurred
#                 ExtraPointResult - 0 XtraPoint NG
#                 Need a flag to clear the logs
# Author:         Rick Burney
#
# Created:        1/23/2017
# Copyright:      (c) Rick 2017
#-----------------------------------------------------------------------------
def CompileStats(homeTeamName,visitingTeamName,homeTeamPlayCount,
                 visitingTeamPlayCount,TeamFlag,HQBName,VQBName,
                 HBackupQBName,VBackupQBName):
    
    
    from openpyxl import load_workbook         #Using openpyxl Python library
    from openpyxl import Workbook
    from openpyxl.styles import Alignment
    import PickAPlayer
    
    HT = homeTeamName       #Used as a partial string to form Ostats and
    VT = visitingTeamName       #Dstats filenames


    
    RushingHeadingRow = 1           #Heading locations on worksheets
    BallCarrierHeadingColumn = 1
    NumberofCarriesColumn = 2
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
    
    homeWorksheet = homeTeamName + ".xlsx"
    visitingWorksheet = visitingTeamName  + ".xlsx"
    
    
    
    
    homeTeamName += "Log.xlsx"      #All log workbooks have an xlsx extension
    visitingTeamName += "Log.xlsx"
    homeTeamStats = HT + "Stats.xlsx"       #All stats workbooks have an xlsx 
    visitingTeamStats = VT + "Stats.xlsx"   #extension
    homeTeamDStats = HT + "DStats.xlsx"
    visitingTeamDStats = VT + "DStats.xlsx"
    wbStats = Workbook()
    wbDStats = Workbook()

#Load workbook based upon TeamFlag
    if TeamFlag == 0:
        wbTeam= load_workbook(filename = homeTeamName, data_only=True)
        wbDefense = load_workbook(filename = visitingWorksheet,data_only=True)
        PlayCount = homeTeamPlayCount
        StatsName = homeTeamStats
        DStatsName = visitingTeamDStats
        QBName = HQBName
        BackupQBName = HBackupQBName
    else:
        wbTeam= load_workbook(filename = visitingTeamName, data_only=True) 
        wbDefense = load_workbook(filename = homeWorksheet, data_only=True)
        PlayCount = visitingTeamPlayCount
        StatsName = visitingTeamStats
        DStatsName = homeTeamDStats
        QBName = VQBName
        BackupQBName = VBackupQBName
    
  
    
    ws = wbTeam.active          #switch to active worksheet
    wsStats = wbStats.active
    wsDefense = wbDefense.active
    wsDStats = wbDStats.active
    
    
    
    
#clear stats sheet
    for row in wsStats['A1:N400']:  #Start at Row 2 so we can have headings 
        for cell in row:
            cell.value = None
    wbStats.save(StatsName)
    
   
    for row in wsStats['B1:U400']:  #Center many of the columns
        for cell in row:
            cell.alignment = Alignment(horizontal="center")  
    for row in wsDStats['B1:U400']:
        for cell in row:
            cell.alignment = Alignment(horizontal="center")  
            
#Adjust width of the columns
    wsStats.column_dimensions["A"].width = 20.0
    wsStats.column_dimensions["B"].width = 15.0
    wsStats.column_dimensions["E"].width = 5.0
    wsStats.column_dimensions["F"].width = 5.0    
    wsStats.column_dimensions["G"].width = 8.0
    wsStats.column_dimensions["H"].width = 20.0
    wsStats.column_dimensions["I"].width = 15.0
    wsStats.column_dimensions["L"].width = 8.0
    wsStats.column_dimensions["M"].width = 5.0
    wsStats.column_dimensions["N"].width = 8.0
    wsStats.column_dimensions["O"].width = 20.0
    wsStats.column_dimensions["P"].width = 10.0
    wsStats.column_dimensions["Q"].width = 15.0
    wsStats.column_dimensions["R"].width = 16.0
    wsStats.column_dimensions["U"].width = 5.0
    
    wsDStats.column_dimensions["A"].width = 20.0
    wsDStats.column_dimensions["B"].width = 15.0
    wsDStats.column_dimensions["D"].width = 20.0

    for row in wsStats['D1:D400']:  #Zero out the cells before populatin
        for cell in row:
            cell.number_format = '0.0'          

    
    PlayCount +=1           #Start at row 2 because there are titles on row 1
    PlayType = ""
    BallCarrierList = []    #These lists are sync'ed to form multiple-
    PassCatcherList = []    #dimensioned arrays
    YardageList = []
    RunLongestGainList = []
    ReceivingLongestGainList = []
    PassingLongestGainList = []
    ReceivingYardageList = []
    NumberofCarriesList = []
    TDList = []
    ReceiverList = []
    NumberofReceptionsList = []
    ReceivingTDList = []
    NewBallCarrierIndex = 0 #Index into the rushing stats array
    NewReceiverIndex = 0    #Index into the receiving stats array
    PassAttempts = 0        #Initialize passing stats
    BackupPassAttempts = 0
    Completions = 0
    BackupCompletions = 0
    PassingYards = 0
    BackupPassingYards = 0
    QBLG = 0
    BackupQBLG = 0
    Ints = 0
    BackupInts = 0
    PassTDs = 0
    BackupPassTDs = 0
    NonTacklingPlays = 0        #This object is used for tackle stats and
                                #indicates that there are no tackles by the 
                                #defense for TDs, Ints and fumbles
    SackCount = 0   #Initialize the number of sacks for the D
    
    while PlayType != "EOF":    #Compile stats until the log EOF is reached
    
        PlayType = ws.cell(row = PlayCount, column = 1).value
        ReceivingYardage = Yardage = ws.cell(row = PlayCount, 
                                             column = 4).value
        
        if ws.cell(row = PlayCount, column = 5).value == "TD":
            ReceivingTD = TD = 1
        else:
            ReceivingTD = TD = 0
        if ws.cell(row = PlayCount, column = 8).value == 1:
            FumbleFlag = 1
        else:
            FumbleFlag = 0
        
        if (TD == 1) or (FumbleFlag == 1):  #No tackles by the defense if there
            NonTacklingPlays += 1           #is a fumble or a TD
                      
        if PlayType == "Run":
            BallCarrier = ws.cell(row = PlayCount, column = 2).value
            
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
                NewBallCarrierIndex += 1
        else:
            PassCatcher = ws.cell(row = PlayCount, column = 2).value
            PassResult = ws.cell(row = PlayCount, column = 3).value
            if PlayType != "EOF":
                if ws.cell(row = PlayCount, column = 9).value == 0:
                    PassAttempts += 1
                else:
                    BackupPassAttempts += 1
            
            if PassResult == "Sack":
                SackCount += 1
            
            if PassResult == "Completed":
                if ws.cell(row = PlayCount, column = 9).value == 0:
                    Completions += 1
                    PassingYards += ReceivingYardage
                else:
                    BackupCompletions += 1
                    BackupPassingYards += ReceivingYardage
                
                if ws.cell(row = PlayCount, column = 9).value == 0:
                    if PassAttempts == 1:
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
                if PassCatcher in PassCatcherList:
                    PassCatcherIndex = PassCatcherList.index(PassCatcher)
                    ReceivingYardageList[PassCatcherIndex] += ReceivingYardage
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
            
            if PassResult == "Int": #No tackle by the defense if there is an Int
                if ws.cell(row = PlayCount, column = 9).value == 0:
                    Ints +=1 
                else:
                    BackupInts += 1
                NonTacklingPlays += 1
                    
        PlayCount += 1
    
    
        #Write column headings
    wsStats.cell(row = RushingHeadingRow, 
                 column = BallCarrierHeadingColumn).value = "Ball Carrier"
    wsStats.cell(row = RushingHeadingRow, 
                 column = NumberofCarriesColumn).value = "Number of Carries"
    wsStats.cell(row = RushingHeadingRow, 
                 column = RushingYardsColumn).value = "Yards"
    wsStats.cell(row = RushingHeadingRow, 
                 column = YPCColumn).value = "Ave"
    wsStats.cell(row = RushingHeadingRow, column = RunLGCol).value = "LG"
    wsStats.cell(row = RushingHeadingRow, 
                 column = RBTDColumn).value = "TD"
    wsStats.cell(row = RushingHeadingRow, 
                 column = ReceiverNameColumn).value = "Receiver"
    wsStats.cell(row = RushingHeadingRow, 
                 column = ReceptionsColumn).value = "Receptions"
    wsStats.cell(row = RushingHeadingRow, 
                 column = ReceivingYardsColumn).value = "Yards"
    wsStats.cell(row = RushingHeadingRow, 
                 column = YPCatchColumn).value = "Ave"
    wsStats.cell(row = RushingHeadingRow, column = RcvgLGCol).value = "LG"
    wsStats.cell(row = RushingHeadingRow, 
                 column = RcvrTDColumn).value = "TD"
    wsStats.cell(row = RushingHeadingRow, 
                 column = QBNameColumn).value = "QB"
    wsStats.cell(row = RushingHeadingRow, 
                 column = PassAttemptColumn).value = "Attempts"
    wsStats.cell(row = RushingHeadingRow, 
                 column = CompletionsColumn).value = "Completions"
    wsStats.cell(row = RushingHeadingRow, 
                 column = YardsColumn).value = "Passing Yards"
    wsStats.cell(row = RushingHeadingRow, 
                 column = QBLGCol).value = "LG"
    wsStats.cell(row = RushingHeadingRow, 
                 column = IntColumn).value = "Int"
    wsStats.cell(row = RushingHeadingRow, 
                 column = PassTDColumn).value = "TD"

    HeadingRow = 1
    TacklerHeadingColumn = 1
    NumberofTacklesHeadingColumn = 2
    SackerHeadingColumn = 4
    NumberofSacksHeadingColumn = 5
    
#Write defensive stat column headings
    wsDStats.cell(row = HeadingRow, 
             column = TacklerHeadingColumn).value = "Name"
    wsDStats.cell(row = HeadingRow, 
             column = NumberofTacklesHeadingColumn).value = "Tackles"
    wsDStats.cell(row = HeadingRow, 
             column = SackerHeadingColumn).value = "Name"
    wsDStats.cell(row = HeadingRow, 
             column = NumberofSacksHeadingColumn).value = "Sacks"

#Fill cells with offensive stats
    for i in range(0,len(BallCarrierList)):
        wsStats.cell(row = i+2, 
                     column = BallCarrierHeadingColumn).value = \
            BallCarrierList[i]
        wsStats.cell(row = i+2, 
                     column = NumberofCarriesColumn).value = \
            NumberofCarriesList[i]        
        wsStats.cell(row = i+2, 
                     column = RushingYardsColumn).value = YardageList[i]
        wsStats.cell(row = i+2, 
                     column = YPCColumn).value = \
            round(YardageList[i]/float(NumberofCarriesList[i]),1)
        wsStats.cell(row = i+2, 
                     column = RunLGCol).value = RunLongestGainList[i]        
        wsStats.cell(row = i+2, column = RBTDColumn).value = TDList[i]
        
        
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
    
    NumPlays = PlayCount - 3

    RushingYardsColumn = 3
    
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
    for i in range(0,len(Sacker.SackerList)):
        wsDStats.cell(row = HeadingRow + i + 1, 
                     column = SackerHeadingColumn).value = \
            Sacker.SackerList[i]  
        wsDStats.cell(row = HeadingRow + i + 1, 
                     column = NumberofSacksHeadingColumn).value = \
            Sacker.NumberOfSacksList[i] 
        
    wbStats.save(StatsName)                 #Write the stats to the files
    wbDStats.save(DStatsName)
    
    return None



