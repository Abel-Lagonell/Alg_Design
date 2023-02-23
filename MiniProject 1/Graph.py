import plotly.express as px #For the visual graph
import pandas as pd #panda library is responsible for the DataFrame

"""
Template for Scatter Plot
    df = px.data.iris() # iris is a pandas DataFrame
    fig = px.scatter(df, x="sepal_width", y="sepal_length")
    fig.show()

data_frame is a 2D data structure like rows and columns of a table that is mutable
    Syntax is : pandas.DataFrame(data, index, columns)

Useful Functions:
    COLOR_DISCRETE_SEQUENCE - modifies colors
    COLOR enables modification of the points
    OPACITY allows you to change transparency of point

Objective:
    Make two graphs, one with an X-axis named Budget from $0-$50 and dynamic Y-axis  named Coverage
    Second graph contains the same X-axis but constant Y-axis will be named Radius from 0-5
"""
