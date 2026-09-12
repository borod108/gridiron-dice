#****************************************************************************
#Method:   TableExtraction
#Purpose:  This class contains all of the methods and objects needed given a Table ID, to 
#                extract the relevant statistics for subsequent xfer to a stats worksheet.  Also 
#                used to help setup the structure of the stats worksheet
# Inputs:  Table_IDs
# Outputs: Extracted team and individual stats for subsequent xfer to a stats worksheet
# Author:           Rick Burney
# Created:          02/19/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
class TableExtraction():

    def __init__(self,Table_IDs,Table_Index, URL, IntURL):

#Import csv file library.  CSV stands for Comma-Separated Values. A comma-separated 
#values (CSV) file is a delimited text file that uses a comma to separate values.         
        import csv          

#Requests is a Python HTTP library, released under the Apache License 2.0. The goal is to 
#make HTTP requests simpler and more human-friendly.        
        import requests

#Beautiful Soup is a Python package for parsing HTML and XML documents. It creates a 
#parse tree for parsed pages that can be used to extract data from HTML, which is useful for 
#web scraping.        
        from bs4 import BeautifulSoup

#pandas is a library written for Python for data manipulation and analysis. In particular, it 
#offers data structures and operations for manipulating numerical tables and time series.        
        import pandas as pd
              
        self.Table_IDs = Table_IDs          #Don't use this, use Table_Index
        self.Table_Index = Table_Index  #Table index within a pandas frame
        self.NumberOfRows = 0              #Initialize number of rows in a table
        self.NumTables = 0                     #Initialize number of tables   
        self.URL = URL                             #Team stat URL except for Ints
        self.IntURL = IntURL     #Int stat URL since Team Stat page does not have Int yardage
                                                          
        dfs = pd.read_html(self.URL)                        #Read stats from team URL into data frame
        
#Not sure if the pandas display options are used.  Would be interesting to see what happens
#if the next two lines are commented out.
        pd.set_option('display.max_columns', 750)   #Set pandas frame display options
        pd.set_option('display.width', 1000)

        self.dfs = dfs                                  #Make data frame visible to all methods of this class
        self.count = 0
        self.idfs = pd.read_html(IntURL)

        
    #def Print_Table_IDs(self):

        #print(self.dfs1)
                

#****************************************************************************
#Method:   DetermineTableRowLengths
#Purpose:  Receives a Pandas data frame and a particular table in that frame and determines
#                the number of rows in that table
# Inputs:   Pandas data frame, Table index identifying the table 
# Outputs: # of rows in that table
# Author:           Rick Burney
# Created:          02/19/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def DetermineTableRowLengths(self):

        Generic_Table = self.dfs[self.Table_Index]          #Extract the table based on the index
        self.NumberOfRows = len(Generic_Table.index)  #Determine # of rows in the table

 
#****************************************************************************
#Method:   DetermineIntTableRowLengths
#Purpose:  Receives a Pandas data frame for interception stats for a particular team and 
#               extracts the interception table and determines the number of rows in that table
# Inputs:   Pandas data frame, Table index identifying the table 
# Outputs: # of rows in that table
# Author:           Rick Burney
# Created:          02/19/2020
# Copyright:        (c) Rick 2020
#****************************************************************************
    def DetermineIntTableRowLengths(self):
        
        Generic_Table = self.idfs[self.Table_Index]          #Extract the table based on the index
        self.NumberOfRows = len(Generic_Table.index)  #Determine # of rows in the table