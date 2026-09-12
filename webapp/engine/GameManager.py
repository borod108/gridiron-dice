#Fully Commented
#-----------------------------------------------------------------------------
# Function Name:    RunningPlay
# Purpose:          Based upon what position is running the ball, select a   
#                   running play that suits the position
#                   Ultimately will add intelligence so that the probability
#                   of running a particular type of play depends on the down
#                   and yards to go.  Also, ultimately will convert this to a
#                   class
# Author:           Rick Burney
# Created:          12/13/2016
# Copyright:        (c) Rick 2016
# Inputs:     RunnerType:    If a running play, this can either be an "RB", a
#                            a "QB" or a "WR".  If a pass play, this can 
#                            either be an "RB" or a "Receiver".  Why it is a
#                            "WR" for running plays and a "Receiver" for pass
#                            plays will remain one of the great mysteries of
#                            the universe but it would be a lot of work to
#                            change this just for the sake of consistency
#             YardsToGo:     Self explanatory but used by this method to 
#                            prevent QB sneaks from anything more than 1 yard
#                            to go.
#-----------------------------------------------------------------------------
def RunningPlay(RunnerType,YardstoGo):
    import random    
   
    #Running plays depends on who is running the ball
    # If it is an RB, then there are 7 plays (no wildcat yet)
    #     1)Up the middle
    #     2)off-tackle right
    #     3)off-tackle left
    #     4)Sweep right
    #     5)Sweep left
    #     6)Pitch right
    #     7)Pitch left
    # If it is a QB, there are 4 plays
    #     1)Sneak if YardstoGo = 1
    #     2)Designed QB run or QB draw
    #     3)Bootleg
    #     4)Scramble which means that although a run was called, the 
    #          implication is that a pass play was called but the QB was forced to run
    # If it is a WR, there are 2 plays
    #     1)Jet sweep right
    #     2)Jet sweep left
    
#Call play based upon the position of the player with the ball
    if RunnerType == "RB":                                                                              #7 running plays                                                         
        dice1 = random.randint(0,6)                                                                  #Roll the dice

#These are the possible running plays
        RunTypeList = ["Up the Middle", "Off-Tackle Right", "Off-Tackle Left","Sweep Right","Sweep Left", 
                       "Pitch Right", "Pitch Left"]
        RunType = RunTypeList[dice1]        #Use the dice results to pick a running play
    if RunnerType == "QB":                       #The runner is the QB
        if YardstoGo == 1:                          #QB sneaks occur only if the YTG is 1
            RunType = "Sneak"                      #So if the runner is the QB and the YTG is 1, then it is a QB sneak
        else:                                               #Other types of QB runs
            dice1 = random.randint(0,2)                                              #If YTG > 1
            RunTypeList = ["Designed QB Run", "Bootleg", "Scramble"]  #These are the other types of QB runs
            RunType = RunTypeList[dice1]
    if RunnerType == "WR":                                              #WRs do jet sweeps
        dice1 = random.randint(0,1)                                   #Two types of jet sweep
        RunTypeList = ["Jet sweep right", "Jet Sweep Left"]  #Left or right
        RunType = RunTypeList[dice1]                               #Pick one
    return RunType                                                    #Return the running play chosen to the calling routine


#-----------------------------------------------------------------------------
# Function Name:    PassPlay
# Purpose:          Based upon what position is the target of the pass, select a pass play that
#                        suits the position                   
# Author:           Rick Burney
# Created:          12/13/2016
# Copyright:       (c) Rick 2016
#-----------------------------------------------------------------------------
def PassPlay(ReceiverType,YardLine,HailMary):
    import random
    
    global PassLength   #short, mid, mid/long and deep
    
#Passing plays depends on to whom the ball is thrown 
    # If it is a RB, there are 4 types of passes
    #     1)Screen
    #     2)Flare
    #     3)Over-the-Middle
    #     4)Wheel route
    # If it is a WR or TE, there are 7 types of passes
    #     1)Bubble Screen
    #     2)Slant
    #     3)Hitch
    #     4)In
    #     5)Out
    #     6)Post
    #     7)Deep

