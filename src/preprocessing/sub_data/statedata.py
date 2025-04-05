# This file contains the StateData class which is used to store information about a state and its counties.
class StateData:
  def __init__(self, _state_name = None, _state_code = None):
    self.state_name = _state_name # string
    self.state_code = _state_code # 2 character state code
    self.counties = [] # list of counties in the state