#1/7/2019  Updated penalties and penalty stats.  Data source is from the NFL
#because I could not find what I wanted from any college sources - 
#https://www.pro-football-reference.com/years/2018/penalties.htm

#-----------------------------------------------------------------------------
# Method Name:    Penalty
# Purpose:             Divides penalties into offensive run, offensive pass, defensive run and
#                           defensive pass.  Penalties on kicks could come later but not likely
# Inputs:               HTeamPenaltyStats - probability of a penalty on any play for the home
#                           team 
#                           VTeamPenaltyStats - probability of a penalty on any play for the visiting
#                           team 
#                           TeamWiththeBallFlag - Indicates which team is on offense                 
#                           PlayType - Run or Pass
#                           YardsonthePlay - Used on spot fouls to determine where the ball will be
#                           placed if the penalty is accepted
#                           PassResult - Used for penalties such as intentional grounding and DPI
#                           ForcePenaltyFlag - Used for debugging
#                           PassLength - Used for spot foul penalties
# Outputs:             PenaltyList - List containing the following elements
#                           PenaltyList[0] = Penalty that was called, string
#                           PenaltyList[1] = Presnap penalty flag, 0 if no presnap, 1 if presnap
#                           PenaltyList[2] = Automatic First Down Flag, N/A for these types of
#                                                    penalties
#                           PenaltyList[3] = Loss of down flag, N/A on running plays
#                           PenaltyList[4] = Penalty yardage, negative if it is on the offense
#                           PenaltyList[5] = Penalty Called flag, 0 if no penalty, 1 if penalty
#                           PenaltyList[6] = Dead ball foul, 1 = dead ball foul
# Author:              Rick Burney
# Created:            Sometime in February, 2017
# Copyright:         (c) Rick 2017
#-----------------------------------------------------------------------------
def Penalty(HTeamPenaltyStats,VTeamPenaltyStats,TeamWiththeBallFlag,PlayType,
            YardsonthePlay,PassResult,ForcePenaltyFlag,PassLength):
    
    import random               #A lot of this uses pseudorandom numbers
    import sys                      #It would be interesting to see what would happen if the next 3 
    import Tkinter                #imports are commented out
    import tkMessageBox
       
    PenaltyFlag = 0                       #Intialize objects
    PenaltyOnThe = ""
    PenaltyList = ["X",0,0,0,0,0,0]
    
#Test for a penalty.  The probability of a penalty is the average of the 2 
#teams statistical penalties per game.  Really need a better way of doing this
    ProbabilityofaPenalty = (HTeamPenaltyStats + VTeamPenaltyStats) / 2
    dice1 = random.randint(0,99)
    #print(dice1, "    ",ProbabilityofaPenalty)
#****************FORCE PLAY CODE - REMOVE WHEN DEBUGGED****************
    #if ForcePenaltyFlag == 1:       #This flag is a debug mechanism to force a penalty
        #dice1 = 0                  
#****************FORCE PLAY DEBUG CODE - REMOVE WHEN DEBUGGED****************
        
    if dice1 <= ProbabilityofaPenalty:  #If there is a penalty, set the penalty flag
        PenaltyFlag = 1                 
        
#See if offense or defense.  
        X10HTeamPenaltyStats = round(10 * HTeamPenaltyStats,0)
        X10VTeamPenaltyStats = round(10 * VTeamPenaltyStats,0)
        SumTeamPenaltyStats = X10HTeamPenaltyStats + X10VTeamPenaltyStats
        
#Remember, TeamWiththeBallFlag = 0 means Home Team is on offense.  This is 
#required to test if a penalty is on the offense or the defense.  You add up
#the probabilities of a penalty for both teams, multiply by 10 to get an
#integer to set the max limit of the random.randint function and then use
#either the Home Team penalty probability as the test limit or the Visiting
#Team  based on the setting of TeamWiththeBallFlag.  
        if TeamWiththeBallFlag == 0:
            ProbabilityPenaltyOnOffense = X10HTeamPenaltyStats
        else:
            ProbabilityPenaltyOnOffense = X10VTeamPenaltyStats
        dice1 = random.randint(1,SumTeamPenaltyStats)

