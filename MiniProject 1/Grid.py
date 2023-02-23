import Node
import random

class Grid:
    #Constructor
    def __init__(self, budget=50, radius=5, type =0):
        self.__budget = budget
        self.__radius = radius
        self.setNodes(type=0)
        self.__set = []
        self.__coverage = 0

    #Get the list of Nodes
    def getNodes(self):
        return self.__Nodes

    #Get the set of used Nodes
    def getSet(self):
        return self.__set

    #Set the list of Nodes and in which ever form
    def setNodes(self, type=0):
        if (type == 0):
            self.__Nodes = [Node.Node() for i in range(100)]
        elif (type == 1):
            totalNodes = 0
            cluster_size = random.randint(3, 6)
            while (totalNodes < 100):
                x = random.randint(0, 1000)
                y = random.randint(0, 1000)
                for i in range(cluster_size):
                    self.__Nodes.append(Node.Node(type=1, x=x, y=y, radius=self.__radius))
                    totalNodes += 1
                cluster_size = random.randint(3, 6)

    #Subtracting from the budget
    def subtractBudget(self, Node):
        self.__budget -= Node.getCost()

    #calculating total coverage
    def calculateCoverage(self):
        for node in self.__Nodes:
            if (node.getVisited() == True) :
                self.__coverage += 1
        return self.__coverage

    #adding to the set of used nodes
    def addToSet(self, Node):
        self.__set.append(Node)

    #Calculating the coverage of the node and setting surrounding nodes as visited
    def coverageCalc(self, index):
        for node in self.__Nodes:
            if (node.getVisited() == False):
                if (node.getDistance(self.__Nodes[index]) <= self.__radius):
                    node.setVisited()

    #subtract the cost from the budget and add the node to the set
    def addIndexToSet(self, index):
        self.subtractBudget(self.__Nodes[index])
        self.__Nodes[index].setVisited()
        self.addToSet(self.__Nodes[index])
        self.coverageCalc(index)

    def subtractIndexToSet(self):
        if(self.__budget != 0):
            self.__budget += self.__set[-1].getCost()
            self.__set.pop()

    #THE ALGORITHMS

    #Random Algorithm
    def randomAlgorithm(self):
        while (self.__budget > 0):
            index = random.randint(0, len(self.__Nodes)-1) #randomly select a node
            self.addIndexToSet(index)
        #This is needed as when the budget is negative it will add the last node's cost to the overall budget
        self.subtractIndexToSet()

    #Pure Greedy Algorithm
    def pureGreedyAlgorithm(self):
        while(self.__budget >0):
            minCost =100
            minIndex = 0
            #Go through the list of nodes and find the one with the lowest cost
            for i in range(len(self.__Nodes)):
                if (self.__Nodes[i].getCost() < minCost and self.__Nodes[i].getVisited() == False):
                    minCost = self.__Nodes[i].getCost()
                    minIndex = i
            self.addIndexToSet(minIndex)
        #This is needed as when the budget is negative it will add the last node's cost to the overall budget
        self.subtractIndexToSet()