#Determine pass play and identify if it is a short, mid or long pass
    if ReceiverType == "RB":                                                                #Running back?
        dice1 = random.randint(0,3)
        PassTypeList = ["Screen", "Flare", "Over-the-Middle","Wheel Route"]
        if dice1 <= 2:                #75% of the passes to RBs are short. 
            PassLength = "Short"      #The mid-length pass is a wheel route
        if dice1 == 3:
            PassLength = "Mid"    
        PassType = PassTypeList[dice1]
    if ReceiverType == "Receiver":
        if YardLine >= 90:          #If within opponent's 10 yardline, don't
            DiceMax = 5             #throw a deep pass
        else:
            DiceMax = 6                     #Otherwise, allow deep passes
        dice1 = random.randint(0,DiceMax)   #Determine pass play
        if dice1 == 0:                      #Classify the pass as short, mid,
            PassLength = "Short"            #midlong or long.  Outside of the 
        if dice1 == 5:                      #opponents 10 YL, 1 out of 7 
            PassLength = "MidLong"          #passes to receivers are short, 4
        if dice1 == 6:                      #out of 7 passes are mid-lenth, 1
            PassLength = "Long"             #out of 7 are mid-long and 1 out
        if (dice1 > 0) and (dice1 < 5):     #of 7 are long.  I suppose that I
            PassLength = "Mid"             #researched these stats but I just
                                           #well could have made them up 
                                           
        PassTypeList = ["Bubble Screen", "Slant", "Hitch","In Pattern",
                        "Out Pattern","Post","Deep"]
        PassType = PassTypeList[dice1]
        if HailMary == 1:               #By definition, Hail Mary's are deep
            PassType = "Deep"           #passes  
       
    return PassType


#-----------------------------------------------------------------------------
# Function Name:    PlayCall
# Purpose:          Select run or pass, choose play type, who gets the ball 
#                   and then run play                   
# Author:           Rick Burney
# Created:          12/13/2016
# Copyright:        (c) Rick 2016
#-----------------------------------------------------------------------------
def PlayCall(TeamWiththeBall,down,YardsToGo,RunnersStartIndex,
             ReceiversStartIndex,RunCentric,PassCentric,Hup,SpiketheBall,
             YardLine,HailMary,FP,Blowout):
    
    import random       #Random variations in situational-based play calling
    import openpyxl     #Use team worksheets for run/pass oriented decisions
    import PickAPlayer  #Class used to identify the location of the pass and  
                        #run oriented team flags from the team worksheets

    global BallCarrier      #Who carries or receives  the ball
    global BallCarrierAve   #Yards per carry or catch
    global PlayType         #Run or pass
    global PassLength       #If pass, short, mid, midlong or deep
    global QBName           #Name of the QB in the game
        
#Instantiate a class object that will identify the worksheet row where the   
#pass or run oriented team flags are listed.
    RequestedRow = PickAPlayer.PickAPlayer(TeamWiththeBall,0,0,0,0,0) 
    RequestedRow.FindStats()
    
    if Blowout == 0:        #If game is not a blowout, use this column for the
        cumProbColumn = 8   #cum probability to see who gets the ball
    else:                   #Otherwise use this column (from the player 
        cumProbColumn = 11  #worksheet. 
    RunAdder = 47           #% adder to RunPercentage when RunCentric = 1
    PassAdder = -50         #% subtractor to RunPercentage when PassCentric=1
    PassOrientedAdder = -10 #Arbitrary constant for pass oriented teams that 
                            #decrease the probability (%) of a run (hence the 
                            #negative value)
    
#Use PickAPlayer class to locate the row containing the flags that identify a 
#team as run-oriented, pass-oriented or balanced
    PassOrientedRow = RequestedRow.QBsPosition + RequestedRow.Offset 
    
    PassOrientedColumn = 10 #Column identifies where these flags are stored
                            #on the  worksheet
    RunOrientedAdder = 10   #Same deal with run oriented teams or run-oriented
    RunOrientedRow = 12     #situations
    MaxRunRow = 12          #This is the last row of RBs in the worksheet.
                            #Ultimately want to make this an autodetect 
                            #situation - NO LONGER USED
    RunnerTypeColumn = 9    #QB, RB or WR

#Pull from worksheet whether this offense is pass oriented, run oriented or
#balanced.  00 = balanced, 01 = pass oriented, 10 = run oriented and 11 is not
#allowed
    PO = TeamWiththeBall.cell(row = PassOrientedRow,
                               column=PassOrientedColumn).value
    RunningTeam = TeamWiththeBall.cell(row = PassOrientedRow,
                                       column=RunOrientedRow).value

#If the Hurry Up check box is checked, then implement a hurry up offense    
    if Hup == 1:
        PassCentric = 1 #Hurry up offense is a pass centric offense, just
                        #takes less time
    
