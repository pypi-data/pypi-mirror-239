import pandas as pd
import importlib

def get_the_data():
    name = importlib.resources.open_binary('farewelltyson', 'all_data.csv').name
    return pd.read_csv(f'{name}')