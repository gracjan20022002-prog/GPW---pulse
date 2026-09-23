import pandas as pd
from datetime import date
from config import ticker, WYNIKI_ATHENY, REGION, BAZA
from pyathena import connect
import os
def sprawdz_daty(df, spolki, dzis):
    problemy = []
    df["dzien"] = pd.to_datetime(df["data"]).dt.date
    if dzis.weekday() < 5:
        for t in spolki:
            dobre_dni = df[df["spolka"] == t]["dzien"].tolist()
            if dzis not in dobre_dni:
                problemy.append(f"{t} brak wpisu z: {dzis}")
    przyszle = df[df["dzien"] > dzis]
    for spolka in przyszle["spolka"].unique():
        przyszle_daty = przyszle[przyszle["spolka"] == spolka]["dzien"].max()
        problemy.append(f"{spolka}: wpis z przyszłości: {przyszle_daty}, dziś jest: {dzis}")
    ile = df.groupby("spolka")["dzien"].nunique()
    if ile.nunique() > 1:
        problemy.append(f"Różna liczba dni między spółkami: {ile.to_dict()}")
    return problemy
if __name__ == "__main__":
    con = connect(
    s3_staging_dir=WYNIKI_ATHENY,
    region_name=REGION,
    schema_name=BAZA
    )
    df = pd.read_sql("SELECT spolka, data FROM gold_dane_dzienne", con)
    print(len(df))
    wynik = sprawdz_daty(df, ticker, date.fromisoformat(os.environ.get("DROGA_DATA", str(date.today()))))
    if wynik:
        print("Dane: Problem - "+"; ".join(wynik))
    else: 
        print("Dane: OK")