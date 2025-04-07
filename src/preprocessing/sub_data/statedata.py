# This file contains the StateData class which is used to store information about a state and its counties.

import sys
from .countydata import CountyData

class StateData:
  def __init__(self, _state_name = None, _state_code = None):
    self.state_name = _state_name # string
    self.state_code = _state_code # 2 character state code
    self.counties = [] # list of counties in the state

  def __str__(self):
      county_str = "\n".join(str(c) for c in self.counties)
      return (
          f"State: {self.state_name} ({self.state_code})\n"
          f"{county_str}"
      )

  def __repr__(self):
      return f"<State: {self.state_code}>"

  def to_dict(self):
    return {
        "state_code": self.state_code,
        "state_name": self.state_name,
        "counties": [c.to_dict() for c in self.counties],
    }

  @staticmethod
  def from_dict(d):
      s = StateData(_state_code=d["state_code"], _state_name=d["state_name"])
      s.counties = [CountyData.from_dict(c) for c in d["counties"]]
      return s
