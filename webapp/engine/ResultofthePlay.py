
#-----------------------------------------------------------------------------
# Function Name:    ResultofthePlay
# Purpose:          Based upon a 3-die roll, index the run or pass yardage
#                   as appropriate, decode the result from the table and
#                   return to the calling function
# Author:           Rick Burney
# Created:          12/14/2016
# Copyright:        (c) Rick 2016
# Objects passed in
#    TeamWiththeBall - If this were a class and one day it will be, this would
#                      be self.Offense - this is the stat worksheet of the 
#                      team on offense
#    PlayType -        STRING, "Run" or "Pass"
#    PassLength -      STRING, "Short", "Mid", "Mid-Long" or "Long"
#    QBStartIndex -    INTEGER, the worksheet row that identifies where to get
#                      the QBs stats for the offense
#    Dstats -          LIST, contains the defensive team stats for the team on
#                      defense
#-----------------------------------------------------------------------------
def ResultofthePlay(TeamWiththeBall,PlayType,PassLength,QBsStartIndex,Dstats,
                    BallCarrierAve,SpiketheBall,HailMary,YardLine,
                                            ConferenceFactorAdder,
                                            ConferenceFactorMultiplier,
                                            Blowout,
                                            TeamthatDoesNotHavetheBall):
    
    import Die          #Method that rolls 3 die to index a yardage table          
    import YardageTable #Method that uses a variety of yardage tables, each
                        #for a different type of play, that are indexed from
                        #the output of the Die Method
    import openpyxl     #Library that allows the use of EXCEL spreadsheets,
                        #which are used to store all player and team stats
    import PickAPlayer  #Primary method for assigning stats to players and
                        #selecting ball carriers.  Prime candidate to convert
                        #to a class.  Also used to extract injury impact stats
                        #from the team worksheet
    import random       #Python library for generating pseudo-random numbers 
                        #which serves as the basis for this simulator
    
    global QBName       #The name of the quarterback that is in the game for
                        #the team that is on offense
    
    InjuryPenalty = 0.1 #Per the injury impact guidelines.  Applies to the
                        #Oline, DLine, linebackers and DBs
    
#Instantiate a class object that will allow the location of the row in the 
#defensive team's worksheet for Injury Impact
    RequestedInjuryImpactRow = \
        PickAPlayer.PickAPlayer(TeamthatDoesNotHavetheBall,0,0,0,0,0)
    
    RequestedInjuryImpactRow.FindStats()    #Extract the injury impact data
    InjuryImpactStartIndex = \
        RequestedInjuryImpactRow.InjuryImpactsPosition + \
        RequestedInjuryImpactRow.Offset
        
#Do the same thing for the offensive player (at this point, offensive linemen)
    RequestedOffensiveInjuryImpactRow = PickAPlayer.PickAPlayer(TeamWiththeBall,0,0,0,0,0) 
    RequestedOffensiveInjuryImpactRow.FindStats()
    OffensiveInjuryImpactStartIndex = \
        RequestedOffensiveInjuryImpactRow.InjuryImpactsPosition + \
        RequestedOffensiveInjuryImpactRow.Offset
    
#Determine the number of starting offensive linemen who are injured
    NumberOfStartingOLInjured = \
        TeamWiththeBall.cell(row = OffensiveInjuryImpactStartIndex, column = 3).value
    
#Determine the number of starting defensive linemen who are injured
    NumberOfStartingDLInjured = \
        TeamthatDoesNotHavetheBall.cell(row = InjuryImpactStartIndex + 1, column = 3).value
    
#Determine the number of starting linebackers who are injured
    NumberOfStartingLBsInjured = \
        TeamthatDoesNotHavetheBall.cell(row = InjuryImpactStartIndex + 2, column = 3).value
    
#Determine the number of starting defensive backs who are injured
    NumberOfStartingDBsInjured = \
        TeamthatDoesNotHavetheBall.cell(row = InjuryImpactStartIndex + 3, column = 3).value
    
#Injury impacts are per the Injury Impact Guidelines
    RustAdjusterInjuryImpact = -NumberOfStartingOLInjured + \
        NumberOfStartingDLInjured + NumberOfStartingLBsInjured
    SackPercentageInjuryImpact = NumberOfStartingOLInjured - \
        NumberOfStartingDLInjured
    PassCompletionDefenseInjuryImpact = \
        float(NumberOfStartingLBsInjured) / 2 + NumberOfStartingDBsInjured
    PassIntPercentageInjuryImpact = \
        -(float(NumberOfStartingLBsInjured) / 2 + NumberOfStartingDBsInjured)
    
