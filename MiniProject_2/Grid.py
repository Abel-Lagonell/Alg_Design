import copy 
import random as rand
import numpy as np
import math as m
import sys 
from PriorityQueue import PriorityQueue as PQ
from Node import Node

class Grid:
    #Constructor
    def __init__(self, budget = 10, uniform = True):
        self.__BUDGET = budget
        self.__NODES = list[Node]()
        self.__PQCOST = PQ()
        self.setNodes(uniform)

    #Returns the PQ of the nodes
    def getNodes(self, type = False):
        if type: return self.__NODES 
        return self.__PQCOST

    #Sets the Nodes to be used in the grid
    def setNodes(self, uniform:bool):
        if (uniform==True):
            cost = round(rand.uniform(0.1,8.0),1)
            self.__NODES = [Node(cost=cost, ID=i) for i in range(18)]
            #self.__NODES = [Node(cost=rand.randint(1,8), ID=i) for i in range(18)]
        else:
            count = 0
            for i in range(3):
                x = rand.randint(10,90)
                y = rand.randint(10,90)
                for j in range(6):
                    if (i == 0):
                        bracket = round(rand.uniform(5,8),1)
                    elif (i ==1):
                        bracket = round(rand.uniform(2,4),1)
                    else: 
                        bracket = round(rand.uniform(0.1,1.0),1)
                    self.__NODES.append(Node(cost = round(bracket,2), x=x, y=y, ID= count,type=1))
                    count+=1
        for node in self.__NODES:
                self.__PQCOST.push(node, node.getCost())

    #Setting the coverage of the nodes
    def setCoverage(self, node:Node, set:list[Node]):
        for node2 in set:
            if (node2.getVisited() == False):
                if (node.getDistance(node2.getX(), node2.getY()) <= 5):
                    node2.setVisited()
    
    #Resetting the coverage of the nodes
    def resetCoverage(self, set:list[Node] = None):
        if (set == None): set = self.__NODES
        for node in set:
            node.setVisited(False)

    #Calculating the coverage of the set
    def totalCover(self, set:list[Node], universe:list[Node] = None):
        count =0
        self.resetCoverage(universe)
        if (universe == None): universe = self.__NODES
        for node in set:
            for node2 in universe:
                if (node.getDistance(node2.getX(), node2.getY()) <= 5 and node2.getVisited() == False):
                    count +=1
                    node2.setVisited()
        self.resetCoverage(universe)
        return count
    
    #Calculating the coverage of the node and setting surrounding nodes as visited
    def calcCover(self, node:Node, set:list[Node]):
        count =0
        for node2 in set:
            if (node.getDistance(node2.getX(), node2.getY()) <= 5 and node2.getVisited() == False):
                count +=1
                node2.setVisited()
        self.resetCoverage(set)
        return count
    
    #Recalculating the coverage of the nodes
    def reCalc(self, set:PQ):
        for i in range(set.getSize()-1):
            tempCalc = self.calcCover(set.getQueue()[i],set.getQueue())
            tempCost = set.getQueue()[i].getCost()
            set.getPQ()[i][1] = round(tempCalc/tempCost,2)
        set.sortWhole()

    #Randomly selecting nodes
    def Random(self):
        tempBudget = self.__BUDGET
        coveredSet = list[Node]()
        tempPQ = copy.deepcopy(self.__PQCOST)
        while (tempBudget > 0):
            ID = rand.randint(0, tempPQ.getSize()-1)
            index = tempPQ.findID(ID=ID)
            tempNode = tempPQ.getQueue()[index]
            if (tempNode.getCost() <= tempBudget):
                self.setCoverage(tempNode, [tempNode])
                tempBudget -= tempNode.getCost()
                coveredSet.append(tempNode)
                tempPQ.popIndex(index)
            else: 
                break
        return (coveredSet, round(self.__BUDGET-tempBudget,1))
    
    #Using the greedy algorithm to select the best nodes
    def Greedy(self):
        tempBudget = self.__BUDGET
        coveredSet= list[Node]()
        tempPQ = copy.deepcopy(self.__PQCOST)
        while (tempPQ.top() != None and tempPQ.top().getCost() < tempBudget):
            tempNode = tempPQ.pop()
            self.setCoverage(tempNode, tempPQ.getQueue())
            coveredSet.append(tempNode)
            tempBudget -= tempNode.getCost()
        return (coveredSet, round(self.__BUDGET-tempBudget,1))

    #Using Set Cover algorithm to select the best nodes
    def SetCover(self):
        tempBudget = self.__BUDGET
        coveredSet= list[Node]()
        tempPQ = copy.deepcopy(self.__PQCOST)
        self.reCalc(tempPQ)
        while(tempPQ.top() != None and tempPQ.top().getCost() < tempBudget):
            tempNode = tempPQ.pop()
            self.setCoverage(tempNode, tempPQ.getQueue())
            coveredSet.append(tempNode)
            tempBudget -= tempNode.getCost()
            tempPQ.prune()
            self.reCalc(tempPQ)
            tempPQ.sortWhole()
        return (coveredSet, round(self.__BUDGET-tempBudget,1))

    #Using dynamic allocation of nodes to get the best coverage recursively
    def DynamicBU(self):
        multiplier = 10
        tempBudget = self.__BUDGET*multiplier
        tempNodes = copy.deepcopy(self.__NODES)
        allNodes = copy.deepcopy(self.__NODES)
        #Multiplying the cost by the multiplier to make it easier to work with
        for node in tempNodes:
            node.setCost(int(node.getCost()*multiplier))
        #Setting up the matrix that will hold all the values
        self.__dtype = np.dtype([('coverage', int), ('IDs', int, (18,))])
        self.__default_val = (0, np.full(shape = (18,), fill_value=-1, dtype=int))
        self.__matrix = np.full(shape = (19,tempBudget+1), fill_value=-1, dtype=self.__dtype) #Matrix Made
        cell = self.__checkMatrix(18,tempBudget,tempNodes) #Starts the recursion bottom up
        coveredSet = list[Node]()
        
        #Getting the nodes that were selected
        for i in cell[1]:
            if (i != -1):
                coveredSet.append(tempNodes[i])
        tempBudget =0
        #Getting the Budget of the set
        for node in coveredSet:
            tempBudget += node.getCost()/multiplier
        if (tempBudget > self.__BUDGET):
            sys.exit("Budget Exceeded")
        return (coveredSet,round(tempBudget,1))
        
    #Dynamic Programming Algorithm uses a bottom-up approach
    def __DynamicRecur(self, n:int, b:int, tempNodes:list[Node]):
        #Base Case
        if (n==0):
            return self.__default_val
        #If the cost of the node is higher than the budget
        cost = tempNodes[n-1].getCost()
        if (cost > b):
            return self.__checkMatrix(n-1,b,tempNodes)
        else:
            #Check if the node should be included
            withNode = self.__checkMatrix(n-1, b-m.ceil(tempNodes[n-1].getCost()),tempNodes)
            withoutNode = self.__checkMatrix(n-1,b,tempNodes)
            coverNode = self.calcCover(tempNodes[n-1],tempNodes)
            if (withNode[0] + coverNode > withoutNode[0]):
                ID = tempNodes[n-1].getID()
                listNode = self.__addArray(withNode[1],ID)
                return (withNode[0] + coverNode, listNode)
            else:
                return withoutNode
        
    def __checkMatrix(self, n:int, b:int, tempNodes:list[Node]) -> tuple[int, list[int]]:
        #Check if the cell has been initialized
        if (self.__matrix[n,b][0] == -1):
            self.__matrix[n,b] = self.__DynamicRecur(n,b,tempNodes)
            return self.__matrix[n,b]
        #If it has been initialized, return the value
        else:
            return self.__matrix[n,b]
        
    #Adds the ID to the array on the first empty spot
    def __addArray(self, arr1:list[int], ID:int) -> list[int]:
        for i in range(len(arr1)):
            for j in range(len(arr1)):
                if (arr1[j] == arr1[i] and arr1[j] != -1 and i != j):
                    return arr1
            if (arr1[i] == -1):
                arr1[i] = ID
                return arr1



if (__name__ == "__main__"):
    grid = Grid(budget=25, uniform=False)
    setBud = grid.SetCover()
    set = setBud[0]
    bud = setBud[1]
    print ("---SET COVER---")
    print("Budget: ", bud)
    print("Set: ", set)
    grid.resetCoverage()
    print("Total Coverage: ", grid.totalCover(set))
    grid.resetCoverage()
    setBud = grid.Greedy()
    set = setBud[0]
    bud = setBud[1]
    print("---GREEDY---")
    print("Budget: ", bud)
    print("Set: ", set)
    grid.resetCoverage()
    print("Total Coverage: ", grid.totalCover(set))
    grid.resetCoverage()
    setBud = grid.Random()
    set = setBud[0]
    bud = setBud[1]
    print("---RANDOM---")
    print("Budget: ", bud)
    print("Set: ", set)
    grid.resetCoverage()
    print("Total Coverage: ", grid.totalCover(set=set))
    grid.resetCoverage()
    setBud = grid.DynamicBU()
    set = setBud[0]
    bud = setBud[1]
    print("---DYNAMIC---")
    print("Budget: ", bud)
    print("Set: ", set)
    grid.resetCoverage()
    print("Total Coverage: ", grid.totalCover(set=set))
