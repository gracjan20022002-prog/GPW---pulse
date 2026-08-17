import pandas as pd
import matplotlib.pyplot as plt
import os
from config import ticker
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dane = pd.read_csv(os.path.join(BASE_DIR, "gold", "dane_dzienne.csv"))
dane["data"] = pd.to_datetime(dane["data"])
dane["cena"] = pd.to_numeric(dane["cena"], errors="coerce")
for tick in ticker:
    jedna_spolka = dane[dane["spolka"] == tick]
    plt.plot(jedna_spolka["data"], jedna_spolka["cena"], label = tick)
plt.legend()
plt.title("Zmiana cen akcji CBF, XTB i SNT w czasie")
plt.xlabel("Data")
plt.ylabel("Cena (zł)")
plt.grid(True)
plt.savefig(os.path.join(BASE_DIR, "wykresy", "wykres3spolek.png"), dpi=150)
plt.show()