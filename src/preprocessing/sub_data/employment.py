class EmploymentData:
  def __init__(self):
    self.civ_labor_force = None # integer size of the civilian labor force
    self.employed = None # integer population size of employed people
    self.unemployed = None # integer population size of unemployed people
    self.unemployment_rate = None # unemployment rate (unemployed / total population)
    self.median_hh_income = None # integer median household income

  def __str__(self):
    return (
        f"Labor Force: {self.civ_labor_force}\n"
        f"Employed: {self.employed}\n"
        f"Unemployed: {self.unemployed}\n"
        f"Unemployment Rate: "
        f"{f'{self.unemployment_rate:.2f}%' if self.unemployment_rate is not None else 'None'}\n"
        f"Median Household Income: "
        f"{f'${self.median_hh_income}' if self.median_hh_income is not None else 'None'}\n"
    )

  def __repr__(self):
      return self.__str__()
  
  def to_dict(self):
    return {
        "civ_labor_force": self.civ_labor_force,
        "employed": self.employed,
        "unemployed": self.unemployed,
        "unemployment_rate": self.unemployment_rate,
        "median_hh_income": self.median_hh_income,
    }

  @staticmethod
  def from_dict(d):
      ed = EmploymentData()
      ed.civ_labor_force = d["civ_labor_force"]
      ed.employed = d["employed"]
      ed.unemployed = d["unemployed"]
      ed.unemployment_rate = d["unemployment_rate"]
      ed.median_hh_income = d["median_hh_income"]
      return ed