#****************FORCE PLAY DEBUG CODE - REMOVE WHEN DEBUGGED****************
    #if ForcePenaltyFlag == 1:                                  #For this go-around, penalty is on defense
        #dice1 =    ProbabilityPenaltyOnOffense + 1              
#****************FORCE PLAY DEBUG CODE - REMOVE WHEN DEBUGGED****************
        
        if dice1 <= ProbabilityPenaltyOnOffense:    #Penalty on O or D 
            PenaltyOnThe = "Offense"
        else:
            PenaltyOnThe = "Defense"


#Run or pass play penalty.  Kicks will come later but this is where we will
#start for kicks.  Need to pass in a kick flag.
        if (PlayType == "Run") and (PenaltyOnThe == "Offense"):
            PenaltyList = ORunLUT(ForcePenaltyFlag)
        if (PlayType == "Pass") and (PenaltyOnThe == "Offense"):
            PenaltyList = OPassLUT(ForcePenaltyFlag)

#Intentional grounding only makes sense if the pass is incomplete
            if ((PenaltyList[0] == "Intentional Grounding") or \
                (PenaltyList[0] == "Facemask by the Defense")) and \
               (PassResult != "Incomplete"):
                PenaltyFlag = 0
                
#Call penalty method based on whethe its on the O or D, and whether it occurs
#during a run or pass play
        if (PlayType == "Run") and (PenaltyOnThe == "Defense"):
            PenaltyList = DRunLUT(ForcePenaltyFlag)
        if (PlayType == "Pass") and (PenaltyOnThe == "Defense"):
            PenaltyList = DPassLUT(YardsonthePlay,PassLength,PassResult,
                                   ForcePenaltyFlag)
        if (PlayType == "Kickoff") and (PenaltyOnThe == "Offense"):
            PenaltyList = KickingTeamLUT(ForcePenaltyFlag)
        if (PlayType == "Kickoff") and (PenaltyOnThe == "Defense"):
            PenaltyList = KickingTeamLUT(ForcePenaltyFlag)

        PenaltyList.append(PenaltyFlag)                 #Penalty List is what
                                                        #is returned to
                                                        #calling program        
        if abs(PenaltyList[4]) > 15:                #Stupid trick to see if
            PenaltyList[4] = int(PenaltyList[4]/10) #penalty should be added
                                                    #after the play
            AfterthePlay = 1 #Flag that indicates that penalty yardage is 
                             #applied after the play
        else:
            AfterthePlay = 0
        PenaltyList.append(AfterthePlay)    #Add dead ball flag to returned
                                            #list
#Can't have a PI if there is a sack because no pass is thrown                                            
        if ((PenaltyList[0] == "Pass Interference on the Defense") or\
           (PenaltyList[0] == "Pass Interference on the Offense")) and\
           (PassResult == "Sack"):
            PenaltyList[1] = PenaltyList[5] = 0

    return PenaltyList


#-----------------------------------------------------------------------------
# Method Name:    ORunLUT
# Purpose:        Lookup Table for a penalty on the offense during a run play
# Inputs:       
# Outputs:        PenaltyList - List containing the following elements
#                      PenaltyList[0] = Penalty that was called, string
#                      PenaltyList[1] = Presnap penalty flag, 0 if no presnap, 
#                                                             1 if presnap
#                      PenaltyList[2] = Automatic First Down Flag, N/A for 
#                                       these types of penalties
#                      PenaltyList[3] = Loss of down flag, N/A on running plays
#                      PenaltyList[4] = Penalty yardage, negative since it is 
#                                       on the offense 
#                      PenaltyList[5] = Penalty Called flag, 0 if no penalty, 
#                                                            1 if penalty
#                      PenaltyList[6] = Dead ball foul, 1 = dead ball foul
# Author:         Rick Burney
#
# Created:        Sometime in February, 2017
# Copyright:      (c) Rick 2017
#-----------------------------------------------------------------------------
def ORunLUT(ForcePenaltyFlag):
    import random
    
