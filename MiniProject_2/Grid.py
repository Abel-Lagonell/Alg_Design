import copy 
import random as rand
import math
from PriorityQueue import PriorityQueue as PQ
from Node import Node

class Grid:
    #Constructor
    def __init__(self, budget = 10, uniform = True):
        self.__BUDGET = budget
        self.__NODES = list[Node]()
        self.__PQCOST = PQ()
        self.setNodes(uniform)

    def getNodes(self):
        return self.__PQCOST

    def setNodes(self, uniform:bool):
        if (uniform==True):
            self.__NODES = [Node(cost=round(rand.uniform(0.1,8.0), 2), ID=i) for i in range(18)]
        else:
            count = 0
            for i in range(3):
                x = rand.randint(10,90)
                y = rand.randint(10,90)
                for j in range(6):
                    if (i == 0):
                        bracket = rand.uniform(5,8)
                    elif (i ==1):
                        bracket = rand.uniform(2,4)
                    else: 
                        bracket = rand.uniform(0.1,1.0)
                    self.__NODES.append(Node(cost = round(bracket,2), x=x, y=y, ID= count,type=1))
                    count+=1
        for node in self.__NODES:
                self.__PQCOST.push(node, node.getCost())

    def setCoverage(self, node:Node, set:list[Node]):
        for node2 in set:
            if (node2.getVisited() == False):
                if (node.getDistance(node2.getX(), node2.getY()) <= 5):
                    node2.setVisited()

    #calculating total coverage
    def totalCover(self):
        coverage = 0
        for node in self.__NODES:
            if (node.getVisited() == True) :
                coverage += 1
        return coverage

    #Calculating the coverage of the node and setting surrounding nodes as visited
    def calcCover(self, Node:Node, set:list[Node]):
        count =0
        for node in set:
            if (node.getDistance(Node.getX(), Node.getY()) <= 5 and Node.getVisited() == False):
                count +=1
        return count
    
    def reCalc(self, set:PQ):
        for i in range(set.getSize()-1):
            set.getPQ()[i][1] = self.calcCover(set.getQueue()[i], set.getQueue())
        set.sortWhole()

    def Random(self):
        tempBudget = self.__BUDGET
        coveredSet= list[Node]()
        tempPQ = copy.deepcopy(self.__PQCOST)
        while (tempPQ.top().getCost() < tempBudget):
            ID = rand.randint(0, tempPQ.getSize()-1)
            index = tempPQ.findID(ID=ID)
            tempNode = tempPQ.getQueue()[index][0]
            if (tempNode.getCost() <= tempBudget):
                self.setCoverage(tempNode, tempPQ.getQueue())
                tempBudget -= tempNode.getCost()
                coveredSet.append(tempNode)
                tempPQ.prune()
            else: 
                tempPQ.popIndex(index)
        return (coveredSet, round(self.__BUDGET-tempBudget))
    
    def Greedy(self):
        tempBudget = self.__BUDGET
        coveredSet= list[Node]()
        tempPQ = copy.deepcopy(self.__PQCOST)
        while (tempPQ.top().getCost() < tempBudget):
            tempNode = tempPQ.pop()
            self.setCoverage(tempNode, tempPQ.getQueue())
            coveredSet.append(tempNode)
            tempBudget -= tempNode.getCost()
            tempPQ.prune()
        return (coveredSet, round(self.__BUDGET-tempBudget,2))

    def SetCover(self):
        tempBudget = self.__BUDGET
        coveredSet= list[Node]()
        tempPQ = copy.deepcopy(self.__PQCOST)
        self.reCalc(tempPQ)
        while(tempPQ.top().getCost() < tempBudget):
            tempNode = tempPQ.pop()
            self.setCoverage(tempNode, tempPQ.getQueue())
            coveredSet.append(tempNode)
            tempBudget -= tempNode.getCost()
            tempPQ.prune()
            self.reCalc(tempPQ)
            print(tempPQ.getQueue())
            print(tempPQ.getWeight())
        return (coveredSet, round(self.__BUDGET-tempBudget,2))

    def Dynamic(self):
    #Dynamic Programming Algorithm uses a bottom-up approach
        #Creating list to store max coverage for each node and remaining budget
        max_coverage = [[0] * (self.__BUDGET + 1) for __ in range(len(self.__NODES) + 1)] 

        #Loop through each node and each remaining budget
        for i in range(1, len(self.__NODES) + 1): 
            for j in range(1, self.__BUDGET + 1):
                node_cost = self.__NODES[i - 1].getCost()
                if node_cost <= j:
                    #If the current node is cheaper than the remaining budget, include it within the current budget
                        #Check if adding result in a higher coverage
                    with_node = self.calcCover(self.__NODES[i - 1], self.__NODES) + max_coverage[i - 1][j - node_cost]
                    without_node = max_coverage[i - 1][j]
                    max_coverage[i][j] = max(with_node, without_node)
                else:
                    #If the current node is more expensive than the remaining budget, do not include it
                    max_coverage[i][j] = max_coverage[i - 1][j]
        #Backtracking to find the nodes that were included in the optimal solution
        #Indicator of dynamic programming as it looks up rather than recalculating
        covered_set = []
        j = self.__BUDGET
        for i in range(len(self.__NODES), 0, -1):
            if max_coverage[i][j] != max_coverage[i - 1][j]:
                #If the node is included in the optimal solution, add it to the covered set, subtract its cost from the remaining budget
                covered_set.append(self.__NODES[i - 1])
                j -= self.__NODES[i - 1].getCost()
        #Return the covered set and the total coverage
        return (covered_set, self.totalCover())

grid = Grid(budget=20, uniform=False)
setBud = grid.SetCover()
set = setBud[0]
bud = setBud[1]
print("Budget: ", bud)
print("Set: ", set)
print(grid.getNodes())
