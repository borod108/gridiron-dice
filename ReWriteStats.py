from openpyxl.styles import Font
from openpyxl.styles import Alignment
from openpyxl import Workbook           #Workbook methods from Excel library 


#****************************************************************************
#Method:   ReWriteStats
#Purpose:  This class contains all of the methods and objects needed to rewrite designated
#                stats from an already created worksheet.  Based upon the type of stat, this class
#                will figure out the starting point and the number of table entries that have to
#                be recomputed
# Inputs:   Worksheet
# Outputs: Updated worksheet that will be rewritten to the original file
# Author:           Rick Burney
# Created:          04/04/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
class ReWriteStats():

    def __init__(self,wsStats, wbStats, FileName):
        
        import os                       #Libriaries for file management
        import sys
        from openpyxl import Workbook     #Workbook methods from Excel library 
        from openpyxl.styles import Font
        
        self.IntStartRow = 60   #Initial value but these will be determined by the row with the 
        self.IntEndRow = 70     #"Int" label and the computed number of players who had INTs
        
        self.ReceivingEndRow = 29   #Last populated row of a the receiving stat category        
        self.ReceivingStartRow = 20 #First populated row of the receiving stat category
        self.RushingEndRow = 10     #Last populated row of a the rushing stat category
        self.RushingStartRow = 1      #First populated row of the rushing stat category
        self.SacksEndRow = 110       #Last populated row of the sacks stat category
        self.TacklesEndRow = 130    #Last populated row of the tackles stat category
        self.TacklesStartRow = 100  #First populated row of the tackles stat category
        self.wsStats = wsStats          #Worksheet in question
        self.wbStats = wbStats         #Workbook in question
        self.FileName = FileName    #Filename of the workbook in question
        

#****************************************************************************
#Method:   AdjustView
#Purpose:  This method adjusts the column widths and zoom for the worksheet
# Inputs:   Worksheet
# Outputs: 
# Author:           Rick Burney
# Created:          04/05/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def AdjustView(self):

#Adjust width of the columns.  Will continue to adjust as needed
        self.wsStats.column_dimensions["A"].width = 16.0
        self.wsStats.column_dimensions["B"].width = 20.0
        self.wsStats.column_dimensions["C"].width = 10.0
        self.wsStats.column_dimensions["D"].width = 15.0
        self.wsStats.column_dimensions["E"].width = 10.0
        self.wsStats.column_dimensions["F"].width = 15.0    
        self.wsStats.column_dimensions["G"].width = 15.0
        self.wsStats.column_dimensions["H"].width = 20.0
        self.wsStats.column_dimensions["I"].width = 10.0
        self.wsStats.column_dimensions["J"].width = 15.0
        self.wsStats.column_dimensions["K"].width = 15.0
        self.wsStats.column_dimensions["L"].width = 15.0
        self.wsStats.column_dimensions["M"].width = 15.0
        self.wsStats.sheet_view.zoomScale = 173        
        for row in self.wsStats['C1:L400']:                  #Center everything  
            for cell in row:
                cell.alignment = Alignment(horizontal='center')   


#****************************************************************************
#Method:   ComputeCPs
#Purpose:  This method computes the CPs for a stat category
# Inputs:   Worksheet, starting row of the column, number of addends, column, column of 
#               independent variable, independent variable total
# Outputs: CP1, CP2 for each row 
# Author:           Rick Burney
# Created:          04/05/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def ComputeCPs(self, StartRow, NumRows, CPColumn, IndepVarColumn, Total):

        for i in range(NumRows):
            IndepVar = self.wsStats.cell(row = StartRow + i, column = IndepVarColumn).value
            if i == 0:
                CP1 = 0
                CP2 = 100*float(IndepVar)/float(Total)
            else:
                CP1 = CP2
                CP2 = CP1 + 100*float(IndepVar)/float(Total)
                
#Round the CPs so there is nothing to the right of the decimal point and write to worksheet
#for each row (and the start and stop rows have been passed into this method)
            self.wsStats.cell(row = StartRow + i, 
                              column = CPColumn).value = round(CP1,0)   
            self.wsStats.cell(row = StartRow + i, 
                          column = CPColumn+1).value  = round(CP2 , 0)          
        self.wbStats.save(filename = self.FileName)                             #Write worksheet to file


