#-------------------------------------------------------------------------------
# Function Name:    ReadGeneralInfo
# Purpose:          Reads a text file that contains general information such
#                   as the names of the last teams that played
# Outputs:          For now, the name of the home team and the visiting team
#                   that played last
# Author:           Rick Burney
#
# Created:          3/31/2017
# Copyright:        (c) Rick 2017
#-------------------------------------------------------------------------------
def ReadGeneralInfo():
    import os
    import sys
    

    f = open('General Info.txt','r')            #Open general info file
    HomeTeam = str(f.readline())                #Read in the name of the home
    TeamNameLocation = HomeTeam.find(" = ") + 3 #team from the previous game
    
    HomeTeamName = HomeTeam[TeamNameLocation:len(HomeTeam)]
    HomeTeamName = HomeTeamName.rstrip('\n')                #Strip out \n char

#Need to take out \n character for the visiting team    
    VisitingTeam = str(f.readline())                #Read in the name of the
    TeamNameLocation = VisitingTeam.find(" = ") + 3 #visiting team from the 
                                                    #previous game
    
    VisitingTeamName = VisitingTeam[TeamNameLocation:len(VisitingTeam)]
    
    TeamsLastPlayed = [HomeTeamName,VisitingTeamName]
    
    f.close()   #Close file
    
    return TeamsLastPlayed


#-----------------------------------------------------------------------------
# Function Name:  WriteGeneralInfo
# Purpose:             Writes general information such as the names of the last teams that 
#                           played, to a text file   
# Inputs:                The names of the teams that are currently playing
# Outputs:             For now, the name of the home team and the visiting team that played 
#                           last
# Author:              Rick Burney
# Created:            4/1/2017
# Copyright:         (c) Rick 2017
#-------------------------------------------------------------------------------
def WriteGeneralInfo(HomeTeamName,VisitingTeamName):
    import os   #OS libraries that are used for file access
    import sys
    
    HomeTeamLeader = "Home Team = "         #Text label for the home team
    VisitingTeamLeader = "Visiting Team = "    #Text label for the visiting team    
    f = open('General Info.txt','w')                     #Open general info file
    
#Write name of last home team that played to the text file
    f.write(HomeTeamLeader + HomeTeamName + '\n') #

#Write name of last visiting team that played to the text file
    f.write(VisitingTeamLeader + VisitingTeamName)
    f.close()                                                                   #close text file
    
    return None