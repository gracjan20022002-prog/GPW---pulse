import pandas as pd
import matplotlib.pyplot as plt
import os
from config import ticker, WYNIKI_ATHENY, REGION, BAZA
from pyathena import connect
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
con = connect(
    s3_staging_dir=WYNIKI_ATHENY,
    region_name=REGION,
    schema_name=BAZA
)
dane = pd.read_sql("SELECT data, cena, spolka FROM gold_dane_dzienne", con)
ostatni = dane["data"].max()[:10]
print(f"Wiersze: {len(dane)}, stan na: {ostatni}")
dane["data"] = pd.to_datetime(dane["data"])
dane["cena"] = pd.to_numeric(dane["cena"], errors="coerce")
dane = dane.sort_values(["spolka", "data"])
for tick in ticker:
    jedna_spolka = dane[dane["spolka"] == tick]
    plt.plot(jedna_spolka["data"], jedna_spolka["cena"], label = tick)
plt.legend()
plt.title(f"Zmiana cen akcji CBF, XTB i SNT w czasie (stan na: {ostatni})")
plt.xlabel("Data")
plt.ylabel("Cena (zł)")
plt.grid(True)
plt.savefig(os.path.join(BASE_DIR, "wykresy", "wykres3spolek.png"), dpi=150)
plt.show()