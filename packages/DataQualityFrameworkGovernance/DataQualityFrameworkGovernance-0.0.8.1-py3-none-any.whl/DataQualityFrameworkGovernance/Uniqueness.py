# Uniqueness

def duplicate_rows(location):
    import pandas as pd
    df = pd.DataFrame(location)
    duplicate = df[df.duplicated()]
    print("Duplicate Rows : ")
    print(duplicate)


def unique_columns(location):
    import pandas as pd

    df = pd.DataFrame(location)
    unique_values = df.unique()

    # Count the unique values
    unique_count = len(unique_values)

    # Calculate the percentage of unique values
    total_count = len(df)
    uniqueness_percentage = (unique_count / total_count) * 100

    print("Unique Value Count:", unique_count)
    print("Uniqueness Percentage:", uniqueness_percentage, "%")
    print("Unique Values:", unique_values)