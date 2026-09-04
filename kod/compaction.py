from datetime import date
import os
import pandas as pd
from pyathena import connect
from config import ticker
import boto3
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
granica = date.today()
granica = granica.replace(day=1)
con = connect(
    s3_staging_dir="s3://gpw-tracker-bucket/athena-results/",
    region_name="eu-north-1",
    schema_name="gpw-tracker_db"
)
df = pd.read_sql(f"SELECT data, cena, spolka FROM bronze WHERE data < '{granica}' UNION SELECT data, cena, spolka FROM live WHERE data < '{granica}'", con)
df["dzien"] = df["data"].str[:10]
dane = df.sort_values(["spolka", "data"])
dane = dane.drop_duplicates(subset=["dzien", "spolka"], keep = "first")
dane = dane.drop(columns=["dzien"])
print(dane.shape)
os.makedirs(os.path.join(BASE_DIR, "bronze"), exist_ok=True)
s3 = boto3.client("s3")
for t in ticker:
    wybrana = dane[dane["spolka"] == t]
    wybrana = wybrana.drop(columns=["spolka"]) 
    sciezka = os.path.join(BASE_DIR, "bronze", f"{t}.parquet")
    wybrana.to_parquet(sciezka, index=False)
    s3.upload_file(sciezka,"gpw-tracker-bucket",f"bronze/spolka={t}/{t}.parquet")
test = pd.read_parquet(os.path.join(BASE_DIR, "bronze", "CBF.WA.parquet"))
print(test.shape)
print(test.dtypes)

