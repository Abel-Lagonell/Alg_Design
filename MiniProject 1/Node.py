import random
import math

# Initialize the Nodes
class Node:
    #Constructor
    def __init__(self):
        self.__x = random.randint(0, 1000)
        self.__y = random.randint(0, 1000)
        self.setCost()
        self.__visited = False
    
    #String representation of the Node
    def __str__(self):
        return "City: (" + str(self.__x) + ", " + str(self.__y) + ") Cost: " + str(self.__cost)
    
    #Setting the cost of the node based on the location
    def setCost(self):
        if (self.inRadius() == 0):
            self.__cost = random.uniform(0.1, 0.5)
        elif (self.inRadius() == 1):
            self.__cost = random.uniform(2, 5)
            self.__cost = random.uniform(5, 7)
        else:
            self.__cost = random.uniform(1, 2)

    #Setting the node as visited
    def setVisited(self):
        self.__visited = True

    #GET FUNCTIONS

    def getCost(self):
        return self.__cost

    def getX(self):
        return self.__x
    
    def getY(self):
        return self.__y

    def getVisited(self):
        return self.__visited

    #Distance between two nodes
    def getDistance(self, node):
        return math.sqrt((self.__x - node.getX())**2 + (self.__y - node.getY())**2)
    
    #Checks if node is in the radius of the price points and returns the price tier
    def inRadius(self):
        xLeft = (self.__x -167.5)**2
        xQuad1 = (self.__x - 781)**2
        xQuad4 = (self.__x - 658)**2
        yTop = (self.__y - 742)**2
        yBottom = (self.__y - 200)**2
        yLeft = (self.__y - 450.6)**2
        if (xLeft + yLeft <= 20600):
            return 0
        elif (xQuad1 + yTop <= 9000):
            return 1
        elif (xQuad4 + yBottom <= 8130):
            return 2