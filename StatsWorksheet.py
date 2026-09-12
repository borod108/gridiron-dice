from openpyxl.styles import Font
from openpyxl.styles import Alignment
from openpyxl import Workbook           #Workbook methods from Excel library 


#****************************************************************************
#Method:   StatsWorksheet
#Purpose:  This class contains all of the methods and objects needed to create 
#          and populate a statistics worksheet
# Inputs:  Table_IDs
# Outputs: Extracted team and individual stats for subsequent xfer to a stats
#          worksheet
# Author:           Rick Burney
# Created:          02/19/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
class StatsWorksheet():

    def __init__(self,TeamThatWasSelected, Table_Row_Lengths, 
                 wsStartingPoints):
        
        import os                       #Libriaries for file management
        import sys
        from openpyxl import Workbook     #Workbook methods from Excel library 
        from openpyxl.styles import Font
        
        wb = Workbook() #Create a workbook
        FileName = TeamThatWasSelected + ".xlsx" #Filename for Excel worksheet

        ws = wb.active                 #Refer to the active worksheet
        ws.title = TeamThatWasSelected #Change title of worksheet to team name  
        wb.save(filename = FileName)   #Create an empty Excel file
        self.wb = wb                   #Make workbook and active worksheet 
        self.ws = ws                   #available to all methods in class
        self.FileName = FileName       #Make available to all methods

        self.wsStartingPoints = wsStartingPoints
        
        
#Table row lengths is needed by multiple methods        
        self.Table_Row_Lengths = Table_Row_Lengths
        self.RowPointer = 1
        self.NumberOfHeadingElements = 1
        self.StatTableHeadings = []
        
        

#NEED A HEADING
    def CreateWorksheetStructure(self):
 
        RushingTableHeadingRow = 1
        
        RushingTableHeadings = ["Runners","Name","Carries","YPC","Available",
                                "Adj Carries","CP1","CP2","Type","BCP1",
                                "BCP2","Backup Flag"]
        QBTableHeadings = ["QBs","Name","PC","PI","Available",
                                "Sack Percentage","","","","Pass Oriented",
                                "","RunOriented"]
        ReceiverTableHeadings = ["Receivers","Name","YPC","Receptions",
                                 "Available","Adj Receptions","CP1","CP2",
                                 "Type","BCP1","BCP2","Backup", "NumBackups"]
        KickerTableHeadings = ["Kickers","FG Kicker","# of Kickoffs",
                               "Kickoff Ave","TB","OB","PATs","0-19","20-29",
                               "30-39","40-49","50-55"]
        PunterTableHeadings = ["","","","Ave","Long","FC"]
        KRTableHeadings = ["KRs","","#","Ave","Long"]
        PR1TableHeadings = ["","","","Ave","Long"]
        PR2TableHeadings = ["PRs"]
        IntTableHeadings = ["INTs","Name","#","PMin","Pmax","Ave"]
        OffFumblesLostHeadings = ["Fumble Lost","","","of out 10000"]
        FumbleRecoveryHeadings = ["Fumble Recoveries"]
        TeamStatsHeadings = ["Teams Stats","Penalties/Game","Conf Factor"]
        TacklesSacksStatsHeadings = ["Tackles","","","","","","Sacks"]
        InjuryFactorHeadings = ["Injury Impacts"]
        IF1Heading = ["","# 0f Starting OL Injured"]
        IF2Heading = ["","# 0f Starting DL Injured"]
        IF3Heading = ["","# 0f Starting LBs Injured"]
        IF4Heading = ["","# 0f Starting DBs Injured"]
        
        self.FormatCellsAndColumns() #As the method call says
        
#Write Rushing Table headings #Write Rushing Table headings
        self.wsStartingPoints['Rushing_Stats'] = self.RowPointer+1
        self.NumberOfHeadingElements = len(RushingTableHeadings)
        self.StatTableHeadings = RushingTableHeadings
        self.WriteHeadings()
        
