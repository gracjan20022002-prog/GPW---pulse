# Notatka 25.10: `kod/data_stream.py` i jego testy — porcje 1 i 2 wyjaśnione w jednym miejscu

Wszystko o kodzie napisanym 24–25.10 w jednym pliku: po co jest, jak płyną przez niego dane, co znaczy
każda linia i co sprawdza każdy test. Kod cytowany dokładnie tak, jak jest w plikach 25.10 (oba po 63
linie). Wartości w tabelach policzone uruchomieniem 25.10 (laptop, Python 3.14.2, pandas 3.0.5) na
danych z testów, a zapis i odczyt `dane.js` — na kopii lokalnego Golda z 20.09. Wynik u Gracjana 25.10:
`pytest kod/test_data_stream.py -v` → `10 passed`, `pytest kod/ -v` → `48 passed`.

Instrukcja, z której powstał kod: [[Notatka-2026-10-24-jak-napisac-strona-dane]] (z częścią 8, zmiany 25.10).

---

## 1. Nad czym pracujemy

Gold codziennie o 18:10 wysyła do S3 dwa pliki: `gold/dane_dzienne/dane_dzienne.csv` (2400 wierszy:
data, cena, spółka, zmiana, miesiąc) i `gold/ranking/ranking.csv` (3 wiersze). Strona ma pokazywać te
liczby, ale sama nie umie czytać plików z S3. Skrypt `kod/data_stream.py` na laptopie robi most:
pobiera oba pliki, **sprawdza je**, obraca w układ wygodny dla strony i zapisuje jeden plik
`strona/dane.js`. Strona (kod pisze Claude) tylko ten plik czyta.

Najważniejsza zasada skryptu: **lepiej stara strona niż zła**. Gdy plik z S3 jest niepełny, z dwóch
różnych biegów albo brakuje spółki — skrypt kończy się komunikatem i nie rusza starego `dane.js`.

| Porcja | Co | Stan 25.10 |
|---|---|---|
| 1 | `sprawdz_pliki` (linie 11–35) i 7 testów | gotowe, testy przechodzą |
| 2 | `zbuduj_dane`, `wczytaj_poprzednie`, `zapisz_js` (36–63) i 3 testy | gotowe, testy przechodzą |
| 3 | część główna: pobranie z S3, wczytanie, wywołanie funkcji, linia wyniku (64–83); `.gitignore` | jeszcze nie |

**Zasada 9 („zrobione”):** porcje 1 i 2 przechodzą testy na zmyślonych danych. Na prawdziwej drodze
danych skrypt jeszcze nie był, nie ma go w gicie, nie ma strony, która czyta `dane.js`.

---

## 2. Droga danych przez funkcje

```
S3: gold/dane_dzienne/dane_dzienne.csv  +  gold/ranking/ranking.csv
        │  download_file → strona/pobrane/                        (porcja 3)
        ▼
read_csv → kolumna "dzien" (data przycięta do 10 znaków) → sort_values   (porcja 3)
        ▼
wczytaj_poprzednie("strona/dane.js")  →  ile sesji było poprzednio (0, gdy pliku nie ma)
        ▼
sprawdz_pliki(dzienne, ranking, ticker, dziś, poprzednie)  →  lista problemów
        │
        ├── niepusta → sys.exit("Strona: problem - …"), kod 1, dane.js NIETKNIĘTY   (porcja 3)
        ▼ pusta
zbuduj_dane(dzienne, ranking, ticker)  →  słownik {"daty", "ceny", "ranking"}
        ▼
zapisz_js(słownik, "strona/dane.js")  →  plik  window.DANE = {…};
```

Funkcje z porcji 1 i 2 **nie czytają same plików i nie łączą się z S3** — dostają gotowe tabele.
Dzięki temu da się je sprawdzić testami na zmyślonych danych, bez sieci (ten sam układ co `kod/path.py`).

---

## 3. Dane, na których pokazuję wartości

To tabele z fixture w pliku testów (część 5). `ticker` z `config.py` = `["CBF.WA", "XTB.WA", "SNT.WA"]`.

`dzienne` — długa tabela, jak `dane_dzienne.csv` po wczytaniu (tylko potrzebne kolumny):
```
        dzien  spolka   cena
0  2026-10-22  CBF.WA  100.0
1  2026-10-22  XTB.WA  200.0
2  2026-10-22  SNT.WA  300.0
3  2026-10-23  CBF.WA  101.0
4  2026-10-23  XTB.WA  202.0
5  2026-10-23  SNT.WA  303.0
```
`ranking` — jak `ranking.csv` (w prawdziwym pliku jest jeszcze `odchylenie_standardowe`, `dni`,
`pierwsza_cena`):
```
   spolka  miesiac  ostatnia_cena  zmiana_caly_okres
0  CBF.WA  2025-01          101.0               10.0
1  XTB.WA  2025-02          202.0               30.0
2  SNT.WA  2025-03          303.0               20.0
```
`ostatnia_cena` w rankingu = cena z 23.10 w `dzienne` — tak jak w prawdziwych plikach z jednego biegu.
W prawdziwych danych: 2400 wierszy, 800 dni, 3 spółki; `miesiac` to najbardziej zmienny pełny miesiąc
spółki, `zmiana_caly_okres` to zmiana ceny w % od pierwszego do ostatniego dnia.

