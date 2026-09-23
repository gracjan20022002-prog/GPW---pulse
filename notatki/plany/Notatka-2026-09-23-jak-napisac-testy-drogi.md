# Notatka 23.09: jak napisać testy prawdziwej drogi (wszystko w jednym miejscu)

Ta notatka zbiera **wszystko**, czego potrzebujesz do testów funkcji `sprawdz_daty`: zasady,
narzędzia, sześć testów z wynikami i listę błędów. Wcześniej dostawałeś to po kawałku,
dopiero po wysłaniu kodu. Od teraz obowiązuje to, co jest tutaj, a nowych zasad w trakcie nie będzie.

Przykład to lodziarnia, nie spółki. Funkcja w przykładzie nazywa się `sprawdz_zeszyt`, ale ma
**dokładnie Twój kod** z `sprawdz_daty`, łącznie z nazwą kolumny `spolka`. Dzięki temu nic nie
trzeba przerabiać w głowie poza nazwami. Wszystkie wyniki poniżej są prawdziwe: przykład został
uruchomiony 23.09 i dał `6 passed`.

---

## Część 1. Dziesięć zasad, wszystkie naraz

1. **Nazwa każdego testu zaczyna się od `test_`**, np. `def test_sobota():`. Bez tego pytest
   pominie test bez słowa.
2. **Nazwa funkcji sprawdzającej NIE zaczyna się od `test_`** (`sprawdz_daty` jest dobrze).
   Inaczej pytest uzna ją za test i wypisze `ERROR … fixture 'df' not found`.
3. **Tabelę tworzysz w samym teście** przez `pd.DataFrame({...})`. Żadnych plików i żadnego `BASE_DIR`.
4. **Kolumny nazywają się `spolka` i `data`**, bo o nie pyta funkcja.
5. **Daty w kolumnie `data` to napisy z godziną**, np. `"2026-09-22 17:00:00"`, tak samo jak z Atheny.
6. **Dzisiejsza data to `date(rok, miesiąc, dzień)`**, nie napis. Napis da
   `AttributeError: 'str' object has no attribute 'weekday'`.
7. **Listę spółek podajesz z `ticker`**, nie z tabeli (`df["spolka"]`). Lista ma mówić, kogo
   **oczekujemy**. Z tabeli nie da się dowiedzieć, kogo w niej brakuje.
8. **Obie kolumny muszą mieć tyle samo elementów.** Inaczej
   `ValueError: All arrays must be of the same length`.
9. **Przed napisaniem `assert` przejdź przez wszystkie trzy sprawdzenia**, nie tylko przez to,
   które testujesz. Jedna usterka w danych często włącza dwa sprawdzenia naraz (Część 3).
10. **Każdy test ma inną tabelę.** Funkcja dopisuje do tabeli kolumnę `dzien`, więc tabeli nie
    przenoś z testu do testu.

---

## Część 2. Narzędzia, każde z wejściem i wyjściem

Wszystkie przykłady na liście `SMAKI = ["wanilia", "czekolada", "pistacjowy"]`.

| Zapis | Co robi | Wynik |
|---|---|---|
| `SMAKI * 2` | powtarza listę 2 razy | `['wanilia', 'czekolada', 'pistacjowy', 'wanilia', 'czekolada', 'pistacjowy']` |
| `["x"] * 3` | lista z 3 takimi samymi elementami | `['x', 'x', 'x']` |
| `lista1 + lista2` | skleja dwie listy | `["a"] + ["b"]` → `['a', 'b']` |
| `len(SMAKI)` | liczba elementów | `3` |
| `SMAKI[0]` | pierwszy element (liczymy od 0) | `'wanilia'` |
| `SMAKI[1]` | drugi element | `'czekolada'` |
| `SMAKI[1:]` | wszystko **od** drugiego do końca, czyli bez pierwszego | `['czekolada', 'pistacjowy']` |
| `["x"] * (len(SMAKI) - 1)` | o jeden mniej niż smaków | `['x', 'x']` |
| `date(2026, 9, 22)` | data, bez godziny | `2026-09-22` |
| `wynik[0]` | pierwszy problem na liście wyników | np. `'wanilia brak wpisu z: 2026-09-22'` |

