from Node import Node as Nd
import random

class PriorityQueue:
    #Constructor
    def __init__(self):
        self.__queue = [(Nd,int)]
        self.__size = 0
    
    def push(self, node:Nd, weight:int):
        self.__queue.append([node, weight])
        self.__size += 1
        self.__sort(self.__size-1)
    
    def pop(self) -> Nd:
        if (self.__size == 0):
            return None
        self.__size -= 1
        temp = self.__queue.pop(0)[0]
        return temp
    
    def sort(self):
        self.__queue.sort(key=lambda x: x[2], reverse=True)

    def __sort(self, index:int):
        if (index == 0):
            return
        while (index > 0):
            if (self.__queue[index][1] > self.__queue[index-1][1]):
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
            if (self.__queue[i].getVisited()):
                self.__queue.pop(i)
                self.__size -= 1
                self.__sort(i)

if (__name__ == "__main__"):
    pq = PriorityQueue()
    for i in range(10):
        pq.push(Nd(ID=i), random.randint(0, 100))
    print(pq.getQueue())
    pq.sort()
    print(pq.getQueue())