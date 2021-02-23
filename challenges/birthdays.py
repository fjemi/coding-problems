'''Determine the date and day of a person's birthdays from birth to the current date
'''


# data analysis
import json
import pandas as pd
# class object models
from dataclasses import dataclass, field, asdict
from typing import List, Dict
# date/time
from calendar import monthrange
from dateutil.parser import parse
from datetime import datetime, date
# for loop progress 
from tqdm import tqdm, trange


@dataclass(order=True)
class Birthdate:
    '''Object model for storing input data'''
    year: int   
    month: int
    day: int
    
    def __post_init__(self):
        '''Validate data after initilization'''
        validator = {
            # float('inf') == positive inifinity
            'year': [0, 'inf'], 
            'month': [1, 12],
            # Fist/last day of a given year (y) and month (m)
            'day': lambda y, m: [1, monthrange(y, m)[1]]
        }
        
        # Iterate over class instance variables
        for key in vars(self).keys():
            result = validator[key]
            if key == 'day':
                result = validator[key](vars(self)['year'], vars(self)['month'])

            # Validate variables
            if result[0] > vars(self)[key] or vars(self)[key] > float(result[1]):
                vars(self)[key] = None
    
    
@dataclass(order=True)
class Birthdays:
    '''Object model for storing output data'''
    date: datetime = None  
    day: str = None
    
  
@dataclass(order=True)
class Model:
    '''Object model for keeping track of birthdays'''
    birthdate: Dict
    birthdays: List[Birthdays] = field(default_factory=list)
    count: Dict[str, int] = field(default_factory=dict)
    created: datetime = field(default_factory=lambda: datetime.utcnow())
    runtime: int = None
    error: str = None
    
    
    def __post_init__(self):
        '''Perform tasks after object initialization'''
        try:
            if len(self.birthdate) == 0:
                raise Exception('Error: No data passed to the class')
                
            # Years to iterate through
            a = self.birthdate['year']
            b = int(self.created.strftime('%Y'))
            
            # List the birthdates since the original
            for i in trange (a, b + 1):                 
                _date = date(i, self.birthdate['month'], self.birthdate['day'])
                weekday = _date.strftime('%a')
                _date = _date.strftime('%G%m%d')
                data = {'date': _date, 'weekday': weekday}
                self.birthdays.append(data)
                
                # Use a dictionary to keep count of days
                if weekday in self.count.keys(): 
                    self.count[weekday] = self.count[weekday] + 1
                else:
                    self.count[weekday] = 1
                    
        except Exception as e:
            # Set variables to None on error
            for key in tqdm(vars(self).keys()):
                if key != 'created':
                    vars(self)[key] == None
                    
            self.error = str(e)
    
        finally:
            # Set function runtime
            self.runtime = (datetime.utcnow() - self.created).total_seconds()
            # Convert datetime to string. Datetime is not JSON serializable
            self.created = self.created.strftime('%Y%m%d.%H%M%S')
            
            
    def get_var(self, name):
        '''Returns data of a class variable in JSON format'''  
        # Check if var name is valid
        var = None
        if name in vars(self).keys():
            var = vars(self)[name]
        return json.dumps({name: var}, indent=2)
           

if __name__ == '__main__':
    # data
    b = [Birthdate(2009, 5, 1), Birthdate(2009, 5, 99)]
    # Convert class object to dictionary
    for data in b:
        data = asdict(data)

        m = Model(data)
        d = asdict(m)
        # Convert dictionary object to JSON
        print(json.dumps(d, indent=2))
        # Get a specific class variable
        print(m.get_var('runtime'))
    
