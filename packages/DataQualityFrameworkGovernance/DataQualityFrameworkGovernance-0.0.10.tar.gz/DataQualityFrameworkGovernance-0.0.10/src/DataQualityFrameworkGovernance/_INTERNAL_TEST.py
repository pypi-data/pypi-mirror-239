print('Internal test')

import pandas as pd

data = {
    'Age': [25, 30, 35, 40, 45, 50, 55, 60, 65, 70,120],
    'Col2': [25, 30, 35, 40, 45, 50, 55, 60, 65, 70,120],
    'Col3': ['25', '30', '35', '40', '45', '50', '55', '60', '65', '70','120']
}

from Validity import validate_age_count
print(validate_age_count(data,'Age',18,99))