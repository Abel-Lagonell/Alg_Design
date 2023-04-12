from Grid import Grid
import plotly.graph_objects as go
import numpy as np

#Making the graph based on what it is given
def makeCoverageGraph(randCov:list[int], greeCov:list[int], coveCov:list[int], dynaCov:list[int], ran:list[int], title:str, x_axis:str):
    fig = go.Figure()
    fig.update_layout(title=title, xaxis_title=x_axis, yaxis_title="Coverage")
    fig.add_trace(go.Scatter(x=ran, y=randCov, mode='markers', name='Random', marker=dict(color='blue')))
    m, b = np.polyfit(ran, randCov, 1)
    line = m * np.array(ran) + b
    fig.add_trace(go.Scatter(x=ran, y=line, mode='lines', name='Random Trend', marker=dict(color='blue')))
    fig.add_trace(go.Scatter(x=ran, y=greeCov, mode='markers', name='Greedy', marker=dict(color='red')))
    m, b = np.polyfit(ran, greeCov, 1)
    line = m * np.array(ran) + b
    fig.add_trace(go.Scatter(x=ran, y=line, mode='lines', name='Greedy Trend', marker=dict(color='red')))
    fig.add_trace(go.Scatter(x=ran, y=coveCov, mode='markers', name='Cover', marker=dict(color='green')))
    m, b = np.polyfit(ran, coveCov, 1)
    line = m * np.array(ran) + b
    fig.add_trace(go.Scatter(x=ran, y=line, mode='lines', name='Greedy Set Cover Trend', marker=dict(color='green')))
    fig.add_trace(go.Scatter(x=ran, y=dynaCov, mode='markers', name='Dynamic', marker=dict(color='purple')))
    m, b = np.polyfit(ran, dynaCov, 1)
    line = m * np.array(ran) + b
    fig.add_trace(go.Scatter(x=ran, y=line, mode='lines', name='Dynamic Trend', marker=dict(color='purple')))
    fig.show()

def makeBudVSCovBudgetGraph( greeCov:list[int], coveCov:list[int], dynaCov:list[int], greeBud:list[int], coveBud:list[int], dynaBud:list[int], ran:list[int], title:str, x_axis:str):
    fig = go.Figure()
    fig.update_layout(title=title, xaxis_title=x_axis, yaxis_title="Coverage/Budget Used")
    #---
    greeCovBud = [round(x/y, 2) for x,y in zip(greeCov,greeBud)]
    fig.add_trace(go.Scatter(x=ran, y=greeCovBud, mode='markers', name='Greedy', marker=dict(color='red')))
    m, b = np.polyfit(ran, greeCovBud, 1)
    line = m * np.array(ran) + b
    fig.add_trace(go.Scatter(x=ran, y=line, mode='lines', name='Greedy Trend', marker=dict(color='red')))
    #---
    coveCovBud = [round(x/y,2) for x,y in zip(coveCov,coveBud)]
    fig.add_trace(go.Scatter(x=ran, y=coveCovBud, mode='markers', name='Cover', marker=dict(color='green')))
    m, b = np.polyfit(ran, coveCovBud, 1)
    line = m * np.array(ran) + b
    fig.add_trace(go.Scatter(x=ran, y=line, mode='lines', name='Greedy Set Cover Trend', marker=dict(color='green')))
    #---
    dynamicCovBud = [round(x/y,2) for x,y in zip(dynaCov,dynaBud)]
    fig.add_trace(go.Scatter(x=ran, y=dynamicCovBud, mode='markers', name='Dynamic', marker=dict(color='purple')))
    m, b = np.polyfit(ran, dynamicCovBud, 1)
    line = m * np.array(ran) + b
    fig.add_trace(go.Scatter(x=ran, y=line, mode='lines', name='Dynamic Trend', marker=dict(color='purple')))
    #---
    fig.show()

#Getting the data for the graph
def getData(type:bool, ran:list[int], randCov:list[int], randBud:list[int] , greeCov:list[int], greeBud:list[int], coveCov:list[int], coveBud:list[int], dynaCov:list[int], dynaBud:list[int]): 
#type = 0 for random, 1 for cluster
    for i in ran:
        grid = Grid(budget=i, uniform=type)
        setBud = grid.Random()
        set = setBud[0]
        bud = setBud[1]
        grid.resetCoverage()
        tC = grid.totalCover(set)
        randCov.append(tC)
        randBud.append(bud)
        grid.resetCoverage()
        setBud = grid.Greedy()
        set = setBud[0]
        bud = setBud[1]
        grid.resetCoverage()
        tC = grid.totalCover(set)
        greeCov.append(tC)
        greeBud.append(bud)
        grid.resetCoverage()
        setBud = grid.SetCover()
        set = setBud[0]
        bud = setBud[1]
        grid.resetCoverage()
        tC = grid.totalCover(set)
        coveCov.append(tC)
        coveBud.append(bud)
        grid.resetCoverage()
        setBud = grid.DynamicBU()
        set = setBud[0]
        bud = setBud[1]
        grid.resetCoverage()
        tC = grid.totalCover(set)
        dynaCov.append(tC)
        dynaBud.append(bud)
        grid.resetCoverage()

list = [10,12,20,25,40]
for independent in [0,1]:
    changing_RAND=[]
    changing_GREED=[]
    changing_COVER=[]
    changing_DYNAMIC=[]
    changing_RAND_BUDGET=[]
    changing_GREED_BUDGET=[]
    changing_COVER_BUDGET=[]
    changing_DYNAMIC_BUDGET=[]
    x_axis = "Budget"
    #Setting up the title and x-axis
    if (independent == 0):
        x_axis = "Total Budget"
        title = "Random Nodes Budget vs Coverage"
    else:
        title = "Clustered Nodes Budget (Iterative Graph) vs Coverage"

    getData(type= type, randCov= changing_RAND, greeCov= changing_GREED, coveCov= changing_COVER, ran=list, randBud= changing_RAND_BUDGET, greeBud= changing_GREED_BUDGET, coveBud= changing_COVER_BUDGET, dynaCov= changing_DYNAMIC, dynaBud= changing_DYNAMIC_BUDGET)
    makeCoverageGraph(randCov=changing_RAND, greeCov=changing_GREED, coveCov=changing_COVER, title=title, x_axis=x_axis, ran=list, dynaCov=changing_DYNAMIC)

for independent in [0,1]:
    changing_RAND=[]
    changing_GREED=[]
    changing_COVER=[]
    changing_DYNAMIC=[]
    changing_RAND_BUDGET=[]
    changing_GREED_BUDGET=[]
    changing_COVER_BUDGET=[]
    changing_DYNAMIC_BUDGET=[]
    x_axis = "Budget"
    #Setting up the title and x-axis
    if (independent == 0):
        title = "Random Nodes Budget vs Coverage/Budget"
    else:
        title = "Clustered Nodes Budget (Iterative Graph) vs Coverage/Budget"
    getData(type= type, randCov= changing_RAND, greeCov= changing_GREED, coveCov= changing_COVER, ran=list, randBud= changing_RAND_BUDGET, greeBud= changing_GREED_BUDGET, coveBud= changing_COVER_BUDGET, dynaCov= changing_DYNAMIC, dynaBud= changing_DYNAMIC_BUDGET)
    makeBudVSCovBudgetGraph(greeCov=changing_GREED, coveCov=changing_COVER, greeBud=changing_GREED_BUDGET, coveBud=changing_COVER_BUDGET, ran=list, title=title, x_axis=x_axis, dynaCov=changing_DYNAMIC, dynaBud=changing_DYNAMIC_BUDGET)