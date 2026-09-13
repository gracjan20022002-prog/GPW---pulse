import pandas as pd
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN_DNI = 15
gold = pd.read_csv(os.path.join(BASE_DIR, "silver", "clean_data.csv"))
print(gold.shape)
gold["data"] = pd.to_datetime(gold["data"])
gold["cena"] = pd.to_numeric(gold["cena"], errors="coerce")
gold["zmiana_proc"] = (gold.groupby("spolka")["cena"].pct_change())*100
calk_zmiana = gold.groupby("spolka")["cena"].agg(["first", "last"]).reset_index()
calk_zmiana["calk_roznica"] = ((calk_zmiana["last"]-calk_zmiana["first"])/calk_zmiana["first"])*100
print(calk_zmiana.sort_values(by="calk_roznica", ascending=False))
calk_zmiana = calk_zmiana.rename(columns={"first":"pierwsza_cena", "last":"ostatnia_cena", "calk_roznica":"zmiana_caly_okres"})
gold["miesiac"] = gold["data"].dt.to_period("M")
zmiana_msc = gold.groupby(["spolka", "miesiac"])["zmiana_proc"].agg(["std", "count"]).reset_index()
zakres = gold.groupby("spolka")["miesiac"].agg(["min", "max"]).rename(columns={"min": "pierwszy_miesiac", "max": "ostatni_miesiac"}).reset_index()
zmiana_msc = zmiana_msc.merge(zakres, on="spolka")
pelne = zmiana_msc[(zmiana_msc["miesiac"] != zmiana_msc["pierwszy_miesiac"]) & (zmiana_msc["miesiac"] != zmiana_msc["ostatni_miesiac"]) & (zmiana_msc["count"] >= MIN_DNI)]
print(f"Pełna liczba wierszy tabeli miesięcznej: {len(zmiana_msc)}, Prawidłowa liczba wierszy tabeli miesięcznej: {len(pelne)}")
sp_rank = pelne.sort_values(by="std", ascending=False).groupby("spolka").head(1).merge(calk_zmiana, on="spolka", how="right")
sp_rank = sp_rank.rename(columns={"std": "odchylenie_standardowe", "count": "dni"}).drop(columns=["pierwszy_miesiac", "ostatni_miesiac"])
print(sp_rank)
gold.to_csv(os.path.join(BASE_DIR, "gold", "dane_dzienne.csv"), index=False)
sp_rank.to_csv(os.path.join(BASE_DIR, "gold", "ranking.csv"), index=False)
