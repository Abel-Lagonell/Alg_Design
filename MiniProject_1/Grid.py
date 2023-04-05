from Node import Node
from PriorityQueue import PriorityQueue as PQ
import random

class Grid:
    #Constructor
    def __init__(self, budget=50, radius=5, type =0):
        self.__budget = budget
        self.__radius = radius
        self.__Nodes = []
        self.setNodes(type)

    #resets the values
    def reset(self, budget=50, radius=5):
        self.__budget = budget
        self.__radius = radius

    #Get the list of Nodes
    def getNodes(self):
        return self.__Nodes

    #Set the list of Nodes and in which ever form
    def setNodes(self, type=0):
        if (type == 0):
            self.__Nodes = [Node(ID=i) for i in range(100)]
        elif (type == 1):
            totalNodes = 0
            cluster_size = random.randint(3, 6)
            while (totalNodes < 100):
                x = random.randint(0, 1000)
                y = random.randint(0, 1000)
                for i in range(cluster_size):
                    self.__Nodes.insert(i, Node(type=1, x=x, y=y, radius=self.__radius, ID=totalNodes+i))
                totalNodes += cluster_size
                cluster_size = random.randint(3, 6)

    #Get the smallest costing node
    def getSmallestCost(self, set:list[Node]):
        smallest = set[0]
        for node in set:
            if (node.getCost() < smallest.getCost() and node.getVisited() == False):
                smallest = node
        return smallest
    
    #Subtracting from the budget
    def subtractBudget(self, Node:Node):
        self.__budget -= Node.getCost()
        self.__budget = round(self.__budget, 2)

    #calculating total coverage
    def calculateCoverage(self):
        coverage = 0
        for node in self.__Nodes:
            if (node.getVisited() == True) :
                coverage += 1
        return coverage

    #adding node to set
    def addToSet(self, Node:Node, set:list[Node]):
        set.append(Node)

    #Setting the coverage of the node
    def setCoverage(self, Node:Node):
        for node in self.__Nodes:
            if (node.getVisited() == False):
                if (node.getDistance(Node.getX(), Node.getY()) <= self.__radius):
                    node.setVisited()

    def resetCoverage(self):
        for node in self.__Nodes:
            node.setVisited(False)

    #Calculating the coverage of the node and setting surrounding nodes as visited
    def calcCoverage(self, Node:Node, set:list[Node]):
        count =0
        for node in set:
            if (node.getDistance(Node.getX(), Node.getY()) <= self.__radius and Node.getVisited() == False):
                count +=1
        return count
    
    def calcTotalCoverage(self, set:list[Node]):
        count =0
        for node in set:
            for node2 in self.__Nodes:
                if (node.getDistance(node2.getX(), node2.getY()) <= self.__radius):
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
            self.__budget += round(list[-1].getCost())
            self.__budget = round(self.__budget, 2)
            list.pop(-1)

    #THE ALGORITHMS

    #Random Algorithm
    def randomAlgorithm(self,totalUsedBudget = [0,0,0]):
        tempBudget = self.__budget
        coveredSet = []
        while (self.__budget > 0):
            index = random.randint(0, len(self.__Nodes)-1) #randomly select a node
            if (self.__Nodes[index].getCost() <= self.__budget):    
                self.addNodeToSet(self.__Nodes[index], coveredSet)
            if (self.getSmallestCost(self.__Nodes).getCost() > self.__budget):
                break
        totalUsedBudget[0] = tempBudget - self.__budget
        self.__budget = tempBudget
        return coveredSet

    #Pure Greedy Algorithm
    def pureGreedyAlgorithm(self, totalUsedBudget = [0,0,0]):
        tempBudget = self.__budget
        coveredSet = []
        while(self.__budget >0):
            minIndex = self.getSmallestCost(self.__Nodes)
            self.addNodeToSet(minIndex, coveredSet)
        #This is needed as when the budget is negative it will add the last node's cost to the overall budget
        self.subtractIndexToSet(coveredSet)
        totalUsedBudget[1] = tempBudget - self.__budget
        self.__budget = tempBudget
        return coveredSet

    def Greedy(self, totalUsedBudget = [0,0,0]):
        tempBudget = self.__budget
        coveredSet = []
        pq = PQ()
        for node in self.__Nodes:
            pq.push(node, node.getCost())
        while(self.__budget >0):
            minIndex = pq.pop()
            self.addNodeToSet(minIndex, coveredSet)
        totalUsedBudget[1] = tempBudget - self.__budget
        self.__budget = tempBudget
        return coveredSet
    
    #Greedy Set Cover Algorithm
    def greedySetCoverAlgorithm(self, totalUsedBudget = [0,0,0]):
        tempBudget = self.__budget
        coveredSet = []
        maxCoverageRatio = 0
        maxIndex = None
        while (self.__budget > 0):
            for node in self.__Nodes:
                tempRatio= self.calcCoverage(node, self.__Nodes)/node.getCost()
                if (tempRatio > maxCoverageRatio):
                    maxCoverageRatio = tempRatio
                    maxIndex = node
            if maxIndex is not None: self.addNodeToSet(maxIndex, coveredSet)
            maxCoverageRatio = 0
        #This is needed as when the budget is negative it will add the last node's cost to the overall budget
        self.subtractIndexToSet(coveredSet)
        totalUsedBudget[2] = tempBudget - self.__budget
        self.__budget = tempBudget
        return coveredSet      
        
    def setCover(self, totalUsedBudget = [0,0,0]):
        tempBudget = self.__budget
        coveredSet = []
        pq = PQ()
        for node in self.__Nodes:
            pq.push(node, self.calcCoverage(node, self.__Nodes)/node.getCost())
        while(self.__budget >0):
            minIndex = pq.pop()
            self.addNodeToSet(minIndex, coveredSet)

        totalUsedBudget[2] = tempBudget - self.__budget
        self.__budget = tempBudget
        return coveredSet