#Offensive Run Occurences - sum of occurrences sets max on random function
#Probabilities for each penalty type where derived somewhere from the web
    Holding = 34
    HandstotheFace = 3
    Unsportsmanlike = 2
    IllegalShift = 2
    FalseStart = 26
    DelayofGame = 6
    PersonalFoul = 2
    IllegalFormation = 3
    IllegalSubstitution = 0
    IllegalBlock = 9
    DeadBallPersonalFoul = 5
    
    PenaltyCalled = ""          #Initialize objects
    PreSnapFlag = 0             
    AutomaticFirstDownFlag = 0
    LossofDownFlag = 0
    YardsifPenaltyAccepted = 0

    SumofOccurrences = Holding + HandstotheFace + Unsportsmanlike + \
        IllegalShift + FalseStart + DelayofGame + PersonalFoul + \
        IllegalFormation + IllegalSubstitution + IllegalBlock + \
        DeadBallPersonalFoul
    
    dice1 = random.randint(1,SumofOccurrences)
    
    if dice1 <= Holding:                            #Penalty yardage will 
        PenaltyCalled = "Holding on the Offense"    #always be assessed from
        PreSnapFlag = 0                             #the original LOS and not
        AutomaticFirstDownFlag = 0                  #from where the holding 
        LossofDownFlag = 0                          #occurred - future upgrade
        YardsifPenaltyAccepted = -10
    elif dice1 <= Holding + HandstotheFace:         
        PenaltyCalled = "Personal Foul on the Offense, Hands to the Face"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0      #Penalty yardage assessed from
        LossofDownFlag = 0              #original line of scrimmage
        YardsifPenaltyAccepted = -15
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike:
        PenaltyCalled = "Unsportsmanlike Conduct on the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0      #Dead ball foul
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -150   
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift:
        PenaltyCalled = "Illegal Shift by the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0  #Motion before the snap
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift + \
         FalseStart:
        PenaltyCalled = "False Start"
        PreSnapFlag = 1
        AutomaticFirstDownFlag = 0  #Presnap Penalty
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift \
         + FalseStart + DelayofGame:
        PenaltyCalled = "Delay of Game by the Offense"  #Presnap Penalty
        PreSnapFlag = 1
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift \
         + FalseStart + DelayofGame + PersonalFoul:
        PenaltyCalled = "Personal Foul by the Offense"  #This covers a variety 
        PreSnapFlag = 0                                 #of penalties but is 
        AutomaticFirstDownFlag = 0                      #not a dead ball
        LossofDownFlag = 0                              #foul 
        YardsifPenaltyAccepted = -15
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift \
         + FalseStart + DelayofGame + PersonalFoul + IllegalFormation:
        PenaltyCalled = "Illegal Formation by the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift \
         + FalseStart + DelayofGame + PersonalFoul + IllegalFormation + \
         IllegalSubstitution:
        PenaltyCalled = "Illegal Substitution by the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift \
         + FalseStart + DelayofGame + PersonalFoul + IllegalFormation + \
         IllegalSubstitution + IllegalBlock:
        PenaltyCalled = "Illegal Block by the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -15
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift \
         + FalseStart + DelayofGame + PersonalFoul + IllegalFormation + \
         IllegalSubstitution + IllegalBlock + DeadBallPersonalFoul:
        PenaltyCalled = "Dead Ball Personal Foul by the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -150

    else:
        print("Fell through")

#Return penalty list    
    PenaltyList = [PenaltyCalled, PreSnapFlag, AutomaticFirstDownFlag, 
                   LossofDownFlag, YardsifPenaltyAccepted]
    
    return PenaltyList


