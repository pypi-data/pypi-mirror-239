print('hello')

dfLocation = "https://media.githubusercontent.com/media/datablist/sample-csv-files/main/files/customers/customers-100.csv"

import pandas as pd
import numpy as np
import re

import re

# Define the alphanumeric format pattern
pattern =  r'^[a-zA-Z0-9]+$'

# Test the pattern with example strings
example_strings = ['A1B', 'x0Y', '123', 'AbcD', '1A2']
for string in example_strings:
    if re.match(pattern, string):
        print(f"'{string}' matches the alphanumeric format.")
    else:
        print(f"'{string}' does not match the alphanumeric format.")

