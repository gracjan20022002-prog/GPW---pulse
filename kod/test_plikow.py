import os
from datetime import datetime
from config import ticker
import pytest
import pandas as pd
print(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
@pytest.mark.parametrize("tick", ticker)
def test_dzialania(tick):
    zly_wiersz = []
    znane_bledy = []
    assert os.path.exists(os.path.join(BASE_DIR, "companies", f"{tick}.txt"))
    licznik = 0
    with open(os.path.join(BASE_DIR, "companies", f"{tick}.txt"), "r", encoding = "utf-8") as plik:
        for wiersz in plik:
            test = wiersz.split(",")
            if len(test) == 2 and len(test[0]) == 19:
                try:
                    data = datetime.strptime(test[0], "%Y-%m-%d %H:%M:%S")
                    liczba = float(test[1])
                    licznik += 1
                except ValueError:
                    if test[1].strip() == "None":
                        znane_bledy.append(wiersz)
                    else:
                        zly_wiersz.append(wiersz)
            else: 
                zly_wiersz.append(wiersz)
    assert not zly_wiersz, f"Wiersz jest nieprawidłowy: {zly_wiersz}"           
    assert  licznik >= 700 , f"Za mało wierszy: {licznik}"

def test_powtorek():
    df = pd.read_csv(os.path.join(BASE_DIR, "silver", "clean_data.csv"))
    df["data"] = pd.to_datetime(df["data"])
    df["dzien"] = df["data"].dt.date
    ile_duplikatow = df.duplicated(subset=['dzien', 'spolka']).sum() 
    assert ile_duplikatow == 0, f"Znaleziono duplikaty: {df.duplicated(subset=['dzien', 'spolka']).sum()}"
