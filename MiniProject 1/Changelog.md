# Changelog

0.1 - Just initialized the Node.py class for further study of the grid. The class includes getters and setters, constructor, and a string representation of the Node itself  
0.2 - Node.py: added the setCost function, one more getter function to get if the node was visited or not, a get Distance function that takes in a node to see the distance between them, and a function to help the setCost function to help determine the price range.  
0.3 - Graph.py: Created the file, adding an import plotly. Created a irrelevant graph. Will modify later to add relevant graph.  
1.0 -  
Grid.py Added functions:

- getSet() - gets the set of used nodes, the ones that are used for radius
- setNodes() - Makes the Nodes in either the random uniform coordinate placement or in clusters throughout the grid
- coverageCalc() - Calculates how many nodes the main node would cover in its radius
- addIndexToSet() - adds the node to the set if the budget allows
- randomAlgorithm() - tries to add a random node to the set, until the budget does not allow it to anymore
- pureGreedyAlgorithm() - tries to add the cheapest node to the set, until the budget does not allow it to anymore

Node.py Added functions:  

- setCoords() - Sets the coordinates of the node wether it is random or clustered

Graph.py: Made some spelling corrections  
1.1 -  
Grid.py Added function:

- greedySetCoverAlgorithm() - tries to add node to the set that is not already in the set, until the budget does not allow it to anymore

1.2 -  
Node.py:
Added Function to make sure that nodes are equal to each other.  

Grid.py: Added Functions:

- reset() - resets the variables to the given values
- calcCoverage() - Returns the amount of nodes that the given node will affect
- addNodeToSet() - A remake of addIndexToSet() that only accepts nodes and a list instead of the index
- greedySetCoverAlgorithm() - the alg for the set Cover greedy algorithm
  
1.3
Graph.py: Added Functions:

- add_node()
- randomize_coordinates()
- plot()

1.4
Graph.py:

-Modified graph to make oval look like a circle
-Modified the circle to have no fill and be made of dashed lines
-Implemnted a feature to highlight an indivudal node

1.5
Graph.py:

-Segmented Graph.py into two functions plot & draw_circle
-Modified draw_circle to use budget and keep circling till it reaches budget
-Added another graphic to the scatterplot displaying budget and money spent

