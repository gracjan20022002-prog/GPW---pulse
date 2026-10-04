# Notatka 03.10: jak przepiąć wykresy na Athenę (wszystko w jednym miejscu)

To instrukcja do [[Notatka-2026-10-03-wykresy-na-athene]] (zatwierdzona 03.10, pięć decyzji
w wariancie (a)). Tu jest **wszystko**: kroki, zasady, nowe pojęcia z wejściem i wyjściem,
przypadki z wynikami i tabela błędów. Przy ocenie kodu odwołuję się tylko do tej notatki. Jeśli
czegoś zabraknie — powiem wprost i dopiszę.

Przykład to pomiary temperatury w dwóch miastach, nie spółki. **Każdy wynik z przykładu pochodzi
z uruchomienia 03.10** (Python 3.14.2, pandas 3.0.5, laptop). Twoich plików nie ruszałem.

---

## Część 1. Kroki (po jednej linii, szczegóły niżej)

1. `kod/wykresy.py`, linia 4: dopisz do importu z `config` trzy nazwy: `WYNIKI_ATHENY, REGION, BAZA`.
2. `kod/wykresy.py`: pod linią 4 dopisz `from pyathena import connect`.
3. `kod/wykresy.py`: zamiast `pd.read_csv(...)` — połączenie `connect(...)` i `pd.read_sql` z `SELECT data, cena, spolka FROM gold_dane_dzienne`.
4. `kod/wykresy.py`: zaraz pod `read_sql` — `ostatni` (data ostatniej świecy jako tekst) i `print` z liczbą wierszy i tą datą.
5. `kod/wykresy.py`: pod linią z `pd.to_numeric` — sortowanie po `spolka` i `data`.
6. `kod/wykresy.py`: tytuł jako f-string z `(stan na {ostatni})`.
7. Uruchom `python kod/wykresy.py` (Część 6). Ma być `Wiersze: 2355, stan na 2026-10-02` i gładkie linie.
8. `kod/ranking.py`: dopisz oba importy (`config` i `connect`).
9. `kod/ranking.py`: zamiast `pd.read_csv(...)` — `connect(...)`, `read_sql` z `SELECT spolka, zmiana_caly_okres FROM gold_ranking_spolek`, sortowanie malejąco, `print(dane)`.
10. `kod/ranking.py`: drugie `read_sql` z `SELECT MAX(data) AS ostatni FROM gold_dane_dzienne`, z niego `ostatni` i `print`.
11. `kod/ranking.py`: tytuł jako f-string z `(stan na {ostatni})`.
12. Uruchom `python kod/ranking.py`. Mają być 3 wiersze w kolejności SNT, XTB, CBF i `stan na 2026-10-02`.
13. Bieg `ranking.py` ze zmyślonymi kluczami AWS — ma paść, a `ranking.png` ma zostać stary (Część 7).
14. `git rm kod/test_plikow.py`, potem `pytest kod/ -v` — ma być `18 passed`.
15. Commit i `git push` (Część 8).

---

## Część 2. Zasady, wszystkie naraz

1. **Połączenie piszesz tak samo jak w `silver.py`, linie 6–10** (`connect` z trzema parametrami
   z `config`). W każdym z dwóch plików osobno — `path.py` nie ruszamy (decyzja 1).
2. **`BASE_DIR` zostaje w obu plikach**, bo `plt.savefig` dalej zapisuje do `wykresy/`.
3. **`SELECT` wymienia kolumny po nazwie**, nigdy `SELECT *`. W `gold_ranking_spolek` dwie kolumny
   mają inne nazwy niż w pliku CSV, a my bierzemy tylko `spolka` i `zmiana_caly_okres`.
4. **Athena oddaje wiersze w przypadkowej kolejności.** Plik CSV był posortowany, tabela nie jest.
   Dlatego w `wykresy.py` sortujesz `dane.sort_values(["spolka", "data"])` (jak `silver.py`,
   linia 15), a w `ranking.py` `dane.sort_values(by="zmiana_caly_okres", ascending=False)` (jak
   `gold.py`, linia 13). Bez sortowania linia wykresu skacze w tył (przypadek C/D i obrazek).
