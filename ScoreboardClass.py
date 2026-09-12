#-----------------------------------------------------------------------------
# Name:        Scoreboard Class
# Purpose:     Methods that sets up the scoreboard with widgets.  Currently,
#              button methods are not called but will be in the future
# Author:      Rick
#
# Created:     11/14/2016
# Copyright:   (c) Rick 2016
# Licence:     <your licence>
#-----------------------------------------------------------------------------

class Scoreboard:





#-----------------------------------------------------------------------------
# Method Name:    PlaceButton
# Purpose:        Places a button into the parent frame.  Currently not used
# Author:         Rick Burney
#
# Created:        11/18/2016
# Copyright:      (c) Rick 2016
#-----------------------------------------------------------------------------
    def PlaceButton(self,Parent,text,row,column,pad):
        import Tkinter

        ButtonName = Tkinter.Button(Parent, text=text).grid(row=row,
                                                            column=column,
                                                            padx=pad,pady=pad)
        return None

#-----------------------------------------------------------------------------
# Method Name:    PlaceCheckBox
# Purpose:        Places a checkbox into the parent frame.
# Author:         Rick Burney
#
# Created:        11/18/2016
# Copyright:      (c) Rick 2016
#-----------------------------------------------------------------------------
    def PlaceCheckBox(self,Parent,text,row,column,pad,sticky):
        import Tkinter

        ButtonName = Tkinter.Checkbutton(Parent, text=text,onvalue = 1,
                                           offvalue = 0 ).grid(row=row,
                                            column=column, padx=pad,pady=pad,
                                            sticky = sticky)


        return None

#-----------------------------------------------------------------------------
# Method Name:    PlaceLabel
# Purpose:        Places a label into the parent frame.  The label is blank
# Author:         Rick Burney
#
# Created:        11/18/2016
# Copyright:      (c) Rick 2016
#-----------------------------------------------------------------------------
    def PlaceLabel(self,Parent,width,height,row,column,pad,sticky):
        import Tkinter

        if sticky == "":
            LabelName = Tkinter.Label(Parent, width=width,
                                    height=height).grid(row=row,column=column,
                                    padx=pad,pady=pad)
        else:
            LabelName = Tkinter.Label(Parent, width=width,
                                    height=height).grid(row=row,column=column,
                                    padx=pad,pady=pad,sticky = sticky)
        return None


#-----------------------------------------------------------------------------
# Method Name:    WriteLabel
# Purpose:        Writes a label into the parent frame.
# Author:         Rick Burney
#
# Created:        11/18/2016
# Copyright:      (c) Rick 2016
#-----------------------------------------------------------------------------
    def WriteLabel(self,Parent,text,width,height,fg,bg,fontsize,row,column,
                   pad,sticky):

        import Tkinter

        if sticky == "":
            LabelName = Tkinter.Label(Parent, text=text, width=width,
                                    height=height,fg=fg,bg=bg,
                                    font=("Helvetica", 
                                          fontsize)).grid(row=row,
                                            column=column,padx=pad,pady=pad)
        else:
            LabelName = Tkinter.Label(Parent, text=text, width=width,
                                    height=height,fg=fg,bg=bg,
                                    font=("Helvetica", 
                                          fontsize)).grid(row=row,
                                            column=column,padx=pad,pady=pad,
                                                            sticky=sticky)

        return None




    def WriteStringVarLabel(self,Parent,text,width,height,fg,bg,fontsize,row,
                            column,pad,sticky):

        import Tkinter

        if sticky == "":
            LabelName = Tkinter.Label(Parent, textvariable=text, width=width,
                                    height=height,fg=fg,bg=bg,
                                    font=("Helvetica", 
                                          fontsize)).grid(row=row,
                                            column=column,padx=pad,pady=pad)
        else:
            LabelName = Tkinter.Label(Parent, textvariable=text, width=width,
                                    height=height,fg=fg,bg=bg,
                                    font=("Helvetica", 
                                          fontsize)).grid(row=row,
                                            column=column,padx=pad,pady=pad,
                                                            sticky=sticky)

        return None
    
    def UpdateScore(self,TeamScore,Score):
        
        TeamScore += Score
        
        return TeamScore

