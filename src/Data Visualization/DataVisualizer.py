from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff
import os


class DataVisualizer:
    def __init__(self, dataframe):
        self.data = dataframe

    def heat_map_visualizer(self, locations, color_freq, color_range, hover_name, hover_data, labels):

        # Creates a heatmap based on the users input
        figure = px.choropleth(self.data, geojson=counties, locations=locations, color=color_freq, 
                               color_continuous_scale="inferno", range_color=color_range, scope='usa', hover_name=hover_name,
                               hover_data=hover_data, labels=labels)
        
        figure.show()


dataFrame = pd.read_csv("https://raw.githubusercontent.com/martinhundrup/315-course-project/refs/heads/main/us-counties-2023.csv",
     dtype={"fips": str})

x = DataVisualizer(dataframe=dataFrame)

x.heat_map_visualizer('fips', 'deaths', (0, 1250), 'county', ['cases'], {'deaths'})