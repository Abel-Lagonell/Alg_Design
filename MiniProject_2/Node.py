import random
import math

# Initialize the Nodes
class Node:
    #Constructor, RADIUS = 5
    def __init__(self, cost:int, type = 0, x=50, y=50, ID=0):
        self.setCoords(type, x, y)
        self.setCost(cost)
        self.__visited = False
        self.ID = ID

    #String representation of the Node
    def __str__(self):
        return "City: ({:3}, {:3})\tCost: {:1.2f}".format(self.__x, self.__y, self.__cost)
    
    def __repr__(self):
        return "{:02}".format(self.ID)

    def __eq__(self, other):
        if (other == None):
            return False
        if (self.__x == other.getX() and self.__y == other.getY() and self.__cost == other.getCost()):
            return True
        
    
    #Setting the coordinates of the node wether it is random or clustered
    def setCoords(self, type=0, x=50, y=50):
        if (type == 0): #Randomly generated coordinates
            self.__x = random.randint(0, 100)
            self.__y = random.randint(0, 100)
        elif (type == 1): #Randomly generated Clustered coordinates
            self.__x = random.randint(0, 10) + x
            self.__y = random.randint(0, 10) + y
    
    def setCost(self, cost:int):
        self.__cost = cost

    #Setting the node as visited
    def setVisited(self, value:bool = True):
        self.__visited = value

    def setID(self, ID:int):
        self.ID = ID

    #GET FUNCTIONS

    def getCost(self):
        return self.__cost

    def getX(self):
        return self.__x
    
    def getY(self):
        return self.__y
    
    def getID(self):
        return self.ID

    def getVisited(self):
        return self.__visited

    #Distance between two nodes
    def getDistance(self, x:int, y:int):
        return math.sqrt((self.__x - x)**2 + (self.__y - y)**2)