#-----------------------------------------------------------------------------
# Method Name:    ResultDisplay
# Purpose:        Updates all items on the Scoreboard using a common method
# Inputs:         Code - See below for code definition
#                 Message - A pre-canned message can be passed into this
#                           method or the method can construct the message
#                 Subcode - depends on the code but an example would be a kick
#                           return for a touchdown - 0 means that there is no
#                           Subcode
#                 Parent - Awkward but the calling routine will have to know
#                          the frame
# Author:         Rick Burney
#
# Created:        11/18/2016
# Copyright:      (c) Rick 2016
#-----------------------------------------------------------------------------
    def ResultDisplay(self,Code,Message,Subcode,Parent):
        
        import Tkinter
        
        global YardLine
        
# Display Location Constants
# Standard constants
        width = 3
        height = 1
        fg = "black"
        bg = "white"
        font = "Helvetica"
        fontsize = 36
        padx = 0
        pady = 0
        sticky = ""
        
#Scoreboard-specific constants
        Down_width = 2
        Down_height = 2
        Down_fg = "white"
        Down_bg = "black"
        Down_fontsize = 24
        Down_row = 7
        Down_column = 1
        Down_sticky = "E"
        HomeScore_row = 4
        HomeScore_column = 1
        HomeScore_padx = HomeScore_pady = 2
        HomeScore_sticky = "NE"
        HomeTeamOnOffense_width = VisitingTeamOnOffense_width = 2
        HomeTeamOnOffense_fontsize = VisitingTeamOnOffense_fontsize = 8
        HomeTeamOnOffense_row = VisitingTeamOnOffense_row = 4
        HomeTeamOnOffense_column = 2
        VisitingTeamOnOffense_column = 6
        HomeTeamOnOffense_sticky = VisitingTeamOnOffense_sticky = "W"
        PlayCall_width = 80
        PlayCall_height = 2
        PlayCall_fontsize = 24 #Best fit so that entire play will fit in field
        PlayCall_row = 1        #Top of Frame #1
        PlayCall_column = 4
        PlayCall_sticky = "W"   #Left-justify
        PlayResult_width = 100  #Essentially allows for 11 characters
        PlayResult_height = 2
        PlayResult_fontsize = 20
        PlayResult_fontsize_determinant = 1440
        PlayResult_row = 4
        PlayResult_column = 4
        PlayResult_padx = 5
        PlayResult_pady = 0
        PlayResult_sticky = "W"
        Quarter_width = 3
        Quarter_height = 1
        Quarter_fontsize = 24
        Quarter_row = 4
        Quarter_column = 4
        Quarter_sticky = "E"
        Time_width = 6
        Time_height = 2
        Time_fg = "white"
        Time_bg = "black"
        Time_row = 3
        Time_column = 4
        HomeTimeouts_fg = "white"
        HomeTimeouts_bg = "black"
        HomeTimeouts_fontsize = 24
        HomeTimeouts_column = 2
        HomeTimeouts_row = 5
        HomeTimeouts_sticky = "W"
        VisitorScore_row = 4
        VisitorScore_column = 6
        VisitorScore_padx = VisitorScore_pady = 5
        VisitorTimeouts_fg = "white"
        VisitorTimeouts_bg = "black"
        VisitorTimeouts_column = 8
        VisitorTimeouts_row = 5
        VisitorTimeouts_fontsize = 24
        VisitorTimeouts_sticky = "W"
        YardLine_height = 2
        YardLine_fg = "white"
        YardLine_bg = "black"
        YardLine_fontsize = 24
        YardLine_row = 7
        YardLine_column = 6
        YardLine_sticky = "W"
        YardsToGo_width = 5
        YardsToGo_height = 2
        YardsToGo_fg = "white"
        YardsToGo_bg = "black"
        YardsToGo_fontsize = 24
        YardsToGo_row = 7
        YardsToGo_column = 4
        YardsToGo_sticky = "W"
        

        
