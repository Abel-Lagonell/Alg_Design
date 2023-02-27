import plotly.graph_objects as go
from Node import Node
from Grid import Grid
#Shout out to my boy Abel couldn't have done this Graph without these two classes excited to have done some work that helped - Jaleel
class Graph:
    def __init__(self, budget=50, radius=5):
        self.grid = Grid(budget=budget, radius=radius)
        self.circle_x = 50  # x-coordinate of the center of the circle
        self.circle_y = 50  # y-coordinate of the center of the circle
        self.circle_radius = 5  # radius of the circle
        
    def add_node(self):
        # Add a new node to the grid
        node = Node()
        self.grid.getNodes().append(node)
        
    def randomize_coordinates(self):
        # Randomize the coordinates of all nodes in the grid
        for node in self.grid.getNodes():
            node.setCoords()
        
    def plot(self):
        # Generate a scatter plot of all nodes in the grid
        x = []
        y = []
        cost = []
        for node in self.grid.getNodes():
            x.append(node.getX())
            y.append(node.getY()) 
            cost.append(node.getCost())
        fig = go.Figure(data=go.Scatter(x=x, y=y, mode='markers', text=cost, hovertemplate='(%{x}, %{y})<br>Cost: %{text:.2f}<extra></extra>')) 
        
        # Customize the layout of the scatter plot
        fig.update_layout(title="Node Scatter Plot",xaxis_title="Coverage",yaxis_title="Radius", 
        #xaxis=dict(range=[0,50]), # Controls the range of the x-axis to an extent 
        #yaxis=dict(range=[0,5]),  # Controls the range of the y-axis to an extent
        )

        # Highlight nodes with cost greater than 0.5 by drawing a circle around them
        nodes_to_highlight = [node for node in self.grid.getNodes() if node.getCost() > 0.5]
        if nodes_to_highlight:
            # calculate the center of the circle
            center_x = sum(node.getX() for node in nodes_to_highlight) / len(nodes_to_highlight)
            center_y = sum(node.getY() for node in nodes_to_highlight) / len(nodes_to_highlight)

            # calculate the radius of the circle
            max_distance = max(((node.getX() - center_x) ** 2 + (node.getY() - center_y) ** 2) ** 0.5 for node in nodes_to_highlight)
            self.circle_radius = max_distance * 1.5

        # Draw a circle around the highlighted nodes
        fig.add_shape(type="circle", xref="x", yref="y", x0=self.circle_x - self.circle_radius, y0=self.circle_y - self.circle_radius, x1=self.circle_x + self.circle_radius, y1=self.circle_y + self.circle_radius, line=dict(color="red", width=2), fillcolor="rgba(255, 0, 0, 0.1)")  
       
        # Show the plot
        fig.show()

# Creating the example and printing it out
graph = Graph()
graph.randomize_coordinates()
graph.plot()
