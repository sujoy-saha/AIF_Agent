import pandas as pd
#import numpy as np

# Read a csv file using panda's dataframe.
def read_csv():
    df = pd.read_csv("C:\documents\data.csv")
    print(df.to_string())       