#Team and individual stats come from 
#http://www.espn.com/college-football/statistics and 
#http://www.ncaa.com/stats/football/fbs  
    

#Defensive Team average stats - defined as constants - from the middle of
#http://www.ncaa.com/stats/football/fbs.  Will be replaced by actual stats
    DrushAve = 5.1          #This is the average number of yards/attempt allowed by defenses
    PComppAAve = 56.0  #This is the average % of completions/attempt allowed by 
                                      #defenses
    PYrdspCompAve = 12.5    # This is the average yards per catch allowed by defenses
                            
#Offensive Team average stats.  Will be replaced by actual individual stats
    OrushAve = 5.3
    YACAve = 14
        
#Play adjusters - rush adjusters are add/subtracts in order that good defenses can have  
#more TFLs.  Pass yardage adjuster is multiplicative.  Add in Conference Factor Adder
    RushAdjuster = (float(Dstats[0]) - DrushAve)+(float(BallCarrierAve) - \
                                            OrushAve) + ConferenceFactorAdder

#Make further adjustments to the rush result based upon injury impacts
    RushAdjuster += RustAdjusterInjuryImpact * InjuryPenalty
    
#Adjust the yardage on pass completions based defensive stats, receiver
#yardage stats and the quality of the conference from which the team belongs
    PassYardageAdjuster = \
        (float(Dstats[2])/PYrdspCompAve)*(float(BallCarrierAve)/YACAve) * \
        ConferenceFactorMultiplier
        
    yardageResult = ""  #Initialize results
    yards = 0
    PassResult ="Run"
    
    roll=Die.RolltheDie()                   #Roll 3 die
    all3die = roll.Dice3Dice6Dice6()
    dice1,dice2,dice3 = roll.dice1,roll.dice2,roll.dice3  #Separate into 3 die
    
#Compute 11x3 array indices, remember to subtract 2 for the row index since it  is the sum 
#of two die and array indices start at 0, subtract 1 for column index.  Extract the name of
#the QB
    rowIndex = dice2 + dice3 - 2
    columnIndex = dice1 - 1 
    
#Determine which of two QBs are in the game
    QBName = TeamWiththeBall.cell(row = QBsStartIndex, column = 2).value
    
    if PlayType == "Run":   #Determine yards gained if the play is a run

#Use the 'dice' result to index into the Yardage Table.  Sometimes, the yardage table
#produces a result that is non-numeric such as "short gain", or "medium gain," or "long gain"
#These alpha-numeric results need to be resolved into an actual yardage value and they are
#using the method 'ResolveGains'
        
#Retrieve the result from  the yardage table
        yardageResult = YardageTable.RunYardageTable(rowIndex,columnIndex)
        
#If the result is non-numeric, resolve the result into a number using the Resolve Gains 
#method
        yards = YardageTable.ResolveGains(yardageResult)
        yards = int(round(yards + RushAdjuster,0))              #Adjust the yardage value based
                                                                                         #the conference quality adder
    else:
            
#Pass, adjust percent completion for the QB with the pass defense efficiency and the 
#conference quality multiplier
        #print(QBsStartIndex)
        PC = ((TeamWiththeBall.cell(row = QBsStartIndex, column = 3).value + Dstats[1])/2) * \
            ConferenceFactorMultiplier

#Make further adjustments to the completion % based upon injury impacts
        PC += PassCompletionDefenseInjuryImpact * InjuryPenalty
         
#Get Int % from the QB stats but then get the defensive INT percent and take the average 
#with QB stats
        PI = ((TeamWiththeBall.cell(row = QBsStartIndex, column = 4).value + \
              Dstats[4]) / 2) / ConferenceFactorMultiplier

#Make further adjustments to the interception % based upon injury impacts
        PI += PassIntPercentageInjuryImpact * InjuryPenalty
                   
        DsackPerc = Dstats[3]   #Extract the sack percentage for the defense

#Adjust the sack % (which is based on the OL performance) with the DL
#performance and account for the conference difficulty
        SackPerc = (((TeamWiththeBall.cell(row = QBsStartIndex, 
                                        column = 6).value) + DsackPerc) / 2)\
            / ConferenceFactorMultiplier

#Make further adjustments to the sack percentage based upon injury impacts
        SackPerc += SackPercentageInjuryImpact * InjuryPenalty
                
#Determine if the pass is completed or not, intercepted or if a sack occurred
        PassResult = YardageTable.ResultofthePass(PassLength,PC,PI,SackPerc,Dstats)
        
