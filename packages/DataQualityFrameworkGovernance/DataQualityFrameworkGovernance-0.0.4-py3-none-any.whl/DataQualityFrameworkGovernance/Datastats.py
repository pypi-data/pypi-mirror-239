def count_rows(location):
    import pandas as pd
    location = pd.DataFrame(location)
    rows = location.shape[0]
    print("Number of rows:", rows)    

def count_columns(location):
    import pandas as pd
    location = pd.DataFrame(location)
    cols = location.shape[1]
    print("Number of rows:", cols)    

def count_dataset(location):
    import pandas as pd
    location = pd.DataFrame(location)
    rows = location.shape[0]
    cols = location.shape[1]
    print("Number of rows:", rows , " & columns ", cols)
