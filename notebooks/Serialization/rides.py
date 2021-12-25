"""Add __repr__ to Ride class and then loads rides from rides.pkl (pickle
format) and print repr of each ride.
"""
from datetime import datetime


class Ride:
    def __init__(self, start, end, distance, num_passengers):
        
        self.start = start  # type: datetime
        self.end = end  # type: datetime
        self.distance = distance  # type: float
        self.num_passengers = num_passengers  # type: int
        
    def __repr__(self):
        cls = self.__class__.__name__
        start, end, distance, num_passengers = self.start, self.end, self.distance, self.num_passengers
        return f'{cls}({start!r}, {end!r}, {distance!r}, {num_passengers!r})'