#Down/Yardage Table to determine run/pass probabilities.  Has
#worked out pretty well to date.  Still looking for website with statistics on
#this.  These numbers did come from a website but I can't remember which one
    if down == 1:                   #1st and >10 is always due to an offensive 
        if YardsToGo > 10:         #penalty on 1st down
            RunPercentage = 15.0    #Arbitrary
        else:                       
            RunPercentage = 51.7
    if down == 2:                        #2nd down
        if YardsToGo >= 10:         #If YTG > 10, most likely a pass
            RunPercentage = 30.0
        elif YardsToGo >= 5:        #If YTG between 5 and 10, still likely a pass
            RunPercentage = 39.3    
        elif YardsToGo > 3:
            RunPercentage = 54.2    #Between 3 or 5, more likely a run
        else:
            RunPercentage = 67.5    #if < 3, most likely a run
    if down == 3:                   #3rd down
        if YardsToGo >= 10:         #If YTG > 10, very likely a pass         
            RunPercentage = 7.4
        elif YardsToGo >= 5:        #Still likely a pass on 3rd and > 5
            RunPercentage = 11.5
        elif YardsToGo > 3:         #Even so if 3rd and 3 or 4
            RunPercentage = 12.6
        else:                       #3rd and 2 or 1, most likely a run
            RunPercentage = 60
    if down == 4:               #If 4th and long, need to select pass-oriented
        RunPercentage = 55.4    #option        
    if RunCentric == 1:             #Run-oriented checkbox has been checked on
        RunPercentage += RunAdder   #the Control Panel 
    if PassCentric == 1:            #Pass-oriented checkbox has been checked
        RunPercentage += PassAdder  #on the Control Panel
    if PO == 1:                             #Team is a pass-oriented team             
        RunPercentage += PassOrientedAdder
    if RunningTeam == 1:                    #Team is a run-oriented team             
        RunPercentage += RunOrientedAdder
        
#Based upon down and yards to go, determine if play call is a run or pass
    dice1 = random.randint(0,99)  

    if dice1 <= RunPercentage:  #The way this works is, roll the dice, it if
        PlayType = "Run"        #is less than the Run% which is set by the 
    else:                       #down and yards to go (also, run or pass
        PlayType = "Pass"       #centric settings, it is a run, otherwise a
                                #pass
        
    if (SpiketheBall == 1) or (HailMary == 1):   #By definition, a pass
        PlayType = "Pass"

 #And now for the details of the play   
    dice1 = random.randint(0,99)
    rr = RunnersStartIndex        #Use shorter variables just for convenience
    ww = ReceiversStartIndex      #These are the start of the position indices
    RunnerType = "RB"           #Initialize position types - may no longer be
    ReceiverType = "WR"         #needed
    RunType = "Pass"
    
#Select who will carry the ball if a run is called and determine the position
# type.  Then choose the type of running play.  This is done by testing a
#random number to see when it is just larger than the cumulative probability
#calculated for each potential ball carrier.  An index is incremented for each
#test and when the random number goes above the indexed cumulative probability
#the ball carrier at that index is chosen along with their yards per carry
    if PlayType == "Run":                               #Read the cum prob
        while dice1 >= TeamWiththeBall.cell(row = rr,   #from the worksheet
                        column=cumProbColumn).value:
            rr += 1                                     #Check the next cum
                                                        #probability
        
#Once dice1 > the cum probability extracted from the worksheet, that is the
#ball carrier.  Extract name and yards per carry average for that ballcarrier
        BallCarrier = TeamWiththeBall.cell(row = rr,column=2).value
        BallCarrierAve = TeamWiththeBall.cell(row = rr,column=4).value
        
#Check for indexing error.  If an error is found, go into the worksheet and
#fix the cumulative probability error which is most always that the largest
#cumulative probability is < 1.00.  THIS HAS BEEN RESOLVED BY MAKING SURE
#CUM PROBABILITY RANGE IS >= 1.00

#The runner type is either a running back, quarterback or wide receiver.  Use
#the same index to select runner type from the worksheet
        RunnerType = \
            TeamWiththeBall.cell(row = rr,column=RunnerTypeColumn).value
        
#Put in on 3/22/22 to ensure that QB does not run the ball during a blowout
        if Blowout == 1:
            RunnerType = "RB"
       
#Based on the runner type, select a running play.
        RunType = RunningPlay(RunnerType,YardsToGo)
        
        T = RunType #Common variable name for run and pass.  Used for error
                    # checking
                                                    
#Select who will receive the pass if a pass is called and determine the
# position type.  Then choose the type of pass play.  Uses same process as
#running plays
    else:
        while dice1 >= TeamWiththeBall.cell(row = ww,
                                            column=cumProbColumn).value:
            
            ww += 1 #Check the next cumulative probability
        
#Ball carrier in this case is the receiver.  Extract name and stats
        BallCarrier = TeamWiththeBall.cell(row = ww,column=2).value
        BallCarrierAve = TeamWiththeBall.cell(row = ww,column=3).value
        ReceiverType = TeamWiththeBall.cell(row = ww,column=9).value
        PassType = PassPlay(ReceiverType,YardLine,HailMary)
        T = PassType

#Format the complete play description into a string for display on the 
#scoreboard
    if T == None:                   #Error check to make sure that ball 
        print("T is the culprit")   #carrier type cell in worksheet is not 
                                    #left blank
    while True:
        try:
            Play = PlayType + "     " + T + "     " + BallCarrier
            break
        except:
            print("Line 272, PC",ww,BallCarrier)
            break
    return Play