#Point to the totals label cell and write to the cell       
        self.RowPointer += self.Table_Row_Lengths['Rushing_Stats']
        self.TotalsLabel() 
        
#Write QB Table headings
        self.wsStartingPoints['Passing_Stats'] = self.RowPointer+1
        self.NumberOfHeadingElements = len(QBTableHeadings)
        self.StatTableHeadings = QBTableHeadings
        self.WriteHeadings()

#Point to the next totals label cell and write to the cell       
        self.RowPointer += self.Table_Row_Lengths['Passing_Stats']
        self.TotalsLabel()

#Write Receiver Table headings 
        self.wsStartingPoints['Receiving_Stats'] = self.RowPointer+1
        self.NumberOfHeadingElements = len(ReceiverTableHeadings)
        self.StatTableHeadings = ReceiverTableHeadings
        self.WriteHeadings()

#Point to the next totals label cell and write to the cell       
        self.RowPointer += self.Table_Row_Lengths['Receiving_Stats']
        self.TotalsLabel()

#Sometimes, a stat group is comprised of multiple stat categories.  Kickoffs
#and fieldgoals are one such example.  

#Write Kicker Table headings 
        self.wsStartingPoints['Kicking_Stats'] = self.RowPointer+1
        self.NumberOfHeadingElements = len(KickerTableHeadings)
        self.StatTableHeadings = KickerTableHeadings
        self.WriteHeadings()

#No totals label, move 2 rows down for next stat group       
        self.RowPointer += 2

#Write Punter Table headings 
        self.wsStartingPoints['Punting_Stats'] = self.RowPointer+1
        self.NumberOfHeadingElements = len(PunterTableHeadings)
        self.StatTableHeadings = PunterTableHeadings
        self.WriteHeadings()

#No totals label, move 8 rows down for next stat group       
        self.RowPointer += 8

#Defensive team stats.  Call method to place headings
        self.wsStartingPoints['DefensiveTeam_Stats'] = self.RowPointer+1       
        self.WriteDefensiveTeamStatHeadings()

        self.RowPointer += 3    #Move 3 rows down for next stat group

#Write Kick Returner Table headings 
        self.wsStartingPoints['KR_Stats'] = self.RowPointer+1       
        self.NumberOfHeadingElements = len(KRTableHeadings)
        self.StatTableHeadings = KRTableHeadings
        self.WriteHeadings()

        self.RowPointer += 3    #Move 3 rows down for next stat group

#Write Punt Returner Table headings, noting that "PR" is one row down 
        self.wsStartingPoints['PR_Stats'] = self.RowPointer+1       
        self.NumberOfHeadingElements = len(PR1TableHeadings)
        self.StatTableHeadings = PR1TableHeadings
        self.WriteHeadings()
        self.RowPointer += 1
        self.NumberOfHeadingElements = len(PR2TableHeadings)
        self.StatTableHeadings = PR2TableHeadings
        self.WriteHeadings()

        self.RowPointer += 2    #Move 2 rows down for next stat group

#Write Int Table headings 
        self.wsStartingPoints['INT_Stats'] = self.RowPointer+1       
        self.NumberOfHeadingElements = len(IntTableHeadings)
        self.StatTableHeadings = IntTableHeadings
        self.WriteHeadings()

#We don't have the length of the INT Table yet so we will take an arbitrary
#table length of 12 until we derive the actual number
#*******REMEMBER TO EXTRACT THE # OF INTERCEPTORS
        self.RowPointer += 12    
        self.TotalsLabel()
        self.RowPointer += 1    

#Write Offensive Fumbles Lost Headings
        self.wsStartingPoints['OFumbles_Stats'] = self.RowPointer       
        self.NumberOfHeadingElements = len(OffFumblesLostHeadings)
        self.StatTableHeadings = OffFumblesLostHeadings
        self.WriteHeadings()

        self.RowPointer += 2    #Move 2 rows down for next stat group

