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
gold.head()
print(gold.iloc[748:753])
calk_zmiana = gold.groupby("spolka")["cena"].agg(["first", "last"]).reset_index()
calk_zmiana["roznica"] = ((calk_zmiana["last"]-calk_zmiana["first"])/calk_zmiana["first"])*100
print(calk_zmiana.sort_values(by="roznica", ascending=False))