#If HailMary, recalculate Pass Completion Percentage and override PassResult.
#For now, the two choices for Hail Mary Passes are complete or incomplete

        if HailMary == 1:       #Hail Mary Pass, compute pass completion %
            if YardLine > 60:
                PassCompletionPerc = 20 #Based upon line of scrimmage.  %s are made up
            elif YardLine > 50:         
                PassCompletionPerc = 15
            elif YardLine > 40:
                PassCompletionPerc = 10
            elif YardLine > 30:
                PassCompletionPerc = 5
            else:
                PassCompletionPerc = 1
            Dice1 = random.randint(0,99)   #Test to see if Hail Mary is completed
            if Dice1 < PassCompletionPerc:  
                PassResult = "Completed"    #If so, the yardage will be calculated specifically for a 
            else:                                        #Hail Mary situation
                PassResult = "Incomplete"           
        if SpiketheBall == 1:                    #Spiking the ball results in an  incomplete pass
            PassResult = "Incomplete"               
        if PassResult == "Sack":                 #If a sack occurs, roll the dice to figure out the sack
            roll=Die.RolltheDie()                   #loss yardage
            all3die = roll.Dice3Dice6Dice6()   

#Uses the Stratomatic method of three dice although die 1 has only three sides.  Die 1 
#chooses one of three columns in the sack yardage table, the sum of die 2 and 3 choose one 
#of eleven rows in the table.  Die 2 and 3 are six-sided dice.  However, in Python, table 
#indices start at 0 so since the minimum sum of two dice = 2, we need to subtract 2 to 
#figure out the row index
            dice1,dice2,dice3 = roll.dice1,roll.dice2,roll.dice3    #3-element list, 1 per die
            
#Subtract 2 to account for the fact that indices start at 0.  There are two dice in this
#computation so we need to subtract 2 instead of 1
            rowIndex = dice2 + dice3 - 2                                
            columnIndex = dice1 - 1    
            yards = YardageTable.SackYardageTable(rowIndex,columnIndex)
            
        elif PassResult == "Completed": #If the pass is completed, use the
            if PassLength == "Short":   #length of the pass and roll the dice
                roll=Die.RolltheDie()   #to figure out the yardage
                
                all3die = roll.Dice3Dice6Dice6()
                dice1,dice2,dice3 = roll.dice1,roll.dice2,roll.dice3
                rowIndex = dice2 + dice3 - 2
                columnIndex = dice1 - 1   
                yardageResult = YardageTable.ShortPassTable(rowIndex,
                                                              columnIndex)
                yards = YardageTable.ResolveGains(yardageResult)
                yards = int(round(yards * PassYardageAdjuster,0))
                    
            if PassLength == "Mid":     #Mid-length pass
                roll=Die.RolltheDie()               
                all3die = roll.Dice3Dice6Dice6()
                dice1,dice2,dice3 = roll.dice1,roll.dice2,roll.dice3    
                rowIndex = dice2 + dice3 - 2
                columnIndex = dice1 - 1    
                yardageResult = YardageTable.MidPassTable(rowIndex,
                                                          columnIndex)
                yards = YardageTable.ResolveGains(yardageResult)
                yards = int(round(yards * PassYardageAdjuster,0))
                
            if PassLength == "MidLong":
                roll=Die.RolltheDie()               
                all3die = roll.Dice3Dice6Dice6()
                dice1,dice2,dice3 = roll.dice1,roll.dice2,roll.dice3    
                rowIndex = dice2 + dice3 - 2
                columnIndex = dice1 - 1    
                yardageResult = YardageTable.MidLongPassTable(rowIndex,
                                                          columnIndex)
                yards = YardageTable.ResolveGains(yardageResult)
                yards = int(round(yards * PassYardageAdjuster,0))
                
            if PassLength == "Long":
                yards = YardageTable.LPGResolve()
                yards = int(round(yards * PassYardageAdjuster,0))
            
            if HailMary == 1:                   #Hail Mary Pass that was  
                dice1 = random.randint(-2,12)   #completed.  #Hail Marys are t
                yards = 100 - YardLine + dice1  #hrown to an area in or around 
                                                #the end zone so compute the
                                                #yardage based on that thought
            
                
        elif PassResult == "Incomplete":
            yards = 0
            
        else:   #Pretty sure there is nothing else but just in case
            yards = 0
        
#Return a list with the play type, pass length, pass result and the pass yards
    ResultList = [PlayType,PassLength,PassResult,yards]
    
    return ResultList



