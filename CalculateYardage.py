#-------------------------------------------------------------------------------
# Name:        CalculateYardage
# Purpose: Calculate yards
# Ultimately, this will take the play call as an input and calculate the
# result.  ALSO THIS WILL TURN INTO A FUNCTION THAT WILL RETURN A DICTIONARY OF
# RESULTS
# Input: PlayCall
# Output: Result of the play
# Author:      Rick
#
# Created:     10/20/2016
# Copyright:   (c) Rick 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Die import *
import random
from YardageTable import*


def CalculateYardage(RPflag, passType):

#The following constants will ultimately be passed into this module
    RBypc = 4.1
    DefenseYardsAllowedperCarry = 3.9

#Change this to an adder/subtractor
    RunYardageMultiplier = RBypc/4 * DefenseYardsAllowedperCarry/4
    print RunYardageMultiplier


#Roll 3 dice
    roll=RolltheDie()
    all3die = roll.Dice3Dice6Dice6()
#print all3die
    dice1,dice2,dice3 = roll.dice1,roll.dice2,roll.dice3

#Compute 11x3 array indices, remember to subtract 2 for the row index since it
#is the sume of two die and array indices start at 0, subtract 1 for column
#index
    rowIndex = dice2 + dice3 -2
    columnIndex = dice1 - 1
#print columnIndex,rowIndex

    yardageResult = str(RunYardageTable(rowIndex,columnIndex))


#Test to see if result is an integer
    try:
        yardageResult = int(yardageResult)
    except ValueError:
#    pass            #This is where Loss, SG, MG, LG gets resolved
        if yardageResult == "Loss":
            lossRoll=RolltheDie()
            all3die = lossRoll.Dice3Dice6Dice6()
            dice1,dice2,dice3 = roll.dice1,roll.dice2,roll.dice3
            rowIndex = dice2 + dice3 -2
            columnIndex = dice1 - 1
            yardageResult = LossTable(rowIndex,columnIndex)
        if yardageResult == "SG":
            SGRoll=RolltheDie()
            all3die = SGRoll.Dice3Dice6Dice6()
            dice1,dice2,dice3 = roll.dice1,roll.dice2,roll.dice3
            rowIndex = dice2 + dice3 -2
            columnIndex = dice1 - 1
            #Add code for
            yardageResult = ShortGainTable(rowIndex,columnIndex)
        if yardageResult == "MG":
            MGRoll = RolltheDie()
            yardageResult = MGRoll.SingleValue366()
        if yardageResult == "LG":
            LGRoll = RolltheDie()
            yardageResult = LGRoll.SingleValue31010()

    yardage = int(round(yardageResult*RunYardageMultiplier,0))
    print yardage

#aggregatedValue1 = roll.SingleValue31010()
#print aggregatedValue1

#aggregatedValue2 = roll.SingleValue366()
#print aggregatedValue2