#****************************************************************************
#Method:   ComputeTotals
#Purpose:  This method totals up a column of numbers.  
# Inputs:   Worksheet, starting row of the column, number of addends, column
# Outputs: Total of the column 
# Author:           Rick Burney
# Created:          04/05/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def ComputeTotals(self, StartRow, NumRows, Column):
        
#Define start column
        Total = 0                                                               #Initialize the total
        for i in range(NumRows):                                      #Keep a running total
            Total += self.wsStats.cell(row = StartRow + i,
                                        column = Column).value
        return Total                                                        #Return the total


#****************************************************************************
#Method:   RedoIntCPs
#Purpose:  This method recomputes the CPs for the Int stats.  In most cases, the worksheet
#                has been manually edited and it is necessary to recompute the CPs for INTs
# Inputs:   Worksheet
# Outputs: Recomputed Int CPs 
# Author:           Rick Burney
# Created:          04/07/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def RedoIntCPs(self):
        
#Define start row by looking for the appropriate heading
        CategoryColumn = 1                                                  #Categories are in the 1st column
        i = 1                                                                           #Start at Row 1
        RowOffset = 1
        while self.wsStats.cell(row = i, column = CategoryColumn).value != "INTs":
            i += 1
        self.IntStartRow = i  +  RowOffset #Once found, store the start row for future use
                
#Look for None cell at end of column 2 and subtract 1 to get last row in category
        NameColumn = 2
        i = self.IntStartRow
        while self.wsStats.cell(row = i, column = NameColumn).value != None:
            i += 1
        self.IntEndRow = i 

#Define columns
        CPColumn = 4
        #AvailabilityColumn = 5
        NumberOfIntsColumn = 3
        NumRows = self.IntEndRow - self.IntStartRow
        Total = self.ComputeTotals(self.IntStartRow, NumRows, NumberOfIntsColumn)
        self.wsStats.cell(row = self.IntEndRow, column = NumberOfIntsColumn).value = Total
        self.ComputeCPs(self.IntStartRow, NumRows, CPColumn, NumberOfIntsColumn, Total)
        self.wbStats.save(filename = self.FileName)                            


#****************************************************************************
#Method:   RedoReceivingBCPs
#Purpose:  This method recomputes the backup CPs for the receiving stats
# Inputs:   Worksheet, already computed starting and end points
# Outputs: Recomputed receiving CPs 
# Author:           Rick Burney
# Created:          04/07/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def RedoReceivingBCPs(self):
        
        BCPColumn = 10                                                              #Define receiving BCP column
        BackupColumn = 12                                                               #Independent variable
        NumRows = self.ReceivingEndRow - self.ReceivingStartRow #Use already computed

#Compute total of backup players 
        Total = self.ComputeTotals(self.ReceivingStartRow, NumRows, BackupColumn)
        
#Write total to worksheet
        self.wsStats.cell(row = self.ReceivingEndRow, column = BackupColumn).value = Total
        
#Compute BCPs
        self.ComputeCPs(self.ReceivingStartRow, NumRows, BCPColumn, BackupColumn, Total)
        
        self.wbStats.save(filename = self.FileName)     #Write to file                           


#****************************************************************************
#Method:   RedoReceivingCPs
#Purpose:  This method recomputes the CPs for the receiving stats
# Inputs:   Worksheet
# Outputs: Recomputed receiving CPs 
# Author:           Rick Burney
# Created:          04/065/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def RedoReceivingCPs(self):
        
#Define start row by looking for the appropriate heading
        CategoryColumn = 1
        i = 1
        RowOffset = 1
        while self.wsStats.cell(row = i, column = CategoryColumn).value != "Receivers":
            i += 1
        self.ReceivingStartRow = i  +  RowOffset #Once found, store the start row for future use
                
#Look for None cell at end of column 2 and subtract 1 to get last row in category
        NameColumn = 2              #Column with the player names
        i = self.ReceivingStartRow  #Row where the receiver table starts
        
        while self.wsStats.cell(row = i, column = NameColumn).value != None:
            i += 1
        self.ReceivingEndRow = i    #Row where the receiver table ends