5. **Sortowanie w `wykresy.py` idzie po `pd.to_datetime`**, bo sortujemy daty, a nie napisy.
6. **`ostatni` liczysz z tekstu, zanim zamienisz `data` na daty:** `dane["data"].max()[:10]`.
   W tabeli Atheny `data` jest tekstem (`string`), a daty w formacie RRRR-MM-DD sortują się
   alfabetycznie tak samo jak w kalendarzu — to samo, na czym stoi granica w `compaction.py`.
   Po `pd.to_datetime` `[:10]` już nie zadziała (przypadek J).
7. **W `ranking.py` datę bierzesz drugim zapytaniem** (tabela rankingu nie ma kolumny z datą):
   `maks = pd.read_sql("SELECT MAX(data) AS ostatni FROM gold_dane_dzienne", con)`, potem
   `ostatni = maks["ostatni"][0][:10]`. Jedno `con` wystarcza na oba zapytania.
8. **Tytuł to f-string** — litera `f` przed cudzysłowem, inaczej na wykresie będzie dosłownie
   `{ostatni}`.
9. **Linie `print` są obowiązkowe** — to one dają liczby do porównania z przewidywaniem:
   w `wykresy.py` `print(f"Wiersze: {len(dane)}, stan na {ostatni}")`, w `ranking.py`
   `print(dane)` po sortowaniu i `print(f"stan na {ostatni}")`.
10. **`plt.savefig` stoi przed `plt.show()`** — tak jak dziś. Nie przestawiaj.
11. **`ranking.py` nie importuje `ticker` z `config`** — nie jest potrzebny.
12. **Ostrzeżenie `pandas` o SQLAlchemy zostaje** (decyzja z 25.09). Python wypisuje je raz na
    każdą linię z `read_sql`, więc `wykresy.py` da je raz, a `ranking.py` dwa razy.
13. **Nie nazywaj zmiennej tak jak funkcję wbudowaną w Pythona** (`max`, `min`, `sum`, `len`,
    `list`). *Dopisane 03.10 po ocenie `ranking.py` — notatka tego nie miała.* Przykład
    (uruchomiony 03.10): `print(max([3, 9, 4]))` → `9`; po `max = pd.DataFrame(...)` to samo
    `print(max([3, 9, 4]))` → `TypeError: 'DataFrame' object is not callable`. Dopóki w pliku nikt
    nie woła `max(...)`, wszystko działa — błąd wychodzi dopiero przy przyszłej zmianie. Stąd `maks`.

---

## Część 3. Nowe pojęcia i przypadki (uruchomione 03.10)

Wejście — tak wygląda tabela prosto z `read_sql`: kolejność przypadkowa, `data` jako tekst.

| data | temp | miasto |
|---|---|---|
| 2026-10-02 12:00:00 | 9.0 | Gdansk |
| 2026-09-30 12:00:00 | 14.0 | Gdansk |
| 2026-10-01 12:00:00 | 11.0 | Gdansk |
| 2026-10-01 12:00:00 | 7.0 | Krakow |
| 2026-10-02 12:00:00 | 6.0 | Krakow |
| 2026-09-30 12:00:00 | 10.0 | Krakow |

### `max()` na tekście i `[:10]`

```python
print(pomiary["data"].max())
ostatni = pomiary["data"].max()[:10]
print(ostatni, type(ostatni).__name__)
```
Wyjście:
```
2026-10-02 12:00:00
2026-10-02 str
```
`max()` na kolumnie tekstu daje „największy alfabetycznie” napis, czyli najpóźniejszą datę.
`[:10]` to pierwsze 10 znaków — samo RRRR-MM-DD, bez godziny.

### Dlaczego sortowanie (C, D)

Po `pd.to_datetime`, przed sortowaniem i po nim — dni w Gdańsku w kolejności wierszy:
```
C: przed sortowaniem Gdansk: [2, 30, 1]
D: po sortowaniu Gdansk: [30, 1, 2]
```
`plt.plot` łączy punkty **w kolejności wierszy**. Bez sortowania linia Gdańska idzie 2.10 → 30.09
→ 1.10, czyli w tył i znowu w przód. Na obrazku `bez_sortowania.png` (przesłany 03.10 w rozmowie)
widać „trójkąt” zamiast linii; `po_sortowaniu.png` ma zwykłą linię.

### Jedna komórka z tabeli: `["kolumna"][0]` (E, F)

```python
maks = pd.DataFrame({"ostatni": ["2026-10-02 12:00:00"]})   # tak oddaje read_sql z MAX(...) AS ostatni
print(maks)
print(maks["ostatni"][0][:10])
```
Wyjście:
```
               ostatni
0  2026-10-02 12:00:00
2026-10-02
```
`AS ostatni` w SQL nadaje kolumnie nazwę. `["ostatni"]` bierze kolumnę, `[0]` pierwszy (jedyny)
wiersz, `[:10]` samą datę.

