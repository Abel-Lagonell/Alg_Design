import random

# Initialize the Nodes
class Node:
    #Constructor
    def __init__(self):
        self.x = random.randint(0, 1000)
        self.y = random.randint(0, 1000)
        setCost()
        self.visited = False
    
    #String representation of the Node
    def __str__(self):
        return "City: (" + str(self.x) + ", " + str(self.y) + ") Cost: " + str(self.cost)
    
    #Setting the cost of the node based on the location
    def setCost(self):
        # calculate cost based on location of city using switch statement

    #Setting the node as visited
    def setVisited(self):
        self.visited = True

    #GET FUNCTIONS

    def getCost(self):
        return self.cost

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
