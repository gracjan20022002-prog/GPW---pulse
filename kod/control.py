from config import ticker
import os
import sys
import requests
from datetime import date
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def sprawdz_blok(blok, spolki, dzis):
    bledy = []
    if f"Data pomiaru Producenta: {dzis}" not in blok:
        bledy.append(f"Brak pomiaru producenta z {dzis}")
    zapisane = [linia.split(":")[0] for linia in blok.splitlines() if "stan: zapisane" in linia]
    for spolka in spolki:
        if spolka not in zapisane:
            bledy.append(f"{spolka}: brak 'stan: zapisane'")
    if "Odebrano" not in blok:
        bledy.append("Konsument nie ukończył zadania: Brak linii 'Odebrano'")
    ile = blok.count("S3: wysłano")
    if ile != 2:
        bledy.append(f"S3: wysłano {ile} razy")
    if "Traceback" in blok:
        bledy.append("Wystąpił błąd: Traceback")
    return bledy
def wytnij_blok(tekst):
    linie = tekst.splitlines()
    start = None
    for i in range(len(linie)):
        if linie[i].startswith("=== Data pomiaru Producenta"):
            start = i
    if start is None:
        return ""
    dzisiejsze = [linia for linia in linie[start:] if not linia.startswith("Kontrola:")]
    return "\n".join(dzisiejsze)
if __name__ == "__main__":
    try:
        KONTROLA_LOG = os.environ.get("KONTROLA_LOG", os.path.join(BASE_DIR, "companies", "errors.txt"))
        KONTROLA_DATA = os.environ.get("KONTROLA_DATA", str(date.today()))
        STROZ_URL = os.environ.get("STROZ_URL")
        with open(KONTROLA_LOG, encoding = "utf-8") as plik:
            raport = plik.read()
        blok = wytnij_blok(raport)
        blad = sprawdz_blok(blok, ticker, KONTROLA_DATA)
        if blad:
            tekst = "Kontrola: AWARIA - " + "; ".join(blad)
        else:
            tekst = "Kontrola: OK"
        print(tekst)
        if STROZ_URL:
            if blad:
                odp = requests.post(STROZ_URL + "/fail", data=(tekst + "\n\n" + blok).encode("utf-8"), timeout=10)
            else:
                odp = requests.get(STROZ_URL, timeout=10)
            if odp.status_code != 200:
                print(f"Kontrola: bramka E-mail odpowiedziała: {odp.status_code}")
                sys.exit(1)
        else:
            print("Kontrola: brak adresu stróża")
    except Exception as e:
        print(f"Kontrola: Błąd skryptu - {e}")
        sys.exit(1)