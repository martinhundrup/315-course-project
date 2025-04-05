class EducationData:  
  def __init__(self, _amount = 0, _attribute_name = '', _attribute_index = 0):
    self.amount = _amount # amount of people at this level
    self.attribute_name = _attribute_name # the english description given to this level
    self.attribute_index = _attribute_index # the index we assigned to this level for numerical comparisons