# Code Definition
# 0     Coin Toss
# 1     Play Result
# 2     Touchdown
# 3     Time
# 4     Quarter
# 5     Down
# 6     Yards to Go     
# 7     Yard Line
# 8     Kickoff to, Kick Return to, (TD)
# 9     Field Goal
# 10    Extra Point
# 11    2-Point Conversion
# 12    Punt to, Punt Return to, (TD)
# 13    Int, Int Return to, (TD)
# 14    Fumble, Who Recovers (TD)
# 15    Team with the Ball
# 16    Which half of the Field
# 17    Go For It on 4th Down
# 18    Home Team Score Update
# 19    Visiting Team Score Update
# 20    Home Team Timeouts
# 21    Visiting Team Timeouts
# 22    Injury on the field
# 23    Penalties
# 24    Play Call
# 25    Home Team has the ball indicator
# 26    Visiting Team has the ball indicator

#Coin Toss - Use Play Result Display
        if Code == 0:
            LabelName = Tkinter.Label(Parent, text=Message, 
                                      width=PlayResult_width,
                                      height=PlayResult_height,fg=fg,bg=bg,
                                      font=("Helvetica", 
                                PlayResult_fontsize)).grid(row=PlayResult_row,
                                column=PlayResult_column,padx=PlayResult_padx,
                                pady=PlayResult_pady,sticky=PlayResult_sticky)

#Play Result - Use Play Result Display
        if Code == 1:
            if len(Message) < 60:
                fontsize = 20
            elif len(Message) < 80:
                fontsize = 18
            else:
                fontsize = 16
            LabelName = Tkinter.Label(Parent, text=Message, 
                                        width=PlayResult_width,
                                        height=PlayResult_height,fg=fg,bg=bg,
                                          font=("Helvetica", 
                                PlayResult_fontsize)).grid(row=PlayResult_row,
                                column=PlayResult_column,padx=PlayResult_padx,
                                pady=PlayResult_pady,sticky=PlayResult_sticky)
            

#Touchdown - Use Play Result Display - Note: TDs from scrimmage plays use Code
#1.  Return touchdowns use this code
        if Code == 2:
            LabelName = Tkinter.Label(Parent, text=Message, 
                                        width=PlayResult_width,
                                        height=PlayResult_height,fg=fg,bg=bg,
                                          font=("Helvetica", 
                                PlayResult_fontsize)).grid(row=PlayResult_row,
                                column=PlayResult_column,padx=PlayResult_padx,
                                pady=PlayResult_pady,sticky=PlayResult_sticky)
            
#Time Left in the Quarter - passed in as Message
        if Code == 3:
            
            LabelName = Tkinter.Label(Parent, text=Message, width=Time_width,
                                        height=Quarter_height,fg=Time_fg,
                                        bg=Time_bg,font=("Helvetica", 
                                fontsize)).grid(row=Time_row,
                                                column=Time_column,padx=padx,
                                pady=pady,sticky=sticky)


            
#Quarter - passed in as Message
        if Code == 4:
            
            LabelName = Tkinter.Label(Parent, text=Message, 
                                      width=Quarter_width,
                                      height=Quarter_height,fg=fg,bg=bg,
                                      font=("Helvetica",
                                    Quarter_fontsize)).grid(row=Quarter_row,
                                    column=Quarter_column,padx=padx,pady=pady,
                                    sticky=sticky)



            
#Down - passed in as Message
        if Code == 5:
            
            LabelName = Tkinter.Label(Parent, text=Message, width=Down_width,
                                      height=Down_height,fg=Down_fg,
                                      bg=Down_bg,font=("Helvetica",
                                    Down_fontsize)).grid(row=Down_row,
                                    column=Down_column,padx=padx,pady=pady,
                                    sticky=Down_sticky)
        

