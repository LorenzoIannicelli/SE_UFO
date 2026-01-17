from dataclasses import dataclass

@dataclass
class State:
    id : str
    lat : float
    lng : float
    neighbors : list

    def __str__(self):
        return f'{self.id}'

    def __hash__(self):
        return hash(self.id)