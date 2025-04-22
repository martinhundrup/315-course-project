import pandas as pd
import numpy as np
import folium
import branca.colormap as cm
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns
import shap

# === Load and Prepare Data === #
df = pd.read_csv("ppdata.csv")
df = df.dropna(subset=['COVID Cases', 'COVID Deaths'])
df = df.drop(columns=['County', 'State'], errors='ignore')
df['Infection Rate'] = df['COVID Cases'] / df['Population']
df['High Risk'] = (df['Infection Rate'] > df['Infection Rate'].median()).astype(int)

X_raw = df.drop(columns=['COVID Cases', 'COVID Deaths', 'Infection Rate', 'High Risk'])
y = df['High Risk']

# Impute missing values for models that can't handle NaNs
imputer = SimpleImputer(strategy='mean')
X = pd.DataFrame(imputer.fit_transform(X_raw), columns=X_raw.columns)

# === Model Training === #
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    'XGBoost': XGBClassifier(eval_metric='logloss'),
    'Random Forest': RandomForestClassifier(),
    'Logistic Regression': LogisticRegression(max_iter=1000)
}

for name, clf in models.items():
    pipe = Pipeline([
        ('scale', StandardScaler()),
        ('clf', clf)
    ])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    print(f"\n===== {name} Classification Report =====")
    print(classification_report(y_test, y_pred))
    if name == 'XGBoost':
        best_model = pipe  # keep the XGBoost pipeline for SHAP + prediction

# === SHAP Values (XGBoost only) === #
explainer = shap.Explainer(best_model.named_steps['clf'])
shap_values = explainer(X)
plt.figure(figsize=(16, 10))  # Wider for better visibility
shap.summary_plot(shap_values, X, show=False)
plt.tight_layout()
plt.savefig("Predicted Data/shap_summary.png", dpi=300)
plt.close()

# How to read SHAP:
# Each dot represents a county's SHAP value for a feature.
# Position left/right: how much it pushed the model prediction lower or higher.
# Color: feature value (red = high, blue = low).
# Higher absolute SHAP value = stronger influence on the prediction.

# === Predict Risk for All Counties === #
df['Risk Prob'] = best_model.predict_proba(X)[:, 1]
df['High Risk Predicted'] = df['Risk Prob'] > 0.5

# === Folium Choropleth === #
import json
import requests
geojson_url = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'
county_geo = requests.get(geojson_url).json()

# Prepare data for mapping
df['FIPS'] = df['FIPS'].astype(str).str.zfill(5)
choropleth_data = df.set_index('FIPS')['Risk Prob']

m = folium.Map(location=[37.8, -96], zoom_start=4)
colormap = cm.linear.YlOrRd_09.scale(choropleth_data.min(), choropleth_data.max())
colormap.caption = 'Predicted County-Level COVID Risk'
colormap.add_to(m)

folium.Choropleth(
    geo_data=county_geo,
    name='choropleth',
    data=choropleth_data,
    columns=[choropleth_data.index, choropleth_data.values],
    key_on='feature.id',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Predicted Risk Level'
).add_to(m)

m.save("Predicted Data/folium_county_risk_map.html")
print("Saved folium map to Predicted Data/folium_county_risk_map.html")

# === KMeans Clustering === #
kmeans_data = StandardScaler().fit_transform(X)
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans_labels = kmeans.fit_predict(kmeans_data)
df['Cluster'] = kmeans_labels

plt.figure(figsize=(8, 6))
sns.countplot(x='Cluster', data=df)
plt.title("County Clusters (KMeans)")
plt.xlabel("Cluster")
plt.ylabel("Number of Counties")
plt.savefig("Predicted Data/kmeans_clusters.png")
plt.close()
print("Saved KMeans cluster plot to Predicted Data/kmeans_clusters.png")

# === Time Series Forecasting (Simulated Example) === #
import datetime
from statsmodels.tsa.arima.model import ARIMA

# Simulated time series (national cases example)
time_series_data = pd.read_csv("ppdata.csv")
time_series_data = time_series_data.dropna(subset=['COVID Cases'])
time_series_data['Date'] = pd.date_range(start='2020-01-01', periods=len(time_series_data), freq='W')
national_trend = time_series_data.groupby('Date')['COVID Cases'].sum()
national_trend.index = pd.to_datetime(national_trend.index)

# Fit ARIMA model
model = ARIMA(national_trend, order=(2, 1, 2))
model_fit = model.fit()
forecast = model_fit.forecast(steps=12)

# Plot forecast
plt.figure(figsize=(10, 5))
national_trend.plot(label='Observed')
forecast.index = pd.date_range(start=national_trend.index[-1] + pd.Timedelta(weeks=1), periods=12, freq='W')
forecast.plot(label='Forecast', style='--')
plt.title("Forecasted National COVID Cases (Next 12 Weeks)")
plt.xlabel("Date")
plt.ylabel("Cases")
plt.legend()
plt.tight_layout()
plt.savefig("Predicted Data/time_series_forecast.png")
plt.close()
print("Saved time series forecast plot to Predicted Data/time_series_forecast.png")