#Define columns
        CPColumn = 7                            #Low number in the cum probability
        AvailabilityColumn = 5               #If 0, leave cum probability as is
        AdjustedReceptionsColumn = 6 #Availability * Receptions
        ReceptionsColumn = 4                                                         #Receptions
        NumRows = self.ReceivingEndRow - self.ReceivingStartRow #Number of receivers
        
#Rewrite (to the worksheet) receiver stats and cum probabilities based upon availability
        for i in range(NumRows):
            Receptions = self.wsStats.cell(row = self.ReceivingStartRow + i, 
                                        column = ReceptionsColumn).value
            Availability = self.wsStats.cell(row = self.ReceivingStartRow + i, 
                                        column = AvailabilityColumn).value
            AdjustedReceptions = Receptions * Availability
            self.wsStats.cell(row = self.ReceivingStartRow + i, 
                              column = AdjustedReceptionsColumn).value = AdjustedReceptions

#Total is used to compute the cum probabilities
        Total = self.ComputeTotals(self.ReceivingStartRow, NumRows, 
                                   AdjustedReceptionsColumn)
        self.wsStats.cell(row = self.ReceivingEndRow, 
                          column = AdjustedReceptionsColumn).value = Total
        self.ComputeCPs(self.ReceivingStartRow, NumRows, CPColumn, 
                        AdjustedReceptionsColumn, Total)
        self.wbStats.save(filename = self.FileName)     #Save to workbook                            


#****************************************************************************
#Method:   RedoRushingBCPs
#Purpose:  This method recomputes the backup CPs for the Rushing stats
# Inputs:   Worksheet, already computed starting and end points
# Outputs: Recomputed rushing CPs 
# Author:           Rick Burney
# Created:          04/05/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def RedoRushingBCPs(self):
        
#Define start column
        BCPColumn = 10          #Backup cum prob column for RBs
        BackupColumn = 12     #1 = legit backup, 0 = not a backup RB
        
        NumRows = self.RushingEndRow - self.RushingStartRow #Number of players
        
#Compute the number of players that can play as backups during a blowout
        Total = self.ComputeTotals(self.RushingStartRow, NumRows, BackupColumn)
        
#Write the total to the worksheet
        self.wsStats.cell(row = self.RushingEndRow, column = BackupColumn).value = Total
        
#Based on the total, compute the cum probs for the backups during a blowout
        self.ComputeCPs(self.RushingStartRow, NumRows, BCPColumn, BackupColumn, Total)
        self.wbStats.save(filename = self.FileName)                            


#****************************************************************************
#Method:   RedoRushingCPs
#Purpose:  This method recomputes the CPs for the Rushing stats
# Inputs:   Worksheet
# Outputs: Recomputed rushing CPs 
# Author:           Rick Burney
# Created:          04/05/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def RedoRushingCPs(self):
        
#Define start row by looking for the appropriate heading
        CategoryColumn = 1
        i = 1
        RowOffset = 1
        while self.wsStats.cell(row = i, column = CategoryColumn).value != "Runners":
            i += 1
        self.RushingStartRow = i  +  RowOffset    #Once found, store the start row for future use
                
#Look for None cell at end of column 2 and subtract 1 to get last row in category
        NameColumn = 2
        i = self.RushingStartRow
        while self.wsStats.cell(row = i, column = NameColumn).value != None:
            i += 1
        self.RushingEndRow = i #- RowOffset

#Define start column
        CPColumn = 7
        AvailabilityColumn = 5
        AdjustedCarriesColumn = 6
        CarriesColumn = 3
        NumRows = self.RushingEndRow - self.RushingStartRow
        for i in range(NumRows):
            Carries = self.wsStats.cell(row = self.RushingStartRow + i, 
                                        column = CarriesColumn).value
            Availability = self.wsStats.cell(row = self.RushingStartRow + i, 
                                        column = AvailabilityColumn).value
            AdjustedCarries = Carries * Availability
            self.wsStats.cell(row = self.RushingStartRow + i, 
                              column = AdjustedCarriesColumn).value = AdjustedCarries
        Total = self.ComputeTotals(self.RushingStartRow, NumRows, AdjustedCarriesColumn)
        self.wsStats.cell(row = self.RushingEndRow, 
                          column = AdjustedCarriesColumn).value = Total
        self.ComputeCPs(self.RushingStartRow, NumRows, CPColumn, AdjustedCarriesColumn, 
                   Total)
        self.wbStats.save(filename = self.FileName)                            