**Nawias przy `len(...) - 1` jest obowiązkowy.** Bez niego Python najpierw mnoży listę, a potem
próbuje odjąć 1 od listy: `TypeError: unsupported operand type(s) for -: 'list' and 'int'`.

**Po co `len(SMAKI)` zamiast `3`:** gdy w `config` dojdzie czwarta spółka, tabela sama urośnie.
Z wpisanym `3` test padnie na zasadzie 8.

**Trzy rodzaje `assert`:**
- `assert wynik == []`: brak problemów;
- `assert len(wynik) == 2`: dokładnie 2 problemy;
- `assert SMAKI[0] in wynik[0]`: pierwszy problem wymienia wanilię.

---

## Część 3. Jak przewidzieć wynik: przejście przez trzy sprawdzenia

Funkcja **zawsze** robi wszystkie trzy, w tej kolejności:

| Nr | Sprawdzenie | Kiedy działa | Kiedy dopisuje problem |
|---|---|---|---|
| 1 | brak dzisiejszego wpisu | tylko pon–pt | spółka z listy nie ma w tabeli dzisiejszej daty |
| 2 | wpis z przyszłości | zawsze | któraś data jest późniejsza niż dziś |
| 3 | liczba dni | zawsze | spółki mają różną liczbę dni |

Problemy trafiają na listę w tej kolejności, więc `wynik[0]` pochodzi z najwcześniejszego
sprawdzenia, które coś znalazło.

**Pułapka:** brak dzisiejszego wpisu to też o jeden dzień mniej, więc włącza sprawdzenia 1 i 3.
Wpis z przyszłości to też o jeden dzień więcej, więc włącza sprawdzenia 2 i 3. Stąd w testach
1 i 3 oczekujemy 2 problemów, a nie 1.

Kalendarz: 18.09 piątek, 21.09 poniedziałek, 22.09 wtorek, 23.09 środa, 24.09 czwartek,
25.09 piątek, 26.09 sobota.

---

## Część 4. Sześć testów

Góra pliku z przykładu:
```python
import pandas as pd
from datetime import date
from lodziarnia import sprawdz_zeszyt
SMAKI = ["wanilia", "czekolada", "pistacjowy"]
```

### Test 1: wtorek, pierwszej spółki brak

```python
def test_brak_we_wtorek():
    zeszyt = pd.DataFrame({
        "spolka": SMAKI + SMAKI[1:],
        "data": ["2026-09-21 17:00:00"] * len(SMAKI) + ["2026-09-22 17:00:00"] * (len(SMAKI) - 1)})
    wynik = sprawdz_zeszyt(zeszyt, SMAKI, date(2026, 9, 22))
    assert len(wynik) == 2
    assert SMAKI[0] in wynik[0]
```
Tabela:
```
       spolka                 data
0     wanilia  2026-09-21 17:00:00
1   czekolada  2026-09-21 17:00:00
2  pistacjowy  2026-09-21 17:00:00
3   czekolada  2026-09-22 17:00:00
4  pistacjowy  2026-09-22 17:00:00
```
Przejście przez sprawdzenia:
- sprawdzenie 1: wtorek, wanilia nie ma 22.09, więc problem;
- sprawdzenie 2: nic po 22.09, więc brak problemu;
- sprawdzenie 3: liczby dni 1, 2, 2, więc problem.

Wynik:
```
['wanilia brak wpisu z: 2026-09-22', "Różna liczba dni między spółkami: {'czekolada': 2, 'pistacjowy': 2, 'wanilia': 1}"]
```

### Test 2: sobota, nikt nie ma wpisu

```python
def test_sobota():
    zeszyt = pd.DataFrame({
        "spolka": SMAKI * 2,
        "data": ["2026-09-24 17:00:00"] * len(SMAKI) + ["2026-09-25 17:00:00"] * len(SMAKI)})
    wynik = sprawdz_zeszyt(zeszyt, SMAKI, date(2026, 9, 26))
    assert wynik == []
```
Przejście przez sprawdzenia:
- sprawdzenie 1: sobota, więc nie działa;
- sprawdzenie 2: nic po 26.09;
- sprawdzenie 3: liczby dni 2, 2, 2.

Wynik: `[]`. Ten test pilnuje heurystyki pon–pt.

### Test 3: druga spółka ma wpis z jutra

