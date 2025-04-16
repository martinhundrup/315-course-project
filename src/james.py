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
covid_percent_transactions = []

MINSUP = 0.5
MINCONF = 0.7

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
            #'covid_cases_percent' : (county.population/county.covid_cases)
        }

        overall_transactions.append(county_data)
        covid_population_transactions.append((county_data))
        covid_poverty_transactions.append((county_data))
        covid_unemployment_transactions.append((county_data))
        covid_income_transactions.append((county_data))
        covid_education_transactions.append((county_data))
        covid_percent_transactions.append(())

print(overall_transactions[0])
