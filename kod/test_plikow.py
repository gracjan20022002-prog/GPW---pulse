import os
print(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
ticker = ["CBF.WA", "XTB.WA", "SNT.WA"]
for tick in ticker:
    result = os.path.exists(os.path.join(BASE_DIR, "companies", f"{tick}.txt"))
    print(f"Czy plik dla tickera {tick} istnieje: {result}")
    with open(os.path.join(BASE_DIR, "companies", f"{tick}.txt"), "r", encoding = "utf-8") as plik:
        for wiersz in plik:
            test = wiersz.split(",")
            if len(test) == 2 and len(test[0]) == 19:
                continue
            else: 
                print(f"Problem w wierszu: {wiersz}")
