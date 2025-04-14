from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff
import os


class DataVisualizer:
    """The user will pass in a dataframe of their choosing, 
       this will directly correlate with the data output and
       what the correlations the user wants to display.  """
    def __init__(self, dataframe):
        self.data = dataframe

    """
            Parameters: 
            locations: (counties), 
            color_freq: (what data you want the color to correlate with),
            color_range: (Dark -> Light, mins and max represented by color),
            hover_name: (what is BOLDED in display when mouse is hovered)
            hover_data: (data is displayed when hovered)
            labels: (labels for the data)
    """
    def heat_map_visualizer(self, locations, color_freq, color_range, hover_name, hover_data, labels):

        # Creates a heatmap based on the users input
        figure = px.choropleth(self.data, geojson=counties, locations=locations, color=color_freq, 
                               color_continuous_scale="inferno", range_color=color_range, scope='usa', hover_name=hover_name,
                               hover_data=hover_data, labels=labels)
        
        figure.show()
    
    def scatter_plot_visualizer(self):
        pass

    def bubble_chart_visualizer(self):
        pass

    def histogram_visualizer(self):
        pass


dataFrame = pd.read_csv("https://raw.githubusercontent.com/martinhundrup/315-course-project/refs/heads/main/us-counties-2023.csv",
     dtype={"fips": str})

x = DataVisualizer(dataframe=dataFrame)


x.heat_map_visualizer('fips', 'deaths', (0, 1250), 'county', ['cases'], {'deaths'})