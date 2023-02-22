import Node

class Grid:
    #Constructor
    def __init__(self, budget=50, radius=5):
        self.__budget = budget
        self.__radius = radius
        self.__Nodes = [Node.Node() for i in range(100)]
        self.__set = []

    #Get the list of Nodes
    def getNodes(self):
        return self.__Nodes

    #Subtracting from the budget
    def subtractBudget(self, Node):
        self.__budget -= Node.getCost()

    #calculating total coverage
    def calculateCoverage(self):
        for node in self.__Nodes:
            if (node.getVisited() == True) :
                self.__coverage += 1

    #adding to the set of used nodes
    def addToSet(self, Node):
        self.__set.append(Node)