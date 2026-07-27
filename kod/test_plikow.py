import os
from datetime import datetime
print(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
ticker = ["CBF.WA", "XTB.WA", "SNT.WA"]
for tick in ticker:
    result = os.path.exists(os.path.join(BASE_DIR, "companies", f"{tick}.txt"))
    print(f"Czy plik dla tickera {tick} istnieje: {result}")
    if result:
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
                        print(f"Wiersz: {wiersz} ma nieprawidłowy format")
                else: 
                    print(f"Problem w wierszu: {wiersz}")
            if licznik < 700:
                print("Za mała liczba wierszy")
    else: 
        print(f"Plik o tickerze: {tick} nie istnieje, dalszy test nie jest możliwy")