#-----------------------------------------------------------------------------
# Function Name:    UpdateTime1
# Purpose:          Updates the scoreboard clock based upon the play and the 
#                   code passed into this method
# Author:           Rick Burney
#
# Created:          2/16/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
def UpdateTime1(TimeCode,TimeLeftinQuarter,Quarter,UntimedDownFlag,
                PenaltyList,TDFlag):
    
    import random
        
    global TimeLeftinQuarterDisplay

#TimeCode definition
# 0  - Incomplete Pass      7 - 14 seconds
# 1  - Touchdown            7 - 14 seconds
# 2  - Touchback (not punt) 7 - 14 seconds
# 3  - reserved             7 - 14 seconds
# 4  - Timeout              Not implemented this way

# 5  - Out of Bounds with 2 or less minutes left in the 2nd or 4th quarter 
#      5 - 12 seconds 

# 6  - Hurry Up           10 - 20 seconds
# 7  - Punt               10 - 20 seconds
# 8  - Kickoff            10 - 20 seconds
# 9  - First Down         10 - 30 seconds   
# 10 - Out of Bounds      10 - 35 seconds   also used for an accepted penalty
# 11 - Field Goal         3 - 5 seconds     
# 12 - Spike the Ball     1 - 2 seconds 

# 13 - Touchback or out-of-bounds on a kick 0 seconds

# 14 - Fair catch and punt touchback 3- 6 seconds
# 15 - None of the above  15 - 41 seconds which are most of the plays 
# 16 - Presnap Penalty - 0 seconds

#This is where out of bounds conditions are tested.  Just guessing at the % of
#plays that go out of bounds.  See TimeCode 5 and 10.  Only applies to 
#incoming TimeCodes 6 and 15 
    OOBFlag = 0             #Assume not out of bounds
    PercOutofBounds = 10            #% of plays that go out of bounds
    OOBRoll = random.randint(0,99)          #Test to see if out of bounds 
    if (TimeCode == 6) or (TimeCode == 15): #Only plays that can be out of 
        if OOBRoll < PercOutofBounds:       #bounds are time codes 6 or 15
            OOBFlag = 1                 #Not sure why but I am certain I knew
    else:                               #at the time I wrote this code
        OOBFlag = 0

#Out of bounds only affects time when within 2 minutes of the end of the 2nd
#and 4th quarter
    if ((Quarter == 2) or (Quarter == 4)) and (TimeLeftinQuarter <= 120):
        if OOBFlag == 1:
            print("Out of Bounds")
            TimeCode = 5
            
    else:                   #Not within 2 minutes of 2nd/4th, clock stops to
        if OOBFlag == 1:    #reset the ball
            TimeCode = 10

#Incomplete pass, TD, non-punt touchback, OOB within 2 minutes of 2nd/4th quarter all use
#same time range
    if TimeCode <= 5:                                             
        ElapsedTime = random.randint(7,17)
    elif TimeCode == 6:                                 #Hurry up offense but only 
        ElapsedTime = random.randint(10,20)  #applies to runs and completions
    elif TimeCode <= 8:                                 #Kickoff timecode        
        ElapsedTime = random.randint(10,20)
    elif TimeCode == 9:                                 #First down timecode
        ElapsedTime = random.randint(15,30)
    elif TimeCode == 10:                                #OOB timecode not within 2 minutes
        ElapsedTime = random.randint(15,35)
    elif TimeCode == 11:                                #FG timecode
        ElapsedTime = random.randint(3,5)
    elif TimeCode == 12:                                #Spike the ball timecode
        ElapsedTime = random.randint(1,2)
    elif TimeCode == 13:
        ElapsedTime = 1     #Kickoff touchback timecode. Make this 1 sec 
                            #instead of 0 so you don't get error message at 
                            #the beginning of the 1st and 3rd quarters
    elif TimeCode == 14:
        ElapsedTime = random.randint(3,6)
    elif TimeCode == 16:                    #Extra Point time code
        ElapsedTime = 0
    elif TimeCode == 17:    #Accepted penalty time code
    
        ElapsedTime = 10
    elif TimeCode == 18:
        ElapsedTime = random.randint(37,40)
    elif TimeCode == 19:                    #Delay of game with clock running
        ElapsedTime = 40
        
    else:        
        ElapsedTime = random.randint(18,41)
    if UntimedDownFlag == 1:
        ElapsedTime = 0
    
    TimeLeftinQuarter -= ElapsedTime
    UntimedDownFlag = 0                                #Initialize these flags
    
    if (PenaltyList[4]) > 0 and (PenaltyList[5] == 1):
        UntimedDownCondition = 1
    elif TDFlag == 1:
        UntimedDownCondition = 1
    else:
        UntimedDownCondition = 0
    if (TimeLeftinQuarter <= 0):
        if UntimedDownCondition == 0:
            Quarter += 1
            TimeLeftinQuarter = 900
        else:
            TimeLeftinQuarter = 0
            UntimedDownFlag = 1
    
    MinutesLeftInQuarter = str(int(TimeLeftinQuarter / 60))
    SecondsLeftInQuarter = str(int(TimeLeftinQuarter % 60))
    if int(SecondsLeftInQuarter) < 10:
        SecondsLeftInQuarter = "0" + SecondsLeftInQuarter
    TimeLeftinQuarterDisplay = MinutesLeftInQuarter+":"+SecondsLeftInQuarter
    TimeList = [TimeLeftinQuarter,Quarter,UntimedDownFlag]       
    return TimeList


