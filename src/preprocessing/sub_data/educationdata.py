from .employment import EmploymentData

class EducationData:  
  def __init__(self, _amount = 0, _attribute_name = '', _attribute_index = 0):
    self.amount = _amount # amount of people at this level
    self.attribute_name = _attribute_name # the english description given to this level
    self.attribute_index = _attribute_index # the index we assigned to this level for numerical comparisons

  def __str__(self):
    return f"{self.attribute_name} = {self.amount} (index {self.attribute_index})"

  def __repr__(self):
    return self.__str__()
  
  def to_dict(self):
    return {
        "amount": self.amount,
        "attribute_name": self.attribute_name,
        "attribute_index": self.attribute_index,
    }

  @staticmethod
  def from_dict(d):
      return EducationData(
          _amount=d["amount"],
          _attribute_name=d["attribute_name"],
          _attribute_index=d["attribute_index"]
      )