#Write Heading for list of potential fumble recoverers
        self.wsStartingPoints['Fumble_Recoveries'] = self.RowPointer+1       
        self.NumberOfHeadingElements = len(FumbleRecoveryHeadings)
        self.StatTableHeadings = FumbleRecoveryHeadings
        self.WriteHeadings()

        self.RowPointer += 21    #Move 21 rows down for next stat group

#Write Heading for the Team Stats
        self.wsStartingPoints['Team_Stats'] = self.RowPointer       
        self.NumberOfHeadingElements = len(TeamStatsHeadings)
        self.StatTableHeadings = TeamStatsHeadings
        self.WriteHeadings()

        self.RowPointer += 3    #Move 3 rows down for next stat group

#Write Heading for the Tackle Stats
        self.wsStartingPoints['Tackle_Stats'] = self.RowPointer + 1       
        self.NumberOfHeadingElements = len(TacklesSacksStatsHeadings)
        self.StatTableHeadings = TacklesSacksStatsHeadings
        self.WriteHeadings()

#Figure out the length of the tackles table so that the totals label for both
#tackles and sacks can be written.  The sacks total label location is 
#customized
        self.RowPointer += self.Table_Row_Lengths['Defensive_Stats'] + 1
        self.TotalsLabel()
 
#Write sack totals Label in a column other that '1'   
        self.RowPointer -= 1                #Back up 1 row
        self.ws.cell(row = self.RowPointer, 
                     column = 8).value = "Totals"
        self.ws.cell(row = self.RowPointer, column = 8).font = Font(bold=True)

        self.RowPointer += 4    #Move 4 rows down for next stat group

#Write Heading for Injury Factors
        self.NumberOfHeadingElements = len(InjuryFactorHeadings)
        self.StatTableHeadings = InjuryFactorHeadings
        self.WriteHeadings()
        self.RowPointer += 1                                     #Move down 1 
        self.NumberOfHeadingElements = len(IF1Heading)
        self.StatTableHeadings = IF1Heading
        self.WriteHeadings()
        self.RowPointer += 1                                     #Move down 1 
        self.NumberOfHeadingElements = len(IF2Heading)
        self.StatTableHeadings = IF2Heading
        self.WriteHeadings()
        self.RowPointer += 1                                     #Move down 1 
        self.NumberOfHeadingElements = len(IF3Heading)
        self.StatTableHeadings = IF3Heading
        self.WriteHeadings()
        self.RowPointer += 1                                     #Move down 1 
        self.NumberOfHeadingElements = len(IF4Heading)
        self.StatTableHeadings = IF4Heading
        self.WriteHeadings()

        self.RowPointer += 2                                     #Move down 2 

#Write the End label
        self.ws.cell(row = self.RowPointer, column = 1).value = "End" 
        self.ws.cell(row = self.RowPointer, column = 1).font = Font(bold=True)

        self.ws.sheet_view.zoomScale = 173
        self.wb.save(filename = self.FileName)        
        self.wsStartingPoints['LastRow'] = self.RowPointer + 10
        
        
#****************************************************************************
#Method:   FormatCellsAndColumns
#Purpose:  Right now, this just sets the column widths but may be expanded to
#          handle other formatting chores
# Inputs:  ws- the active worksheet
# Outputs: Worksheet formatting
# Author:           Rick Burney
# Created:          02/27/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def FormatCellsAndColumns(self):