#-----------------------------------------------------------------------------
# Function Name:    Fumble
# Purpose:          Tests to see if there is a fumble lost.  ~75% of fumbles
#                   are not returned.  This is a programmable constant.  This
#                   method pulls a fumble lost number from the team with the 
#                   ball (parts per 10,000) and tests to see if a fumble 
#                   occurred.
# Inputs:           TeamtWiththeBall
#                   TeamthatDoesNotHavetheBall - to figure out who recovered
# Outputs:          FumbleFlag -    1 = Fumble
#                   Fumble Return if any
#                   YardLine - location after the fumble return
#                   FumbleRecoverer - Who recovers the fumble
# Author:           Rick Burney
#
# Created:          1/16/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
def Fumble(TeamWiththeBall,TeamthatDoesNotHavetheBall,YardLine,Dstats, Force):
    
    import PickAPlayer #Allows extraction of fumbles lost by the offense stats
    import random
    import openpyxl

#Instantiate a class object that will allow the location of the row in the 
#defensive team's worksheet for offensive fumbles lost stats
    RequestedOFumbleRow = PickAPlayer.PickAPlayer(TeamWiththeBall,0,0,0,0,0) 
    RequestedOFumbleRow.FindStats()
    FumblesLostRow = RequestedOFumbleRow.OFumblesLostPosition

    PercFumblesReturned = 75    #Just a guess
    #FumblesLostRow = 67         #Location of fumble stats
    FumblesLostCol = 2
    FumbleFlag = 0          #Start off with no fumble
    FumbleReturn = 0        #And if there is, no return
    FumbleRecoverRow = 70   #OK, probably no such phrase as fumble recoverer
    FumbleRecovererCol = 2
    
    FumbleRecoverer = ""    #Initialize

#Extract fumble stats for the offense - 1 number for the offense
    FumblesLost = round((TeamWiththeBall.cell(row = FumblesLostRow,
                                       column=FumblesLostCol).value + \
                         Dstats[5]) / 2,2)

#Generate random number to see if a fumble occurred
    dice1 = random.randint(0,9999)  
    if dice1 <= FumblesLost:        #Test for a fumble
        FumbleFlag = 1              #Fumble occurred
        
        dice1 = random.randint(0,99)    #Test to see if fumble is returned
        
        if dice1 >= PercFumblesReturned:    #Most fumbles have no return
            dice1 = random.randint(1,10)    
            if dice1 <= 2:                              #20% of returns range
                FumbleReturn = random.randint(-2,10)    #from -2 to 10 yards
            elif dice1 <= 8:
                FumbleReturn = random.randint(11,25)    #60% of returns range
            else:                                       #from 11 to 25 yards
                FumbleReturn = random.randint(26,99)    #20% of returns range
                                                        #from 26 to 99 yards

#Instantiate a class object that will allow the location of the row in the 
#defensive team's worksheet for offensive fumbles lost stats
        RequestedFumbleRecovererRow = \
            PickAPlayer.PickAPlayer(TeamthatDoesNotHavetheBall,0,0,0,0,0) 
        RequestedFumbleRecovererRow.FindStats()
        FumbleRecoverRow = \
            RequestedFumbleRecovererRow.FumbleRecoveriesPosition + \
            RequestedFumbleRecovererRow.Offset
        
        dice1 = random.randint(0,17)                    #See who recovers by                    
        FumbleRecovererIndex = FumbleRecoverRow + dice1 #indexing into list
        
        FumbleRecoverer = \
            TeamthatDoesNotHavetheBall.cell(row = FumbleRecovererIndex,
                                       column=FumbleRecovererCol).value
        
#Return fumble flag, return yardage, and who recovered.  The new yardline is
#handled in the calling routine
    FumbleResult = [FumbleFlag,FumbleReturn,YardLine,FumbleRecoverer]
    return FumbleResult
        
    
    
