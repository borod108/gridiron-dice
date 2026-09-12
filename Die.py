#-----------------------------------------------------------------------------
# Name:        Class-Roll 3 Die
# Purpose:     Methods for die with varying radices
#
# Author:      Rick
#
# Created:     10/19/2016
# Copyright:   (c) Rick 2016
# License:     <We don't need no stinking license>
#-----------------------------------------------------------------------------
class RolltheDie:
    import random

    """A dice rolling class.  Different functions for different radices but
    always 3 die"""

    def __init__(self):
        self.dice1 = 1
        self.dice2 = 1
        self.dice3 = 1


    def Dice3Dice6Dice6(self):
        import random               #Each function needs to import random

#roll 3 die
        self.dice1=random.randint(1,3)
        self.dice2=random.randint(1,6)
        self.dice3=random.randint(1,6)
        return self.dice1,self.dice2,self.dice3   #return is a 3 element tuple

    def SingleValue31010(self):
        import random               #Each function needs to import random

#roll 3 die
        self.dice1=random.randint(1,3)
        self.dice2=random.randint(1,10)
        self.dice3=random.randint(1,10)
        result = self.dice3*self.dice2+self.dice1
        return result               #Single value return for this function


    def SingleValue366(self):
        import random               #Each function needs to import random

#roll 3 die
        self.dice1=random.randint(1,3)
        self.dice2=random.randint(4,7)  #Changed range from (1,6) to (4,7) on
        self.dice3=random.randint(4,7)  #1/31/2017
        
        result = self.dice3*self.dice2+self.dice1
        return result               #Single value return for this function



    


    def SingleValue577(self):
        import random               #Each function needs to import random
    
    #roll 3 die
        self.dice1=random.randint(1,5)
        self.dice2=random.randint(1,7)
        self.dice3=random.randint(1,7)
        result = self.dice3*self.dice2+self.dice1
        return result               #Single value return for this function



    def SingleValue91010(self):
        import random               #Each function needs to import random
    
    #roll 3 die
        self.dice1=random.randint(1,9)
        self.dice2=random.randint(4,10) #Changed min value from 1 to 4 on
        self.dice3=random.randint(4,10)             #1/22/17
        result = self.dice3*self.dice2+self.dice1
        return result               #Single value return for this function
