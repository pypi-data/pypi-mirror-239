#Validity

def validate_age(location, age_column, min_age, max_age):
    import pandas as pd

    df = pd.DataFrame(location)

    # Check the validity of the 'Age' column
    df['Age Validity'] = (df[age_column] >= min_age) & (df[age_column] <= max_age)

    return df

def validate_age_count(location, age_column, min_age, max_age):
    import pandas as pd

    df = pd.DataFrame(location)

    # Check the validity of the 'Age' column
    validity_check = (df[age_column] >= min_age) & (df[age_column] <= max_age)

    # Count the number of valid and invalid rows
    valid_count = validity_check.sum()
    invalid_count = len(df) - valid_count

    data = pd.DataFrame({
        'Count of dataset': [len(df)],
        'Valid count': [valid_count],
        'Invalid count': [invalid_count],
        'Valid count (%)': [(valid_count / len(df))*100],
        'Invalid count (%)': [(invalid_count / len(df))*100]
        })

    return data

def is_within_range(location, column_name_to_look, array_list):
    import pandas as pd

    df = pd.DataFrame(location)
    df['Within Range'] = df[column_name_to_look].isin(array_list)

    return df