#Adjust width of the columns.  Will continue to adjust as needed
        self.ws.column_dimensions["A"].width = 16.0
        self.ws.column_dimensions["B"].width = 20.0
        self.ws.column_dimensions["C"].width = 10.0
        self.ws.column_dimensions["D"].width = 15.0
        self.ws.column_dimensions["E"].width = 10.0
        self.ws.column_dimensions["F"].width = 15.0    
        self.ws.column_dimensions["G"].width = 15.0
        self.ws.column_dimensions["H"].width = 20.0
        self.ws.column_dimensions["I"].width = 10.0
        self.ws.column_dimensions["J"].width = 15.0
        self.ws.column_dimensions["K"].width = 15.0
        self.ws.column_dimensions["L"].width = 15.0
        self.ws.column_dimensions["M"].width = 15.0
        
#Some cells with be left justified later
        for row in self.ws['A1:U400']:                  #Center everything  
            for cell in row:
                cell.alignment = Alignment(horizontal='center')   
        
        
#****************************************************************************
#Method:   TotalsLabel
#Purpose:  Stupid method to write the text "Totals" and to right-justify the 
#          text
# Inputs:  ws- the active worksheet, RowPointer
# Outputs: Worksheet formatting
# Author:           Rick Burney
# Created:          02/28/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def TotalsLabel(self):
 
#Write Totals Label, make bold and right-justify   
        #self.ws.cell(row = self.RowPointer, 
                     #column = 1).value = "                 Totals"
        #self.ws.cell(row = self.RowPointer, column = 1).font = Font(bold=True)
        
        self.RowPointer += 1    #Move to next row
       
        
#****************************************************************************
#Method:   WriteHeadings
#Purpose:  Write the headings for a stat group
# Inputs:  ws- the active worksheet, RowPointer, stat group headings
# Outputs: Worksheet formatting
# Author:           Rick Burney
# Created:          02/28/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def WriteHeadings(self):


#Write heading that is specific to the stat group and use bold font        
        for StatGroupHeader in range(self.NumberOfHeadingElements):
            self.ws.cell(row = self.RowPointer, 
                column = StatGroupHeader+1).value = \
                self.StatTableHeadings[StatGroupHeader] 
            self.ws.cell(row = self.RowPointer, 
                column = StatGroupHeader+1).font = Font(bold=True)
 
 
#****************************************************************************
#Method:   WriteDefensiveTeamStatHeadings
#Purpose:  Write the headings for a stat group
# Inputs:  ws- the active worksheet, RowPointer, stat group headings
# Outputs: Worksheet formatting
# Author:           Rick Burney
# Created:          02/28/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def WriteDefensiveTeamStatHeadings(self):

        DTRow1 = ["","D Rushing Ave","","","Kick Block %","","Punt Block %","",
                  "INT %"]
        DTRow2 = ["","P Completion %","","","Dsacks %","","","",
                  "FRec by D","","out of 10000"]
        DTRow3 = ["","Passing YPCatch"]
        

#Write general heading         
        self.ws.cell(row = self.RowPointer, 
                     column = 1).value = "Defensive Team Stats"
        self.ws.cell(row = self.RowPointer, column = 1).font = Font(bold=True)
        
        self.RowPointer += 1    #Next row
        
        for DTStatHeader in range(len(DTRow1)):
            self.ws.cell(row = self.RowPointer, 
                         column = DTStatHeader+1).value = DTRow1[DTStatHeader]
            self.ws.cell(row = self.RowPointer, 
                         column = DTStatHeader+1).font = Font(bold=True)
        
        self.RowPointer += 1    #Next row
        
        for DTStatHeader in range(len(DTRow2)):
            self.ws.cell(row = self.RowPointer, 
                         column = DTStatHeader+1).value = DTRow2[DTStatHeader]
            self.ws.cell(row = self.RowPointer, 
                         column = DTStatHeader+1).font = Font(bold=True)
        
        self.RowPointer += 1    #last row
        
        for DTStatHeader in range(len(DTRow3)):
            self.ws.cell(row = self.RowPointer, 
                         column = DTStatHeader+1).value = DTRow3[DTStatHeader]
            self.ws.cell(row = self.RowPointer, 
                         column = DTStatHeader+1).font = Font(bold=True)
        
