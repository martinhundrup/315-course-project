import random
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# Load and preprocess data
ppdata = pd.read_csv("ppdata.csv")
df = ppdata.dropna(subset=['COVID Cases', 'COVID Deaths'])
df = df.drop(columns=['FIPS', 'County', 'State'], errors='ignore')

df['Infection Rate'] = df['COVID Cases'] / df['Population']
df['High Risk'] = (df['Infection Rate'] > df['Infection Rate'].median()).astype(int)

X = df.drop(columns=['COVID Cases', 'COVID Deaths', 'Infection Rate', 'High Risk'])
y = df['High Risk']

# Model pipeline
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = Pipeline([
    ('scale', StandardScaler()),
    ('clf', XGBClassifier(eval_metric='logloss'))
])
model.fit(X_train, y_train)

# Constants
city_population = random.randint(80000, 120000)
pop_density = random.randint(800, 5000)
hospital_beds_per_1000 = round(random.uniform(1.5, 5.0), 2)

# Build city function
def build_city(median_income):
    city = {}
    for col in X.columns:
        if 'Population' in col:
            city[col] = city_population
        elif 'Income' in col:
            city[col] = median_income
        elif 'Density' in col:
            city[col] = pop_density
        elif 'Beds' in col:
            city[col] = hospital_beds_per_1000
        elif 'Unemployed' in col or 'Employed' in col or 'Labor Force' in col:
            city[col] = random.randint(1000, 70000)
        else:
            city[col] = round(random.uniform(5, 40), 2)
    return city

# Create both cities
wealthy_city = build_city(median_income=95000)
poor_city = build_city(median_income=22000)

wealthy_df = pd.DataFrame([wealthy_city])
poor_df = pd.DataFrame([poor_city])

wealthy_risk = model.predict_proba(wealthy_df)[0][1]
poor_risk = model.predict_proba(poor_df)[0][1]

# Estimate death count
def estimate_deaths(pred_risk, pop, income):
    infection_rate = pred_risk * 0.8
    infected = pop * infection_rate
    if income < 30000:
        cfr = 0.015
    elif income > 75000:
        cfr = 0.005
    else:
        cfr = 0.01
    return round(infected * cfr)

wealthy_deaths = estimate_deaths(wealthy_risk, city_population, 95000)
poor_deaths = estimate_deaths(poor_risk, city_population, 22000)

# Add to DataFrame
comparison_df = pd.DataFrame([
    {"City": "Wealthy", "Predicted High Risk Probability": wealthy_risk,
     "Population": city_population, "Estimated COVID Deaths": wealthy_deaths, **wealthy_city},
    {"City": "Poor", "Predicted High Risk Probability": poor_risk,
     "Population": city_population, "Estimated COVID Deaths": poor_deaths, **poor_city}
])

# Save city comparison
comparison_df.to_csv("Predicted Data/wealth_vs_poor_city_risk_with_deaths.csv", index=False)
print("Saved city risk and death estimates to 'Predicted Data/wealth_vs_poor_city_risk_with_deaths.csv'")

# Generate 5 residents per city
first_names = ["Bob", "Alice", "Jamal", "Maria", "Tyler", "Grace", "Emma", "Liam", "Olivia", "Noah"]
last_names = ["Jones", "Smith", "Lee", "Garcia", "Brown", "Nguyen", "Martinez", "Davis", "Wilson", "Lopez"]

def simulate_residents(city_name, city_df, income_base, pred_risk):
    residents = []
    for _ in range(5):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        age = random.randint(18, 90)
        income = random.randint(income_base - 5000, income_base + 5000)
        essential_worker = random.choice([0, 1])

        personal_risk = (
            0.4 * (income < 40000) +
            0.3 * (age > 65) +
            0.2 * essential_worker +
            0.1 * random.random()
        )
        overall_risk_score = 0.6 * pred_risk + 0.4 * personal_risk
        likely_to_survive = overall_risk_score <= 0.5

        residents.append({
            'City': city_name,
            'Name': name,
            'Age': age,
            'Income': income,
            'Essential Worker': bool(essential_worker),
            'Overall Risk Score': round(overall_risk_score, 3),
            'Likely to Survive': likely_to_survive
        })
    return residents

wealthy_residents = simulate_residents("Wealthy", wealthy_df, 95000, wealthy_risk)
poor_residents = simulate_residents("Poor", poor_df, 22000, poor_risk)

# Save resident data
all_residents = pd.DataFrame(wealthy_residents + poor_residents)
all_residents.to_csv("Predicted Data/resident_simulation_rich_vs_poor.csv", index=False)
print("Saved resident simulation to 'Predicted Data/resident_simulation_rich_vs_poor.csv'")