```python
def test_przyszlosc():
    zeszyt = pd.DataFrame({
        "spolka": SMAKI * 2 + [SMAKI[1]],
        "data": ["2026-09-21 17:00:00"] * len(SMAKI) + ["2026-09-22 17:00:00"] * len(SMAKI) + ["2026-09-23 17:00:00"]})
    wynik = sprawdz_zeszyt(zeszyt, SMAKI, date(2026, 9, 22))
    assert len(wynik) == 2
    assert SMAKI[1] in wynik[0]
    assert "przyszłości" in wynik[0]
```
Przejście przez sprawdzenia:
- sprawdzenie 1: każdy ma 22.09, więc brak problemu;
- sprawdzenie 2: czekolada ma 23.09, więc problem;
- sprawdzenie 3: liczby dni 2, 3, 2, więc problem.

Wynik:
```
['czekolada: wpis z przyszłości: 2026-09-23, dziś jest: 2026-09-22', "Różna liczba dni między spółkami: {'czekolada': 3, 'pistacjowy': 2, 'wanilia': 2}"]
```
`[SMAKI[1]]` stoi w nawiasach kwadratowych, bo do listy można doklejać tylko listę (zasada `lista + lista`).
Słowo `"przyszłości"` musi być w **Twoim** komunikacie. Gdy go zmienisz, zmień też to słowo w teście.

### Test 4: pierwsza spółka ma dodatkowy stary dzień

```python
def test_rozna_liczba_dni():
    zeszyt = pd.DataFrame({
        "spolka": SMAKI * 2 + [SMAKI[0]],
        "data": ["2026-09-21 17:00:00"] * len(SMAKI) + ["2026-09-22 17:00:00"] * len(SMAKI) + ["2026-09-18 17:00:00"]})
    wynik = sprawdz_zeszyt(zeszyt, SMAKI, date(2026, 9, 22))
    assert len(wynik) == 1
    assert SMAKI[0] in wynik[0]
```
Przejście przez sprawdzenia:
- sprawdzenie 1: każdy ma 22.09;
- sprawdzenie 2: 18.09 to przeszłość;
- sprawdzenie 3: liczby dni 3, 2, 2, więc problem.

Wynik:
```
["Różna liczba dni między spółkami: {'czekolada': 2, 'pistacjowy': 2, 'wanilia': 3}"]
```
To jedyny test, w którym odzywa się samo sprawdzenie 3. Nazwa wanilii jest w słowniku z `.to_dict()`.

### Test 5: wtorek, komplet

```python
def test_komplet_wtorek():
    zeszyt = pd.DataFrame({
        "spolka": SMAKI * 2,
        "data": ["2026-09-21 17:00:00"] * len(SMAKI) + ["2026-09-22 17:00:00"] * len(SMAKI)})
    wynik = sprawdz_zeszyt(zeszyt, SMAKI, date(2026, 9, 22))
    assert wynik == []
```
Wynik: `[]`. To zwykły dobry dzień.

### Test 6: poniedziałek, komplet (po weekendzie)

```python
def test_komplet_poniedzialek():
    zeszyt = pd.DataFrame({
        "spolka": SMAKI * 2,
        "data": ["2026-09-18 17:00:00"] * len(SMAKI) + ["2026-09-21 17:00:00"] * len(SMAKI)})
    wynik = sprawdz_zeszyt(zeszyt, SMAKI, date(2026, 9, 21))
    assert wynik == []
```
Wynik: `[]`. Ten test pilnuje, że poniedziałek jest dniem giełdowym, a przerwa weekendowa nie jest problemem.

---

## Część 5. Przykład → projekt

| Lodziarnia | Projekt |
|---|---|
| `from lodziarnia import sprawdz_zeszyt` | `from <Twój plik bez .py> import sprawdz_daty` |
| `SMAKI = [...]` | nie tworzysz. Importujesz `from config import ticker` |
| `SMAKI` wszędzie w testach | `ticker` |
| `SMAKI[0]`, `SMAKI[1]`, `SMAKI[1:]` | `ticker[0]`, `ticker[1]`, `ticker[1:]` |
| `sprawdz_zeszyt(zeszyt, SMAKI, date(...))` | `sprawdz_daty(df, ticker, date(...))` |
| wanilia / czekolada | CBF.WA / XTB.WA (`ticker` to `["CBF.WA", "XTB.WA", "SNT.WA"]`) |

