from Node import Node
import random as rand
from MiniProject_1 import PriorityQueue as PQ

class Grid:
    #Constructor
    def __init__(self, budget = 10, uniform = True):
        self.__BUDGET = budget
        self.__NODES = list[Node]()

    def setNodes(self, uniform:bool):
        self.PQCOST = PQ()
        if (uniform==True):
            self.__NODES = [Node(cost=rand.uniform(0.1,8.0),ID=i) for i in range(18)]
            return
        #*INSERT HERE THE WAY WE ARE GOING TO CLUSTER THIS
        for node in self.__NODES:
                self.PQCOST.push(node, node.__cost)

    def Random(self) :
        tempBudget = self.__BUDGET
        coveredSet= list[Node]()
        tempPQ = PQ()
        tempPQ = self.PQCOST()
        while (tempBudget>0):
            index = rand.randint(0, tempPQ.getSize()-1)
            


        return (coveredSet, self.__BUDGET-tempBudget)
