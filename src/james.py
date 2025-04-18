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


print(covidData.head())
#print()

print(pop_df.head())#[["Attribute","Value"]].T)

print(covidData.merge(pop_df, on = 'fips'))
#print()
#print(unemp_df.head().stack())

#print(covidData)
#print(pop_df[pop_df["Area_Name"] == "Autauga County"])

# data = {'Header_Column': ['Header1', 'Header2', 'Header3'], 
#         'Value1': [1, 2, 3], 
#         'Value2': [4, 5, 6],
#         'Value3': [7,8,9]}
# df = pd.DataFrame(data)
# df = df.set_index('Header_Column').T
# print(df)


# pp = pd.read_json("./src/ppdata.json")
# print()
# print(pp)