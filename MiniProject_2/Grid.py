import copy 
import random as rand
import numpy as np
import math as m
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
    
    
    #calculating total coverage
    def totalCover(self):
        coverage = 0
        for node in self.__NODES:
            if (node.getVisited() == True) :
                coverage += 1
        return coverage
    
    def resetCoverage(self):
        for node in self.__NODES:
            node.setVisited(False)

    #Calculating the coverage of the set
    def totalCover(self, set:list[Node]):
        count =0
        self.resetCoverage()
        for node in set:
            for node2 in self.__NODES:
                if (node.getDistance(node2.getX(), node2.getY()) <= 5 and node2.getVisited() == False):
                    count +=1
                    node2.setVisited()
        return count
    
    #Calculating the coverage of the node and setting surrounding nodes as visited
    def calcCover(self, node:Node, set:list[Node]):
        count =0
        for node2 in set:
            if (node.getDistance(node2.getX(), node2.getY()) <= 5 and node2.getVisited() == False):
                count +=1
        return count
    
    def reCalc(self, set:PQ):
        for i in range(set.getSize()-1):
            tempCalc = self.calcCover(set.getQueue()[i],set.getQueue())
            tempCost = set.getQueue()[i].getCost()
            set.getPQ()[i][1] = round(tempCalc/tempCost,2)
        set.sortWhole()

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
        return (coveredSet, round(self.__BUDGET-tempBudget))
    
    def Greedy(self):
        tempBudget = self.__BUDGET
        coveredSet= list[Node]()
        tempPQ = copy.deepcopy(self.__PQCOST)
        while (tempPQ.top() != None and tempPQ.top().getCost() < tempBudget):
            tempNode = tempPQ.pop()
            self.setCoverage(tempNode, tempPQ.getQueue())
            coveredSet.append(tempNode)
            tempBudget -= tempNode.getCost()
        return (coveredSet, round(self.__BUDGET-tempBudget,2))

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
        return (coveredSet, round(self.__BUDGET-tempBudget,2))

    def Dynamic(self):
        # Dynamic Programming Algorithm uses a bottom-up approach
        # Creating list to store max coverage for each node and remaining budget
        # Abel yelled at me for not creating temp values
        # Deepcopy ensure that the new copy will not affect the original nodes list
        tempBudget = self.__BUDGET
        tempNodes = copy.deepcopy(self.__NODES)
        max_coverage = [[0] * (tempBudget + 1) for __ in range(len(tempNodes) + 1)]

        # Initialize list to store covered nodes
        covered_nodes = list[Node]()

        # Loop through each node and each possible budget
        for i in range(len(tempNodes) + 1):
            for j in range(tempBudget + 1):
                # Base case: if the budget is 0 or the node index is 0, set max coverage to 0
                if i == 0 or j == 0:
                    max_coverage[i][j] = 0
                else:
                    # Calculate the coverage of the current node
                    node_coverage = self.calcCover(tempNodes[i-1], tempNodes)
                    # Calculate the remaining budget after selecting the current node
                    remaining_budget = j - tempNodes[i-1].getCost()
                    # Calculate the maximum coverage with and without the current node
                    max_with_node = node_coverage + max_coverage[int(i-1)][int(remaining_budget)]
                    max_without_node = max_coverage[i-1][j]
                    # Choose the maximum coverage between with and without the current node
                    if max_with_node > max_without_node:
                        # Set the coverage of the current node and add it to the covered nodes list
                        tempNodes[i-1].setVisited()
                        covered_nodes.append(tempNodes[i-1])
                        max_coverage[i][j] = max_with_node
                    else:
                        max_coverage[i][j] = max_without_node

        # Reset the visited flag of all nodes
        self.resetCoverage()

        return (covered_nodes, round(self.__BUDGET - remaining_budget,2))

    #Using dynamic allocation of nodes to get the best coverage recursively
    def Dynamic2(self):#! Does not preform better than the set cover and greedy but does do better than random
        tempBudget = self.__BUDGET
        tempNodes = copy.deepcopy(self.__PQCOST.getQueue())
        allNodes = copy.deepcopy(self.__NODES)

        #Setting up the matrix that will hold all the values
        self.__dtype = np.dtype([('coverage', int), ('IDs', int, (18,))])
        self.__default_val = (0, np.full(shape = (18,), fill_value=-1, dtype=int))
        self.__matrix = np.full(shape = (19,tempBudget+1), fill_value=-1, dtype=self.__dtype)
        cell = self.__checkMatrix(18,tempBudget,tempNodes)
        coveredSet = list[Node]()
        for i in cell[1]:
            if (i != -1):
                coveredSet.append(allNodes[i])
        tempBudget =0
        for node in coveredSet:
            tempBudget += node.getCost()
        return (coveredSet,tempBudget)
        
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
            withNode = self.__checkMatrix(n-1, b-m.ceil(tempNodes[n-1].getCost()),tempNodes)
            withoutNode = self.__checkMatrix(n-1,b,tempNodes)
            coverNode = self.calcCover(tempNodes[n-1],tempNodes)
            if (withNode[0] + coverNode > withoutNode[0]):
                ID = tempNodes[n-1].getID()
                list = self.__addArray(withNode[1],ID)
                return (withNode[0] + coverNode, list)
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
        
    def __addArray(self, arr1:list[int], ID:int) -> list[int]:
        for i in range(len(arr1)):
            for j in range(len(arr1)):
                if (arr1[j] == arr1[i] and arr1[j] != -1 and i != j):
                    return arr1
            if (arr1[i] == -1):
                arr1[i] = ID
                return arr1



if (__name__ == "__main__"):
    grid = Grid(budget=40, uniform=True)
    setBud = grid.SetCover()
    set = setBud[0]
    bud = setBud[1]
    print ("---SET COVER---")
    print("Budget: ", bud)
    print("Set: ", set)
    print("Total Coverage: ", grid.totalCover(set))
    grid.resetCoverage()
    setBud = grid.Greedy()
    set = setBud[0]
    bud = setBud[1]
    print("---GREEDY---")
    print("Budget: ", bud)
    print("Set: ", set)
    print("Total Coverage: ", grid.totalCover(set))
    grid.resetCoverage()
    setBud = grid.Random()
    set = setBud[0]
    bud = setBud[1]
    print("---RANDOM---")
    print("Budget: ", bud)
    print("Set: ", set)
    print("Total Coverage: ", grid.totalCover(set=set))
    grid.resetCoverage()
    setBud = grid.Dynamic2()
    set = setBud[0]
    bud = setBud[1]
    print("---DYNAMIC---")
    print("Budget: ", bud)
    print("Set: ", set)
    print("Total Coverage: ", grid.totalCover(set=set))