#-----------------------------------------------------------------------------
# Method Name:    OPassLUT
# Purpose:        Lookup Table for a penalty on the offense during a pass play
# Inputs:       
# Outputs:        PenaltyList - List containing the following elements
#                      PenaltyList[0] = Penalty that was called, string
#                      PenaltyList[1] = Presnap penalty flag, 0 if no presnap, 
#                                                             1 if presnap
#                      PenaltyList[2] = Automatic First Down Flag, N/A for 
#                                       these types of penalties
#                      PenaltyList[3] = Loss of down flag, N/A on running plays
#                      PenaltyList[4] = Penalty yardage, negative since it is 
#                                       on the offense 
#                      PenaltyList[5] = Penalty Called flag, 0 if no penalty, 
#                                                            1 if penalty
#                      PenaltyList[6] = Dead ball foul, 1 = dead ball foul
# Author:         Rick Burney
#
# Created:        Sometime in February, 2017
# Copyright:      (c) Rick 2017
#-----------------------------------------------------------------------------
def OPassLUT(ForcePenaltyFlag):
    import random    
    
#Offensive Pass Occurences - sum of occurrences sets max on random function
#Will revisit types of penalties and penalty frequency
    Holding = 34        #10 yard penalty against the offense.  IMPLEMENT - 
                        #HOLDING IN THE ENDZONE
    HandstotheFace = 3  #DEAD BALL FOUL on defense, 15 yards from LOS offense
    Unsportsmanlike = 2 #DEAD BALL FOUL
    IllegalShift = 2    #Offensive player is not set before the snap
    FalseStart = 26                 #Presnap penalty
    IllegalForwardPass = 3          #QB is over the LOS or illegal touching
    IneligibleReceiverDownfield = 0 #Covered under illegal forward pass
    ChopBlock = 0                   #Does not happen enough
    PassInterference = 11            #Specific to pass
    IntentionalGrounding = 3        #Specific to pass
    DelayofGame = 6
    PersonalFoul = 2
    IllegalFormation = 3
    IllegalSubstitution = 0
    IllegalBlock = 9
    DeadBallPersonalFoul = 5
    
    PenaltyCalled = ""
    PreSnapFlag = 0
    AutomaticFirstDownFlag = 0
    LossofDownFlag = 0
    YardsifPenaltyAccepted = 0

    SumofOccurrences = Holding + HandstotheFace + Unsportsmanlike + \
        IllegalShift + FalseStart + DelayofGame + PersonalFoul + \
        IllegalFormation + IllegalSubstitution + IllegalForwardPass + \
        IneligibleReceiverDownfield + ChopBlock\
        + PassInterference + IntentionalGrounding + IllegalBlock + \
        DeadBallPersonalFoul


    dice1 = random.randint(1,SumofOccurrences)  

    if dice1 <= Holding:                            
        PenaltyCalled = "Holding on the Offense"    
        PreSnapFlag = 0                             
        AutomaticFirstDownFlag = 0                  
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -10
    elif dice1 <= Holding + HandstotheFace:
        PenaltyCalled = "Personal Foul on the Offense, Hands to the Face"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0  #Assessed from original LOS
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -15 
        
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike:
        PenaltyCalled = "Unsportsmanlike Conduct on the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -150   #Dead ball foul
        
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift:
        PenaltyCalled = "Illegal Shift by the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift + \
         FalseStart:
        PenaltyCalled = "False Start"
        PreSnapFlag = 1                 #Pre-snap penalty
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift + \
         FalseStart + DelayofGame:
        PenaltyCalled = "Delay of Game by the Offense"
        PreSnapFlag = 1                                 #Pre-snap penalty
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift + \
         FalseStart + DelayofGame + PersonalFoul:
        PenaltyCalled = "Personal Foul by the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0      #A variety of different personal foul
        LossofDownFlag = 0              #penalties that are all dead ball 
        YardsifPenaltyAccepted = -150
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift + \
         FalseStart + DelayofGame + PersonalFoul + IllegalFormation:
        PenaltyCalled = "Illegal Formation by the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift + \
         FalseStart + DelayofGame + PersonalFoul + IllegalFormation + \
         IllegalSubstitution:
        PenaltyCalled = "Illegal Substitution by the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift + \
         FalseStart + DelayofGame + PersonalFoul + IllegalFormation + \
         IllegalSubstitution + IllegalForwardPass:
        PenaltyCalled = "Illegal Forward Pass by the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift + \
         FalseStart + DelayofGame + PersonalFoul + IllegalFormation + \
         IllegalSubstitution + IllegalForwardPass + \
         IneligibleReceiverDownfield: 
        PenaltyCalled = "Ineligible Receiver Downfield"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift + \
         FalseStart + DelayofGame + PersonalFoul + IllegalFormation + \
         IllegalSubstitution + IllegalForwardPass + \
         IneligibleReceiverDownfield + ChopBlock: 
        PenaltyCalled = "Chop Block"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0  #Assessed from the original LOS
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -15
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift + \
         FalseStart + DelayofGame + PersonalFoul + IllegalFormation + \
         IllegalSubstitution + IllegalForwardPass + \
         IneligibleReceiverDownfield + ChopBlock + PassInterference: 
        PenaltyCalled = "Pass Interference on the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0  #Assessed from original LOS
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -15
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift + \
         FalseStart + DelayofGame + PersonalFoul + IllegalFormation + \
         IllegalSubstitution + IllegalForwardPass + \
         IneligibleReceiverDownfield + ChopBlock + PassInterference + \
         IntentionalGrounding:
        PenaltyCalled = "Intentional Grounding"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 1
        SpotoftheFoul = random.randint(-10,-3)
        YardsifPenaltyAccepted = SpotoftheFoul
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift + \
         FalseStart + DelayofGame + PersonalFoul + IllegalFormation + \
         IllegalSubstitution + IllegalForwardPass + \
         IneligibleReceiverDownfield + ChopBlock + PassInterference + \
         IntentionalGrounding + IllegalBlock:
        PenaltyCalled = "Illegal Block by the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -15
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + IllegalShift + \
         FalseStart + DelayofGame + PersonalFoul + IllegalFormation + \
         IllegalSubstitution + IllegalForwardPass + \
         IneligibleReceiverDownfield + ChopBlock + PassInterference + \
         IntentionalGrounding + IllegalBlock+ DeadBallPersonalFoul:
        PenaltyCalled = "Dead Ball Personal Foul by the Offense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -150        
    PenaltyList = [PenaltyCalled, PreSnapFlag, AutomaticFirstDownFlag, 
                   LossofDownFlag, YardsifPenaltyAccepted]
    return PenaltyList