---

## 4. `kod/data_stream.py` linia po linii

### 4.1 Linie 1–10: importy i stałe

```python
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
```

| Linia | Co znaczy | Gdzie używane |
|---|---|---|
| 1 | `json` — zamiana słownika na tekst JSON (`dumps`) i z powrotem (`loads`) | 59, 63 |
| 2 | `os` — ścieżki (`os.path.join`, `dirname`) i sprawdzanie plików (`exists`) | 8, 55 |
| 3 | `sys` — `sys.exit("tekst")`: koniec z komunikatem i kodem 1 | porcja 3 |
| 4 | `date.today()` — dzisiejsza data; `datetime.now()` — data z godziną | porcja 3 |
| 5 | `boto3` — połączenie z S3 (`download_file`); sam import niczego nie wysyła | porcja 3 |
| 6 | `pandas` — tabele; w funkcjach z porcji 1–2 skrót `pd` nie występuje (dostają gotowe tabele) | porcja 3 (`read_csv`) |
| 7 | `ticker` = `["CBF.WA", "XTB.WA", "SNT.WA"]`, `BUCKET` = `"gpw-tracker-bucket"` | porcja 3 |
| 8 | folder projektu: `abspath(__file__)` → `…\GPW - pulse\kod\data_stream.py`, pierwszy `dirname` → `…\kod`, drugi → `…\GPW - pulse` (tak samo jak w `gold.py`, linia 5) | porcja 3 |
| 9 | początek pliku `dane.js` | 59, 63 |
| 10 | koniec pliku `dane.js` | 59, 63 |

**Dlaczego 9 i 10 to stałe:** ten sam tekst służy do zapisu (linia 63) i do odczytu (linia 59). Gdyby był
wpisany dwa razy i różnił się jedną spacją, odczyt by się nie udał.

### 4.2 `sprawdz_pliki` — linie 11–35 (porcja 1)

```python
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
```

**Co robi:** zbiera wszystkie znalezione problemy na listę i ją oddaje. Pusta lista = wszystko dobrze.
Nic nie wypisuje i nie kończy programu — o tym decyduje część główna (porcja 3). Wzór: `sprawdz_daty`
w `kod/path.py`.

**Parametry:** `dzienne` (tabela z kolumną `dzien` w postaci `"RRRR-MM-DD"`), `ranking`, `spolki` (lista
`ticker`), `dzis` (dzisiejsza data jako **tekst**), `poprzednie` (liczba sesji z poprzedniego `dane.js`).