### Sortowanie malejąco (G)

```python
rank = pd.DataFrame({"miasto": ["Gdansk", "Krakow", "Sopot"], "zmiana": [12.5, -3.0, 40.1]})
print(rank.sort_values(by="zmiana", ascending=False))
```
Wyjście:
```
   miasto  zmiana
2   Sopot    40.1
0  Gdansk    12.5
1  Krakow    -3.0
```
Numery po lewej to stare numery wierszy — po sortowaniu idą „nie po kolei” i tak ma być.

### f-string w tytule (H)

`f"Ranking (stan na {ostatni})"` → `Ranking (stan na 2026-10-02)`.

### Dwie pomyłki, które się zdarzają (I, J)

```
I: maks["ostatni"][0].date()            → AttributeError: 'str' object has no attribute 'date'
J: pomiary["data"].max()[:10] po to_datetime → TypeError: 'Timestamp' object is not subscriptable
```
I: `.date()` działa na dacie, a z Atheny przyszedł tekst. J: `[:10]` działa na tekście, a po
`to_datetime` kolumna ma już daty (`Timestamp`). Dlatego `ostatni` liczysz **przed**
`to_datetime` (zasada 6).

---

## Część 4. Przykład → projekt

| Przykład | Projekt |
|---|---|
| `pomiary` | `dane` z `SELECT data, cena, spolka FROM gold_dane_dzienne` |
| `temp` | `cena` |
| `miasto`, pętla po `["Gdansk", "Krakow"]` | `spolka`, pętla po `ticker` |
| `sort_values(["miasto", "data"])` | `sort_values(["spolka", "data"])` |
| `maks` z kolumną `ostatni` | `read_sql("SELECT MAX(data) AS ostatni FROM gold_dane_dzienne", con)` |
| `rank`, `zmiana` | `dane` z `gold_ranking_spolek`, `zmiana_caly_okres` |
| `"Temperatura (stan na …)"` | dotychczasowy tytuł + ` (stan na {ostatni})` |

---

## Część 5. Błędy, które możesz zobaczyć, i co znaczą

| Co widzisz | Co to znaczy |
|---|---|
| `ModuleNotFoundError: No module named 'pyathena'` | `(.venv)` nie jest włączone |
| `ImportError: cannot import name '…' from 'config'` | literówka w nazwie (`WYNIKI_ATHENY`, `REGION`, `BAZA`) |
| `NameError: name 'connect' is not defined` | brak `from pyathena import connect` |
| `Failed to execute query.` + `Traceback` z `TABLE_NOT_FOUND` / `does not exist` | literówka w nazwie tabeli |
| `… COLUMN_NOT_FOUND …` | literówka w nazwie kolumny w `SELECT` |
| `KeyError: 'zmiana_caly_okres'` | kolumny nie ma w `SELECT` albo ma inną nazwę |
| `TypeError: 'Timestamp' object is not subscriptable` | `[:10]` po `pd.to_datetime` (przypadek J) |
| `AttributeError: 'str' object has no attribute 'date'` | `.date()` na tekście (przypadek I) |
| linie wykresu z „trójkątami”, skaczą w tył | brak sortowania (C/D) |
| słupki rankingu przy każdym biegu w innej kolejności | brak sortowania w `ranking.py` |
| w tytule dosłownie `{ostatni}` | brak `f` przed cudzysłowem |
| `TypeError: 'DataFrame' object is not callable` | zmienna nazwana jak funkcja wbudowana, np. `max` (zasada 13) |
| `UnrecognizedClientException` | złe klucze AWS — oczekiwane **tylko** w kroku 13 |

---

## Część 6. Uruchomienie i co ma wyjść

Przewidywania liczone 03.10 z ręcznego Golda na EC2 (dane te same co w S3 od 02.10 16:10 UTC,
ważne do poniedziałku 05.10, 18:10).

**[lokalny PowerShell]** z folderu projektu, `(.venv)` włączone (`.\.venv\Scripts\Activate.ps1`).

`python kod/wykresy.py`:
- 2 linie ostrzeżenia `pandas` (SQLAlchemy),
- `Wiersze: 2355, stan na 2026-10-02`,
- okno z wykresem: trzy gładkie linie, tytuł `Zmiana cen akcji CBF, XTB i SNT w czasie (stan na 2026-10-02)`;
  po zamknięciu okna program się kończy, `wykresy/wykres3spolek.png` ma dzisiejszą godzinę.

