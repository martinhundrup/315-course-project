import pandas as pd
from DevVisualizer import DataVisualizer

# Load COVID data
covid_df = pd.read_csv(
    "https://raw.githubusercontent.com/martinhundrup/315-course-project/refs/heads/main/us-counties-2023.csv",
    dtype={"fips": str}
)

# Load income data
income_df = pd.read_csv(
    "https://raw.githubusercontent.com/martinhundrup/315-course-project/blob/Data-Visualization/src/us-income-2022.csv?raw=true",
    dtype={"fips": str}
)

# Merge on FIPS code
merged_df = pd.merge(covid_df, income_df, on='fips', how='left')

# Add dummy month if not present (for animation)
if 'month' not in merged_df.columns:
    import numpy as np
    merged_df['month'] = np.random.choice(['2020-03', '2020-04', '2020-05', '2020-06'], size=len(merged_df))

# Initialize visualizer
viz = DataVisualizer(merged_df)

# -- Tests --

print("🗺️ Heatmap of Deaths")
viz.heatmap(location_col='fips', value_col='deaths', color_range=(0, 2000), hover_data=['county', 'state'])

print("📈 Scatter: Income vs Deaths")
viz.scatter(x_col='median_household_income', y_col='deaths', hover_data=['county', 'state'])

print("🫧 Bubble Chart: Income vs Deaths (Size=Cases)")
viz.bubble_chart(x_col='median_household_income', y_col='deaths', size_col='cases', color_col='state', hover_data=['county'])

print("📊 Histogram of Income")
viz.histogram(column='median_household_income')

print("📊 Bar Chart: Cases by State")
viz.barchart(x_col='state', y_col='cases')

print("🧊 Correlation Heatmap")
viz.correlation_heatmap()

print("📉 Box Plot: Deaths by State")
viz.box_plot(x_col='state', y_col='deaths')

print("🌀 Animated Heatmap of Cases Over Time")
viz.animated_heatmap(time_col='month', location_col='fips', value_col='cases', color_range=(0, 10000), hover_data=['county'])

print("🌀 Animated Scatter: Income vs Deaths Over Time")
viz.animated_scatter(
    x_col='median_household_income',
    y_col='deaths',
    time_col='month',
    size_col='cases',
    color_col='state',
    hover_data=['county']
)
