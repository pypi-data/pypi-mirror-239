import pandas as pd
import importlib

def new_data():
    name = importlib.resources.open_binary('farewelltyson', 'the_new_data.csv').name
    return pd.read_csv(f'{name}')