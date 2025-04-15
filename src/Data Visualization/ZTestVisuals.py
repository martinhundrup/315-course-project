import pandas as pd
import plotly.express as px
from urllib.request import urlopen
import json

def test_visuals_with_income():
    # ---- Step 1: Load US county GeoJSON for mapping ----
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties_geojson = json.load(response)

    # ---- Step 2: Load COVID-19 county-level data ----
    covid_df = pd.read_csv(
        "https://raw.githubusercontent.com/martinhundrup/315-course-project/refs/heads/main/us-counties-2023.csv",
        dtype={"fips": str}
    )

    # ---- Step 3: Load and clean income data ----
    income_df = pd.read_csv(
        "https://raw.githubusercontent.com/martinhundrup/315-course-project/Data-Visualization/src/us-income-2022.csv",
        skiprows=3,  # skip metadata row
        header=0,
        dtype=str
    )

    # Strip column whitespace
    income_df.columns = income_df.columns.str.strip()

    # DEBUG: Print column names to verify
    # print("Actual columns:", income_df.columns.tolist())

    # Select correct columns (now we know the exact names)
    income_df = income_df[["State FIPS Code", "County FIPS Code", "Median Household Income"]]
    income_df.columns = ["state_fips", "county_fips", "median_income"]

    # Create full FIPS code
    income_df["fips"] = income_df["state_fips"].str.zfill(2) + income_df["county_fips"].str.zfill(3)
    income_df["median_income"] = pd.to_numeric(income_df["median_income"].str.replace(",", ""), errors="coerce")
    income_df = income_df.dropna(subset=["fips", "median_income"])

    # ---- Step 4: Merge datasets on FIPS ----
    merged_df = covid_df.merge(income_df, on="fips", how="inner")

    # ---- Step 5: Choropleth map of income ----
    fig_income = px.choropleth(
        merged_df,
        geojson=counties_geojson,
        locations='fips',
        color='median_income',
        color_continuous_scale="Viridis",
        scope="usa",
        hover_name='county',
        hover_data=['deaths'],
        labels={'median_income': "Median Income"}
    )
    fig_income.update_layout(title="Median Household Income by U.S. County (2022)")
    fig_income.show()

    # ---- Step 6: Scatter Plot - Deaths vs Income ----
    fig_scatter = px.scatter(
        merged_df,
        x="median_income",
        y="deaths",
        trendline="ols",
        title="Correlation between COVID-19 Deaths and Median Household Income",
        labels={"deaths": "COVID-19 Deaths", "median_income": "Median Income"}
    )
    fig_scatter.show()

# ---- Execute when run directly ----
if __name__ == "__main__":
    test_visuals_with_income()
