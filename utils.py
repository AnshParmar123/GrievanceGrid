# utils.py
import pandas as pd

def save_results_to_csv(category, location, filename="results.csv"):
    df = pd.DataFrame([{
        "Most Complained Product Category": category,
        "Most Complained Store Location": location
    }])
    df.to_csv(filename, index=False)