#-----------------------------------------------------------------------------
# Function Name:    Int
# Purpose:          Handles all of the processing after the play result
#                   determines that an interception has occurred.  
# Author:           Rick Burney
#
# Created:          1/16/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
def Int(TeamthatDoesNotHavetheBall,PassLength,YardLine,force):
    
    import PickAPlayer  #Allows extraction of interception stats
    import random
    import YardageTable
    import openpyxl
    
#Instantiate a class object that will allow the location of the row in the 
#defensive team's worksheet for INT stats
    RequestedIntRow = PickAPlayer.PickAPlayer(TeamthatDoesNotHavetheBall,0,0,
                                              0,0,0) 
    RequestedIntRow.FindStats()
    si = RequestedIntRow.INTsPosition + RequestedIntRow.Offset
    
    #si = 58                 #StartIndex of people who can intercept the ball
    PercIntCol = 5          #Column for the probability of intercepting for
    InterceptorNameCol = 2  #each defensive player.  Where to find the name
    InterceptorAveCol = 6   #and return average for each player who can 
    IntReturn = 0           #intercept.  Start with a return of 0
    
    TouchdownFlag = 0       #Assume no pick-6, initially
    TouchbackFlag = 0       #Assume no touchback, initially
    IResult = ""            #Initially, will fill in later
    
#Short passes travel between 0 and 5 yards, Mid Passes travel between 6 and 20 
#yards and long passes travel between 21 and 50 yards
    if PassLength == "Short":
        PassLengthinYards = random.randint(0,5)
    if PassLength == "Mid":
        PassLengthinYards = random.randint(6,20)
    if PassLength == "MidLong":
        PassLengthinYards = random.randint(12,25)
    if PassLength == "Long":
        PassLengthinYards = random.randint(21,50)

    YardLine += PassLengthinYards
    PassInterceptedAt = YardLine

        
#Who intercepts
    dice1 = random.randint(0,99)

#Select who will intercept the ball
    
    while dice1 >= TeamthatDoesNotHavetheBall.cell(row = si,
                                                   column=PercIntCol).value:
        si += 1
    Interceptor = TeamthatDoesNotHavetheBall.cell(row = si,
                                       column=InterceptorNameCol).value
    
#Test for a touchback
    if YardLine > 99:   #Touchback, this won't be used here
        YardLine = 80
        TouchbackFlag = 1
        IResult = "Touchback"
        
#If not touchback, determine length of return
    else:
        InterceptorAve = int(round(TeamthatDoesNotHavetheBall.cell(row = si,         #Read Ave
                                           column=InterceptorAveCol).value,0))

#Calculate INT return
        FirstRoll = random.randint(1,10)  #Int returns are divided into groups.   20% of ints are 
        if FirstRoll <= 2:                          #not returned. 30% of returns range from 0 yards to
            IntReturn = 0                           #the interceptor's return average.  30% of returns 
        elif FirstRoll <= 5:                       #range from 1 yard above the return ave to 10 yards
            
            IntReturn = random.randint(0,InterceptorAve)        #above the return ave.  The
        elif FirstRoll <=8:                                                      #remaining 20% of returns range 
            IntReturn = random.randint(InterceptorAve + 1,    #from 11 yards above the average 
                                       InterceptorAve + 10)                  #to 100 yards
        else:    
            IntReturn = random.randint(InterceptorAve + 11,100)         

        YardLine -= IntReturn   #Returns decrease the value of the Yardline        
        if YardLine <= 0:           #Pick-6, will be tested later so this won't be be used
            TouchdownFlag = 1 
            IResult = "Pick 6"
                
    #IntResult is a multi-type list
    # IntResult[0] indicates whether a Pick-6 or touchback occurred - this 
    #    will not be used in this revision
    # IntResult[1] is the name of the player that intercepted
    # IntResult[2] is the return yardage
    # IntResult[3] is the yard line - Not used in this revision
    # IntResult[4] is the yard line where the pass was intercepted
    # IntResult[5] is the int flag and by virtue of being here, will be 1
    
#Place Int results in a list and return the list to the calling routine
    IntResult = [IResult,Interceptor,IntReturn,YardLine,PassInterceptedAt,1]
     
    return IntResult


#-----------------------------------------------------------------------------
# Function Name:    KickBlock
# Purpose:          Handles all of the processing required to determine if a
#                   field goal or extra point is blocked and where the ball 
#                   ends up
# Author:           Rick Burney
# Created:          2/17/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
def KickBlock(TeamthatDoesNotHavetheBall,YardLine,KickFlag):
    
    import PickAPlayer  #Allows extraction of kick block stats
    import random       
    import YardageTable
    import openpyxl
    
