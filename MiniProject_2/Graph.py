import plotly.graph_objects as go
from Node import Node
from Grid import Grid
from TimeComplexity import TimeComplexity

class Graph:
    def __init__(self, budget=10, uniform=True):
        self.grid = Grid(budget=budget, uniform=uniform) #Grid object
    
    def plot(self):
        #Generate the x and y coordinates for the nodes in the grid
        nodeList = self.grid.getNodes().getQueue()
        x_coords = [node.getX() for node in nodeList]
        y_coords = [node.getY() for node in nodeList]
        cost = [node.getCost() for node in nodeList]

        #Create a color map to color code each algorithm
        color_map = {'Random Algorithm': 'blue', 'Pure Greedy Algorithm': 'green', 'Greedy Set Cover Algorithm': 'red'}

        #initialize the figure
        timeComplexity = TimeComplexity()
        scatter = go.Figure()
        tComFig = go.Figure()

        #Add a scatter trace for all nodes in the grid
        scatter.add_trace(go.Scatter(x=x_coords, y=y_coords, 
            mode='markers', marker=dict(color='black'), text=cost, hovertemplate='(%{x}, %{y})<br>Cost: %{text:.2f}<extra></extra>', 
            name='All Nodes'))
        
        #Add the bar graph for the time complexity
        tComFig.add_trace(go.Bar(x=['Random Algorithm', 'Pure Greedy Algorithm', 'Greedy Set Cover Algorithm'], y=[timeComplexity.getAverageTimeRandomAlgorithm(), timeComplexity.getAverageTimePureGreedyAlgorithm(), timeComplexity.getAverageTimeGreedySetCoverAlgorithm()], marker_color=['blue', 'green', 'red'], name='Average Time of Algorithms'))

        #Add a trace for each algorithm
        for i, (name, NodeBudget) in enumerate(
            [('Random Algorithm', self.grid.Random()), 
             ('Pure Greedy Algorithm', self.grid.Greedy()), 
             ('Greedy Set Cover Algorithm', self.grid.SetCover())]
        ):
            Node = NodeBudget[0]
            Budget = NodeBudget[1]
            #draw circles for the nodes selected by the algorithm
            self.draw_circle(fig = scatter, nodes = Node, color = color_map[name], enclosedCost = Budget, type=i)
            #Add a legend for the algorithm
            scatter.add_trace(go.Scatter(x=[node.getX() for node in Node], y=[node.getY() for node in Node], mode='markers', marker=dict(color=color_map[name]), name=name))

        #Customize the layout of the scatter plot
        scatter.update_layout(
            title="Node Scatter Plot",
            legend=dict(title='Algorithms', yanchor='top', xanchor='left'),
            showlegend=True,
            height=900, width=900, xaxis_range=[-6, 106], yaxis_range=[-6, 106],
        )
        tComFig.update_layout(
            title='Average Time of Algorithms', 
            xaxis_title='Algorithm', yaxis_title='Average Time (s)', 
            height=600, width=800,
        )

        scatter.show()
        tComFig.show()

    def draw_circle(self, fig:go.Figure, nodes:list[Node], color:str, enclosedCost:int, type:int):
        radius = 5
        for node in nodes:
            fig.add_shape(type="circle", xref="x", yref="y", x0=node.getX()-radius, y0=node.getY()-radius, x1=node.getX()+radius, y1=node.getY()+radius, line=dict(color=color, width=2, dash='dash'))
            
        if (type==0):
            fig.add_annotation(x=1.3, y=.85,xref = "paper", yref = "paper",  text=f'Random cost: {enclosedCost:.2f}',font=dict(size=16), showarrow=False, bgcolor = 'white', bordercolor = 'black', borderwidth = 2, borderpad = 4)
        elif(type==1):
            fig.add_annotation(x=1.3, y=0.80,xref = "paper", yref = "paper",  text=f'Greedy cost: {enclosedCost:.2f}',font=dict(size=16), showarrow=False, bgcolor = 'white', bordercolor = 'black', borderwidth = 2, borderpad = 4)
        elif(type==2):
            fig.add_annotation(x=1.3, y=0.75,xref = "paper", yref = "paper",  text=f'Set Cover cost: {enclosedCost:.2f}',font=dict(size=16), showarrow=False, bgcolor = 'white', bordercolor = 'black', borderwidth = 2, borderpad = 4)

        
    
if (__name__ == "__main__"):
    graph = Graph(uniform=False)
    graph.plot()