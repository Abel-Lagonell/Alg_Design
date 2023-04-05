from Node import Node
from PriorityQueue import PriorityQueue as PQ
import random

class Grid:
    #Constructor
    def __init__(self, budget=50, radius=5, type =0):
        self.__budget = budget
        self.__radius = radius
        self.__Nodes = []
        self.pqCost = PQ()
        self.pqWeight = PQ()
        self.setNodes(type)

    #Reset
    def reset(self, budget=50, radius=5):
        self.__budget = budget
        self.__radius = radius

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
        for node in self.__Nodes:
            self.pqCost.push(node, node.getCost())

    #Adding the node to the set and subtracting the cost from the budget
    def addNodeToSet(self, Node:Node,  pq:PQ, set:list[Node]):
        self.subtractBudget(Node)
        set.append(Node)
        self.setCoverage(Node)
        pq.prune()

    #Subtracting from the budget
    def subtractBudget(self, Node:Node):
        self.__budget -= Node.getCost()
        self.__budget = round(self.__budget, 2)

    #Get the list of Nodes
    def getNodes(self):
        return self.__Nodes

    #Setting the coverage of the node
    def setCoverage(self, Node:Node):
        for node in self.__Nodes:
            if (node.getVisited() == False):
                if (node.getDistance(Node.getX(), Node.getY()) <= self.__radius):
                    node.setVisited()

    def calcCoverage(self, Node:Node, set:list[Node]):
        count =0
        for node in set:
            if (node.getDistance(Node.getX(), Node.getY()) <= self.__radius and Node.getVisited() == False):
                count +=1
        return count

    #Random Algorithm
    def randomAlgorithm(self,totalUsedBudget = [0,0,0]):
        tempBudget = self.__budget
        tempPQCost = self.pqCost
        coveredSet = []
        while (self.__budget > 0):
            index = random.randint(0, len(self.__Nodes)-1) #randomly select a node
            if (self.__Nodes[index].getCost() <= self.__budget):    
                self.addNodeToSet(self.__Nodes[index], tempPQCost, coveredSet)
            if (tempPQCost.top().getCost() > self.__budget):
                break
        totalUsedBudget[0] = tempBudget - self.__budget
        self.__budget = tempBudget
        return coveredSet
    
    #Greedy Algorithm
    def Greedy(self, totalUsedBudget = [0,0,0]):
        tempBudget = self.__budget
        coveredSet = []
        tempPQ = self.pqCost()
        while(self.__budget >0):
            minIndex = tempPQ.pop()
            self.addNodeToSet(minIndex, coveredSet)
        totalUsedBudget[1] = tempBudget - self.__budget
        self.__budget = tempBudget
        return coveredSet

    def setCover(self, totalUsedBudget = [0,0,0]):
        tempBudget = self.__budget
        coveredSet = []
        listNodes = []
        for node in self.__Nodes:
            listNodes.append((node, self.calcCoverage(node, self.__Nodes), node.getCost()))
        print(listNodes)

        totalUsedBudget[2] = tempBudget - self.__budget
        self.__budget = tempBudget
        return coveredSet
    
if (__name__ == "__main__"):
    grid = Grid()
    totalUsedBudget = [0,0,0]
    for node in grid.getNodes():
        print(node)