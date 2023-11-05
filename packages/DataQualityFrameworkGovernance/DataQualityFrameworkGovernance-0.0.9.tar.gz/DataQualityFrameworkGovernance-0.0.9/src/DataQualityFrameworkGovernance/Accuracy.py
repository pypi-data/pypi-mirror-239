#Accuracy

def accuracy_tolerance_numeric(location, base_column, lookup_column, tolernace_percentage):
    import pandas as pd
    df = pd.DataFrame(location)

    # Calculate the accuracy of each value
    accuracy = [1 - abs((calculated - correct) / correct) for calculated, correct in zip(df[base_column], df[lookup_column])]

    # Convert accuracy to percentages
    accuracy_percentage = [acc * 100 for acc in accuracy]

    # Check if accuracy is within a tolerance level
    tol_percentage = tolernace_percentage
    within_tolerance = [acc >= tol_percentage for acc in accuracy_percentage]

    df = pd.DataFrame({
        'Base Values': df[base_column],
        'Lookup Values': df[lookup_column],
        'Accuracy (%)': accuracy_percentage,
        f'{"Within tolernance"} ({tol_percentage})%' : within_tolerance
        })

    return df