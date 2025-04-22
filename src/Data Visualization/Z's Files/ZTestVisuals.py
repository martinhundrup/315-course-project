import pandas as pd
from DataVisualizer import DataVisualizer  # ✅ import your class
from urllib.request import urlopen
import json
import plotly.graph_objects as go  # For bivariate choropleth

def test_visuals_with_income():
    # ---- Load GeoJSON data for choropleth ----
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties_geojson = json.load(response)

    # ---- Load COVID-19 Data ----
    covid_df = pd.read_csv(
        "https://raw.githubusercontent.com/martinhundrup/315-course-project/refs/heads/main/us-counties-2023.csv",
        dtype={"fips": str}
    )

    # ---- Load and clean income data ----
    income_df = pd.read_csv(
        "https://raw.githubusercontent.com/martinhundrup/315-course-project/Data-Visualization/src/us-income-2022.csv",
        skiprows=3,
        header=0,
        dtype=str
    )

    income_df.columns = income_df.columns.str.strip()
    income_df = income_df[["State FIPS Code", "County FIPS Code", "Median Household Income"]]
    income_df.columns = ["state_fips", "county_fips", "median_income"]
    income_df["fips"] = income_df["state_fips"].str.zfill(2) + income_df["county_fips"].str.zfill(3)
    income_df["median_income"] = pd.to_numeric(income_df["median_income"].str.replace(",", ""), errors="coerce")
    income_df = income_df.dropna(subset=["fips", "median_income"])

    # ---- Merge COVID + income data ----
    merged_df = covid_df.merge(income_df, on="fips", how="inner")
    merged_df["deaths"] = pd.to_numeric(merged_df["deaths"], errors="coerce").fillna(0)
    merged_df["deaths_per_100k"] = (merged_df["deaths"] / 30000) * 100000  # Estimate

    # ---- Create visualizer instance ----
    visualizer = DataVisualizer(merged_df)

    # ---- Show heat map ----
    visualizer.heat_map_visualizer(
        locations="fips",
        color_freq="median_income",
        color_range=(30000, 100000),
        hover_name="county",
        hover_data=["deaths"],
        labels={"median_income": "Median Income"}
    )

    # ---- Show scatter plot with deaths per 100k vs income ----
    visualizer.scatter_plot_visualizer(
        x_axis="median_income",
        y_axis="deaths_per_100k",
        hover_data=["county", "state"]
    )

    # ---- Bivariate Choropleth ----
    # 1. Bin into categories
    merged_df["income_bin"] = pd.qcut(merged_df["median_income"], q=3, labels=["Low", "Mid", "High"])
    merged_df["death_bin"] = pd.qcut(merged_df["deaths_per_100k"], q=3, labels=["Low", "Mid", "High"])
    merged_df["bivariate_class"] = merged_df["income_bin"].astype(str) + "-" + merged_df["death_bin"].astype(str)

    # 2. Define color mapping and numeric codes
    bivariate_codes = {
        "Low-Low": 0,
        "Low-Mid": 1,
        "Low-High": 2,
        "Mid-Low": 3,
        "Mid-Mid": 4,
        "Mid-High": 5,
        "High-Low": 6,
        "High-Mid": 7,
        "High-High": 8
    }
    color_scale = [
        [0/8, "#e8e8e8"],
        [1/8, "#ace4e4"],
        [2/8, "#5ac8c8"],
        [3/8, "#dfb0d6"],
        [4/8, "#a5add3"],
        [5/8, "#5698b9"],
        [6/8, "#be64ac"],
        [7/8, "#8c62aa"],
        [8/8, "#3b4994"]
    ]

    merged_df["bivariate_code"] = merged_df["bivariate_class"].map(bivariate_codes)

    # 3. Plot bivariate choropleth
    fig = go.Figure(go.Choropleth(
        geojson=counties_geojson,
        locations=merged_df["fips"],
        z=merged_df["bivariate_code"],
        text=merged_df["county"] + ", " + merged_df["state"] +
             "<br>Income: $" + merged_df["median_income"].astype(str) +
             "<br>Deaths/100k: " + merged_df["deaths_per_100k"].round(1).astype(str) +
             "<br>Category: " + merged_df["bivariate_class"],
        colorscale=color_scale,
        colorbar=dict(title="Income vs Deaths"),
        marker_line_color='white',
        marker_line_width=0.2
    ))

    fig.update_layout(
        title_text="Bivariate Choropleth: Median Income vs. Deaths per 100k",
        geo=dict(scope='usa', showlakes=True, lakecolor='white')
    )

    fig.show()

# ---- Execute if run directly ----
if __name__ == "__main__":
    test_visuals_with_income()

