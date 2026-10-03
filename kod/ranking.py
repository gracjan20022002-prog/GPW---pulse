import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os
import pandas as pd
from config import REGION, BAZA, WYNIKI_ATHENY
from pyathena import connect
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
con = connect(
    s3_staging_dir=WYNIKI_ATHENY,
    region_name=REGION,
    schema_name=BAZA
)
dane = pd.read_sql("SELECT spolka, zmiana_caly_okres FROM gold_ranking_spolek", con)
dane = dane.sort_values(by="zmiana_caly_okres", ascending=False)
print(dane)
maks = pd.read_sql("SELECT MAX(data) AS ostatni FROM gold_dane_dzienne", con)
ostatni = maks["ostatni"][0][:10]
print(f"stan na: {ostatni}")
plt.bar(dane["spolka"], dane["zmiana_caly_okres"])
plt.title(f"Ranking spółek z GPW (stan na: {ostatni})")
plt.xlabel("Nazwa spółki")
plt.ylabel("Całkowita procentowa zmiana w okresie")
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda wartosc, pozycja: f"{wartosc:.0f}%"))
plt.savefig(os.path.join(BASE_DIR, "wykresy", "ranking.png"), dpi=150)
plt.show()