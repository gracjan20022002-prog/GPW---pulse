import pandas as pd
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gold = pd.read_csv(os.path.join(BASE_DIR, "silver", "clean_data.csv"))
print(gold.shape)
print(gold.dtypes)
gold["data"] = pd.to_datetime(gold["data"])
gold["cena"] = pd.to_numeric(gold["cena"], errors="coerce")
print(gold.dtypes)
gold["zmiana_proc"] = (gold.groupby("spolka")["cena"].pct_change())*100
print(gold.dtypes)
print(gold.iloc[748:753])
calk_zmiana = gold.groupby("spolka")["cena"].agg(["first", "last"]).reset_index()
calk_zmiana["calk_roznica"] = ((calk_zmiana["last"]-calk_zmiana["first"])/calk_zmiana["first"])*100
print(calk_zmiana.sort_values(by="calk_roznica", ascending=False))
calk_zmiana = calk_zmiana.rename(columns={"first":"pierwsza_cena", "last":"ostatnia_cena", "calk_roznica":"zmiana_caly_okres"})
gold["max_zmienny_miesiac"] = gold["data"].dt.to_period("M")
print(gold.head())
print(gold["max_zmienny_miesiac"].nunique())
zmiana_msc = gold.groupby(["spolka", "max_zmienny_miesiac"])["zmiana_proc"].std().reset_index().sort_values(by="zmiana_proc", ascending=False)
sp_rank = zmiana_msc.groupby("spolka").head(1).merge(calk_zmiana, on="spolka")
print(sp_rank)
gold.to_csv(os.path.join(BASE_DIR, "gold", "dane_dzienne.csv"), index=False)
sp_rank.to_csv(os.path.join(BASE_DIR, "gold", "ranking.csv"), index=False)