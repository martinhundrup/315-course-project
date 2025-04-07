from .employment import EmploymentData
from .educationdata import EducationData

class CountyData:
  def __init__(self):
    self.county_name = None
    self.population = None
    self.covid_cases = None
    self.covid_deaths = None
    self.education_data = None
    self.poverty_raw = None
    self.poverty_rate = None
    self.employment_data = None
    self.fips = None # integer value, has state fips build in, so 1001 for Autauga County alabama

  def __str__(self):
    poverty = (
        f"{self.poverty_rate:.2%}" if self.poverty_rate is not None else "None"
    )

    # Format education data
    edu_str = (
        "\n      " + "\n      ".join(str(e) for e in self.education_data)
        if self.education_data else "      None"
    )

    # Format employment
    emp_str = (
      "      " + str(self.employment_data).replace("\n", "\n      ")
      if self.employment_data else "      None"
    )


    return (
        f"  County: {self.county_name}\n"
        f"    FIPS: {self.fips}\n"
        f"    Population: {self.population}\n"
        f"    COVID Cases: {self.covid_cases}\n"
        f"    COVID Deaths: {self.covid_deaths}\n"
        f"    Poverty Rate: {poverty}\n"
        f"    Employment:\n{emp_str}\n"
        f"    Education:{edu_str}"
    )

  def __repr__(self):
      return f"<County: {self.county_name}>"
  
  def to_dict(self):
    return {
        "county_name": self.county_name,
        "fips": self.fips,
        "population": self.population,
        "covid_cases": self.covid_cases,
        "covid_deaths": self.covid_deaths,
        "poverty_rate": self.poverty_rate,
        "education_data": [e.to_dict() for e in self.education_data] if self.education_data else [],
        "employment_data": self.employment_data.to_dict() if self.employment_data else None,
    }

  @staticmethod
  def from_dict(d):
      c = CountyData()
      c.county_name = d["county_name"]
      c.fips = d["fips"]
      c.population = d["population"]
      c.covid_cases = d["covid_cases"]
      c.covid_deaths = d["covid_deaths"]
      c.poverty_rate = d["poverty_rate"]
      c.education_data = [EducationData.from_dict(e) for e in d["education_data"]]
      c.employment_data = EmploymentData.from_dict(d["employment_data"]) if d["employment_data"] else None
      return c

