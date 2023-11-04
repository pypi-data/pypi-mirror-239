# Uniqueness

def duplicate_rows(location):
    import pandas as pd
    df = pd.DataFrame(location)
    duplicate = df[df.duplicated()]
    print("Duplicate Rows : ")
    print(duplicate)