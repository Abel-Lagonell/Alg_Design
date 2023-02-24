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
1.5 - 
Grid.py Added function:

- greedySetCoverAlgorithm() - tries to add node to the set that is not already in the set, until the budget does not allow it to anymore