Nazwa zmiennej na tabelę (`zeszyt` czy `df`) jest dowolna.

---

## Część 6. Błędy, które możesz zobaczyć, i co znaczą

| Co widzisz | Przyczyna | Zasada |
|---|---|---|
| `collected 0 items` / `no tests ran` albo mniej testów niż napisałeś | test bez `test_` na początku nazwy | 1 |
| `ERROR … fixture 'df' not found` | funkcja sprawdzająca ma `test_` w nazwie | 2 |
| `AttributeError: 'str' object has no attribute 'weekday'` | dzisiejsza data jako napis zamiast `date(...)` | 6 |
| `ValueError: All arrays must be of the same length` | kolumny mają różną liczbę elementów | 8 |
| `TypeError: unsupported operand type(s) for -: 'list' and 'int'` | brak nawiasu przy `len(...) - 1` | Część 2 |
| `assert 0 == 2` / `assert 1 == 2` | dane nie zawierają usterki albo nie policzyłeś wszystkich sprawdzeń | 9 |
| `KeyError: 'spolka'` albo `'data'` | literówka w nazwie kolumny | 4 |
| `ModuleNotFoundError` | zła nazwa pliku po `from` | Część 5 |

---

## Część 7. Uruchomienie

1. **[lokalny PowerShell, venv nieistotne]** `cd "C:\Users\gracj\OneDrive\Dokumenty\DE\GPW - pulse"`.
   Wiersz ma się kończyć na `GPW - pulse>`.
2. **[lokalny PowerShell]** `.\.venv\Scripts\Activate.ps1`. Na początku wiersza ma się pojawić `(.venv)`.
3. **[lokalny PowerShell, (.venv) włączone]** `pytest kod/<Twój plik testów>.py -v`.
   Sukces: `6 passed`. Porażka: `FAILED` albo `ERROR` przy nazwie testu. Wtedy szukasz komunikatu w Części 6.
4. **Opcjonalnie:** dopisz `-s`, jeśli w testach masz `print(...)` i chcesz zobaczyć tabelę albo wynik.

**Przewidywanie:** z funkcją w wersji, którą przysłałeś (trzy sprawdzenia po poprawkach) i sześcioma
testami zgodnymi z tą notatką: `6 passed`. Przykład z lodziarni, z tym samym kodem funkcji, dał dokładnie to.

**Wynik 23.09:** `kod/test_path.py`, `6 passed`, zgodnie z przewidywaniem.

---

## Część 8. Warstwa łącząca się z Athena (część `__main__` w `kod/path.py`)

Funkcja i testy są gotowe. Brakuje kawałka, który bierze **prawdziwą** tabelę z Atheny, woła
funkcję i wypisuje wynik. Wszystko, czego potrzebujesz, jest poniżej.

### Zasady

1. **Wszystko, co łączy się z Atheną, stoi w środku `if __name__ == "__main__":`**, na samym dole
   pliku. Tylko wtedy `pytest` (który importuje `path.py`) nie łączy się z Atheną. `silver.py` łączy
   się od razu przy imporcie, więc tu **nie** kopiujesz jego układu, tylko same linie połączenia.
2. **Importy na górze pliku:** `from config import ticker, WYNIKI_ATHENY, REGION, BAZA` (dopisujesz
   trzy nazwy do istniejącej linii 3) i `from pyathena import connect`. Import niczego jeszcze nie łączy.
3. **Połączenie:** te same trzy parametry co w `silver.py`, linie 6–10: `s3_staging_dir=WYNIKI_ATHENY`,
   `region_name=REGION`, `schema_name=BAZA`.
4. **Zapytanie:** `SELECT spolka, data FROM gold_dane_dzienne`, przez `pd.read_sql(zapytanie, con)`,
   jak w `silver.py`, linia 11.
5. **Dzisiejsza data:** `date.today()` (zegar laptopa). Uruchamiać po 18:10 czasu polskiego, bo
   wcześniej danych z dziś jeszcze nie ma (to nie usterka, tylko za wcześnie).
6. **Wypisz liczbę wierszy** (`len(df)`), zanim zawołasz funkcję. To liczba do porównania
   z przewidywaniem (3 × liczba dni na spółkę).
