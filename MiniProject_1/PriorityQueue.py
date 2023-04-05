from Node import Node as Nd
import random

class PriorityQueue:
    #Constructor
    def __init__(self):
        self.__queue = list[tuple[Nd, int]]()
        self.__size = 0
    
    def push(self, node:Nd, weight:int):
        self.__queue.append([node, weight])
        self.__size += 1
        self.sort(self.__size-1)
    
    def pop(self) -> Nd:
        if (self.__size == 0):
            return None
        self.__size -= 1
        temp = self.__queue.pop(0)[0]
        return temp
    
    def popIndex(self, index:int) -> Nd:
        return self.__queue.pop(index)[0]

    
    def top(self) -> Nd:
        if (self.__size == 0):
            return None
        return self.__queue[0][0]

    def sort(self):
        self.__queue.sort(key=lambda x: x[1], reverse=True)

    def sort(self, index:int):
        if (index == 0):
            return
        while (index> 0):
            temp1 = self.__queue[index][1]
            temp2 = self.__queue[index-1][1]
            if (temp1 > temp2):
                self.__swap(index, index-1)
                index -= 1
            else:
                break

    def __swap(self, index1:int, index2:int):
        temp = self.__queue[index1]
        self.__queue[index1] = self.__queue[index2]
        self.__queue[index2] = temp

    def getSize(self) -> int:
        return self.__size
    
    def getQueue(self) -> list:
        return self.__queue
    
    def prune(self):
        for i in range(self.__size):
            if (self.__queue[i][0].getVisited()):
                self.__queue.pop(i)
                self.__size -= 1
                self.__sort(i)
    
    def setWeight(self, weight:int, index:int):
        self.__queue[index][1] = weight
        self.sort(index)

    def getNodeIndex(self, index:int) -> Nd:
        if (index >= self.__size or index < 0):
            return None
        return self.__queue[index][0]
    
    def getNodeID(self, ID:int) -> Nd:
        for i in range(self.__size):
            if (self.__queue[i][0].getID() == ID):
                return self.__queue[i][0]
        return None
    
    def findNode(self, node:Nd) -> int:
        for i in range(self.__size):
            if (self.__queue[i][0] == node):
                return i
        return -1