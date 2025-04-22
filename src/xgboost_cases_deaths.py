import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

# Load the dataset
df = pd.read_csv("ppdata.csv")

# Drop rows with missing target values
df = df.dropna(subset=['COVID Cases', 'COVID Deaths'])

# Drop non-feature columns (identifiers)
columns_to_drop = ['FIPS', 'State', 'County']
features = df.drop(columns=['COVID Cases', 'COVID Deaths'] + columns_to_drop)
targets = df[['COVID Cases', 'COVID Deaths']]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

# Optional: scale numerical features (helps XGBoost a little with variance)
preprocessor = ColumnTransformer([
    ('scale', StandardScaler(), features.columns.tolist())
])

# Create the pipeline
pipeline = Pipeline([
    ('preprocess', preprocessor),
    ('model', MultiOutputRegressor(XGBRegressor(random_state=42)))
])

# Train the model
pipeline.fit(X_train, y_train)

# Predict
predictions = pipeline.predict(X_test)

# Evaluate
mse_cases = mean_squared_error(y_test['COVID Cases'], predictions[:, 0])
mse_deaths = mean_squared_error(y_test['COVID Deaths'], predictions[:, 1])
r2_cases = r2_score(y_test['COVID Cases'], predictions[:, 0])
r2_deaths = r2_score(y_test['COVID Deaths'], predictions[:, 1])

print(f"MSE (Cases): {mse_cases:.2f}")
print(f"MSE (Deaths): {mse_deaths:.2f}")
print(f"R^2 (Cases): {r2_cases:.2f}")
print(f"R^2 (Deaths): {r2_deaths:.2f}")

# Output predictions
output = df.copy()
full_predictions = pipeline.predict(features)
output['Predicted Cases'] = full_predictions[:, 0]
output['Predicted Deaths'] = full_predictions[:, 1]
output['Cases Error'] = output['Predicted Cases'] - output['COVID Cases']
output['Deaths Error'] = output['Predicted Deaths'] - output['COVID Deaths']

# Save to CSV
os.makedirs("Predicted Data", exist_ok=True)
output.to_csv("Predicted Data/predicted_cases_and_deaths.csv", index=False)
print("Saved predictions to Predicted Data/predicted_cases_and_deaths.csv")