7. **Jedna linia wyniku ze stałym początkiem**, np. `Droga: OK` albo `Droga: PROBLEM - …`. Słowa
   wybierasz sam. Listę problemów sklejasz w jeden napis przez `"; ".join(wynik)`, jak w `control.py`,
   linia 43.
8. **Po dopisaniu `__main__` uruchom jeszcze raz testy.** Nadal `6 passed` i nadal szybko (poniżej
   sekundy) oznacza, że testy nie łączą się z Atheną.

### Przykład na lodziarni (uruchomiony 23.09)

Zamiast Atheny: plik `zeszyt.csv`. W projekcie w tym miejscu jest `connect(...)` i `pd.read_sql(...)`.

```python
if __name__ == "__main__":
    SMAKI = ["wanilia", "czekolada", "pistacjowy"]
    zeszyt = pd.read_csv("zeszyt.csv")
    print(len(zeszyt))
    wynik = sprawdz_zeszyt(zeszyt, SMAKI, date(2026, 9, 23))
    if wynik:
        print("Zeszyt: PROBLEM - " + "; ".join(wynik))
    else:
        print("Zeszyt: OK")
```

Zeszyt z kompletem (każdy smak 22 i 23.09), wyjście:
```
6
Zeszyt: OK
```
Zeszyt bez ostatniego wiersza (pistacjowy bez 23.09), wyjście:
```
5
Zeszyt: PROBLEM - pistacjowy brak wpisu z: 2026-09-23; Różna liczba dni między spółkami: {'czekolada': 2, 'pistacjowy': 1, 'wanilia': 2}
```
Po skasowaniu `zeszyt.csv` testy dalej dają `6 passed`. To dowód, że `pytest` nie wchodzi do `__main__`.
Gdyby wchodził, padłby na braku pliku.

`if wynik:` oznacza „jeśli lista nie jest pusta". Pusta lista `[]` liczy się jak `False`.

### Przykład → projekt

| Lodziarnia | Projekt |
|---|---|
| `SMAKI = [...]` w `__main__` | nic, `ticker` jest już zaimportowany z `config` |
| `pd.read_csv("zeszyt.csv")` | `con = connect(...)` i `pd.read_sql("SELECT spolka, data FROM gold_dane_dzienne", con)` |
| `date(2026, 9, 23)` | `date.today()` |
| `Zeszyt: OK` | Twoje słowa, np. `Droga: OK` |

### Błędy, które możesz zobaczyć

| Co widzisz | Przyczyna |
|---|---|
| `NameError: name 'connect' is not defined` | brak `from pyathena import connect` |
| `NameError: name 'WYNIKI_ATHENY' is not defined` | nie dopisałeś nazw do importu z `config` |
| `TABLE_NOT_FOUND` / `does not exist` | literówka w nazwie tabeli |
| `COLUMN_NOT_FOUND` | literówka w nazwie kolumny w `SELECT` |
| `UserWarning: pandas only supports SQLAlchemy…` | ostrzeżenie, nie błąd. Znana sprawa z listy (`pd.read_sql` przez SQLAlchemy). Na laptopie tego nie sprawdziłem |
| testy nagle trwają kilka sekund albo pytają AWS | połączenie stoi poza `if __name__ == "__main__":` |

### Uruchomienie

1. **[lokalny PowerShell, (.venv) włączone]** `pytest kod/test_path.py -v`: `6 passed`, jak wcześniej.
2. **[lokalny PowerShell, (.venv) włączone]** `python kod/path.py`.

**Przewidywanie na 23.09 wieczorem**, pod warunkiem że dzisiejszy bieg o 18:00/18:10 na EC2 się udał
(dziś jeszcze tego nie sprawdzaliśmy): liczba wierszy **2334** (3 × 778), potem linia „OK" bez problemów.
Każdy inny wynik to informacja o prawdziwych danych, nie o kodzie. Wtedy wklej całość i niczego nie poprawiaj.

**Wynik 23.09 ok. 19:20:** `2334`, `Dane: OK`, zgodnie z przewidywaniem.

---

## Część 9. Udawany dzień przez zmienną środowiskową (test alarmu na żywych danych)

