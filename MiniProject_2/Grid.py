import copy 
import random as rand
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
        print(tempPQ.getPQ())
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

        # Loop through each node and each possible budget
        for i in range(len(tempNodes) + 1):
            for j in range(tempBudget + 1):
                # Base case: if the budget is 0 or the node index is 0, set max coverage to 0
                if i == 0 or j == 0:
                    max_coverage[i][j] = 0
                # If the node's cost is less than or equal to the remaining budget, 
                # calculate the coverage for including and excluding the node, and take the maximum
                elif tempNodes[i - 1].getCost() <= j:
                    coverage_include = tempNodes[i - 1].getCoverage() + max_coverage[i - 1][j - tempNodes[i - 1].getCost()]
                    coverage_exclude = max_coverage[i - 1][j]
                    max_coverage[i][j] = max(coverage_include, coverage_exclude)
                # If the node's cost is greater than the remaining budget, set max coverage to the coverage 
                # without including the node
                else:
                    max_coverage[i][j] = max_coverage[i - 1][j]
        # Backtrack to find the nodes with the maximum coverage
        i = len(tempNodes)
        j = tempBudget
        selected_nodes = []
        while i > 0 and j > 0:
            # If the current node was included in the maximum coverage, add it to the selected nodes list
            if max_coverage[i][j] != max_coverage[i - 1][j]:
                selected_nodes.append(tempNodes[i - 1])
                j -= tempNodes[i - 1].getCost()
            i -= 1
        # Set the coverage status of the selected nodes
        for node in self.__NODES:
            if node in selected_nodes:
                node.setVisited(True)
            else:
                node.setVisited(False)
        # Return the selected nodes and the total coverage
        return (selected_nodes, max_coverage[len(tempNodes)][tempBudget])

if (__name__ == "__main__"):
    grid = Grid(budget=40, uniform=True)
    setBud = grid.SetCover()
    set = setBud[0]
    bud = setBud[1]
    print("Budget: ", bud)
    print("Set: ", set)
    print("Total Coverage: ", grid.totalCover(set))
    grid.resetCoverage()
    setBud = grid.Greedy()
    set = setBud[0]
    bud = setBud[1]
    print("Budget: ", bud)
    print("Set: ", set)
    print("Total Coverage: ", grid.totalCover(set))
    grid.resetCoverage()
    setBud = grid.Random()
    set = setBud[0]
    bud = setBud[1]
    print("Budget: ", bud)
    print("Set: ", set)
    print("Total Coverage: ", grid.totalCover(set=set))
    grid.resetCoverage()
