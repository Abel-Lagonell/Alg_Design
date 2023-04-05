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
        #*INSERT HERE THE WAY WE ARE GOING TO CLUSTER THIS
        for node in self.__NODES:
                self.__PQCOST.push(node, node.getCost())

    def setCoverage(self, node:Node, set:list[Node]):
        for node2,j in set:
            if (node2.getVisited() == False):
                if (node.getDistance(node2.getX(), node2.getY()) <= 5):
                    node2.setVisited()

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
        return (coveredSet, self.__BUDGET-tempBudget)
    
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
        return (coveredSet, self.__BUDGET-tempBudget)
        


grid = Grid(budget=40)
setBud = grid.Greedy()
set = setBud[0]
bud = setBud[1]
print("Budget: ", bud)
print("Set: ", set)
print(grid.getNodes().getQueue())