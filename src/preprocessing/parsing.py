from .ppdata import PPData
from preprocessing.sub_data.countydata import CountyData
from preprocessing.sub_data.educationdata import EducationData
from preprocessing.sub_data.employment import EmploymentData
from preprocessing.sub_data.statedata import StateData
import pandas as pd

# Mapping of 2-letter state codes to full names
STATE_NAMES = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming'
}

def parse_education(data: PPData, df):
    state_map = {s.state_code: s for s in data.states}
    set_count = 0
    skipped_county_count = 0
    skipped_state_count = 0
    bad_data_count = 0

    # Only parse education values from the most recent period
    TARGET_YEAR_SUFFIX = '2019-23'

    for _, row in df.iterrows():
        attr_raw = str(row['Attribute']).strip()
        if not attr_raw.endswith(TARGET_YEAR_SUFFIX):
            continue  # Only care about 2019-23

        state_code = row['State'].strip().upper()
        area_name = row['Area name'].strip()
        value = row['Value']

        # Normalize for matching
        search_name = area_name.lower()

        try:
            amount = float(value)
        except:
            bad_data_count += 1
            continue

        # Skip if state not in map
        if state_code not in state_map:
            skipped_state_count += 1
            continue

        state = state_map[state_code]

        # Skip state-level entries
        if state_code in STATE_NAMES and area_name == STATE_NAMES[state_code]:
            continue

        # Find matching county
        county = next(
            (c for c in state.counties if c.county_name and c.county_name.strip().lower() == search_name),
            None
        )

        if not county:
            skipped_county_count += 1
            continue

        # Initialize the county's education list if needed
        if county.education_data is None:
            county.education_data = []

        # Assign a consistent attribute index based on sort order
        attribute_name = attr_raw
        attribute_index = len(county.education_data)

        ed = EducationData(
            _amount=amount,
            _attribute_name=attribute_name,
            _attribute_index=attribute_index
        )

        county.education_data.append(ed)
        set_count += 1

    return (
        f"Finished parsing education data.\n"
        f"  Set {set_count} education entries\n"
        f"  Skipped {bad_data_count} rows due to bad values\n"
        f"  Skipped {skipped_state_count} rows with unknown state\n"
        f"  Skipped {skipped_county_count} counties not found in state\n"
    )

def parse_population(data: PPData, df):
    state_map = {}
    bad_data_count = 0
    county_count = 0
    state_count = 0

    for _, row in df.iterrows():
        if row['Attribute'] != 'POP_ESTIMATE_2023':
            continue

        state_code = row['State']
        area_name = row['Area_Name']
        population = row['Value']

        # Convert population to int
        try:
            population = int(population)
        except:
            bad_data_count += 1
            continue

        # Treat it as a state if name matches known state name
        if state_code in STATE_NAMES and area_name == STATE_NAMES[state_code]:
            state_count += 1
            if state_code not in state_map:
                state = StateData(_state_name=area_name, _state_code=state_code)
                state_map[state_code] = state
            else:
                state = state_map[state_code]
                if not state.state_name:
                    state.state_name = area_name
        else:
            # Treat all others as counties
            if state_code not in state_map:
                #print(f"County '{area_name}' found, but state code '{state_code}' has not been parsed yet.")
                continue

            state = state_map[state_code]

            existing = next((c for c in state.counties if c.county_name == area_name), None)
            if existing:
                existing.population = population
            else:
                county = CountyData()
                county.county_name = area_name
                county.population = population
                state.counties.append(county)
                county_count += 1

    data.states = list(state_map.values())
    return (f"Finished parsing poverty data.\n"
      f"  Skipped {bad_data_count} rows due to bad values\n"
      f"  Processed {state_count} states\n"
      f"  Processed {county_count} counties\n")

def parse_poverty(data: PPData, df):
    bad_data_count = 0
    set_count = 0
    skipped_county_count = 0
    skipped_state_count = 0

    # Pre-build lookup for efficiency
    state_map = {s.state_code: s for s in data.states}

    for _, row in df.iterrows():
        if row['Attribute'] != 'POVALL_2023':
            continue

        state_code = row['State']
        area_name = row['Area_Name']
        poverty_value = row['Value']

        try:
            poverty_raw = int(poverty_value)
        except:
            bad_data_count += 1
            continue

        # Skip if state wasn't already parsed
        if state_code not in state_map:
            skipped_state_count += 1
            continue

        state = state_map[state_code]

        # Skip state-level rows
        if state_code in STATE_NAMES and area_name == STATE_NAMES[state_code]:
            continue

        # Find county
        county = next((c for c in state.counties if c.county_name == area_name), None)
        if not county:
            skipped_county_count += 1
            continue

        # Set poverty rate
        county.poverty_raw = poverty_raw
        county.poverty_rate = float(poverty_raw) / county.population
        set_count += 1

    return (f"Finished parsing poverty data."
      f"  Set poverty rate for {set_count} counties\n"
      f"  Skipped {bad_data_count} rows due to bad values\n"
      f"  Skipped {skipped_state_count} rows with unknown state codes\n"
      f"  Skipped {skipped_county_count} counties not found in state\n")

def parse_employment(data: PPData, df):
    bad_data_count = 0
    set_count = 0
    skipped_state_count = 0
    skipped_county_count = 0

    state_map = {s.state_code: s for s in data.states}

    for _, row in df.iterrows():
        attr = str(row['Attribute']).strip()
        if not attr.endswith('_2023'):
            continue  # we only want 2023 data

        #print(f'on attribute {repr(attr)}')
        state_code = row['State']
        area_name = row['Area_Name']
        value = row['Value']

        try:
            parsed_value = float(value) if "rate" in attr.lower() else int(value)
        except:
            bad_data_count += 1
            continue
        
        if state_code not in state_map.keys():
          skipped_state_count += 1
          continue


        state = state_map[state_code]

        # Skip state-level rows
        if state_code in STATE_NAMES and area_name == STATE_NAMES[state_code]:
            continue
        
        if "," in area_name: # this csv is named weird
          area_name = area_name.split(",")[0].strip()

        county = next((c for c in state.counties if c.county_name == area_name), None)
        if not county:   
            skipped_county_count += 1
            continue

        
        if county.employment_data is None:
            county.employment_data = EmploymentData()

        edata = county.employment_data
        if attr == 'Civilian_labor_force_2023':
            edata.civ_labor_force = parsed_value
        elif attr == 'Employed_2023':
            edata.employed = parsed_value
        elif attr == 'Unemployed_2023':
            edata.unemployed = parsed_value
        elif attr == 'Unemployment_rate_2023':
            edata.unemployment_rate = parsed_value
        elif attr == 'Median_Household_Income_2023':
            edata.median_hh_income = parsed_value
        else:
            continue

        set_count += 1

    return (
        f"Finished parsing employment data.\n"
        f"  Set {set_count} employment attributes across counties\n"
        f"  Skipped {bad_data_count} rows due to bad values\n"
        f"  Skipped {skipped_state_count} rows with unknown state\n"
        f"  Skipped {skipped_county_count} counties not found in state\n"
    )