#-------------------------------------------------------------------------------
# Function Name:    UpdateYTG
# Purpose:          Limited use - Used by CallPlay in Control Panel.py to 
#                   update the yards to go.  CallPlay determines if there is
#                   a 1st down
# Author:           Rick Burney
#
# Created:          11/10/2016
# Copyright:        (c) Rick 2016
#-------------------------------------------------------------------------------
def UpdateYTG(down,YTG,ResultList):
    if ResultList[0] == "Pass":
        if ResultList[2] == "Incomplete":
            YTG = YTG
        else:
            YTG = YTG - int(ResultList[3])
    else:
        YTG = YTG - int(ResultList[3])
    
    return YTG
            