import json
import os
import sys
from datetime import date, datetime
import boto3
import pandas as pd
from config import ticker, BUCKET
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POCZATEK = "window.DANE = "
KONIEC = ";"
def sprawdz_pliki(dzienne, ranking, spolki, dzis, poprzednie):
    problemy = []
    if set(dzienne['spolka']) != set(spolki):
        problemy.append(f"Spółki w danych dziennych: {sorted(set(dzienne['spolka']))}")
    if set(ranking['spolka']) != set(spolki):
        problemy.append(f"Spółki w rankingu: {sorted(set(ranking['spolka']))}")
    if problemy:
        return problemy
    if dzienne["cena"].isna().sum() > 0:
        problemy.append("Pusta cena")
    if dzienne.duplicated(subset=["dzien", "spolka"]).sum() > 0:
        problemy.append("Powtórzony dzień")
    dni = dzienne["dzien"].nunique()
    if len(dzienne) != dni * len(spolki):
        problemy.append(f"Spółki mają złą ilość danych/różne dni: {len(dzienne)} wierszy, {dni} dni")
    if dzienne["dzien"].max() > dzis:
        problemy.append(f"Sesja z przyszłości: {dzienne['dzien'].max()}, dziś: {dzis}")
    if dni < poprzednie:
        problemy.append(f"Mniej sesji niż poprzednio: {dni} < {poprzednie}")
    for t in spolki:
        ostatnia = dzienne[dzienne["spolka"] == t]["cena"].tolist()[-1]
        w_rankingu = ranking[ranking["spolka"] == t]["ostatnia_cena"].tolist()[0]
        if round(ostatnia, 2) != round(w_rankingu, 2):
            problemy.append(f"{t}: ostatnia cena: {round(ostatnia, 2)}, w rankingu: {round(w_rankingu, 2)}")
    return problemy
def zbuduj_dane(dzienne, ranking, spolki):
    tabela = dzienne.pivot(index="dzien", columns="spolka", values="cena").reset_index()
    ceny = {}
    for t in spolki:
        ceny[t.replace(".WA", "")] = [round(c, 2) for c in tabela[t].tolist()]
    ranking = ranking.sort_values(by="zmiana_caly_okres", ascending=False)
    lista = []
    for s, m, z in zip(ranking["spolka"], ranking["miesiac"], ranking["zmiana_caly_okres"]):
        lista.append({
            "spolka": s.replace(".WA", ""),
            "miesiac": m,
            "zmiana": round(z, 2)
        })
    return {
        "daty": tabela["dzien"].tolist(),
        "ceny": ceny,
        "ranking": lista
    }
def wczytaj_poprzednie(sciezka):
    if not os.path.exists(sciezka):
        return 0
    with open(sciezka, encoding="utf-8") as plik:
        tekst = plik.read()
    dane = json.loads(tekst.removeprefix(POCZATEK).removesuffix(KONIEC))
    return len(dane["daty"])
def zapisz_js(dane, sciezka):
    with open(sciezka, "w", encoding = "utf-8") as plik:
        plik.write(POCZATEK + json.dumps(dane, ensure_ascii=False) + KONIEC)
if __name__ == "__main__":
    pobrane = os.path.join(BASE_DIR, "strona", "pobrane")
    os.makedirs(pobrane, exist_ok=True)
    s3 = boto3.client("s3")
    for nazwa in ["dane_dzienne", "ranking"]:
        s3.download_file(BUCKET, f"gold/{nazwa}/{nazwa}.csv", os.path.join(pobrane, f"{nazwa}.csv"))
    dzienne = pd.read_csv(os.path.join(pobrane, "dane_dzienne.csv"))
    ranking = pd.read_csv(os.path.join(pobrane, "ranking.csv"))
    dzienne["dzien"] = dzienne["data"].str[:10]
    dzienne = dzienne.sort_values(["spolka", "dzien"])
    sciezka = os.path.join(BASE_DIR, "strona", "dane.js")
    poprzednie = wczytaj_poprzednie(sciezka)
    problemy = sprawdz_pliki(dzienne, ranking, ticker, str(date.today()), poprzednie)
    if problemy:
        sys.exit("Strona: problem - "+"; ".join(problemy))
    dane = zbuduj_dane(dzienne, ranking, ticker)
    dane["wygenerowano"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    dane["rozmiar_dzienne"] = os.path.getsize(os.path.join(pobrane, "dane_dzienne.csv"))
    zapisz_js(dane, sciezka)
    ostatnie = ", ".join([f"{t} {dane['ceny'][t][-1]}" for t in dane["ceny"]])
    print(f"Strona: {len(dane['daty'])} sesji ({dane['daty'][0]} - {dane['daty'][-1]}), poprzednio {poprzednie}, ostatnie: {ostatnie}")