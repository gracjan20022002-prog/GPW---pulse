import pandas as pd
# plik = pd.read_csv("companies/CBF.WA.txt", header = None, names = ["data", "cena"], skipinitialspace=True)
# print(plik.head())
# plik.info()
# print(plik.dtypes)
# plik["data"] = pd.to_datetime(plik["data"])
# plik["cena"] = pd.to_numeric(plik["cena"], errors="coerce")
# print(plik.dtypes)
# print(plik.isna().sum())
# print(plik.duplicated().sum())

ticker = ["CBF.WA", "XTB.WA", "SNT.WA"]
dft = []
for t in ticker:
    df = pd.read_csv(f"companies/{t}.txt", header=None, names=["data", "cena"], skipinitialspace=True)
    df["data"] = pd.to_datetime(df["data"])
    df["cena"] = pd.to_numeric(df["cena"], errors="coerce")
    df["spolka"] = t
    dft.append(df)
dane = pd.concat(dft, ignore_index=True)
print(dane.shape)
print(dane["spolka"].unique())
dane = dane.sort_values(["spolka", "data"])
print(dane.describe())
print(dane.head(10))
dane.to_csv("silver/clean_data.csv", index=False)
