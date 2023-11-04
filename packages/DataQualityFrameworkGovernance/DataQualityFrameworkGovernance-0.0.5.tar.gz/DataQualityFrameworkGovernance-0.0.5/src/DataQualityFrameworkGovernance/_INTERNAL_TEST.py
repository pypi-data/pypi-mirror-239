print('Internal test')

import pandas as pd

dfLocation = pd.read_csv("https://media.githubusercontent.com/media/datablist/sample-csv-files/main/files/customers/customers-100.csv")


# List of Tuples
employees = [
            ('Saumya', 32, 'Delhi'),
            ('Saumya', 32, 'Delhi'),
            ('Saumya', 32, (None)),
            ('Aaditya', 40, (None)),
            ('Seema', 32, 'Delhi')
            ]
 
# Creating a DataFrame object
df = pd.DataFrame(employees,
                  columns = ['Name', 'Age', 'City'])

#
from Uniqueness import duplicate_rows

duplicate_rows(df)
