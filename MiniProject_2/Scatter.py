from Grid import Grid
import plotly.graph_objects as go
import numpy as np

#Making the graph based on what it is given
def makeGraph(rand:list[int], greed:list[int], cover:list[int], ran:list[int], title:str, x_axis:str):
    fig = go.Figure()
    fig.update_layout(title=title, xaxis_title=x_axis, yaxis_title="Coverage")
    fig.add_trace(go.Scatter(x=ran, y=rand, mode='markers', name='Random', marker=dict(color='blue')))
    m, b = np.polyfit(ran, rand, 1)
    line = m * np.array(ran) + b
    fig.add_trace(go.Scatter(x=ran, y=line, mode='lines', name='Random Trend', marker=dict(color='blue')))
    fig.add_trace(go.Scatter(x=ran, y=greed, mode='markers', name='Greedy', marker=dict(color='red')))
    m, b = np.polyfit(ran, greed, 1)
    line = m * np.array(ran) + b
    fig.add_trace(go.Scatter(x=ran, y=line, mode='lines', name='Greedy Trend', marker=dict(color='red')))
    fig.add_trace(go.Scatter(x=ran, y=cover, mode='markers', name='Cover', marker=dict(color='green')))
    m, b = np.polyfit(ran, cover, 1)
    line = m * np.array(ran) + b
    fig.add_trace(go.Scatter(x=ran, y=line, mode='lines', name='Greedy Set Cover Trend', marker=dict(color='green')))
    fig.show()

#Getting the data for the graph
def getData(type:bool, ran:list[int] ,graph:bool, rand:list[int], greed:list[int], cover:list[int]): 
#type = 0 for random, 1 for cluster; graph = 0 for singular graph, 1 for iterative graph 
    grid = Grid(uniform=type)
    for i in ran:
        if (graph==1): grid = Grid(budget=i, uniform=type)
        grid.Random()
        tC = grid.totalCover()
        rand.append(tC)
        grid.resetCoverage()
        grid.Greedy()
        tC = grid.totalCover()
        greed.append(tC)
        grid.resetCoverage()
        grid.SetCover()
        tC = grid.totalCover()
        cover.append(tC)
        grid.resetCoverage()

list = [10,12,20,25,40]
for independent in [0,1]:
    for constant in [0,1]:
        changing_RAND=[]
        changing_GREED=[]
        changing_COVER=[]
        x_axis = "Budget"
        #Setting up the titl and x-axis
        if (independent == 0):
                x_axis = "Budget"
                if (constant==0):
                    title = "Random Budget (Single Graph) vs Coverage"
                else:
                    title = "Random Budget (Iterative Graph) vs Coverage"
        else:

                if (constant==0):
                    title = "Clustered Budget (Single Graph) vs Coverage"
                else:
                    title = "Clustered Budget (Iterative Graph) vs Coverage"

        getData(type= type, graph=constant, rand= changing_RAND, greed= changing_GREED, cover= changing_COVER, ran=list)
        makeGraph(rand=changing_RAND, greed=changing_GREED, cover=changing_COVER, title=title, x_axis=x_axis, ran=list)