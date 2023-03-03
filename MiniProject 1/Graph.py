import plotly.graph_objects as go
import Node
from Grid import Grid
#Shout out to my boy Abel couldn't have done this Graph without these two classes excited to have done some work that helped -
class Graph:
    def __init__(self, budget=50, radius=5, type=1):
        self.grid = Grid(budget=budget, radius=radius, type=type)
        self.circle_x = 10  # x-coordinate of the center of the circle
        self.circle_y = 10  # y-coordinate of the center of the circle
        self.circle_radius = 5  # radius of the circle
        self.budget = budget
        self.enclosed_cost = 0 
    
    #def find_nodes_randomly(self):
    #    self.grid.randomAlgorithm(self)
    
    def plot(self):
        # Generate a scatter plot of all nodes in the grid
        x = [node.getX() for node in self.grid.getNodes()]
        y = [node.getY() for node in self.grid.getNodes()]
        cost = [node.getCost() for node in self.grid.getNodes()]
        fig = go.Figure(data=go.Scatter(x=x, y=y, mode='markers', text=cost, hovertemplate='(%{x}, %{y})<br>Cost: %{text:.2f}<extra></extra>')) 
        
        # Customize the layout of the scatter plot
        fig.update_layout(title="Node Scatter Plot",xaxis_title="Coverage",yaxis_title="Radius", height=600, width=800, margin=dict(l=50, r=50, b=50, t=50, pad=4),
        #xaxis=dict(range=[0,50]), # Controls the range of the x-axis to an extent 
        #yaxis=dict(range=[0,5]),  # Controls the range of the y-axis to an extent
        )
        
        #nodes_to_enclose = self.grid.getNodesToEnlose(self.budget)
        #if nodes_to_enclose:
        #    self.draw_circle(fig, nodes_to_enclose, self.budget)
#
        #    # Show the plot
        #    fig.show()

        self.draw_circle(fig, self.grid.randomAlgorithm(), self.budget)
        self.draw_circle(fig, self.grid.pureGreedyAlgorithm(), self.budget)
        self.draw_circle(fig, self.grid.greedySetCoverAlgorithm(), self.budget)
        fig.show()

    def draw_circle(self, fig, nodes:list[Node.Node], budget:int): #Create separate functions for each algorithm and then call them from this function
        # calculate the center of the circle
        center_x = sum(node.getX() for node in nodes) / len(nodes)
        center_y = sum(node.getY() for node in nodes) / len(nodes)

        # calculate the radius of the circle
        max_distance = max(((node.getX() - center_x) ** 2 + (node.getY() - center_y) ** 2) ** 0.5 for node in nodes)
        self.circle_radius = max_distance * .1
        self.circle_x = center_x
        self.circle_y = center_y

        for node in nodes:
            fig.add_shape(type="circle", xref="x", yref="y", x0=node.getX()-self.circle_radius, y0=node.getY()-self.circle_radius, x1=node.getX()+self.circle_radius, y1=node.getY()+self.circle_radius, line=dict(color="red", width=2, dash='dash')) #Visually encircles nodes
            fig.add_annotation(x=self.circle_x, y=self.circle_y,text=f'Budget: {budget:.2f}<br>Enclosed cost: {self.enclosed_cost:.2f}',font=dict(size=16), showarrow=False, bgcolor = 'white', bordercolor = 'black', borderwidth = 2, borderpad = 4) #Adds the textbox to the graph
            # Draw a circle around the highlighted nodes
           # if (node.getX() - self.circle_x) ** 2 + (node.getY() - self.circle_y) ** 2 <= self.circle_radius ** 2:
                
              

# Creating the example and printing it out
graph = Graph()
#graph.find_nodes_randomly()
graph.plot()