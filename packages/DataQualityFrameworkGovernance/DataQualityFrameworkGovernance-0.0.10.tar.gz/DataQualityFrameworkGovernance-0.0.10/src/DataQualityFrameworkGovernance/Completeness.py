# Completeness

def missing_values(location):
    import pandas as pd
    # Load dataset
    df = pd.DataFrame(location)
    missing_values = df.isnull().sum()
    valid_entries = df.count()
    total_entries = len(df)

    df = pd.DataFrame({
        'Missing values': missing_values,
        'Valid entries': valid_entries,
        'Completeness %': (valid_entries / total_entries)*100
        })

    return df

def overall_completeness_percentage(location):
    import pandas as pd
    # Load dataset
    df = pd.DataFrame(location)
    total_entries = df.shape[0]
    complete_entries = df.dropna().shape[0]
    completeness_percentage = (complete_entries / total_entries) * 100
    completeness_percentage = f"Data completeness: {completeness_percentage:.2f}%"
    return completeness_percentage