| Linia | Co znaczy | Na danych z części 3 |
|---|---|---|
| 12 | pusta lista na problemy | `[]` |
| 13 | `set` — zbiór nazw: bez powtórzeń, bez kolejności; porównanie zbiorów | `{'SNT.WA', 'CBF.WA', 'XTB.WA'}` = zbiór `ticker` → `False`, nic się nie dzieje |
| 14 | komunikat; `sorted` układa nazwy alfabetycznie, bo zbiór wypisuje się w przypadkowej kolejności | przy `ABC.WA`: `Spółki w danych dziennych: ['ABC.WA', 'CBF.WA', 'SNT.WA', 'XTB.WA']` |
| 15–16 | to samo dla rankingu | przy `ABC.WA` zamiast SNT: `Spółki w rankingu: ['ABC.WA', 'CBF.WA', 'XTB.WA']` |
| 17 | `if problemy:` — pusta lista to `False`, niepusta to `True` | `[]` → `False` |
| 18 | **wczesny `return`**: przy złych spółkach koniec funkcji tutaj | patrz niżej |
| 19 | `isna()` — `True` przy pustej cenie; `sum()` liczy `True` jako 1 | `[False × 6]` → 0; z `None` w wierszu 1 → 1 |
| 20 | komunikat | `Pusta cena` |
| 21 | `duplicated(subset=[…])` — `True` przy wierszu, którego para (dzień, spółka) już była wyżej | `[False × 6]` → 0 |
| 22 | komunikat | `Powtórzony dzień` |
| 23 | `nunique()` — liczba **różnych** dat | 2 (prawdziwy plik: 800) |
| 24 | każda spółka ma mieć każdy dzień: wierszy = dni × spółki | 6 = 2 × 3 → dobrze (prawdziwy: 2400 = 800 × 3) |
| 25 | komunikat | bez CBF z 22.10: `Spółki mają złą ilość danych/różne dni: 5 wierszy, 2 dni` |
| 26 | `max()` na tekście daje najpóźniejszą datę, bo `RRRR-MM-DD` układa się jak daty | `"2026-10-23" > "2026-10-24"` → `False` |
| 27 | komunikat | przy `dzis = "2026-10-22"`: `Sesja z przyszłości: 2026-10-23, dziś: 2026-10-22` |
| 28 | ochrona przed „pół tabeli” | `2 < 2` → `False` |
| 29 | komunikat | przy `poprzednie = 3`: `Mniej sesji niż poprzednio: 2 < 3` |
| 30 | pętla po spółkach | `CBF.WA`, `XTB.WA`, `SNT.WA` |
| 31 | wiersze spółki → kolumna `cena` → lista → **ostatni element** | CBF: `[100.0, 101.0]` → `101.0` |
| 32 | jedyny wiersz spółki w rankingu → `ostatnia_cena` → **pierwszy element** | CBF: `[101.0]` → `101.0` |
| 33 | porównanie po zaokrągleniu do 2 miejsc (ceny z Yahoo mają długi ogon) | `101.0 != 101.0` → `False` |
| 34 | komunikat | przy CBF 100 w rankingu: `CBF.WA: ostatnia cena: 101.0, w rankingu: 100.0` |
| 35 | oddaje listę | `[]` |

**Dlaczego wczesny `return` (linia 18).** Linie 31–32 szukają każdej spółki z `ticker`. Gdyby jakiejś
brakowało, filtr dałby pustą listę, a `[-1]` albo `[0]` na pustej liście kończy się `IndexError`. Poza
tym przy obcej spółce reszta sprawdzeń mówi o złych danych, które i tak są złe — jeden komunikat wystarcza.

**Dlaczego linie 30–34 (decyzja D2 a).** Oba pliki muszą być z tego samego biegu Golda. Gdyby pobrać je
w chwili, gdy Gold wysyła (18:10), mógłby przyjść nowy `dane_dzienne.csv` i stary `ranking.csv` —
wtedy ostatnia cena w danych nie zgadza się z `ostatnia_cena` w rankingu.

**Ważne przy linii 31:** `[-1]` to ostatni **wiersz w tabeli**, nie najpóźniejszy dzień. Dlatego część
główna (porcja 3) najpierw sortuje tabelę po spółce i dniu, a dopiero potem woła `sprawdz_pliki`.

**Kolejność sprawdzeń i ile komunikatów przy jednej usterce:** sprawdzenia nie wykluczają się (poza
wczesnym `return`). Przykład z 25.10 na kopii lokalnego Golda: plik bez ostatniego dnia daje naraz
`Mniej sesji niż poprzednio: 774 < 775` i trzy rozjazdy z rankingiem (po jednym na spółkę).

### 4.3 `zbuduj_dane` — linie 36–53 (porcja 2)

```python
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
```

**Co robi:** z dwóch tabel robi jeden słownik w kształcie, którego potrzebuje strona: jedna lista dat
i do niej po jednej liście cen na spółkę (ceny na tych samych pozycjach co daty), plus krótki ranking.
Woła się ją **dopiero po** `sprawdz_pliki` — przy powtórzonym dniu `pivot` kończy się
`ValueError: Index contains duplicate entries, cannot reshape`, a przy brakującym dniu zostawia `NaN`.

**Co robi `pivot` + `reset_index` (linia 37)** — obraca długą tabelę w szeroką. Wejście: tabela z części 3
(z SNT 23.10 = `334.20001220703125`, jak w teście). Wyjście:
```
spolka       dzien  CBF.WA      SNT.WA  XTB.WA
0       2026-10-22   100.0  300.000000   200.0
1       2026-10-23   101.0  334.200012   202.0
```
Jeden wiersz na dzień (`index="dzien"`), jedna kolumna na spółkę (`columns="spolka"`), w komórkach ceny
(`values="cena"`). Daty wychodzą posortowane rosnąco. Bez `reset_index()` daty byłyby **indeksem**
(numerem wiersza), a nie kolumną — kolumny to wtedy tylko `['CBF.WA', 'SNT.WA', 'XTB.WA']` i linia 50
kończy się `KeyError: 'dzien'`. (Napis `spolka` w lewym górnym rogu to nazwa nagłówka kolumn — nie
przeszkadza.)