#Yards to Go - passed in as Message
        if Code == 6:
            
            LabelName = Tkinter.Label(Parent, text=Message, 
                                      width=YardsToGo_width,
                                      height=YardsToGo_height,fg=YardsToGo_fg,
                                      bg=YardsToGo_bg,font=("Helvetica",
                                YardsToGo_fontsize)).grid(row=YardsToGo_row,
                                column=YardsToGo_column,padx=padx,pady=pady,
                                sticky=YardsToGo_sticky)

#Yardline - passed in as Message
        if Code == 7:
            
            LabelName = Tkinter.Label(Parent, text=Message, width=width,
                                      height=YardLine_height,fg=YardLine_fg,
                                      bg=YardLine_bg,font=("Helvetica",
                                YardLine_fontsize)).grid(row=YardLine_row,
                                column=YardLine_column,padx=padx,pady=pady,
                                sticky=YardLine_sticky)


#Kickoffs - Making this up as I go along - Need to deal with the Kickoff,
#return and use the subcode if a kickoff return for a touchdown happens - 
#wound up not using the subcode
        if Code == 8:
            
            LabelName = Tkinter.Label(Parent, text=Message, 
                                        width=PlayResult_width,
                                        height=PlayResult_height,fg=fg,bg=bg,
                                          font=("Helvetica", 
                                PlayResult_fontsize)).grid(row=PlayResult_row,
                                column=PlayResult_column,padx=PlayResult_padx,
                                pady=PlayResult_pady,sticky=PlayResult_sticky)


#Field Goals 
        if Code == 9:
            
            LabelName = Tkinter.Label(Parent, text=Message, 
                                        width=PlayResult_width,
                                        height=PlayResult_height,fg=fg,bg=bg,
                                          font=("Helvetica", 
                                PlayResult_fontsize)).grid(row=PlayResult_row,
                                column=PlayResult_column,padx=PlayResult_padx,
                                pady=PlayResult_pady,sticky=PlayResult_sticky)


#Extra Points 
        if Code == 10:
            
            LabelName = Tkinter.Label(Parent, text=Message, 
                                        width=PlayResult_width,
                                        height=PlayResult_height,fg=fg,bg=bg,
                                          font=("Helvetica", 
                                PlayResult_fontsize)).grid(row=PlayResult_row,
                                column=PlayResult_column,padx=PlayResult_padx,
                                pady=PlayResult_pady,sticky=PlayResult_sticky)


#2 Point Conversion 
        if Code == 11:
            
            LabelName = Tkinter.Label(Parent, text=Message, 
                                        width=PlayResult_width,
                                        height=PlayResult_height,fg=fg,bg=bg,
                                          font=("Helvetica", 
                                PlayResult_fontsize)).grid(row=PlayResult_row,
                                column=PlayResult_column,padx=PlayResult_padx,
                                pady=PlayResult_pady,sticky=PlayResult_sticky)

#Punts and returns
        if Code == 12:
            
            LabelName = Tkinter.Label(Parent, text=Message, 
                                        width=PlayResult_width,
                                        height=PlayResult_height,fg=fg,bg=bg,
                                          font=("Helvetica", 
                                PlayResult_fontsize)).grid(row=PlayResult_row,
                                column=PlayResult_column,padx=PlayResult_padx,
                                pady=PlayResult_pady,sticky=PlayResult_sticky)






#Home Team Score Update
        if Code == 18:
            
            LabelName = Tkinter.Label(Parent, text=Message, width=width,
                                        height=height,fg=fg,bg=bg,
                                          font=("Helvetica", 
                                fontsize)).grid(row=HomeScore_row,
                                column=HomeScore_column,padx=HomeScore_padx,
                                pady=HomeScore_pady,sticky=HomeScore_sticky)



#Visiting Team Score Update
        if Code == 19:
            
            LabelName = Tkinter.Label(Parent, text=Message, width=width,
                                        height=height,fg=fg,bg=bg,
                                          font=("Helvetica", 
                            fontsize)).grid(row=VisitorScore_row,
                            column=VisitorScore_column,padx=VisitorScore_padx,
                            pady=VisitorScore_pady,sticky=sticky)

