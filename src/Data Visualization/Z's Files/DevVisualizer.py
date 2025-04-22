# --- Imports ---
from urllib.request import urlopen
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from matplotlib.animation import FuncAnimation

# Load GeoJSON for choropleth
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


# --- DataVisualizer Class ---
class DataVisualizer:
    def __init__(self, dataframe):
        """Initialize with any user-provided DataFrame."""
        self.data = dataframe

    def filter_data(self, filter_func):
        """Filter the dataset using a lambda function."""
        self.data = filter_func(self.data)

    def heatmap(self, location_col, value_col, color_range=None, hover_data=None):
        """Generate a US choropleth heatmap."""
        fig = px.choropleth(
            self.data,
            geojson=counties,
            locations=location_col,
            color=value_col,
            color_continuous_scale="Inferno",
            range_color=color_range,
            scope="usa",
            hover_data=hover_data
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title=f"Heatmap: {value_col}")
        fig.show()

    def animated_heatmap(self, time_col, location_col, value_col, color_range=None, hover_data=None):
        """Generate animated choropleth over time."""
        fig = px.choropleth(
            self.data,
            geojson=counties,
            locations=location_col,
            color=value_col,
            animation_frame=time_col,
            color_continuous_scale="Viridis",
            range_color=color_range,
            scope="usa",
            hover_data=hover_data
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title=f"Animated Heatmap: {value_col} over {time_col}")
        fig.show()

    def scatter(self, x_col, y_col, hover_data=None):
        """Static scatter plot."""
        fig = px.scatter(self.data, x=x_col, y=y_col, hover_data=hover_data)
        fig.update_layout(title=f"Scatter Plot: {y_col} vs {x_col}")
        fig.show()

    def animated_scatter(self, x_col, y_col, time_col, size_col=None, color_col=None, hover_data=None):
        """Scatter with animation over time."""
        fig = px.scatter(
            self.data,
            x=x_col,
            y=y_col,
            animation_frame=time_col,
            size=size_col,
            color=color_col,
            hover_data=hover_data,
            size_max=60
        )
        fig.update_layout(title=f"Animated Scatter: {y_col} vs {x_col} over {time_col}")
        fig.show()

    def bubble_chart(self, x_col, y_col, size_col, color_col=None, hover_data=None):
        """Bubble chart with size and optional color."""
        fig = px.scatter(
            self.data,
            x=x_col,
            y=y_col,
            size=size_col,
            color=color_col,
            hover_data=hover_data,
            size_max=60
        )
        fig.update_layout(title=f"Bubble Chart: {y_col} vs {x_col} (Size: {size_col})")
        fig.show()

    def histogram(self, column):
        """Histogram for a single column."""
        fig = px.histogram(self.data, x=column)
        fig.update_layout(title=f"Histogram: {column}")
        fig.show()

    def barchart(self, x_col, y_col):
        """Bar chart for categorical x and numerical y."""
        fig = px.bar(self.data, x=x_col, y=y_col)
        fig.update_layout(title=f"Bar Chart: {y_col} by {x_col}")
        fig.show()

    def correlation_heatmap(self):
        """Seaborn correlation heatmap for numeric columns."""
        corr = self.data.corr(numeric_only=True)
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.show()

    def pair_plot(self, columns):
        """Seaborn pair plot for selected columns."""
        sns.pairplot(self.data[columns].dropna())
        plt.show()

    def box_plot(self, x_col, y_col):
        """Box plot to show distribution across categories."""
        fig = px.box(self.data, x=x_col, y=y_col)
        fig.update_layout(title=f"Box Plot: {y_col} by {x_col}")
        fig.show()