#-----------------------------------------------------------------------------
# Method Name:    DRunLUT
# Purpose:        Lookup Table for a penalty on the defense during a run play
# Inputs:       
# Outputs:        PenaltyList - List containing the following elements
#                      PenaltyList[0] = Penalty that was called, string
#                      PenaltyList[1] = Presnap penalty flag, 0 if no presnap, 
#                                                             1 if presnap
#                      PenaltyList[2] = Automatic First Down Flag
#                      PenaltyList[3] = Loss of down flag, N/A on running plays
#                      PenaltyList[4] = Penalty yardage, negative since it is 
#                                       on the offense 
#                      PenaltyList[5] = Penalty Called flag, 0 if no penalty, 
#                                                            1 if penalty
#                      PenaltyList[6] = Dead ball foul, 1 = dead ball foul
# Author:         Rick Burney
#
# Created:        Sometime in February, 2017
# Copyright:      (c) Rick 2017
#-----------------------------------------------------------------------------
def DRunLUT(ForcePenaltyFlag):
    import random
    
#Defensive Run Occurences - sum of occurrences sets max on random function
    Holding = 0
    HandstotheFace = 5
    FaceMask = 9            #Add to sum and individual test
    Unsportsmanlike = 5
    NeutralZoneInfraction = 5  #Add to sum and individual test
    DelayofGame = 0
    PersonalFoul = 0   #Need to determine which personal fouls are dead ball
    Offside = 30             #Add to sum and individual test
    IllegalSubstitution = 5
    DeadBallPersonalFoul = 12
    
    PenaltyCalled = ""  #Innitialize penalty list objects
    PreSnapFlag = 0
    AutomaticFirstDownFlag = 0
    LossofDownFlag = 0
    YardsifPenaltyAccepted = 0
    
