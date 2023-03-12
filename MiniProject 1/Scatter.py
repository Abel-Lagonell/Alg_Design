from Grid import Grid
import plotly.graph_objects as go
import numpy as np

#Making the graph based on what it is given
def makeGraph(rand:list[int], greed:list[int], cover:list[int], ran:int, title:str, x_axis:str):
    fig = go.Figure()
    fig.update_layout(title=title, xaxis_title=x_axis, yaxis_title="Coverage")
    fig.add_trace(go.Scatter(x=list(range(1,ran+1)), y=rand, mode='markers', name='Random', marker=dict(color='blue')))
    m, b = np.polyfit(list(range(1,ran+1)), rand, 1)
    line = m * np.array(list(range(1,ran+1))) + b
    fig.add_trace(go.Scatter(x=list(range(1,ran+1)), y=line, mode='lines', name='Random Trend', marker=dict(color='blue')))
    fig.add_trace(go.Scatter(x=list(range(1,ran+1)), y=greed, mode='markers', name='Greedy', marker=dict(color='red')))
    m, b = np.polyfit(list(range(1,ran+1)), greed, 1)
    line = m * np.array(list(range(1,ran+1))) + b
    fig.add_trace(go.Scatter(x=list(range(1,ran+1)), y=line, mode='lines', name='Greedy Trend', marker=dict(color='red')))
    fig.add_trace(go.Scatter(x=list(range(1,ran+1)), y=cover, mode='markers', name='Cover', marker=dict(color='green')))
    m, b = np.polyfit(list(range(1,ran+1)), cover, 1)
    line = m * np.array(list(range(1,ran+1))) + b
    fig.add_trace(go.Scatter(x=list(range(1,ran+1)), y=line, mode='lines', name='Greedy Set Cover Trend', marker=dict(color='green')))
    fig.show()

#Getting the data for the graph
def getData(type:bool, number:bool, graph:bool, ran:int, rand:list[int], greed:list[int], cover:list[int]): 
#type = 0 for random, 1 for cluster; number = 0 for budget, 1 for radius; graph = 0 for singular graph, 1 for iterative graph 
    Grid1 = Grid(type=type)
    for i in range(1,ran+1):
        if (number==0):
            if (graph==0): Grid1.reset(budget=i)
            else: Grid1 = Grid(budget=i, type=type)
        else:
            if (graph==0): Grid1.reset(radius=i)
            else: Grid1 = Grid(radius=i, type=type)
        Grid1.randomAlgorithm()
        rand.append(Grid1.calculateCoverage())
        Grid1.resetCoverage()
        Grid1.pureGreedyAlgorithm()
        greed.append(Grid1.calculateCoverage())
        Grid1.resetCoverage()
        Grid1.greedySetCoverAlgorithm()
        cover.append(Grid1.calculateCoverage())
        Grid1.resetCoverage()

for type in [0,1]:
    for independent in [0,1]:
        for constant in [0,1]:
            changing_RAND=[]
            changing_GREED=[]
            changing_COVER=[]
            
            #Setting up the range
            if (type == 0):
                ran = 100
            else:
                ran = 20

            #Setting up the title and x-axis
            if (independent == 0):
                if (type == 0): 
                    x_axis = "Budget"
                    if (constant==0):
                        title = "Random Budget (Single Graph) vs Coverage"
                    else:
                        title = "Random Budget (Iterative Graph) vs Coverage"
                else:
                    x_axis = "Radius"
                    if (constant==0):
                        title = "Random Radius (Single Graph) vs Coverage"
                    else:
                        title = "Random Radius (Iterative Graph) vs Coverage"
            else:
                if (type == 0): 
                    x_axis = "Budget"
                    if (constant==0):
                        title = "Clustered Budget (Single Graph) vs Coverage"
                    else:
                        title = "Clustered Budget (Iterative Graph) vs Coverage"
                else:
                    x_axis = "Radius"
                    if (constant==0):
                        title = "Clustered Radius (Single Graph) vs Coverage"
                    else:
                        title = "Clustered Radius (Iterative Graph) vs Coverage"
                        
            getData(type= type,number= independent, graph=constant, ran= ran, rand= changing_RAND, greed= changing_GREED, cover= changing_COVER)
            makeGraph(rand=changing_RAND, greed=changing_GREED, cover=changing_COVER, ran=ran, title=title, x_axis=x_axis)