| Linia | Co znaczy | Na danych |
|---|---|---|
| 36 | trzy parametry, te same co pierwsze trzy w `sprawdz_pliki` | — |
| 37 | obrót tabeli (wyżej) | 2 wiersze, kolumny `dzien`, `CBF.WA`, `SNT.WA`, `XTB.WA` |
| 38 | pusty słownik na ceny | `{}` |
| 39 | pętla po spółkach w kolejności `ticker` | `CBF.WA`, `XTB.WA`, `SNT.WA` |
| 40 | klucz: nazwa bez `.WA`; wartość: lista cen tej kolumny, każda zaokrąglona do 2 miejsc (lista składana) | `ceny["SNT"] = [300.0, 334.2]` |
| 41 | sortowanie rankingu malejąco po zmianie; **wynik przypisany z powrotem** do `ranking` (sam `sort_values` nie zmienia tabeli, tylko oddaje nową) | kolejność XTB (30), SNT (20), CBF (10) |
| 42 | pusta lista na pozycje rankingu | `[]` |
| 43 | `zip` z trzema kolumnami: w każdym obrocie po jednej wartości z każdej | 1. obrót: `s="XTB.WA"`, `m="2025-02"`, `z=30.0` |
| 44–48 | dopisuje słownik z trzema kluczami; łamanie linii wewnątrz `{ }` jest dozwolone | `{"spolka": "XTB", "miesiac": "2025-02", "zmiana": 30.0}` |
| 49–53 | oddaje słownik z trzema kluczami; `return` stoi **za** obiema pętlami (4 spacje) | wynik niżej |

**Wynik `zbuduj_dane` na tych danych (uruchomione 25.10):**
```
{'daty': ['2026-10-22', '2026-10-23'],
 'ceny': {'CBF': [100.0, 101.0], 'XTB': [200.0, 202.0], 'SNT': [300.0, 334.2]},
 'ranking': [{'spolka': 'XTB', 'miesiac': '2025-02', 'zmiana': 30.0},
             {'spolka': 'SNT', 'miesiac': '2025-03', 'zmiana': 20.0},
             {'spolka': 'CBF', 'miesiac': '2025-01', 'zmiana': 10.0}]}
```
Strona czyta to tak: data `daty[i]` ma ceny `ceny["CBF"][i]`, `ceny["XTB"][i]`, `ceny["SNT"][i]`.

**Wcięcia w tej funkcji (pomyłka z 25.10, poprawiona):** linie 41–53 stały o poziom głębiej, a `return`
w pętli po rankingu. Funkcja kończyła się wtedy w pierwszym obrocie: `ceny` miały tylko CBF, ranking tylko
XTB. Testy z porcji 1 tego nie widziały (nie wołają `zbuduj_dane`), złapał to dopiero `test_zbuduj_dane`.

### 4.4 `wczytaj_poprzednie` — linie 54–60 (porcja 2)

```python
def wczytaj_poprzednie(sciezka):
    if not os.path.exists(sciezka):
        return 0
    with open(sciezka, encoding="utf-8") as plik:
        tekst = plik.read()
    dane = json.loads(tekst.removeprefix(POCZATEK).removesuffix(KONIEC))
    return len(dane["daty"])
```

**Co robi:** mówi, ile sesji miał `dane.js` z poprzedniego biegu. Ta liczba idzie do `sprawdz_pliki`
jako `poprzednie` (linia 28) — chroni przed nadpisaniem dobrej strony plikiem z połową historii.

| Linia | Co znaczy | Na wartościach |
|---|---|---|
| 55 | `os.path.exists` — `True`, gdy plik jest, `False`, gdy nie ma (bez błędu); `not` odwraca | przy pierwszym biegu pliku nie ma → `not False` → `True` |
| 56 | pierwszy bieg kończy się tutaj | `0` |
| 57 | otwiera plik do odczytu (bez `"w"`); `encoding="utf-8"` — jak przy zapisie | — |
| 58 | cały plik jako jeden tekst | `window.DANE = {"daty": ["2023-08-14", …], …};` |
| 59 | odcina `POCZATEK` i `KONIEC` (`removeprefix` / `removesuffix`), resztę zamienia w słownik (`json.loads`) | `{"daty": […], "ceny": {…}, …}` |
| 60 | liczba dat = liczba sesji | lokalny Gold z 20.09: `775` |

**Czym jest `sciezka`** (pytanie Gracjana 25.10). To parametr — funkcja sama nie wie, który plik czytać;
podaje go ten, kto ją woła. W części głównej (porcja 3) linia 74 robi
`sciezka = os.path.join(BASE_DIR, "strona", "dane.js")`, czyli tekst
`C:\Users\gracj\OneDrive\Dokumenty\DE\GPW - pulse\strona\dane.js`, a linia 75 woła
`wczytaj_poprzednie(sciezka)`. Ta sama `sciezka` idzie potem do `zapisz_js` (linia 81) — odczyt i zapis
dotyczą tego samego pliku. Parametr zamiast ścieżki wpisanej w funkcję: na kopii albo w teście można
podać inny plik i nie ruszyć prawdziwego `dane.js` (tak było przy próbie 25.10).

