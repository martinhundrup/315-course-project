from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff
import os

def test_visuals():
    # here we well be trying to visualize the Covid cases vs deaths in the US Counties using Plotly Express
    dataFrame = pd.read_csv('C:\\Users\\13606\\Desktop\\CPT_S 315 Data Project\\315-course-project\\us-counties-2023.csv')

    dataFrame['fips'] = dataFrame['fips'].astype(str)
    # above is reading the csv from the github
    dataFrame['deaths'] = dataFrame['deaths']

    figure = px.choropleth_map(dataFrame, geojson=counties, locations='fips', color='deaths',
                           color_continuous_scale="Viridis",
                           range_color=(0, 10),
                           map_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
    figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    figure.show()




test_visuals()  # Call the test function to execute the visualization