#Home Team Timeouts
        if Code == 20:
            
            LabelName = Tkinter.Label(Parent, text=Message, width=width,
                                        height=height,fg=HomeTimeouts_fg,
                                        bg=HomeTimeouts_bg,font=("Helvetica", 
                            HomeTimeouts_fontsize)).grid(row=HomeTimeouts_row,
                            column=HomeTimeouts_column,padx=VisitorScore_padx,
                            pady=VisitorScore_pady,sticky=HomeTimeouts_sticky)

#Home Team Timeouts
        if Code == 21:
            
            LabelName = Tkinter.Label(Parent, text=Message, width=width,
                    height=height,fg=VisitorTimeouts_fg,
                    bg=VisitorTimeouts_bg,font=("Helvetica", 
                    VisitorTimeouts_fontsize)).grid(row=VisitorTimeouts_row,
                    column=VisitorTimeouts_column,padx=VisitorScore_padx,
                    pady=VisitorScore_pady,sticky=VisitorTimeouts_sticky)

#Play Call Field
        if Code == 24:
            
            LabelName = Tkinter.Label(Parent, text=Message, 
                                      width=PlayCall_width,
                                        height=PlayCall_height,fg=fg,bg=bg,
                                          font=("Helvetica", 
                            PlayCall_fontsize)).grid(row=PlayCall_row,
                            column=PlayCall_column,padx=padx,
                            pady=pady,sticky=PlayCall_sticky)

#Home Team has the ball indicator - message passed in a color with no quotes
#for the fg/bg - not currently call by the indicator routine
        if Code == 25:
            
            LabelName = Tkinter.Label(Parent, text="", 
                                        width=HomeTeamOnOffense_width,
                                        height=height,fg=Message,bg=Message,
                font=("Helvetica", 
                HomeTeamOnOffense_fontsize)).grid(row=HomeTeamOnOffense_row,
                column=HomeTeamOnOffense_column,padx=padx,pady=pady,
                sticky=HomeTeamOnOffense_sticky)

#Visiting Team has the ball indicator
        if Code == 26:
            
            LabelName = Tkinter.Label(Parent, text="", 
                                        width=VisitingTeamOnOffense_width,
                                        height=height,fg=Message,bg=Message,
        font=("Helvetica", 
        VisitingTeamOnOffense_fontsize)).grid(row=VisitingTeamOnOffense_row,
        column=VisitingTeamOnOffense_column,padx=padx,pady=pady,
        sticky=VisitingTeamOnOffense_sticky)

        return None


#-----------------------------------------------------------------------------
# Method Name:    ErrorMessage
# Purpose:        Opens up a message box to tell the user that they have 
#                 pressed a button inappropriately (illegal touching).  For 
#                 example, pressing the Call Play button at the beginning of 
#                 the 3rd quarter without doing a kickoff.  The burden of  
#                 detecting the error is on the calling program.
# Inputs:         Title - title of the message box, usually Error but may also
#                         mention that the wrong button was pushed
#                 Message - the error message displayed in the message box.
# Author:         Rick Burney
#
# Created:        1/25/2017
# Copyright:      (c) Rick 2017
#-----------------------------------------------------------------------------
    def ErrorMessage(self,Title,Message):

#This module provides access to some variables used or maintained by the interpreter and 
#to functions that interact strongly with the interpreter.
        import sys  
        
        if sys.version_info < (3,0):               #Really no idea what this code does.  Taken from
            import Tkinter as tkinter            #the web.  Need to research and then document
            import tkMessageBox as mbox   #Used to display message boxes
        else:
            import tkinter                      #Tkinter is Python's de-facto
            import tkinter.messagebox as mbox   #standard GUI (Graphical User
                                                #Interface) package
        window = tkinter.Tk()            #Don't show the main TK Window in the
        window.wm_withdraw()             #background.  This is essential

        mbox.showinfo(Title,Message)        
        
        
        
        return None
   