#****************************************************************************
#Method:    DrawField
#Purpose:   Executive routine for drawing the field.  Places the field and
#           then draws the outline, endzones, yardlines and yardmarkers.  Also
#           places the ball after a play
# Author:           Rick Burney
#
# Created:          Sometime in 2017
# Copyright:        (c) Rick 2017
#****************************************************************************
def DrawField():

    import turtle   #Turtle graphics library
    
    Win_width = 800   #In pixels, aspect ratio is purposely off
    Win_Height = 400
    Win_Startx = 300
    Win_Starty = 600
    Field_offset = 25                       #Number of pixels from the top of 
    Field_setx = Field_offset - Win_Height  #the window
    Field_sety = 175                        #Field outline dimensions
    Forwardx = 750                          #Field length                          
    FieldDrawAngle = 90                #Allows the turtle to make right angles
    Forwardy = 160                     #Field width
    EndZone_width = 75                 #Endzone width
    HomeEndZone_x = -300          #Starting x position of the home endzone
    VisitorEndZone_x = 375        #Starting y position of the visitors endzone
    
    turtle.speed(0)        #Sets the speed to fast.  Consider using 0 for 
                            #the fastest graphics

#Set the size and the position of the turtle window
    turtle.setup(width=Win_width,height=Win_Height,startx=Win_Startx,
                 starty=Win_Starty)
    turtle.color("black","green")
    turtle.penup()

#Draw field outline and fill 
    turtle.setx(Field_setx)
    turtle.sety(Field_sety)
    turtle.pendown()
    turtle.begin_fill()             #Start to draw field
    turtle.forward(Forwardx)        #Draw line to the right
    turtle.right(FieldDrawAngle)    #Turn 90 degrees
    turtle.forward(Forwardy)        #Draw line down
    turtle.right(FieldDrawAngle)    #Turn 90 degrees
    turtle.forward(Forwardx)        #Draw lilne to the left
    turtle.right(FieldDrawAngle)    #Turn 90 degrees
    turtle.forward(Forwardy)        #Draw line up to complete the field
    turtle.end_fill()               #Fill the field with the field color
    
#Draw both endzones
    DrawEndZones(HomeEndZone_x,Field_sety,Forwardy,FieldDrawAngle,
                     EndZone_width)    
    DrawEndZones(VisitorEndZone_x,Field_sety,Forwardy,FieldDrawAngle,
                     EndZone_width) 

#Draw the yardlines
    DrawYardLines(HomeEndZone_x,Field_sety,FieldDrawAngle,Forwardy) 


#****************************************************************************
#Method:    DrawEndZones
#Purpose:   Draw an endzone
# Author:           Rick Burney
#
# Created:          Sometime in 2017
# Copyright:        (c) Rick 2017
#****************************************************************************    
def DrawEndZones(EndZone_x,Field_sety,Forwardy,FieldDrawAngle,
                    EndZone_width):

    import turtle   #Use Turtle Graphics to do the drawing
    
    turtle.penup()                      #Lift pen before moving cursor
    turtle.setpos(EndZone_x,Field_sety) #Move cursor to positions that were
                                        #passed into this method
    
    turtle.color("black","black")       
    turtle.pendown()
    turtle.begin_fill()
    turtle.back(Forwardy)
    turtle.left(FieldDrawAngle)
    turtle.forward(EndZone_width)
    turtle.right(FieldDrawAngle)
    turtle.forward(Forwardy)
    turtle.right(FieldDrawAngle)
    turtle.forward(EndZone_width)
    turtle.end_fill()
    turtle.left(FieldDrawAngle)
    

#****************************************************************************
#Method:    DrawYardLines
#Purpose:   Draws the yardlines
# Author:           Rick Burney
#
# Created:          Sometime in 2017
# Copyright:        (c) Rick 2017
#****************************************************************************
def DrawYardLines(EndZone_x,Field_sety,FieldDrawAngle,Forwardy):
    
    import turtle
    
    NumberofYardLines = 10
    
    turtle.penup()                      #Make sure pen is up before you move
    turtle.setpos(EndZone_x,Field_sety) #position
    
    turtle.color("white","white")   #White lines with white outline 

    for i in range(0,NumberofYardLines-1):    #Draw 10 evenly-spaced yardlines
        turtle.setheading(0)                #Point east
        turtle.forward(60)                  #Move to the next yardline
        turtle.right(FieldDrawAngle)        #Point south
        turtle.pendown()
        turtle.forward(160) #Draw the yardlines
        turtle.penup()
        turtle.setheading(90)   #Move to the top of the field
        turtle.forward(160)

#write the yardline markers, 10 - 50 - 10        
    turtle.setposition(-240,120)
    turtle.write("10",False,align="center",font=("Arial", 22, "normal"))
    turtle.setposition(-180,120)
    turtle.write("20",False,align="center",font=("Arial", 22, "normal"))
    turtle.setposition(-120,120)
    turtle.write("30",False,align="center",font=("Arial", 22, "normal"))
    turtle.setposition(-60,120)
    turtle.write("40",False,align="center",font=("Arial", 22, "normal"))
    turtle.setposition(0,120)
    turtle.write("50",False,align="center",font=("Arial", 22, "normal"))
    turtle.setposition(60,120)
    turtle.write("40",False,align="center",font=("Arial", 22, "normal"))
    turtle.setposition(120,120)
    turtle.write("30",False,align="center",font=("Arial", 22, "normal"))
    turtle.setposition(180,120)
    turtle.write("20",False,align="center",font=("Arial", 22, "normal"))
    turtle.setposition(240,120)
    turtle.write("10",False,align="center",font=("Arial", 22, "normal"))
     


#****************************************************************************
#Method:    PlaceBall
#Purpose:   Receives the yardline and who is on offense (to determine the
#           direction) and uses these inputs to place the ball on the field
# Author:           Rick Burney
#
# Created:          Sometime in 2017
# Copyright:        (c) Rick 2017
#****************************************************************************
def PlaceBall(YardLine,TeamwiththeBallFlag):
    
    import turtle
    

    HomeTeamEndzone_x = -300    #Starting points for knowing where to place 
    VisitingTeamEndzone_x = 300 #the ball
    BallPosition_y = 80         #Places the ball in the middle of the field
    HomeTeamHeading = 0         #Home team always moves left to right
    VisitingTeamHeading = 180   #Visiting team always moves right to left
    YardageScaleFactor = 6      #Horizontal position scale factor per yard
    
    turtle.penup()
    astamp = turtle.stamp()        #Create an ID for the turtle icon
    turtle.clearstamp(astamp)      #Now clear the icon at the current position
    if TeamwiththeBallFlag == 0:        #Determine if home team is on offense
        Endzone_x = HomeTeamEndzone_x   #Register the endzone position and set
        Heading = HomeTeamHeading       #the direction of forward yardage
        
    else:
        Endzone_x = VisitingTeamEndzone_x   #Do the same but for the visiting
        Heading = VisitingTeamHeading       #team.  Remember to make the 
        YardLine = -YardLine                #yardline negative since going R>L

#Determine the direction of forward yardage
    turtle.setheading(Heading)              
    BallPosition = Endzone_x + YardLine*YardageScaleFactor  #Place the ball at
    turtle.setposition(BallPosition,BallPosition_y)         #the new yardline
    
    return None