Decyzja z 23.09: data jak w `control.py` (`KONTROLA_DATA`). Jest zmienna, więc skrypt bierze datę
z niej. Nie ma zmiennej, więc bierze `date.today()`. Dane zostają prawdziwe, udajemy tylko dzień.

### Zasady

1. **Na górze pliku `import os`**, bo `os.environ.get` jest w module `os`.
2. **Nazwa zmiennej należy do Ciebie.** Proponuję `DROGA_DATA`.
3. **Zmienna zawsze jest tekstem**, a funkcja potrzebuje daty. Dlatego tekst trzeba zamienić:
   `date.fromisoformat(tekst)`.
4. **Zapasowa wartość to `str(date.today())`**, czyli dzisiejsza data jako tekst. Wtedy obie drogi
   przechodzą przez `fromisoformat` tak samo. Ten sam układ masz w `control.py`, linia 36.
5. **Format tekstu: `RRRR-MM-DD`**, np. `2026-09-24`. Inny format da `ValueError`.
6. **Zmienna ustawiona w PowerShellu zostaje w tym oknie**, aż ją usuniesz (`Remove-Item Env:DROGA_DATA`)
   albo zamkniesz okno. Po teście ją usuń, żeby następny bieg nie udawał dnia.

### Nowe pojęcie: `date.fromisoformat` (uruchomione 23.09)

```python
print(repr(date.fromisoformat("2026-09-24")))
print(date.fromisoformat("2026-09-24").weekday())
date.fromisoformat("24.09.2026")
```
```
datetime.date(2026, 9, 24)
3
ValueError: Invalid isoformat string: '24.09.2026'
```
`repr(...)` pokazuje, czym wartość jest naprawdę: `datetime.date(...)` to data, nie napis. `3` to czwartek.

### Przykład na lodziarni (uruchomiony 23.09)

```python
print(repr(os.environ.get("LODY_DATA", str(date.today()))))
os.environ["LODY_DATA"] = "2026-09-26"
print(repr(os.environ.get("LODY_DATA", str(date.today()))))
print(date.fromisoformat(os.environ.get("LODY_DATA", str(date.today()))))
```
```
'2026-09-23'
'2026-09-26'
2026-09-26
```
Bez zmiennej dostajemy dzisiejszą datę jako tekst. Ze zmienną dostajemy tekst ze zmiennej. `fromisoformat`
zamienia jedno i drugie na datę. (W przykładzie zmienna ustawiona jest z Pythona. U Ciebie ustawiasz ją
w PowerShellu przez `$env:`.)

### Przykład → projekt

| Lodziarnia | Projekt |
|---|---|
| `LODY_DATA` | `DROGA_DATA` (albo Twoja nazwa) |
| `date(2026, 9, 23)` w wywołaniu | `date.fromisoformat(os.environ.get(...))` w miejscu `date.today()` w linii 29 |

### Trzy biegi i przewidywania (dane z 23.09 w Athenie: 2334 wiersze, 778 na spółkę)

| Zmienna | Dzień | Przewidywanie |
|---|---|---|
| `2026-09-24` | czwartek, jutro | `2334`, potem `Dane: Problem -` i 3 × `brak wpisu z: 2026-09-24` (CBF.WA, XTB.WA, SNT.WA w tej kolejności, bo tak idzie `ticker`) |
| `2026-09-22` | wtorek, wczoraj | `2334`, potem `Dane: Problem -` i 3 × `wpis z przyszłości: 2026-09-23, dziś jest: 2026-09-22`. Kolejności spółek nie przewiduję, bo zależy od kolejności wierszy z Atheny |
| brak (usunięta) | dziś | `2334`, `Dane: OK` |

W żadnym biegu nie ma `Różna liczba dni`, bo wszystkie spółki mają po 778 dni.

**Wynik 23.09 wieczorem: trzy biegi, trzy trafienia co do słowa.** A: `2334` i trzy braki
z 24.09 w kolejności CBF.WA, XTB.WA, SNT.WA. B: `2334` i trzy wpisy z przyszłości (Athena oddała
kolejność CBF.WA, SNT.WA, XTB.WA). C: `2334`, `Dane: OK`. Przed każdym wynikiem dwie linie
`UserWarning` o SQLAlchemy (`kod/path.py:28`, `pd.read_sql`). To znana sprawa z listy, nie błąd.