**Po co `POCZATEK` i `KONIEC` w linii 59** — krok po kroku na pogodzie (uruchomione 25.10,
`POCZATEK = "window.POGODA = "`, `KONIEC = ";"`):
```
tekst:  window.POGODA = {"daty": ["2026-10-21", "2026-10-22"], "temp": {"KRK": [9.9, 12.1]}};
krok1:  {"daty": ["2026-10-21", "2026-10-22"], "temp": {"KRK": [9.9, 12.1]}};      ← removeprefix(POCZATEK)
krok2:  {"daty": ["2026-10-21", "2026-10-22"], "temp": {"KRK": [9.9, 12.1]}}       ← removesuffix(KONIEC)
dane:   {'daty': ['2026-10-21', '2026-10-22'], 'temp': {'KRK': [9.9, 12.1]}}       ← json.loads, typ dict
len(dane["daty"]) → 2
```
Plik to linia JavaScriptu, a `json.loads` rozumie tylko sam JSON — część w klamrach. `window.POGODA = `
i `;` to JavaScript, więc trzeba je odciąć. Bez odcięcia: `JSONDecodeError: Expecting value: line 1
column 1 (char 0)` (na pierwszym znaku stoi `w`, a nie `{`). Z odciętym tylko początkiem:
`JSONDecodeError: Extra data: line 1 column 69 (char 68)` (za `}` został `;`). Gdy tekst nie zaczyna się
od podanego początku, `removeprefix` nic nie zmienia: `"abc".removeprefix("window.POGODA = ")` → `'abc'`.

### 4.5 `zapisz_js` — linie 61–63 (porcja 2)

```python
def zapisz_js(dane, sciezka):
    with open(sciezka, "w", encoding = "utf-8") as plik:
        plik.write(POCZATEK + json.dumps(dane, ensure_ascii=False) + KONIEC)
```

| Linia | Co znaczy |
|---|---|
| 61 | słownik do zapisania i ścieżka pliku |
| 62 | `"w"` — zapis od nowa: stara treść znika w chwili otwarcia; `encoding = "utf-8"` (spacje wokół `=` bez wpływu, zwykle pisze się bez nich) |
| 63 | skleja `window.DANE = ` + słownik jako tekst JSON + `;`. `ensure_ascii=False` zostawia polskie litery jako litery, a nie kody `ł` |

**Dlaczego `window.DANE = …;`, a nie samo JSON.** Strona otwierana z dysku (bez serwera) nie może
wczytać pliku `.json` — przeglądarka to blokuje — ale może wczytać skrypt `.js`. Ten plik to jedna linia
JavaScriptu: „zapisz ten słownik pod nazwą `DANE`”. Strona potem czyta `DANE.daty`, `DANE.ceny`…
(decyzja D1 a z 23.10; D3 a: `dane.js` poza gitem, bo jest generowany).

**Zapis i odczyt razem (uruchomione 25.10 na kopii, lokalny Gold z 20.09):** przed zapisem
`wczytaj_poprzednie` → `0`; po `zapisz_js` → `775`; plik 26 980 B, zaczyna się od
`window.DANE = {"daty": ["2023-08-14", "2023-08-16", …`, kończy na `…"wygenerowano": "…"};`.
**W pytest te dwie funkcje nie mają testu** — sprawdzi je pierwszy i drugi bieg w porcji 3
(`poprzednio 0`, potem `poprzednio 800`).

---

## 5. `kod/test_data_stream.py` linia po linii

### 5.1 Linie 1–19: importy i dwie fixture

```python
import pandas as pd
import pytest
from config import ticker
from data_stream import sprawdz_pliki, zbuduj_dane
@pytest.fixture
def dzienne():
    return pd.DataFrame({
        "dzien": ["2026-10-22"] * len(ticker) + ["2026-10-23"] * len(ticker),
        "spolka": ticker * 2,
        "cena": [100.0, 200.0, 300.0, 101.0, 202.0, 303.0]
    })
@pytest.fixture
def ranking():
    return pd.DataFrame({
        "spolka": ticker,
        "miesiac": ["2025-01", "2025-02", "2025-03"],
        "ostatnia_cena": [101.0, 202.0, 303.0],
        "zmiana_caly_okres": [10.0, 30.0, 20.0]
    })
```

