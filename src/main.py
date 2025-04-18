from preprocessing.ppdata import PPData
from preprocessing.classification import *
from efficient_apriori import apriori
import random

# get object heiarchy
# this data consists of state objects, which contain county objects,
# which contain education objects and contain employment objects
pp_data = PPData.load_from_json("src/ppdata.json")

overall_transactions = []
covid_population_transactions = []
covid_poverty_transactions = []
covid_unemployment_transactions = []
covid_income_transactions = []
covid_education_transactions = []
covid_deaths_transactions = []

MINSUP = 0.5
MINCONF = 0.8

for state in pp_data.states:
    for county in state.counties:
        county_data = {
            'county_name': county.county_name,
            'population': county.population,
            'poverty_rate': county.poverty_rate,
            'unemployment_rate': (
                float(county.employment_data.unemployment_rate)
                if county.employment_data and county.employment_data.unemployment_rate is not None
                else None
            ),            
            'median_hh_income': (
                int(county.employment_data.median_hh_income)
                if county.employment_data and county.employment_data.median_hh_income is not None
                else None
            ),
            'education_levels': [e.amount for e in county.education_data],
            'covid_cases': county.covid_cases,
            'covid_deaths': county.covid_deaths,
        }

        overall_transactions.append(classify_county(county_data))
        covid_population_transactions.append(classify_covid_population(county_data))
        covid_poverty_transactions.append(classify_covid_poverty(county_data))
        covid_unemployment_transactions.append(classify_covid_unemployment(county_data))
        covid_income_transactions.append(classify_covid_income(county_data))
        covid_education_transactions.append(classify_covid_education(county_data))
        covid_deaths_transactions.append(classify_covid_covid_deaths(county_data))

_, overall_rules = apriori(overall_transactions, min_support=MINSUP, min_confidence=MINCONF)
_, covid_population_rules = apriori(covid_population_transactions, min_support=MINSUP, min_confidence=MINCONF)
_, covid_poverty_rules = apriori(covid_poverty_transactions, min_support=MINSUP, min_confidence=MINCONF)
_, covid_unemployment_rules = apriori(covid_unemployment_transactions, min_support=MINSUP, min_confidence=MINCONF)
_, covid_income_rules = apriori(covid_income_transactions, min_support=MINSUP, min_confidence=MINCONF)
_, covid_education_rules = apriori(covid_education_transactions, min_support=MINSUP, min_confidence=MINCONF)
_, covid_deaths_rules = apriori(covid_deaths_transactions, min_support=MINSUP, min_confidence=MINCONF)

# print the rules in a readable way
print(f"\nOverall Rules with [min_sup {MINSUP}] and [min_conf {MINCONF}]:")
for rule in overall_rules:
    print("     ", rule)
    
print(f"\nCOVID-Population Rules with [min_sup {MINSUP}] and [min_conf {MINCONF}]:")
for rule in covid_population_rules:
    print("     ", rule)
    
print(f"\nCOVID-Poverty Rules with [min_sup {MINSUP}] and [min_conf {MINCONF}]:")
for rule in covid_poverty_rules:
    print("     ", rule)
    
print(f"\nCOVID-Unemployment Rules with [min_sup {MINSUP}] and [min_conf {MINCONF}]:")
for rule in covid_unemployment_rules:
    print("     ", rule)
    
print(f"\nCOVID-Income Rules with [min_sup {MINSUP}] and [min_conf {MINCONF}]:")
for rule in covid_income_rules:
    print("     ", rule)
    
print(f"\nCOVID-Education Rules with [min_sup {MINSUP}] and [min_conf {MINCONF}]:")
for rule in covid_education_rules:
    print("     ", rule)
    
print(f"\nCOVID-Education Rules with [min_sup {MINSUP}] and [min_conf {MINCONF}]:")
for rule in covid_education_rules:
    print("     ", rule)
    
print(f"\nCOVID-Deaths Rules with [min_sup {MINSUP}] and [min_conf {MINCONF}]:")
for rule in covid_deaths_rules:
    print("     ", rule)
    