`python kod/ranking.py`:
- 4 linie ostrzeżenia `pandas` (dwa `read_sql`),
- tabela 3 wierszy w kolejności **SNT.WA 382.485864, XTB.WA 265.208230, CBF.WA 165.873021**
  (numery po lewej dowolne),
- `stan na 2026-10-02`,
- okno: słupki SNT, XTB, CBF malejąco, tytuł `Ranking spółek z GPW (stan na 2026-10-02)`.

---

## Część 7. Bieg z awarią (krok 13)

1. **[lokalny PowerShell, venv nieistotne]** zapisz godzinę obrazka: `(Get-Item wykresy\ranking.png).LastWriteTime`.
2. **[lokalny PowerShell]** `$env:AWS_ACCESS_KEY_ID = "zmyslony"` i `$env:AWS_SECRET_ACCESS_KEY = "zmyslony"`.
3. **[lokalny PowerShell, (.venv) włączone]** `python kod/ranking.py` — ma paść: `Failed to execute
   query.`, `Traceback`, ostatnia linia z `UnrecognizedClientException`; **żadnego okna**.
4. **[lokalny PowerShell]** `(Get-Item wykresy\ranking.png).LastWriteTime` — ta sama godzina co w punkcie 1.
5. **[lokalny PowerShell]** `Remove-Item Env:AWS_ACCESS_KEY_ID`, `Remove-Item Env:AWS_SECRET_ACCESS_KEY`,
   potem `Get-ChildItem Env:AWS*` — nic.

To jest warunek (c) definicji „zrobione”: brak dostępu do danych to błąd na ekranie, a nie stary
wykres podany jako aktualny.

---

## Część 8. Commit

W commicie: `kod/wykresy.py`, `kod/ranking.py`, usunięty `kod/test_plikow.py`, oba obrazki
w `wykresy/`, dwie notatki z 03.10 o wykresach i dopisane wyniki w notatce o Pythonie. Liczby do
przewidzenia podam przed komendą, po `git status --short`. README (opis `test_plikow.py`,
Power BI z danymi do 20.09) — w poniedziałek, razem z punktem 10.

---

## Wyniki 03.10 (wszystko przewidziane przed uruchomieniem)

- `wykresy.py` (27 linii, `git diff` 12/3): `Wiersze: 2355, stan na: 2026-10-02`, 1 ostrzeżenie,
  gładkie linie, tytuł z datą. Gracjan wybrał `stan na:` z dwukropkiem i nawias w obu tytułach.
- `ranking.py` (25 linii, `git diff` 14/2): pierwsza wersja z `max` jako nazwą zmiennej — stąd
  zasada 13; po poprawce na `maks`: tabela SNT 382.485864, XTB 265.208230, CBF 165.873021,
  `stan na: 2026-10-02`, słupki malejąco. Pomyłka w instrukcji: „24 linie” dla `wykresy.py`
  (jest 27, liczba nie zgadzała się z numerami kroków).
- `test_plikow.py` usunięty (`git rm`), `pytest kod/ -v` → `18 passed in 0.63s` (pierwsza próba
  w oknie bez `(.venv)` → `ModuleNotFoundError: pyathena`, pierwszy wiersz tabeli błędów).
- Commit `96f191b`: `8 files changed, 373 insertions(+), 41 deletions(-)` — co do liczby.
- **Awaria (warunek (c)):** zmyślone klucze → 1 ostrzeżenie, `Failed to execute query.`,
  `Traceback` od `pyathena`, potem ten sam błąd jeszcze raz jako błąd całego programu, ostatnia
  linia `pyathena.error.DatabaseError: … (UnrecognizedClientException) …`; okna nie było;
  `ranking.png` dalej 12:22:03; zmienne usunięte (`Get-ChildItem Env:AWS*` pusty).

Stan definicji „zrobione”: (a) ✅ czyta koniec drogi danych, (b) ✅ liczby przewidziane i trafione,
(c) ✅ awaria głośna, obrazek nienadpisany, (d) ✅ działa tam, gdzie ma działać (laptop — EC2 nie
rysuje), (e) README do poprawy w poniedziałek (opis `test_plikow.py`, Power BI z danymi do 20.09).
Power BI świadomie odłożony (decyzja 4).
