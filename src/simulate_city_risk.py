import random
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# Load real county-level data
ppdata = pd.read_csv("ppdata.csv")

# Drop NAs and clean up
df = ppdata.dropna(subset=['COVID Cases', 'COVID Deaths'])
df = df.drop(columns=['FIPS', 'County', 'State'], errors='ignore')

# Features and labels for basic infection model
df['Infection Rate'] = df['COVID Cases'] / df['Population']
df['High Risk'] = (df['Infection Rate'] > df['Infection Rate'].median()).astype(int)

X = df.drop(columns=['COVID Cases', 'COVID Deaths', 'Infection Rate', 'High Risk'])
y = df['High Risk']

# Train model to estimate risk based on city-level info
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = Pipeline([
    ('scale', StandardScaler()),
    ('clf', XGBClassifier(eval_metric='logloss'))
])
model.fit(X_train, y_train)

# Define 25 fictional residents in a fictional American city
city_population = random.randint(10000, 500000)  # realistic for smaller towns
median_income = random.randint(35000, 85000)
pop_density = random.randint(500, 7000)  # people per square mile
hospital_beds_per_1000 = round(random.uniform(1.5, 5.0), 2)

# Dynamically create fictional city using required columns
fictional_city = {}
for col in X.columns:
    if 'Population' in col:
        fictional_city[col] = city_population
    elif 'Income' in col:
        fictional_city[col] = median_income
    elif 'Density' in col:
        fictional_city[col] = pop_density
    elif 'Beds' in col:
        fictional_city[col] = hospital_beds_per_1000
    elif 'Unemployed' in col or 'Employed' in col or 'Labor Force' in col:
        fictional_city[col] = random.randint(500, 90000)
    else:
        fictional_city[col] = round(random.uniform(5, 40), 2)

# Align columns with training features
fictional_city_df = pd.DataFrame([fictional_city])

# Generate residents
residents = []
first_names = ["Bob", "Alice", "Jamal", "Maria", "Tyler", "Grace", "Emma", "Liam", "Olivia", "Noah"]
last_names = ["Jones", "Smith", "Lee", "Garcia", "Brown", "Nguyen", "Martinez", "Davis", "Wilson", "Lopez"]

for _ in range(25):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    age = random.randint(18, 90)
    income = random.randint(20000, 120000)
    essential_worker = random.choice([0, 1])

    risk_pred = model.predict_proba(fictional_city_df)[0][1]

    personal_risk = (
        0.4 * (income < 40000) +
        0.3 * (age > 65) +
        0.2 * essential_worker +
        0.1 * random.random()
    )
    overall_risk_score = 0.6 * risk_pred + 0.4 * personal_risk

    residents.append({
        'Name': name,
        'Age': age,
        'Income': income,
        'Essential Worker': bool(essential_worker),
        'Predicted Risk Score': round(overall_risk_score, 3),
        'High Risk': overall_risk_score > 0.5
    })

# Save to CSV
df_residents = pd.DataFrame(residents)
df_residents.to_csv("Predicted Data/fictional_resident_risks.csv", index=False)
print("Saved 25 fictional residents and their risk scores to 'Predicted Data/fictional_resident_risks.csv'")

