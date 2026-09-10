import pandas as pd
import os
from config import ticker, WYNIKI_ATHENY, REGION, BAZA
from pyathena import connect
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
con = connect(
    s3_staging_dir=WYNIKI_ATHENY,
    region_name=REGION,
    schema_name=BAZA
)
df = pd.read_sql("SELECT data, cena, spolka FROM bronze UNION SELECT data, cena, spolka FROM live", con)
df["data"] = pd.to_datetime(df["data"])
df["cena"] = pd.to_numeric(df["cena"], errors="coerce")
df = df.dropna(subset=["cena"])
dane = df.sort_values(["spolka", "data"])
dane["dzien"] = dane["data"].dt.date
dane = dane.drop_duplicates(subset=["dzien", "spolka"], keep = "first")
dane = dane.drop(columns=["dzien"])
print(dane.shape)
assert set(dane["spolka"].unique()) == set(ticker), f"Nieoczekiwane spółki: {dane['spolka'].unique()}"
assert dane["cena"].isna().sum() == 0, "W kolumnie cena pozostały NaN, pomimo użycia dropna()"
assert dane.duplicated().sum() == 0, f"Znaleziono duplikaty: {dane.duplicated().sum()}"
dane.to_csv(os.path.join(BASE_DIR, "silver", "clean_data.csv"), index=False)