| Linia | Co znaczy |
|---|---|
| 1 | `pd.DataFrame` — tabela ze słownika: klucz = nazwa kolumny, wartość = lista |
| 2 | dostęp do `@pytest.fixture` |
| 3 | ta sama lista spółek co w projekcie |
| 4 | testowane funkcje; import wykonuje linie 1–10 z `data_stream.py`, ale **nie** część główną |
| 5, 12 | `@pytest.fixture` nad `def` — dla pytest: to składnik dla testów, nie test |
| 6, 13 | nazwa funkcji = nazwa parametru, pod którą test ją dostanie |
| 7, 14 | `return` od razu z tabelą |
| 8 | lista razy liczba powtarza listę, `+` skleja dwie listy: 3 × `2026-10-22`, potem 3 × `2026-10-23` |
| 9 | `ticker * 2` → CBF, XTB, SNT, CBF, XTB, SNT |
| 10 | ceny z 22.10 (100/200/300) i z 23.10 (101/202/303) |
| 15–18 | 3 wiersze; `ostatnia_cena` = ceny z 23.10; `miesiac` i `zmiana_caly_okres` czyta tylko `zbuduj_dane` |
| 11, 19 | zamykają słownik i nawias `DataFrame` |

**Jak działa fixture.** Test ma parametry `(dzienne, ranking)`. Pytest widzi nazwę `dzienne`, szuka
fixture o tej nazwie, woła ją i podaje wynik — **osobno dla każdego testu**. W środku testu `dzienne`
to już tabela, nie funkcja. Dzięki temu zmiana tabeli w jednym teście (np. `None` w cenie) nie przechodzi
do następnego.

**Dlaczego nie stała na górze pliku** (sprawdzone 25.10 na kopii): jedna tabela na cały plik, trzy testy
ją zmieniają → `3 failed, 4 passed`, a ten sam test uruchomiony osobno przechodzi. Wynik zależałby od
tego, które testy i w jakiej kolejności się uruchomi.

**Wzór, który powtarza się w testach:**
1. `def test_…(dzienne, ranking):` — dostaje świeże tabele;
2. (czasem) jedna linia psuje dane: `tabela["kolumna"] = nowa_lista` — **nawias kwadratowy, jeden `=`**;
3. `wynik = sprawdz_pliki(dzienne, ranking, ticker, "2026-10-24", 2)` — `dzis` = 24.10 (dzień po ostatniej
   sesji), `poprzednie` = 2 (tyle, ile dni w danych), chyba że test zmienia właśnie to;
4. `assert` — pełna lista (`==`) albo fragment tekstu (`in`).

`==` z całą listą stoi tam, gdzie tekst jest krótki i stały — sprawdza przy okazji, że nie odpaliło się
nic innego. `in` z fragmentem stoi tam, gdzie liczy się tylko, **który** problem się pojawił.

### 5.2 Dziesięć testów

| Linie | Test | Co psuje | Co zwraca funkcja (uruchomione 25.10) | `assert` |
|---|---|---|---|---|
| 20–22 | `test_komplet` | nic | `[]` | `== []` |
| 23–26 | `test_brak_dnia_jednej_spolki` | `dzienne.drop(index=0)` — bez wiersza 0 (CBF 22.10); nowa tabela, fixture bez zmian | `['Spółki mają złą ilość danych/różne dni: 5 wierszy, 2 dni']` | 1 problem, zawiera `różne dni` |
| 27–30 | `test_pusta_cena` | `cena` z `None` w wierszu 1 (XTB 22.10) → `NaN` | `['Pusta cena']` | `== ["Pusta cena"]` |
| 31–34 | `test_przyszlosc` | `dzis = "2026-10-22"` | `['Sesja z przyszłości: 2026-10-23, dziś: 2026-10-22']` | 1 problem, zawiera `przyszłości` |
| 35–37 | `test_mniej_sesji` | `poprzednie = 3` | `['Mniej sesji niż poprzednio: 2 < 3']` | pełny tekst |
| 38–42 | `test_ranking_z_innego_dnia` | `ostatnia_cena` CBF = 100 (w danych 101) | `['CBF.WA: ostatnia cena: 101.0, w rankingu: 100.0']` | 1 problem, zawiera `ticker[0]` (`CBF.WA`) |
| 43–47 | `test_obca_spolka` | ostatni wiersz (SNT 23.10) → `ABC.WA` | `["Spółki w danych dziennych: ['ABC.WA', 'CBF.WA', 'SNT.WA', 'XTB.WA']"]` | 1 problem (wczesny `return`), zawiera `ABC.WA` |
| 48–51 | `test_powtorzony_dzien` | daty `22, 22, 22, 22, 23, 23` — CBF ma 22.10 dwa razy, 23.10 wcale | `['Powtórzony dzień']` | pełny tekst |
| 52–56 | `test_obca_spolka_w_rankingu` | ranking: CBF, XTB, `ABC.WA` (bez SNT) | `["Spółki w rankingu: ['ABC.WA', 'CBF.WA', 'XTB.WA']"]` | 1 problem, zawiera `rankingu` |
| 57–63 | `test_zbuduj_dane` | SNT 23.10 = `334.20001220703125` (ogon jak z Yahoo) | słownik z części 4.3 | daty po kolei; ceny bez `.WA`, SNT `334.2`; pierwszy XTB (30.0); ostatni CBF |

