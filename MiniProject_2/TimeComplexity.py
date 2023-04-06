import time
from Grid import Grid

class TimeComplexity:
    def __init__(self):
        pass
    
    def getAverageTimeRandomAlgorithm(self):
        total_time = 0
        for i in range(10):
            start_time = time.time()
            grid = Grid(10, 50)
            nodes = grid.Random()
            end_time = time.time()
            total_time += end_time - start_time
        return total_time/10

    def getAverageTimePureGreedyAlgorithm(self):
        total_time = 0
        for i in range(10):
            start_time = time.time()
            grid = Grid(10, 50)
            nodes = grid.Greedy()
            end_time = time.time()
            total_time += end_time - start_time
        return total_time/10
    
    def getAverageTimeGreedySetCoverAlgorithm(self):
        total_time = 0
        for i in range(10):
            start_time = time.time()
            grid = Grid(10, 50)
            nodes = grid.SetCover()
            end_time = time.time()
            total_time += end_time - start_time
        return total_time/10
    
if __name__ == "__main__":
    timeComplexity = TimeComplexity()
    print("Random Algorithm:", timeComplexity.getAverageTimeRandomAlgorithm())
    print("Pure Greedy Algorithm:", timeComplexity.getAverageTimePureGreedyAlgorithm())
    print("Greedy Set Cover Algorithm:",timeComplexity.getAverageTimeGreedySetCoverAlgorithm())