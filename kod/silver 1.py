import pandas as pd
import os
from config import ticker
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dft = []
for t in ticker:
    df = pd.read_csv(os.path.join(BASE_DIR, "companies", f"{t}.txt"), header=None, names=["data", "cena"], skipinitialspace=True)
    df["data"] = pd.to_datetime(df["data"])
    df["cena"] = pd.to_numeric(df["cena"], errors="coerce")
    df = df.dropna(subset=["cena"])
    df["spolka"] = t
    dft.append(df)
dane = pd.concat(dft, ignore_index=True)
dane = dane.sort_values(["spolka", "data"])
print(dane.shape)
assert set(dane["spolka"].unique()) == set(ticker), f"Nieoczekiwane spółki: {dane['spolka'].unique()}"
assert dane["cena"].isna().sum() == 0, "W kolumnie cena pozostały NaN, pomimo użycia dropna()"
assert dane.duplicated().sum() == 0, f"Znaleziono duplikaty: {dane.duplicated().sum()}"
dane.to_csv(os.path.join(BASE_DIR, "silver", "clean_data.csv"), index=False)
