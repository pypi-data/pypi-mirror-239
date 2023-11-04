print('hello')

dfLocation = "https://media.githubusercontent.com/media/datablist/sample-csv-files/main/files/customers/customers-100.csv"

import DataQualityFrameworkGovernance.Completeness as ct
import pandas as pd

# print(ct.completeness_percentage(dfLocation))
# print(ct.missing_values(dfLocation))
# print(ct.count_dataset(dfLocation))
# print(ct.duplicate_rows(dfLocation))

import pandas as pd
 
# List of Tuples
employees = [('Stuti', 28, 'Varanasi'),
            ('Saumya', 32, 'Delhi'),
            ('Aaditya', 25, 'Mumbai'),
            ('Saumya', 32, 'Delhi'),
            ('Saumya', 32, 'Delhi'),
            ('Saumya', 32, 'Mumbai'),
            ('Aaditya', 40, 'Dehradun'),
            ('Seema', 32, 'Delhi')
            ]
 
# Creating a DataFrame object
df = pd.DataFrame(employees,
                  columns = ['Name', 'Age', 'City'])
 
# Selecting duplicate rows except first 
# occurrence based on all columns
duplicate = df[df.duplicated()]
 
print("Duplicate Rows : ")
print(duplicate)