#Note: KickFlag is zero for no forced block and 1 for forced block-added 
#1/19/2019

#Instantiate a class object that will allow the location of the row in the 
#defensive team's worksheet for kick block percentage
    RequestedKickBlockRow = \
        PickAPlayer.PickAPlayer(TeamthatDoesNotHavetheBall,0,0,0,0,0) 
    RequestedKickBlockRow.FindStats()
    KickBlockRow = RequestedKickBlockRow.DStatsPosition + \
        RequestedKickBlockRow.Offset
    
    PercentKickBlockColumn = 6  #Column of worksheet which determines the 
    KickBlockMessage = ""       #% of kicks that are blocked by the defense
    KickBlockFlag = 0          #If set, indicates that a kick has been blocked
    ProbNoReturnFG = 70     #On a blocked FG, the probability that there is no
                            #return.  Made this one up
    ProbNoReturnXPt = 90    #On a blocked extra point, the probability 
                            #that there is no return.  Made this one up
    ProbShortReturn = 75    #On a blocked kick, the probability 
                            #that there is a short return.  Made this one up
    BFGReturn = 0           #Initial assumption is that blocked FGs are not
    TDFlag = 0              #returned and therefore, there is no TD
    TestForaReturn = 0      #Flag to see if a blocked kick will be returned
    TestForaShortReturn = 0 #If a return, will it be short or long
    if YardLine > 50:                       #Adjust the yardline.  This is
        AdjustedYardLine = 100 - YardLine   #necesary because the ball is 
    else:                                   #kicked from 7 yards behind the
        AdjustedYardLine = YardLine         #LOS
    
#Extract kick block percentage from the defense
    KickBlockPercentage = TeamthatDoesNotHavetheBall.cell(row = KickBlockRow,
                                        column=PercentKickBlockColumn).value
        
#Test to see if the kick is blocked.
    KickBlockTest = random.randint(0,99)
    if (KickBlockTest < KickBlockPercentage) or (KickFlag == 1): #If blocked
        InitialYardLine = YardLine
        KickBlockFlag = 1                   #Set blocked flag and message
        KickBlockMessage = "Kick Blocked, "
               
#A blocked FG will always go somewhere.  It may go for a touchback. It may
#roll past the 20 which means YardLine will be adjusted to 80.  It may not
#make it to the 20 which means that YardLine will be where the ball stops.  It
#may be returned
        NewBallLocation = random.randint(-10,50)    
        YardLine += NewBallLocation              #Where the ball ends up        
        TestForaReturn = random.randint(0,99)    #See if there is a return   

#As longs as the ball does not go into the endzone (Ignoring Alabama vs 
#Auburn), the ball may be returned.  Note that this is the probability of not
#returning the blocked kick
        if (TestForaReturn >= ProbNoReturnFG) and (YardLine <= 99):  
                 
#See if it is a short return.  By the way, if it is a return for a touchdown,
#the return yardage is clamped by the yardline from where it was returned.
#Eliminates a 99 yard return that was scooped up at the 40 yardline
            TestForaShortReturn = random.randint(0,99)               
            TDYardage = YardLine                        #Clamp the return
            if TestForaShortReturn < ProbShortReturn:   #Short returns 
                BFGReturn = random.randint(0,25)        #range from 0 to                
            else:                                       #25 yards. Long
                BFGReturn = random.randint(0,100)    #returns go up to 100
                
            YardLine -= BFGReturn                   #Adjust the Yardline
        else:                                       #based upon the return
            KickBlockMessage += ", no return"   #Otherwise, no return
            
#If the ball ended up (prior to a return) inside of the defense's 20 yardline
#then the ball will be placed at the 20 and possession will change.  
        if YardLine > 80: 
            YardLine = 80   
            KickBlockMessage += ", ball goes to the 20"
        elif YardLine <= 0:                             #In this case, 
            TDFlag = 1                                  #returned for a TD
            KickBlockMessage += ", returned " + str(TDYardage) + \
                    " for a touchdown"

#Blocked field goal is returned.  Calculate where the ball ended up                
        else:                           
            if BFGReturn != 0:
                KickBlockMessage += ", returned " + str(BFGReturn) + " yards"
        if YardLine > 50:                   
            AdjustedYardLine = 100 - YardLine
        else:
            AdjustedYardLine = YardLine
            
#Form the kick block list and return list to calling program
    KickBlockResult = [KickBlockFlag,KickBlockMessage,YardLine,TDFlag,
                       AdjustedYardLine]    
    return KickBlockResult


