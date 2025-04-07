import os
import pandas as pd
from .ppdata import PPData
from preprocessing.sub_data.countydata import CountyData
from preprocessing.sub_data.educationdata import EducationData
from preprocessing.sub_data.employment import EmploymentData
from preprocessing.sub_data.statedata import StateData
from .parsing import *


import os

# Get the directory this script is in
BASE_DIR = os.path.dirname(__file__)


#######################################
## read csv data files as dataframes ##
#######################################

# columns: ['FIPStxt', 'State', 'Area_Name', 'Attribute', 'Value']
pop_df = pd.read_csv(os.path.join(BASE_DIR, '../../other-data/PopulationEstimates.csv'), encoding='latin1')

# columns: ['FIPS Code', 'State', 'Area name', 'Attribute', 'Value']
edu_df = pd.read_csv(os.path.join(BASE_DIR, '../../other-data/Education2023.csv'), encoding='latin1')

# columns: ['FIPS_Code', 'State', 'Area_Name', 'Attribute', 'Value']
pov_df = pd.read_csv(os.path.join(BASE_DIR, '../../other-data/Poverty2023.csv'), encoding='latin1')

# columns: ['FIPS_Code', 'State', 'Area_Name', 'Attribute', 'Value']
unemp_df = pd.read_csv(os.path.join(BASE_DIR, '../../other-data/Unemployment2023.csv'), encoding='latin1')

########################################
## store into centralized object list ##
########################################

pp_data= PPData()

# Load (if already exported)
if os.path.exists("ppdata.json"):
  pp_data = PPData.load_from_json("ppdata.json")
else:
  pop_results = parse_population(pp_data, pop_df) # should come first
  pov_results = parse_poverty(pp_data, pov_df)
  empl_results = parse_employment(pp_data, unemp_df)
  edu_results = parse_education(pp_data, edu_df)

  print(pop_results)
  print(pov_results)
  print(empl_results)
  print(edu_results)
  pp_data.save_to_json("ppdata.json")