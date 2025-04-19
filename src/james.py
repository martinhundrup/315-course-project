from preprocessing.ppdata import PPData
from preprocessing.classification import *






















import pandas as pd
import numpy as np
import os

covidData = pd.read_csv("./us-counties-2022.csv")
covidData = covidData.drop(columns=['county','date','state'])
covidData = covidData.drop_duplicates(subset= ["fips"],keep= "last")
covidData = covidData.reset_index()
covidData = covidData.drop(columns=['index'])

# Get the directory this script is in
BASE_DIR = os.path.dirname(__file__)

# columns: ['FIPStxt', 'State', 'Area_Name', 'Attribute', 'Value']
pop_df = pd.read_csv(os.path.join(BASE_DIR, '../other-data/PopulationEstimates.csv'), encoding='latin1')
pop_df = pop_df.drop(columns=['State', "Area_Name"])
pop_df = pop_df[pop_df["Attribute"] == "POP_ESTIMATE_2022"]
pop_df = pop_df.rename(columns= {'FIPStxt':"fips"})
pop_df = pop_df.rename(columns= {'Value':pop_df['Attribute'][4]})
pop_df = pop_df.drop(columns=["Attribute"])

# columns: ['FIPS Code', 'State', 'Area name', 'Attribute', 'Value']
#edu_df = pd.read_csv(os.path.join(BASE_DIR, '../other-data/Education2023.csv'), encoding='latin1')
# columns: ['FIPS_Code', 'State', 'Area_Name', 'Attribute', 'Value']
#pov_df = pd.read_csv(os.path.join(BASE_DIR, '../other-data/Poverty2023.csv'), encoding='utf-8-sig')
# columns: ['FIPS_Code', 'State', 'Area_Name', 'Attribute', 'Value']
unemp_df = pd.read_csv(os.path.join(BASE_DIR, '../other-data/Unemployment2023.csv'), encoding='latin1')
unemp_df = unemp_df.drop(columns=['State','Area_Name'])
unemp_df = unemp_df[unemp_df["Attribute"].str.contains('2022')]
unemp_df = unemp_df.rename(columns= {'FIPS_Code':"fips"})

#print(covidData[covidData["fips"] == 1003])#[covidData['fips'] == 1001])
#print(unemp_df[unemp_df["fips"] == 1003])
#print(pop_df[pop_df["fips"] == 1003])


#print(covidData.head())
#print()


#print(pop_df.head())#[["Attribute","Value"]].T)

allData = covidData.merge(pop_df, on = 'fips')
allData = allData.drop(columns = "fips")




allData = pd.read_csv("./src/ppdata.csv")
allData = allData.drop(columns = ["State","County","FIPS"])

allData.corr().to_csv("Coorelation-Population.csv")


allData = allData.drop(columns = ["Poverty Raw","Unemployed",
                        "Less than high school graduate, 2019-23",
        "High school graduate (or equivalency), 2019-23",
        "Some college or associate degree, 2019-23",
        "Bachelor's degree or higher, 2019-23"
                        ])

allData[[
    "COVID Cases","COVID Deaths","Labor Force","Employed",
         ]] = allData[[
    "COVID Cases","COVID Deaths","Labor Force","Employed",
         ]].div(allData["Population"], axis = 0)
allData = allData.drop(columns = ["Population"])
print(allData.corr())
allData.corr().to_csv("Coorelation-Percent.csv")
#allData = allData.drop(columns = ["Poverty Raw","Labor Force","Less than high school graduate, 2019-23","High school graduate (or equivalency), 2019-23","Some college or associate degree, 2019-23","Bachelor's degree or higher, 2019-23","Percent of adults who are not high school graduates, 2019-23","Percent of adults who are high school graduates (or equivalent), 2019-23","Percent of adults completing some college or associate degree, 2019-23","Percent of adults with a bachelor's degree or higher, 2019-23"])


from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


# X = allData[['cases', 'POP_ESTIMATE_2022']]
# Y = allData['deaths']

