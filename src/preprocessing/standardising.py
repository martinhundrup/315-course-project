import pandas as pd

def classify_population(population):
    if type(population) != int:
        return 'unknown_population'
    elif population < 50000:
        return 'small_population'
    elif population < 200000:
        return 'medium_population'
    else:
        return 'large_population'

def classify_poverty_rate(rate):
    if type(rate) != float:
        return 'unknown_poverty_rate'
    elif rate < 10:
        return 'low_poverty'
    elif rate < 20:
        return 'medium_poverty'
    else:
        return 'high_poverty'

def classify_unemployment_rate(rate):
    if type(rate) != float:
        return 'unknown_unemployment_rate'
    elif rate < 3:
        return 'low_unemployment'
    elif rate < 6:
        return 'medium_unemployment'
    else:
        return 'high_unemployment'
    
def classify_income(income):
    if type(income) != int:
        return 'unknown_income'
    elif income < 30000:
        return 'low_income'
    elif income < 60000:
        return 'medium_income'
    else:
        return 'high_income'

def classify_education_level(education_data):
    if type(education_data) != list or len(education_data) < 8:
        return 'unknown_education_level'
    elif education_data[7] > 30:  # index 7 is the attribute "high percentage of bachelor's degree or higher" and yileds a percentage
        return 'high_education'
    else:
        return 'low_education'

def classify_covid_cases(cases):
    if type(cases) != int:
        return 'unknown_covid_cases'
    elif cases < 1000000:
        return 'low_covid_cases'
    elif cases < 10000000:
        return 'medium_covid_cases'
    else:
        return 'high_covid_cases'

# the functions below are used to convert the data into transactions for apriori

def classify_county(county_data):
    transaction = []    
    transaction.append(classify_population(county_data['population']))
    transaction.append(classify_poverty_rate(county_data['poverty_rate']))
    transaction.append(classify_unemployment_rate(county_data['unemployment_rate']))
    transaction.append(classify_income(county_data['median_hh_income']))
    transaction.append(classify_education_level(county_data['education_levels']))
    transaction.append(classify_covid_cases(county_data['covid_cases']))
    return transaction

def classify_covid_population(county_data):
    transaction = []
    transaction.append(classify_population(county_data['population']))
    transaction.append(classify_covid_cases(county_data['covid_cases']))
    return transaction

def classify_covid_poverty(county_data):
    transaction = []
    transaction.append(classify_poverty_rate(county_data['poverty_rate']))
    transaction.append(classify_covid_cases(county_data['covid_cases']))
    return transaction

def classify_covid_unemployment(county_data):
    transaction = []
    transaction.append(classify_unemployment_rate(county_data['unemployment_rate']))
    transaction.append(classify_covid_cases(county_data['covid_cases']))
    return transaction

def classify_covid_income(county_data):
    transaction = []
    transaction.append(classify_income(county_data['median_hh_income']))
    transaction.append(classify_covid_cases(county_data['covid_cases']))
    return transaction

def classify_covid_education(county_data):
    transaction = []
    transaction.append(classify_education_level(county_data['education_levels']))
    transaction.append(classify_covid_cases(county_data['covid_cases']))
    return transaction