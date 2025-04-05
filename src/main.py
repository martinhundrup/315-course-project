import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

# ---- Step 1: Load shapefile (U.S. counties) ----
shapefile_path = os.path.join("shapes", "cb_2022_us_county_20m.shp")
counties = gpd.read_file(shapefile_path)
counties["GEOID"] = counties["GEOID"].astype(str).str.zfill(5)

# ---- Step 2: Load COVID data ----
covid_path = os.path.join("..", "us-counties-2023.csv")
covid_df = pd.read_csv(covid_path)

# ---- Step 3: Fix FIPS formatting ----
covid_df = covid_df[covid_df["fips"].notna()]  # Drop rows with missing FIPS
covid_df["fips"] = covid_df["fips"].apply(lambda x: str(int(x)).zfill(5))

# ---- Step 4: Merge on FIPS ----
merged = counties.merge(covid_df, left_on="GEOID", right_on="fips")

# ---- Step 5: Debug if merge fails ----
if merged.empty:
    print("❌ Merge failed! No rows matched.")
    print("Sample GEOIDs from shapefile:", counties['GEOID'].head())
    print("Sample FIPS from COVID data:", covid_df['fips'].head())
    exit()

# ---- Step 6: Plotting ----
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
merged.plot(
    column="deaths",
    cmap="Reds",
    linewidth=0.1,
    ax=ax,
    edgecolor="0.3",
    legend=True
)

ax.set_title("COVID-19 Deaths by U.S. County (2023)", fontsize=18)
ax.set_aspect("auto")  # Prevents aspect ratio error
ax.axis("off")
plt.tight_layout()
plt.show()