#Set the max against which the test to determine the type of defensive run
#penalty has occurred
    SumofOccurrences = Holding + HandstotheFace + Unsportsmanlike + \
        PersonalFoul + IllegalSubstitution + FaceMask + NeutralZoneInfraction\
        + Offside + DeadBallPersonalFoul
    dice1 = random.randint(1,SumofOccurrences)     #See which penalty occurred 

#****************FORCE PLAY DEBUG CODE - REMOVE WHEN DEBUGGED****************
    #print(ForcePenaltyFlag)
    #if ForcePenaltyFlag == 1:       #This flag is a debug mechanism to force a penalty
        #dice1=  Holding+ HandstotheFace -1
        #PersonalFoul + IllegalSubstitution + FaceMask -  1 
        #print("dice1 = ", dice1)
#****************FORCE PLAY DEBUG CODE - REMOVE WHEN DEBUGGED****************


    if dice1 <= Holding:                            #Defensive holding is 10
        PenaltyCalled = "Holding on the Defense"    #yards and an automatic 
        PreSnapFlag = 0                             #1st down if accepted
        AutomaticFirstDownFlag = 1
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 10
        
#Hands to the face is 15 yards and an automatic 1st down if accepted.  
#DEAD BALL FOUL
    elif dice1 <= Holding + HandstotheFace: 
        PenaltyCalled = "Personal Foul on the Defense, Hands to the Face"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 1
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 150
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike:       #Dead ball
        PenaltyCalled = "Unsportsmanlike Conduct on the Defense"    #foul.
        PreSnapFlag = 0                                             #Assessed
        AutomaticFirstDownFlag = 1  #after the play.  15 yards against the D
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 150    #Set to 150 to tell Penalty() that a 
                                        #dead ball foul has occurred and to 
                                        #divide the 150 by 10 to get a 15 yard
                                        #penalty against the D
                                        
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + PersonalFoul:
        PenaltyCalled = "Personal Foul by the Defense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 1      #Late hits, out of bounds hits
        LossofDownFlag = 0              #eVentually will include targeting
        YardsifPenaltyAccepted = 150
        
#Illegal substitution by the D.  Usually means someone did not get off the 
#field in time
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + PersonalFoul + \
         IllegalSubstitution:
        PenaltyCalled = "Illegal Substitution by the Defense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 5
        
#Facemask penalty is considered a dead ball foul.  Penalty yards of 150 is a
#trick to tell the calling method that this is a dead ball foul, the 150 will
#be divided by 10 to get a 15 yard penalty against the defense
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + PersonalFoul + \
         IllegalSubstitution + FaceMask:
        PenaltyCalled = "Facemask by the Defense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 1
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 150    #Will be divided by 10 to get 15 yards
        
#Presnap version of defensive offsides
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + \
         PersonalFoul + IllegalSubstitution + FaceMask + \
         NeutralZoneInfraction:
        PenaltyCalled = "Neutral Zone Infraction by the Defense"
        
        PreSnapFlag = 1             #Presnap penalty
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 5
        
#Just offsides
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + PersonalFoul + \
         IllegalSubstitution + FaceMask + NeutralZoneInfraction + Offside:
        PenaltyCalled = "Offside on the Defense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 5

    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + PersonalFoul + \
         IllegalSubstitution + FaceMask + NeutralZoneInfraction + Offside + \
         DeadBallPersonalFoul:
        PenaltyCalled = "Dead Ball Personal Foul by the Defense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 1
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 150        
    else:
        print("Fell through.")

#Return penalty info to main Penalty method
    PenaltyList = [PenaltyCalled, PreSnapFlag, AutomaticFirstDownFlag, 
                   LossofDownFlag, YardsifPenaltyAccepted]
    
    return PenaltyList


#-----------------------------------------------------------------------------
# Method Name:    DPassLUT
# Purpose:        Lookup Table for a penalty on the defense during a pass play
# Author:         Rick Burney
# Created:        Sometime in February, 2017
# Copyright:      (c) Rick 2017
# Objects passed in: YardsonthePlay - Needed for DPI
#                    PassLength - Needed for DPI
#                    PassResult - Needed fpr DPI
#                    ForcePenaltyFlag - If set, allows for a specific penalty
#                                       to occur - used for debug
#-----------------------------------------------------------------------------
def DPassLUT(YardsonthePlay,PassLength,PassResult,ForcePenaltyFlag):
    
    import random       #Used to pick a defensive penalty on a pass play
    import Tkinter      #Used for debug
    import tkMessageBox #Used for debug
    
