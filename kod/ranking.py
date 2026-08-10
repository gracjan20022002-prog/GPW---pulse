import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os
import pandas as pd
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dane = pd.read_csv(os.path.join(BASE_DIR, "gold", "ranking.csv"))
plt.bar(dane["spolka"], dane["zmiana_caly_okres"])
plt.title("Ranking spółek z GPW")
plt.xlabel("Nazwa spółki")
plt.ylabel("Całkowita procentowa zmiana w okresie")
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda wartosc, pozycja: f"{wartosc:.0f}%"))
plt.savefig(os.path.join(BASE_DIR, "wykresy", "ranking.png"), dpi=150)
plt.show()