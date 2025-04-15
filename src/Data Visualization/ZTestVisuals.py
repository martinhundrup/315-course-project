import pandas as pd
from DataVisualizer import DataVisualizer  # ✅ import your class
from urllib.request import urlopen
import json

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

# ---- Execute if run directly ----
if __name__ == "__main__":
    test_visuals_with_income()