#Defensive Pass Occurences - sum of occurrences sets max on random function
    Holding = 24
    HandstotheFace = 5
    FaceMask = 9            
    Unsportsmanlike = 4
    NeutralZoneInfraction = 5  
    DelayofGame = 0
    PersonalFoul = 0
    Offside = 30             
    IllegalSubstitution = 5
    PassInterference = 27   #Add to sum and individual test
    DeadBallPersonalFoul = 12
    RoughingThePasser = 11
    
    PenaltyCalled = ""  #Initialize objects
    PreSnapFlag = 0
    AutomaticFirstDownFlag = 0
    LossofDownFlag = 0
    YardsifPenaltyAccepted = 0

    SumofOccurrences = Holding + HandstotheFace + Unsportsmanlike + \
        PersonalFoul + IllegalSubstitution + FaceMask + NeutralZoneInfraction\
        + Offside + PassInterference + DeadBallPersonalFoul + \
        RoughingThePasser
    
    dice1 = random.randint(1,SumofOccurrences)
    #if ForcePenaltyFlag == 1:
        #dice1 = Holding + HandstotheFace + Unsportsmanlike + \
        #PersonalFoul + IllegalSubstitution + FaceMask
#****************FORCE PLAY DEBUG CODE - REMOVE WHEN DEBUGGED****************
    #if ForcePenaltyFlag == 1:       #This flag is a debug mechanism to force a penalty
        #dice1=  Holding + HandstotheFace -1
        #PersonalFoul + IllegalSubstitution + FaceMask -  1 
#****************FORCE PLAY DEBUG CODE - REMOVE WHEN DEBUGGED****************
        
    if dice1 <= Holding:                            #Defensive holding,
        PenaltyCalled = "Holding on the Defense"    #automatic 1st down
        PreSnapFlag = 0                             #10 yards assessed
        AutomaticFirstDownFlag = 1
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 10
    elif dice1 <= Holding + HandstotheFace: #Hands to the Face, automatic
                                            #1st down - dead ball foul
        
        PenaltyCalled = "Personal Foul on the Defense, Hands to the Face"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 1
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 150
        
#Dead ball foul.  Refer to other comments about 150 yard trick
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike:
        PenaltyCalled="Unsportsmanlike Conduct on the Defense-Dead Ball Foul"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 1
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 150
        
#Dead ball foul
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + PersonalFoul:
        PenaltyCalled = "Personal Foul by the Defense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 1
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 150
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + PersonalFoul + \
         IllegalSubstitution:
        PenaltyCalled = "Illegal Substitution by the Defense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + PersonalFoul + \
         IllegalSubstitution + FaceMask:
        PenaltyCalled = "Facemask by the Defense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 1  #Dead ball foul
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 150
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + PersonalFoul + \
         IllegalSubstitution + FaceMask + NeutralZoneInfraction:
        PenaltyCalled = "Neutral Zone Infraction by the Defense"
        PreSnapFlag = 1
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + PersonalFoul + \
         IllegalSubstitution + FaceMask + NeutralZoneInfraction + Offside:
        PenaltyCalled = "Offside on the Defense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 5
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + PersonalFoul + \
         IllegalSubstitution + FaceMask + NeutralZoneInfraction + Offside + \
         PassInterference:
        PenaltyCalled = "Pass Interference on the Defense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 1
        LossofDownFlag = 0     
        
