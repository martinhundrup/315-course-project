from preprocessing.sub_data.statedata import StateData
import json
import pandas
#the highest level of data outputted by the preprocessing module

class PPData:
    def __init__(self):
        self.states = [] #a list of state objects

    def __str__(self):
        return "PPData:\n\n" + "\n\n".join(str(s) for s in self.states)

    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        return {
            "states": [s.to_dict() for s in self.states]
        }

    @staticmethod
    def from_dict(d):
        p = PPData()
        p.states = [StateData.from_dict(s) for s in d["states"]]
        return p
    
    def save_to_json(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"Saved PPData to '{filepath}'")

    @classmethod
    def load_from_json(cls, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded PPData from '{filepath}'")
        return cls.from_dict(data)
    
    def create_csv(self, filepath: str):
        rows = []

        for state in self.states:
            for county in state.counties:
                row = {
                    "FIPS": county.fips,
                    "State": state.state_code,
                    "County": county.county_name,
                    "Population": county.population,
                    "Poverty Raw": county.poverty_raw,
                    "Poverty Rate": round(county.poverty_rate, 4) if county.poverty_rate is not None else None,
                    "COVID Cases": county.covid_cases,
                    "COVID Deaths": county.covid_deaths,
                }

                # Add employment info
                if county.employment_data:
                    row.update({
                        "Labor Force": county.employment_data.civ_labor_force,
                        "Employed": county.employment_data.employed,
                        "Unemployed": county.employment_data.unemployed,
                        "Unemployment Rate": round(county.employment_data.unemployment_rate, 2)
                            if county.employment_data.unemployment_rate is not None else None,
                        "Median Household Income": county.employment_data.median_hh_income,
                    })

                # Add each education data point as its own column
                if county.education_data:
                    for edu in county.education_data:
                        row[edu.attribute_name] = edu.amount

                rows.append(row)

        df = pandas.DataFrame(rows)
        df.to_csv(filepath, index=False)
        print(f"County data exported to '{filepath}' with {len(df)} rows and {len(df.columns)} columns")
