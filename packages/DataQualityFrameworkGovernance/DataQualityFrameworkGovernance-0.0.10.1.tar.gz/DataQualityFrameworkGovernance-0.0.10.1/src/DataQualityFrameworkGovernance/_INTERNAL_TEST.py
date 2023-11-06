print('Internal test')

import pandas as pd
import re

# Date range
data = {
        'Product Name': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
        'Date': ['2023-01-15', '2023-02-01', '2023-01-30', '2023-03-10', 'invalid-date']
    }
df = pd.DataFrame(data)


from Accuracy import filter_datetime_range
print(filter_datetime_range(df, 'Date', '2023-01-20', '2023-03-05','%Y-%m-%d'))
