# Notatka 03.10.2026 — wykresy, `test_plikow.py` i Power BI na Athenę

Status: **zatwierdzona przez Gracjana 03.10 — wszystkie pięć decyzji w wariancie (a).** Instrukcja przed kodem: [[Notatka-2026-10-03-jak-przepiac-wykresy]].

## Sedno w trzech zdaniach

1. Od 21.09 wynik liczy tylko EC2, a `wykresy.py`, `ranking.py`, `test_plikow.py` i Power BI dalej
   czytają **lokalne** pliki na laptopie, które stoją od 20.09 — pokazują stare dane i nie mówią
   o tym ani słowem.
2. Proponuję, żeby oba skrypty wykresów pytały Athenę o tabele `gold_dane_dzienne`
   i `gold_ranking_spolek` (koniec drogi danych, ta sama, którą sprawdza codzienna kontrola),
   a w tytule wykresu pisały **datę ostatniej świecy** — wtedy stary wykres widać gołym okiem.
3. `test_plikow.py` i Power BI wymagają osobnych decyzji, bo dla nich „przepięcie” nie jest
   najlepszą drogą (niżej).

## Fakty (odczyt kodu 03.10)

| Plik | Czyta dziś | Stan tego źródła na laptopie |
|---|---|---|
| `kod/wykresy.py` | `gold/dane_dzienne.csv` | stoi od 20.09 |
| `kod/ranking.py` | `gold/ranking.csv` (kolumny `spolka`, `zmiana_caly_okres`) | stoi od 20.09 |
| `kod/test_plikow.py`, `test_dzialania` | `companies/*.txt` (pamięć Producenta) | pamięć **laptopa**, który od września nie jest Producentem |
| `kod/test_plikow.py`, `test_powtorek` | `silver/clean_data.csv` | stoi od 20.09 |
| `wykresy/PowerBi_do_dopracowania.pbix` | lokalne pliki (nie sprawdzone, plik binarny) | — |

W Athenie: `gold_dane_dzienne` (5 kolumn, w tym `data`, `cena`, `spolka`),
`gold_ranking_spolek` (7 kolumn; `spolka` i `zmiana_caly_okres` mają te same nazwy co w CSV).

## Przykład na innych danych: tablica z pogodą w kiosku

Kiosk wywiesza temperaturę. Kioskarz co rano przepisywał ją z wydruku ze stacji. Od 20.09 wydruków
nikt nie przynosi, a kioskarz dalej przepisuje ostatni.

| Dzień | Stacja mówi | Tablica w kiosku (z wydruku) | Tablica po zmianie (ze stacji, z datą) |
|---|---|---|---|
| 20.09 | 14°C | 14°C | 14°C (pomiar 20.09) |
| 03.10 | 9°C | **14°C** — nikt nie wie, że to stare | 9°C (pomiar 03.10) |
| stacja nie odpowiada | — | 14°C | **błąd na tablicy** — głośno, nie po cichu |

| Przykład | Projekt |
|---|---|
| stacja | Athena, tabele `gold_*` |
| wydruk w szufladzie | lokalne `gold/*.csv` na laptopie |
| tablica w kiosku | `wykres3spolek.png`, `ranking.png` |
| „(pomiar 03.10)” | data ostatniej świecy w tytule wykresu |

## Co może pójść źle

- **Athena nie odpowiada / brak kluczy na laptopie** → skrypt pada z błędem i nie zapisuje
  obrazka. To dobrze (głośno); stary obrazek zostaje w folderze, ale ma starą datę w tytule.
- **Wykres w trakcie biegu o 18:10** → S3 podmienia plik w całości, więc Athena zwróci albo
  wczorajszy, albo dzisiejszy plik, nigdy pół.
- **Kolejność kolumn w `gold_ranking_spolek`** (nazwy `pierwotna_cena`/`aktualna_cena` inne niż
  w CSV) → `ranking.py` bierze tylko `spolka` i `zmiana_caly_okres`, więc nie dotyczy; brać
  kolumny po nazwie, nie `SELECT *`.
- **Kolumna `data` przychodzi z Atheny jako tekst** → `pd.to_datetime` już jest w `wykresy.py`.
- **Koszt** → oba zapytania czytają ok. 150 kB; Athena liczy minimum 10 MB na zapytanie, czyli
  ułamek grosza. Wyniki zapytań odkładają się w `athena-results/` (kilka kB na bieg).
- **Kod na EC2 bez zmian** → wykresy chodzą tylko na laptopie (EC2 nie ma `matplotlib`), więc
  żadnego wdrożenia i żadnego ryzyka dla `cron`.
- **Czwarta spółka** → zapytanie bez `WHERE` weźmie ją samo, pętla w `wykresy.py` idzie po
  `config.ticker`.
- **Za miesiąc** → obrazki w gicie (`wykresy/*.png`) zmieniają się przy każdym biegu; commit tylko
  wtedy, gdy chcemy nowy obrazek w repozytorium.

## Decyzje do podjęcia (rekomendacja Claude'a pierwsza)

1. **Skąd wykresy biorą dane:** (a) **Athena, w każdym z dwóch skryptów osobno** (`connect` +
   `pd.read_sql`, tak jak w `silver.py`) — `path.py` zostaje nietknięty, więc nic nie trzeba
   wdrażać na EC2; (b) wspólna funkcja w `path.py` — mniej powtórzeń, ale zmiana pliku, który
   chodzi w `cron`, czyli wdrożenie; (c) pobieranie CSV z S3 na laptop (`aws s3 cp`) i skrypty bez
   zmian — najprościej, ale zapomniane pobranie znowu daje stary wykres po cichu.
2. **Data w tytule wykresu:** (a) **tak, „stan na RRRR-MM-DD”** z ostatniej świecy; (b) nie.
3. **`test_plikow.py`:** (a) **usunąć cały plik** — oba testy dublują silniejsze sprawdzenia:
   pamięć Producenta na EC2 pilnuje `stan: zapisane` w kontroli o 18:30, a powtórki usuwa
   i sprawdza `assert`-em sam `silver.py` (padnięcie = `Traceback` = alarm u stróża); pamięć
   laptopa nic już nie znaczy; (b) przepiąć `test_powtorek` na Athenę, `test_dzialania` usunąć;
   (c) zostawić bez zmian — dalej będzie „przechodził” na danych z 20.09.
4. **Power BI:** (a) **odłożyć** zgodnie z priorytetem z 08.09 (Power BI na końcu), a do tego czasu
   zapisać w README, że raport pokazuje dane do 20.09; gdy przyjdzie jego kolej — łącznik Athena
   w Power BI (wymaga instalacji sterownika ODBC na laptopie, osobna notatka); (b) łącznik Athena
   teraz; (c) CSV z S3 ręcznie przed odświeżeniem raportu.
5. **Lokalne `gold/` i `silver/` na laptopie:** (a) **zostawić** (nic ich już nie czyta poza
   wyłączonym `pipeline.bat`); (b) wyczyścić, żeby nikt nie wziął ich za aktualne.

## Jak sprawdzimy (po zatwierdzeniu)

Przed biegiem zapisujemy: liczbę wierszy (= ostatnia `Kontrola: Dane` z logu, np. 2355), datę
ostatniej świecy (np. 2026-10-02) i trzy wartości `zmiana_caly_okres` (z rankingu w logu z 18:10).
Po biegu skrypt ma wypisać te same liczby, a tytuł wykresu — tę samą datę. Awaria: bieg ze
zmyślonymi kluczami AWS w oknie ma paść błędem i nie nadpisać obrazka.
