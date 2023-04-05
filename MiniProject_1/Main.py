from Graph import Graph
from Grid import Grid

def main():
    # Create a Grid object
    grid = Grid(10, 0)

    # Generate nodes using randomAlgorithm
    nodes = grid.randomAlgorithm()

    # Create a Graph object
    graph = Graph()

    # Create a scatter plot of the nodes
    graph.scatterPlot(nodes)

if __name__ == "__main__":
    main()