#Logic here is that if pass is incomplete, determine the length of the pass.  
#If over 15 yards, then penalty is 15 yards.  Otherwise spot of the ball.  If
#pass is completed, do the same thing.  Make sure DPI can only occur on passes
#and not runs or sacks.  
        if PassResult == "Incomplete":  #Compute length of pass 
            if PassLength == "Short":
                YardsonthePlay = random.randint(0,10)   #YardsonthePlay is
            elif PassLength == "Mid":                   #passed in so should
                YardsonthePlay = random.randint(10,20)  #be local
            elif PassLength == "MidLong":
                YardsonthePlay = random.randint(15,25)
            else:
                YardsonthePlay = random.randint(20,40)

        if YardsonthePlay > 15:
            YardsifPenaltyAccepted = 15
        else:
            YardsifPenaltyAccepted = YardsonthePlay
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + PersonalFoul + \
         IllegalSubstitution + FaceMask + NeutralZoneInfraction + Offside + \
         PassInterference + DeadBallPersonalFoul:
        PenaltyCalled = "Dead Ball Personal Flag on the Defense"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 1
        LossofDownFlag = 0     
        YardsifPenaltyAccepted = 150
    elif dice1 <= Holding + HandstotheFace + Unsportsmanlike + PersonalFoul + \
         IllegalSubstitution + FaceMask + NeutralZoneInfraction + Offside + \
         PassInterference + DeadBallPersonalFoul + RoughingThePasser:
        PenaltyCalled = "Roughing the Passer"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 1
        LossofDownFlag = 0     
        YardsifPenaltyAccepted = 150
    else:
        print("Fell through")
    
    PenaltyList = [PenaltyCalled, PreSnapFlag, AutomaticFirstDownFlag, 
                   LossofDownFlag, YardsifPenaltyAccepted]
    
    return PenaltyList


def ForcePenalty(HTeamPenaltyStats,VTeamPenaltyStats,TeamWiththeBallFlag,
                 PlayType,YardsonthePlay):
    import random
    
    PenaltyList = ["False Start", 1, 0, 
                   0, -5,1]
    
    return PenaltyList


#NOT IN USE AT THIS TIME
#-----------------------------------------------------------------------------
# Method Name:    KickingTeamLUT
# Purpose:        Lookup Table for a penalty on the kicking team during a 
#                 kickoff.  All penalties are dead ball
# Author:         Rick Burney
# Created:        1/28/2018
# Copyright:      (c) Rick 2018
#-----------------------------------------------------------------------------
def KickingTeamLUT(ForcePenaltyFlag):
    import random
    
#Kickoff penalty occurences - sum of occurrences sets max on random function
    Unsportsmanlike = 4
    Offside = 4
    PersonalFoul = 8
    Facemask = 8
    
    PenaltyCalled = ""  #Initialize objects
    PreSnapFlag = 0
    AutomaticFirstDownFlag = 0
    LossofDownFlag = 0
    YardsifPenaltyAccepted = 0

    SumofOccurrences = Unsportsmanlike + Offside + PersonalFoul + Facemask
    
    dice1 = random.randint(1,SumofOccurrences)

#Determine what kind of penalty occurred and set flags and penalty yardage  
    if dice1 <= Unsportsmanlike:                            
        PenaltyCalled = "Unsportsmanlike Conduct on the Kicking Team"    
        PreSnapFlag = 0                             
        AutomaticFirstDownFlag = 1                  
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 150        #Dead ball foul
    elif dice1 <= Unsportsmanlike + Offside:
        PenaltyCalled = "Offside on the Kicking Team"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 0
        LossofDownFlag = 0
        YardsifPenaltyAccepted = -50
    elif dice1 <= Unsportsmanlike + Offside + PersonalFoul:
        PenaltyCalled = "Personal Foul on the Kicking Team"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 1
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 150   
    elif dice1 <= Unsportsmanlike + Offside + PersonalFoul + Facemask:
        PenaltyCalled = "Facemask by the Kicking Team"
        PreSnapFlag = 0
        AutomaticFirstDownFlag = 1
        LossofDownFlag = 0
        YardsifPenaltyAccepted = 150
    else:
        print("Fell through.")

#Return penalty list    
    PenaltyList = [PenaltyCalled, PreSnapFlag, AutomaticFirstDownFlag, 
                   LossofDownFlag, YardsifPenaltyAccepted]
    
    return PenaltyList


