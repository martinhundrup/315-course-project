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

# not currently used, but now we have it - mapping of fips code to 2 letter state codes
STATE_FIPS = {
    '0100': 'AL',
    '0200': 'AK',
    '0400': 'AZ',
    '0500': 'AR',
    '0600': 'CA',
    '0800': 'CO',
    '0900': 'CT',
    '1000': 'DE',
    '1200': 'FL',
    '1300': 'GA',
    '1500': 'HI',
    '1600': 'ID',
    '1700': 'IL',
    '1800': 'IN',
    '1900': 'IA',
    '2000': 'KS',
    '2100': 'KY',
    '2200': 'LA',
    '2300': 'ME',
    '2400': 'MD',
    '2500': 'MA',
    '2600': 'MI',
    '2700': 'MN',
    '2800': 'MS',
    '2900': 'MO',
    '3000': 'MT',
    '3100': 'NE',
    '3200': 'NV',
    '3300': 'NH',
    '3400': 'NJ',
    '3500': 'NM',
    '3600': 'NY',
    '3700': 'NC',
    '3800': 'ND',
    '3900': 'OH',
    '4000': 'OK',
    '4100': 'OR',
    '4200': 'PA',
    '4400': 'RI',
    '4500': 'SC',
    '4600': 'SD',
    '4700': 'TN',
    '4800': 'TX',
    '4900': 'UT',
    '5000': 'VT',
    '5100': 'VA',
    '5300': 'WA',
    '5400': 'WV',
    '5500': 'WI',
    '5600': 'WY'
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
        fips_code = row['FIPS Code']

        # Normalize for matching
        try:
            fips_int = int(fips_code)
        except:
            bad_data_count += 1 #fips not an integer
            continue

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
            (c for c in state.counties if c.fips == fips_int),
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
        if row['Attribute'] != 'POP_ESTIMATE_2022':
            continue

        state_code = row['State']
        area_name = row['Area_Name']
        fips_code = row['FIPStxt']
        population = row['Value']

        try:
            fips_int = int(fips_code)
        except:
            bad_data_count += 1
            continue

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
                state = StateData(_state_name=area_name, _state_code=state_code, _fips=fips_int)
                state_map[state_code] = state
            else:
                state = state_map[state_code]
                if not state.state_name:
                    state.state_name = area_name
                if not state.fips:
                    state.fips = fips_int
        else:
            # Treat all others as counties
            if state_code not in state_map:
                #print(f"County '{area_name}' found, but state code '{state_code}' has not been parsed yet.")
                continue

            state = state_map[state_code]

            existing = next((c for c in state.counties if c.fips == fips_code), None)
            if existing:
                existing.population = population
            else:
                county = CountyData()
                county.county_name = area_name
                county.population = population
                county.fips = fips_code
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
    line_count = 0

    for _, row in df.iterrows():
        line_count += 1
        state_fips = str(row['State FIPS Code']).zfill(2)
        county_fips = str(row['County FIPS Code']).zfill(3)
        state_code = str(row['Postal Code']).strip().upper()
        area_name = row['Name']
        poverty_value = row['Poverty Estimate, All Ages']

        # Combine state + county FIPS
        try:
            fips_int = int(state_fips + county_fips)
        except:
            bad_data_count += 1
            continue

        # Parse poverty count
        try:
            poverty_cleaned = str(poverty_value).replace(",", "").strip()
            poverty_raw = int(poverty_cleaned)
        except:
            bad_data_count += 1
            continue


        if state_code not in state_map:
            skipped_state_count += 1
            continue

        state = state_map[state_code]

        # Match by FIPS
        county = next((c for c in state.counties if c.fips == fips_int), None)
        if not county:
            skipped_county_count += 1
            continue

        county.poverty_raw = poverty_raw
        county.poverty_rate = float(poverty_raw) / county.population
        set_count += 1

    return (
        f"Finished parsing poverty data.\n"
        f"  Set poverty rate for {set_count} counties\n"
        f"  Skipped {bad_data_count} rows due to bad values\n"
        f"  Skipped {skipped_state_count} rows with unknown state codes\n"
        f"  Skipped {skipped_county_count} counties not found in state\n"
    )

def parse_employment(data: PPData, df):
    bad_data_count = 0
    set_count = 0
    skipped_state_count = 0
    skipped_county_count = 0

    state_map = {s.state_code: s for s in data.states}

    for _, row in df.iterrows():
        attr = str(row['Attribute']).strip()
        if not attr.endswith('_2022'):
            continue  # we only want 2023 data

        #print(f'on attribute {repr(attr)}')
        state_code = row['State']
        area_name = row['Area_Name']
        value = row['Value']
        fips_code = row['FIPS_Code']

        try:
            fips_int = int(fips_code)
        except:
            bad_data_count += 1
            continue

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

        county = next((c for c in state.counties if c.fips == fips_int), None)
        if not county:   
            skipped_county_count += 1
            continue

        
        if county.employment_data is None:
            county.employment_data = EmploymentData()

        edata = county.employment_data
        if attr == 'Civilian_labor_force_2022':
            edata.civ_labor_force = parsed_value
        elif attr == 'Employed_2022':
            edata.employed = parsed_value
        elif attr == 'Unemployed_2022':
            edata.unemployed = parsed_value
        elif attr == 'Unemployment_rate_2022':
            edata.unemployment_rate = parsed_value
        elif attr == 'Median_Household_Income_2022':
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

def parse_covid(data: PPData, df):
    bad_data_count = 0
    skipped_counties = 0
    line = 0

    # Build FIPS → CountyData lookup
    fips_to_county = {
        county.fips: county
        for state in data.states
        for county in state.counties
        if county.fips is not None
    }

    # --- Track min/max values by fips ---
    covid_tracker = {}  # fips -> {'min': (cases, deaths), 'max': (cases, deaths)}

    for _, row in df.iterrows():
        line += 1
        try:
            fips = int(row['fips'])
            cases = int(row['cases'])
            deaths = int(row['deaths'])
        except:
            # print(f'[BAD DATA] something wrong with integer conversions on line {line}')
            bad_data_count += 1
            continue

        if fips not in fips_to_county:
            # print(f'[SKIPPED COUNTIES] fips code {fips} not found as a county')
            skipped_counties += 1
            continue

        # --- Update tracker for first and last occurrence of this FIPS ---
        if fips not in covid_tracker:
            covid_tracker[fips] = {
                'min_cases': cases,
                'min_deaths': deaths,
                'max_cases': cases,
                'max_deaths': deaths,
            }
        else:
            covid_tracker[fips]['max_cases'] = cases
            covid_tracker[fips]['max_deaths'] = deaths

    # --- Apply final totals to counties ---
    updated_counties = 0
    for fips, data_point in covid_tracker.items():
        county = fips_to_county[fips]

        # Compute difference between last and first seen values
        county.covid_cases = data_point['max_cases'] - data_point['min_cases']
        county.covid_deaths = data_point['max_deaths'] - data_point['min_deaths']
        updated_counties += 1

    return (
        f"Finished parsing COVID data.\n"
        f"  Updated {updated_counties} county entries\n"
        f"  Skipped {skipped_counties} counties not found\n"
        f"  Skipped {bad_data_count} rows due to bad values\n"
    )


