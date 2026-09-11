# URUCHAMIANIE WYŁĄCZNIE LOKALNIE, POMIJAĆ NA EC2 - BRAK BIBLIOTEKI PYARROW, KTÓRA JEST POTRZEBNA JEDYNIE DO ZAPISU .PARQUET, EC2 NIE ZAPISUJE .PARQUET, CZYTA GO POPRZEZ ATHENĘ
from datetime import date
import os
import pandas as pd
from pyathena import connect
from config import ticker, WYNIKI_ATHENY, REGION, BAZA, BUCKET
import boto3
from botocore.exceptions import ClientError
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
granica = date.today()
granica = granica.replace(day=1)
con = connect(
    s3_staging_dir=WYNIKI_ATHENY,
    region_name=REGION,
    schema_name=BAZA
)
os.makedirs(os.path.join(BASE_DIR, "bronze"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "bronze/poprzedni"), exist_ok=True)
s3 = boto3.client("s3")
df = pd.read_sql(f"SELECT data, cena, spolka FROM bronze WHERE data < '{granica}' UNION SELECT data, cena, spolka FROM live WHERE data < '{granica}'", con)
df["dzien"] = df["data"].str[:10]
dane = df.sort_values(["spolka", "data"])
dane = dane.drop_duplicates(subset=["dzien", "spolka"], keep = "first")
dane = dane.drop(columns=["dzien"])
poprzedni = {}
for t in ticker:
    kopia = os.path.join(BASE_DIR, "bronze", "poprzedni", f"{t}.parquet")
    try:
        s3.download_file(BUCKET, f"bronze/spolka={t}/{t}.parquet", kopia)
        poprzedni[t] = len(pd.read_parquet(kopia))
    except ClientError:
        poprzedni[t] = 0
nowe = dane.groupby("spolka").size()
for spolka in ticker:
    stara_ilosc = poprzedni.get(spolka, 0)
    nowa_ilosc = nowe.get(spolka, 0)
    assert nowa_ilosc >= stara_ilosc, f"{spolka}: stara ilosc: {stara_ilosc}, nowa_ilosc: {nowa_ilosc} - przerywam dzialanie przed zapisem"
    print(f"{spolka}: stara ilosc: {stara_ilosc}, nowa_ilosc: {nowa_ilosc}")
for t in ticker:
    wybrana = dane[dane["spolka"] == t]
    wybrana = wybrana.drop(columns=["spolka"]) 
    sciezka = os.path.join(BASE_DIR, "bronze", f"{t}.parquet")
    wybrana.to_parquet(sciezka, index=False)
    s3.upload_file(sciezka, BUCKET, f"bronze/spolka={t}/{t}.parquet")
sprawdzenie = pd.read_sql(f"""SELECT "$path" AS plik, MAX(data) AS ostatni
FROM live
GROUP BY "$path"
HAVING MAX(data) < '{granica}'""", con)
licznik = 0
for adres in sprawdzenie["plik"]:
    nazwa = adres.split("/", 3)[3]
    s3.delete_object(Bucket=BUCKET, Key=nazwa)
    licznik += 1
print(f"Usunięto {licznik} plików")
