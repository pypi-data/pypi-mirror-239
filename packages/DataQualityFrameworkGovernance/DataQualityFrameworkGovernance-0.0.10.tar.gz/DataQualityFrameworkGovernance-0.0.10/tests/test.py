print('hello')

dfLocation = "https://media.githubusercontent.com/media/datablist/sample-csv-files/main/files/customers/customers-100.csv"

import pandas as pd
from  DataQualityFrameworkGovernance import Consistency as dq

import pandas as pd

# Create a sample DataFrame with Start Date and End Date columns
data = {
    'Task': ['Task A', 'Task B', 'Task C', 'Task D'],
    'Start Date': ['2023-01-15', '2023-02-01', '2023-01-30', '2023-03-10'],
    'End Date': ['2023-02-15', '2023-02-28', '2023-03-10', '2023-02-15']
}
df = pd.DataFrame(data)

data = dq.start_end_date_consistency(df, 'Start Date','End Date','%Y-%m-%d')
print(data)

data = dq.count_start_end_date_consistency(df, 'Start Date','End Date','%Y-%m-%d')
print(data)