#-----------------------------------------------------------------------------
# Function Name:    PuntBlock
# Purpose:          Handles all of the processing required to determine if a
#                   punt is blocked and where the ball ends up
# Inputs:           TeamthatDoesNotHavetheBall - Team on defense
#                   YardLine
# Outputs:          KickBlockMessage
#                   YardLine - Where the ball ends up
#                   PuntBlockFlag
# Author:           Rick Burney
#
# Created:          2/17/2017
# Copyright:        (c) Rick 2017
#-----------------------------------------------------------------------------
def PuntBlock(TeamthatDoesNotHavetheBall,YardLine,FBP):
    import random
    import YardageTable
    import openpyxl
    import PickAPlayer

#Instantiate a class object that will allow the location of the row in the 
#defensive team's worksheet for kick block percentage
    RequestedPuntBlockRow = \
        PickAPlayer.PickAPlayer(TeamthatDoesNotHavetheBall,0,0,0,0,0) 
    RequestedPuntBlockRow.FindStats()
    PuntBlockRow = RequestedPuntBlockRow.DStatsPosition + \
        RequestedPuntBlockRow.Offset
    
    #PuntBlockRow = 46 #Row of defense worksheet of kick block probability
    
    PercentPuntBlockColumn = 8
    
    PuntBlockMessage = ""
    PuntBlockFlag = 0
    ProbNoReturn = 50
    ProbShortReturn = 50    #50% of all punt returns are for short yardage.
    TDFlag = 0              #Initialize punt return TD flag
    if YardLine > 50:                       #Provide an initial value so no
        AdjustedYardLine = 100 - YardLine   #unreferenced variable error 
    else:                                   #occurs
        AdjustedYardLine = YardLine
    
#Extract punt block percentage from the defense    
    PuntBlockPercentage = TeamthatDoesNotHavetheBall.cell(row = PuntBlockRow,
                                        column=PercentPuntBlockColumn).value

#Test to see if the punt is blocked.  
    if random.randint(0,99) < PuntBlockPercentage:
        PuntBlockFlag = 1
        PuntBlockMessage = "Punt Blocked, "
        
#Determine where blocked punt ends before any return, if any
        NewBallLocation = random.randint(-30,0)

            
        YardLine += NewBallLocation             #Update YL
        TestForaReturn = random.randint(0,99)

        if (TestForaReturn >= ProbNoReturn) and (YardLine <= 99): #In case 
            TestForaShortReturn = random.randint(0,99)            #there is a
            if TestForaShortReturn < ProbShortReturn:             #return
                BPuntReturn = random.randint(0,25)
            else:
                BPuntReturn = random.randint(0,100)
            
            YardLine -= BPuntReturn
                    
        else:                       #No return
            PuntBlockMessage += "No return"
            BPuntReturn = 0
        if YardLine <= 0:           #Returned for a TD
            TDFlag = 1
            PuntBlockMessage += " Returned for a touchdown"
        else:
            TDFlag = 0
            PuntBlockMessage += " Returned " + str(BPuntReturn) + " yards"
    
#This may not be necessary
        if YardLine > 50:                                   #Adjust the yardline
            AdjustedYardLine = 100 - YardLine
        else:
            AdjustedYardLine = YardLine
                                                                      
#Note that there is no chance of a touchback so won't be handled.  Return the punt block
#results in a list
    PuntBlockResult = [PuntBlockFlag,PuntBlockMessage,YardLine,TDFlag,AdjustedYardLine]
    return PuntBlockResult


#-----------------------------------------------------------------------------
# Function Name:    WhoRecoverstheOnsideKick
# Purpose:               Determines whether the kicking team or the receiving team recovers an 
#                              onside kick - not sure why we need a function
# Inputs:           None
# Outputs:         OnsideKickRecoveryFlag
#                       0 if kicking team recovers (low probability)
#                       1 if receiving team recovers (High probability
# Author:           Rick Burney
# Created:          2/19/2017
# Copyright:       (c) Rick 2017
#-----------------------------------------------------------------------------
def WhoRecoverstheOnsideKick():
    import random

#from http://archive.advancedfootballanalytics.com/2009/09/onside-kicks.html    
    PercentageOfSuccessfulOnsideKicks = 20 
    OnsideKickRecoveryFlag = 0                      #Initialize the recovery flag so that it is 
                                                                      #unsuccessful 
        
#Test to see if the onside kick is successful
    if random.randint(0,99) < PercentageOfSuccessfulOnsideKicks:
        OnsideKickRecoveryFlag = 1    
    return OnsideKickRecoveryFlag   #Return the flag