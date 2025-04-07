from preprocessing.sub_data.statedata import StateData
import json
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