#****************************************************************************
#Method:   RedoSacksCPs
#Purpose:  This method recomputes the CPs for the sack stats
# Inputs:   Worksheet
# Outputs: Recomputed sack CPs 
# Author:           Rick Burney
# Created:          04/07/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def RedoSacksCPs(self):
        
#Use self.TacklesStartRow for starting point but must recompute NumRows
#Look for None cell at end of column 8 to get last row in category
        NameColumn = 8
        i = self.TacklesStartRow
        while self.wsStats.cell(row = i, column = NameColumn).value != None:
            i += 1
        self.SacksEndRow = i    #ID last row of sacks and assign it to a variable

#Define columns
        CPColumn = 10                       #Lower bound of cumulative probability
        NumberOfSacksColumn = 9    #Number of sacks for each defensive player
        
#Number of players who had sacks
        NumRows = self.SacksEndRow - self.TacklesStartRow
        
#Compute the number of sacks for the entire team and write to the stats worksheet
        Total = self.ComputeTotals(self.TacklesStartRow, NumRows, NumberOfSacksColumn)
        self.wsStats.cell(row = self.SacksEndRow, 
                          column = NumberOfSacksColumn).value = Total
        
#Compute the upper and lower bounds of the cum probabilities for each player who had a
#sack and write each pair of cum probabilities to the stats worksheet
        self.ComputeCPs(self.TacklesStartRow, NumRows, CPColumn, NumberOfSacksColumn, 
                        Total)
        self.wbStats.save(filename = self.FileName)                            


#****************************************************************************
#Method:   RedoTacklesCPs
#Purpose:  This method recomputes the CPs for the tackles stats
# Inputs:   Worksheet
# Outputs: Recomputed tackles CPs 
# Author:           Rick Burney
# Created:          04/07/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def RedoTacklesCPs(self):
        
#Define start row by looking for the appropriate heading
        CategoryColumn = 1                                          
        i = 1                           #Start at row 1
        RowOffset = 1
        while self.wsStats.cell(row = i, column = CategoryColumn).value != "Tackles":
            i += 1
        self.TacklesStartRow = i  +  RowOffset   #Once found, store the start row for future use
                
#Look for None cell at end of column 2 and subtract 1 to get last row in category
        NameColumn = 2
        i = self.TacklesStartRow
        while self.wsStats.cell(row = i, column = NameColumn).value != None:
            i += 1
        self.TacklesEndRow = i #- RowOffset

#Define columns
        CPColumn = 4
        NumberOfTacklesColumn = 3
        NumRows = self.TacklesEndRow - self.TacklesStartRow
        print(NumRows)
        Total = self.ComputeTotals(self.TacklesStartRow, NumRows, NumberOfTacklesColumn)
        self.wsStats.cell(row = self.TacklesEndRow, 
                          column = NumberOfTacklesColumn).value = Total
        self.ComputeCPs(self.TacklesStartRow, NumRows, CPColumn, NumberOfTacklesColumn, 
                        Total)
        self.wbStats.save(filename = self.FileName)                            
        

#****************************************************************************
#Method:   ReWriteStatsExec
#Purpose:  This method goes through the sequence of updating stats
# Inputs:   Worksheet
# Outputs: 
# Author:           Rick Burney
# Created:          04/04/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def ReWriteStatsExec(self):

        self.AdjustView()
        self.RedoRushingCPs()
        self.RedoRushingBCPs()
        self.RedoReceivingCPs()
        self.RedoReceivingBCPs()
        self.RedoIntCPs()
        self.RedoTacklesCPs()
        self.RedoSacksCPs()
