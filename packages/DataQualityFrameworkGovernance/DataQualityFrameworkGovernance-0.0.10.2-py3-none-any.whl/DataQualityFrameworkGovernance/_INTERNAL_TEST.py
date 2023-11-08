print('Internal test')

import pandas as pd
import re


import pandas as pd

# Load the sample dataset
data = {
    'id': [True, False, False, False, True, False, True, False, True, True],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry', 'Isabel', 'Jack'],
    'age': [28, 32, 24, 29, 35, 22, 31, 26, 29, 30],
    'city': ['New York', 'Los Angeles', 'Chicago', 'San Francisco', 'Boston', 'Houston', 'Seattle', 'Miami', 'Austin', 'Denver']
}



from Validity import is_within_range
df = is_within_range(data, 'id',[True])

print(df)
