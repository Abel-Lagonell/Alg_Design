from Node import Node
import random

class Grid:
    #Constructor
    def __init__(self, budget=50, radius=5, type =0):
        self.__budget = budget
        self.__radius = radius
        self.setNodes(type)
        self.__set = []
        self.__coverage = 0

    #resets the values
    def reset(self, budget=50, radius=5):
        self.__budget = budget
        self.__radius = radius


    #Get the list of Nodes
    def getNodes(self):
        return self.__Nodes

    #Get the set of used Nodes
    def getSet(self):
        return self.__set

    #Set the list of Nodes and in which ever form
    def setNodes(self, type=0):
        if (type == 0):
            self.__Nodes = [Node() for i in range(100)]
        elif (type == 1):
            totalNodes = 0
            cluster_size = random.randint(3, 6)
            while (totalNodes < 100):
                x = random.randint(0, 1000)
                y = random.randint(0, 1000)
                for i in range(cluster_size):
                    self.__Nodes.append(Node(type=1, x=x, y=y, radius=self.__radius))
                    totalNodes += 1
                cluster_size = random.randint(3, 6)

    #Subtracting from the budget
    def subtractBudget(self, Node:Node):
        self.__budget -= Node.getCost()

    #calculating total coverage
    def calculateCoverage(self):
        for node in self.__Nodes:
            if (node.getVisited() == True) :
                self.__coverage += 1
        return self.__coverage

    #adding node to set
    def addToSet(self, Node:Node, set:list[Node]):
        set.append(Node)

    #Setting the coverage of the node
    def setCoverage(self, Node:Node):
        for node in self.__Nodes:
            if (node.getVisited() == False):
                if (node.getDistance(Node.getX(), Node.getY()) <= self.__radius):
                    node.setVisited()

    #Calculating the coverage of the node and setting surrounding nodes as visited
    def calcCoverage(self, Node:Node, set:list[Node]):
        count =0
        for node in set:
            if (node.getDistance(Node.getX(), Node.getY()) <= self.__radius and Node.getVisited() == False):
                count +=1
        return count

    #Adding the node to the set and subtracting the cost from the budget
    def addNodeToSet(self, Node:Node, set:list[Node]):
        self.subtractBudget(Node)
        self.addToSet(Node, set)
        self.setCoverage(Node)

    #subtract the cost from the budget and add the node to the set
    def subtractIndexToSet(self, list:list[Node]):
        if(self.__budget != 0):
            self.__budget += list[-1].getCost()
            list.pop(-1)

    #THE ALGORITHMS

    #Random Algorithm
    def randomAlgorithm(self) -> list[Node]:
        coveredSet = []
        while (self.__budget > 0):
            index = random.randint(0, len(self.__Nodes)-1) #randomly select a node
            self.addNodeToSet(self.__Nodes[index], coveredSet)
        #This is needed as when the budget is negative it will add the last node's cost to the overall budget
        self.subtractIndexToSet(coveredSet)
        return coveredSet

    #Pure Greedy Algorithm
    def pureGreedyAlgorithm(self):
        coveredSet = []
        while(self.__budget >0):
            minCost =100
            minIndex = 0
            #Go through the list of nodes and find the one with the lowest cost
            for node in self.__Nodes:
                if (node.getCost() < minCost and node.getVisited() == False):
                    minCost = node.getCost()
                    minIndex = node
            self.addNodeToSet(minIndex, coveredSet)
        #This is needed as when the budget is negative it will add the last node's cost to the overall budget
        self.subtractIndexToSet(coveredSet)
        return coveredSet
    
    #Greedy Set Cover Algorithm
    def greedySetCoverAlgorithm(self):
        
        universe = self.__Nodes
        uncoveredSet = universe
        coveredSet = []
        maxCoverageRatio = 0

        while (self.__budget > 0):
            count =0
            for node in uncoveredSet:
                if (node.getVisited() == True):
                    uncoveredSet.pop(count)
                count +=1
            for node in uncoveredSet:
                if (self.calcCoverage(node,uncoveredSet)/node.getCost() > maxCoverageRatio):
                    maxCoverageRatio = self.calcCoverage(node,uncoveredSet)/node.getCost()
                    maxIndex = node
            self.addNodeToSet(maxIndex, coveredSet)
            maxCoverageRatio = 0
        #This is needed as when the budget is negative it will add the last node's cost to the overall budget
        self.subtractIndexToSet(coveredSet)
        return coveredSet