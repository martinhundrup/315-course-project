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
    dataFrame = pd.read_csv('C:\\Users\\13606\\Desktop\\CPT_S 315 Data Project\\315-course-project\\us-counties-2023.csv',
     dtype={"fips": str})

    #dataFrame['fips'] = dataFrame['fips'].astype(str)
    # above is reading the csv from the github
    #dataFrame['deaths'] = dataFrame['deaths']

    figure = px.choropleth(dataFrame, geojson=counties, locations='fips', color='deaths',color_continuous_scale="inferno",
                           range_color=(0,750), scope="usa", hover_name='county', hover_data=['cases'], labels={'deaths'})

    
    #figure.update_geos(fitbounds='locations', visible=False)
    figure.show()




test_visuals()  # Call the test function to execute the visualization