**Ciekawy przypadek — `test_powtorzony_dzien`.** Tabela po zmianie:
```
        dzien  spolka   cena
0  2026-10-22  CBF.WA  100.0
1  2026-10-22  XTB.WA  200.0
2  2026-10-22  SNT.WA  300.0
3  2026-10-22  CBF.WA  101.0
4  2026-10-23  XTB.WA  202.0
5  2026-10-23  SNT.WA  303.0
```
Wierszy dalej 6 = 2 dni × 3 spółki, więc linia 24 milczy. Ostatnia cena CBF to 101 (wiersz 3) = 101
w rankingu, więc linia 33 też milczy. Usterkę łapie **tylko** `duplicated` (linia 21). Bez tego
sprawdzenia CBF miałby na stronie dwie ceny z 22.10 i żadnej z 23.10.

### 5.3 Które sprawdzenie łapie który test

| Linie w `data_stream.py` | Sprawdzenie | Test |
|---|---|---|
| 13–14 | spółki w danych dziennych | `test_obca_spolka` |
| 15–16 | spółki w rankingu | `test_obca_spolka_w_rankingu` |
| 17–18 | wczesny `return` | oba wyżej (po 1 problemie) |
| 19–20 | pusta cena | `test_pusta_cena` |
| 21–22 | powtórzony dzień | `test_powtorzony_dzien` |
| 23–25 | każda spółka ma każdy dzień | `test_brak_dnia_jednej_spolki` |
| 26–27 | sesja z przyszłości | `test_przyszlosc` |
| 28–29 | mniej sesji niż poprzednio | `test_mniej_sesji` |
| 30–34 | ranking z tego samego biegu | `test_ranking_z_innego_dnia` |
| 11–35 razem | dobre dane → `[]` | `test_komplet` |
| 36–53 | `zbuduj_dane` | `test_zbuduj_dane` |
| 54–63 | `wczytaj_poprzednie`, `zapisz_js` | **brak** — porcja 3, dwa biegi |

---

## 6. Pojęcia użyte w kodzie (wejście → wyjście)

- **`set(lista)`** — zbiór bez powtórzeń i bez kolejności: `set(["CBF", "XTB", "CBF"])` → `{'CBF', 'XTB'}`.
- **`sorted(zbiór)`** — lista alfabetycznie: `sorted({'XTB.WA', 'ABC.WA'})` → `['ABC.WA', 'XTB.WA']`.
- **Wczesny `return`** — `return` w środku funkcji kończy ją od razu; linie niżej się nie wykonują.
- **`isna().sum()`** — liczba pustych: `[100.0, NaN, 300.0]` → `1`.
- **`None` na liście wpisanej do kolumny liczb** — pandas zamienia go na `NaN`.
- **`duplicated(subset=[…])`** — `True` przy powtórzonej parze kolumn: pary (22, CBF), (22, CBF) → `[False, True]`.
- **`nunique()`** — liczba różnych wartości: `["22", "22", "23"]` → `2`.
- **`max()` na tekście dat** — `["2026-10-22", "2026-10-23"]` → `"2026-10-23"`; tekst porównany z tekstem:
  `"2026-10-23" > "2026-10-25"` → `False`, ale `"2026-10-23 17:00:00" > "2026-10-23"` → `True` (dlatego
  w porcji 3 data przycięta `[:10]`).
- **`tabela[tabela["spolka"] == t]["cena"].tolist()[-1]`** — filtr wierszy → kolumna → lista → ostatni.
- **`round(x, 2)`** — `round(334.20001220703125, 2)` → `334.2`.
- **`pivot(index, columns, values)`** — długa tabela → szeroka (część 4.3); **`reset_index()`** — indeks
  wraca jako zwykła kolumna.
- **`sort_values(by=…, ascending=False)`** — malejąco; oddaje **nową** tabelę, trzeba ją przypisać.
- **`t.replace(".WA", "")`** — `"CBF.WA"` → `"CBF"`.
- **Lista składana** — `[round(c, 2) for c in [100.004, 101.0]]` → `[100.0, 101.0]`.
- **`zip` z trzema** — `zip(["CBF.WA", "XTB.WA"], ["2025-01", "2025-02"], [10.0, 30.0])` →
  `('CBF.WA', '2025-01', 10.0)`, `('XTB.WA', '2025-02', 30.0)`.
- **`lista.append(x)`** — dopisuje `x` na koniec listy.
- **`os.path.exists(ścieżka)`** — `True` / `False`, bez błędu; **`not`** odwraca warunek.
- **`with open(…) as plik:`** — otwiera i sam zamyka plik; bez trybu = odczyt, `"w"` = zapis od nowa.
- **`json.dumps(słownik, ensure_ascii=False)`** — słownik → tekst JSON; **`json.loads(tekst)`** — odwrotnie.
- **`removeprefix` / `removesuffix`** — `'window.DANE = {"a": 1};'.removeprefix("window.DANE = ").removesuffix(";")`
  → `'{"a": 1}'`; gdy nie pasuje — tekst bez zmian.
- **`@pytest.fixture`** — funkcja-składnik; pytest woła ją dla każdego testu, który ma parametr o tej nazwie.
- **`tabela.drop(index=0)`** — nowa tabela bez wiersza 0; reszta numerów zostaje (1, 2, 3…).
- **`tabela["kolumna"] = lista`** — podmienia całą kolumnę (tak samo jak w `gold.py`, linie 9–16).
- **Przypisanie łańcuchowe** — `a = b = wartość`: ta sama wartość naraz w dwóch miejscach (pułapka niżej).

---

## 7. Pułapki, na które trafiliśmy 24–25.10

| Co było | Co się działo | Jak jest dobrze |
|---|---|---|
| `wynik = dzienne[dzienne("cena")==[…]]` | `TypeError: 'DataFrame' object is not callable` — okrągły nawias = wywołanie | `dzienne["cena"] = […]`, potem osobno `wynik = sprawdz_pliki(…)` |
| `wynik = dzienne["cena"]=[…]` | przypisanie łańcuchowe: `wynik` = lista cen; `AssertionError` | bez `wynik =` w linii ze zmianą kolumny |
| `return` wcięty w pętli w `zbuduj_dane` | koniec funkcji w pierwszym obrocie: ceny tylko CBF | `return` na 4 spacjach, za pętlami |
| stała `DZIENNE` zamiast fixture | zmiany przechodzą między testami: `3 failed, 4 passed` | `@pytest.fixture` |
| tabela zmieniana w teście 1, czytana w teście 2 | — | fixture daje świeżą tabelę każdemu testowi |
| `[-1]` bez sortowania | ostatni wiersz pliku, nie ostatni dzień | `sort_values(["spolka", "dzien"])` przed `sprawdz_pliki` (porcja 3) |
| `zbuduj_dane` przed `sprawdz_pliki` | `pivot` przy powtórce → `ValueError`, przy braku dnia → `NaN` | najpierw sprawdzenie, potem budowa |
| `sort_values` bez przypisania | tabela w starej kolejności (CBF, XTB, SNT) | `ranking = ranking.sort_values(…)` |
| bez `reset_index()` | `KeyError: 'dzien'` w linii 50 | `.reset_index()` za `pivot` |

**Czego nauczyło czytanie testów:** testy `sprawdz_pliki` nie widzą błędów w `zbuduj_dane` — `7 passed`
przy zepsutej funkcji znaczyło tylko „plik nie ma błędu składni”. Każda funkcja potrzebuje własnego testu.

---

## 8. Co dalej

- **Porcja 3:** linie 64–83 (część główna, kroki podane 25.10) i dwie linie w `.gitignore`
  (`strona/dane.js`, `strona/pobrane/`). `pytest kod/ -v` dalej `48 passed`.
- **Pierwszy bieg po kontroli 25.10 (po 18:32):** przewidywanie `Strona: 800 sesji (2023-08-14 – 2026-10-23),
  poprzednio 0, ostatnie: CBF 192.0, XTB 137.0, SNT 334.2`, kod 0; drugi bieg `poprzednio 800`;
  `git status --short` bez `strona/`. Niesprawdzone: dostęp klucza laptopa do `gold/` w S3.
- **Potem Claude:** szkic strony → `strona/index.html`, który czyta `dane.js`.
- **Commit i `git push`** — oba pliki i notatki.

## Powiązane notatki

- [[Notatka-2026-10-24-jak-napisac-strona-dane]] — instrukcja porcji 1–3 (część 8: zmiany 25.10)
- [[Notatka-2026-10-23-dane-na-strone]] — notatka projektowa (co i dlaczego, D1–D6)
- [[Notatka-2026-10-19-strona-nowy-kierunek]] — strona, decyzje 19–23.10
