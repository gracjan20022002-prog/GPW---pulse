# Notatka 27.10: testy `wczytaj_poprzednie` i `zapisz_js` — nad czym pracujemy i co piszemy

Instrukcja do propozycji z 26.10 („testy `wczytaj_poprzednie` i `zapisz_js` w pytest, `tmp_path`”),
wybranej przez Gracjana 27.10. Kształt jak w notatce z 24.10. Wszystkie wyniki niżej pochodzą
z uruchomienia 27.10 (laptop, `.venv`, Python 3.14.2, pytest 9.1.1) w katalogu roboczym Claude'a:
przykład pogody i kopia folderu `kod/` z dopisanymi testami. Twoich plików nie ruszałem; prawdziwy
`strona/dane.js` po wszystkich biegach ten sam (27 931 B, z 26.10, 18:32).

---

## 1. Nad czym pracujemy

**Co jest dziś.** `kod/data_stream.py` ma cztery funkcje. Dwie z nich (`sprawdz_pliki`, `zbuduj_dane`)
mają 10 testów. Dwie pozostałe nie mają żadnego:
- `wczytaj_poprzednie` (linie 54–60) — ile sesji miał poprzedni `dane.js`; brak pliku → `0`;
- `zapisz_js` (linie 61–63) — zapisuje `window.DANE = {…};` do pliku.

Sprawdził je dotąd tylko prawdziwy bieg 26.10: pierwszy dał `poprzednio 0`, drugi `poprzednio 800`.

**Dlaczego te dwie są ważne.**
- `wczytaj_poprzednie` daje liczbę do sprawdzenia „Mniej sesji niż poprzednio” — to ochrona przed
  plikiem z połową tabeli. Jeśli funkcja po cichu odda `0` zamiast `801`, ochrona przestaje działać,
  a skrypt dalej kończy się dobrze.
- `zapisz_js` pisze jedyny plik, który czyta strona. Jeden zły znak (brak `;`, inny początek, dopisanie
  zamiast nadpisania) i strona nie dostaje danych.

**Dlaczego dotąd nie było testu.** Obie funkcje pracują na pliku na dysku. Test, który pisze do
prawdziwego `strona/dane.js`, nadpisałby dane strony. Rozwiązanie: **`tmp_path`** — pytest daje
każdemu testowi świeży, pusty folder poza projektem (`AppData\Local\Temp\pytest-of-gracj\…`).
Test zapisuje tam, czyta stamtąd, a projekt zostaje nietknięty.

**Co powstaje.** 5 testów na końcu `kod/test_data_stream.py` i 3 zmiany na górze tego pliku.
Kod `data_stream.py` **bez zmian**. Wynik: `pytest kod/test_data_stream.py -v` → `15 passed`
(dziś 10), `pytest kod/ -v` → **`53 passed`** (dziś 48) — sprawdzone na kopii.

---

## 2. Dwie decyzje przed kodem

- **T1 — jak zbudować ścieżkę do pliku w folderze testu.** (a) `os.path.join(tmp_path, "dane.js")` —
  rekomendacja: znane, to samo co w części głównej skryptu (linie 65, 74); (b) `tmp_path / "dane.js"` —
  krótsze, ale nowe pojęcie (`tmp_path` to obiekt ścieżki z modułu `pathlib`, w którym `/` skleja
  folder z nazwą pliku). Obie drogi działają z obiema funkcjami (sprawdzone 27.10).
- **T2 — test zepsutego pliku z `pytest.raises`.** (a) tak, 5 testów — rekomendacja: to jedyny test,
  który pokazuje, że zepsuty `dane.js` daje **głośny** błąd, a nie ciche `poprzednio 0` (zasada 9,
  warunek c); kosztuje jedno nowe pojęcie; (b) nie, 4 testy, bez nowego pojęcia.

Niżej wszystko w wariancie (a) obu decyzji.

---

## 3. Co zmienia się w kodzie

### `kod/test_data_stream.py` — dziś 63 linie i 10 testów, potem 89 linii i 15 testów

**Na górze pliku (3 zmiany):**
- nowa linia `import json` — potrzebna tylko do nazwy błędu `json.JSONDecodeError` w teście 5;
- nowa linia `import os` — do `os.path.join`;
- linia `from data_stream import sprawdz_pliki, zbuduj_dane` — dopisane dwie nazwy:
  `wczytaj_poprzednie` i `zapisz_js`.

**Na końcu pliku 5 testów.** Każdy ma `tmp_path` w nawiasie, a jego pierwsza linia to
`sciezka = os.path.join(tmp_path, "dane.js")`. Pliku jeszcze nie ma — powstaje dopiero przy zapisie.

| # | Test | Co robi | Co ma wyjść | Jaką pomyłkę łapie (sprawdzone na kopii) |
|---|---|---|---|---|
| 1 | `test_wczytaj_brak_pliku(tmp_path)` | nic nie zapisuje, woła `wczytaj_poprzednie(sciezka)` | `0` | zły wynik przy braku pliku (np. `return 1`) |
| 2 | `test_zapisz_js_tresc(tmp_path)` | `zapisz_js({"daty": ["2026-10-22", "2026-10-23"]}, sciezka)`, potem czyta plik przez `with open(sciezka, encoding="utf-8")` i `read()` | cały tekst równy `'window.DANE = {"daty": ["2026-10-22", "2026-10-23"]};'` | brak `;`, zmieniony `POCZATEK`, `\n` na końcu |
| 3 | `test_zapisz_i_wczytaj(dzienne, ranking, tmp_path)` | zapisuje wynik `zbuduj_dane(dzienne, ranking, ticker)` (Twoje fixture, jak w `test_zbuduj_dane`), potem `wczytaj_poprzednie(sciezka)` | `2` | odczyt bez `removesuffix`; `len(dane)` zamiast `len(dane["daty"])` (słownik ma 3 klucze → `assert 3 == 2`) |
| 4 | `test_zapisz_nadpisuje(tmp_path)` | zapisuje 3 daty, potem 1 datę **w ten sam plik**, potem `wczytaj_poprzednie` | `1` | tryb `"a"` zamiast `"w"` (w pliku byłyby dwa `window.DANE = …;` → `JSONDecodeError`) |
| 5 | `test_zepsuty_plik(tmp_path)` | sam pisze do pliku obcięty tekst `'window.DANE = {"daty": ["2026-10-22"'` (jak plik przerwany w połowie zapisu), potem `with pytest.raises(json.JSONDecodeError):` i **wcięte pod nim** `wczytaj_poprzednie(sciezka)` | test przechodzi, bo funkcja rzuca błąd | `try/except` w `wczytaj_poprzednie`, który zamieniłby zepsuty plik na ciche `0` |

**Celowe pomyłki w kopii `data_stream.py`, po jednej naraz, `pytest kod/` (uruchomione 27.10):**

| Pomyłka | Wynik | Który test |
|---|---|---|
| `return 1` przy braku pliku | `1 failed, 52 passed` | 1 |
| zapis bez `+ KONIEC` | `1 failed, 52 passed` | 2 |
| `POCZATEK = "window.DANE="` (bez spacji) | `1 failed, 52 passed` | 2 |
| `+ "\n"` na końcu zapisu | `3 failed, 50 passed` | 2, 3, 4 |
| odczyt bez `.removesuffix(KONIEC)` | `2 failed, 51 passed` | 3, 4 |
| `return len(dane)` | `1 failed, 52 passed` | 3 |
| `"a"` zamiast `"w"` | `1 failed, 52 passed` | 4 |
| `try/except json.JSONDecodeError` → `return 0` | `1 failed, 52 passed` | 5 (`DID NOT RAISE`) |
| bez pomyłki | **`53 passed`** | — |

---

## 4. Przykład na innych danych: stacja pogodowa

Ta sama para funkcji co w notatce z 24.10 (`pogoda_strona.py`), tylko z `window.POGODA = `.

`pogoda_strona.py`:
```python
import json
import os
POCZATEK = "window.POGODA = "
KONIEC = ";"
def wczytaj_poprzednie(sciezka):
    if not os.path.exists(sciezka):
        return 0
    with open(sciezka, encoding="utf-8") as plik:
        tekst = plik.read()
    dane = json.loads(tekst.removeprefix(POCZATEK).removesuffix(KONIEC))
    return len(dane["daty"])
def zapisz_js(dane, sciezka):
    with open(sciezka, "w", encoding="utf-8") as plik:
        plik.write(POCZATEK + json.dumps(dane, ensure_ascii=False) + KONIEC)
```

`test_pogoda_strona.py` (pierwszy test tylko pokazuje, gdzie jest `tmp_path` — w projekcie go nie ma):
```python
import json
import os
import pytest
from pogoda_strona import wczytaj_poprzednie, zapisz_js
def test_gdzie_jest_tmp_path(tmp_path):
    print("tmp_path =", tmp_path)
    print("plik =", os.path.join(tmp_path, "pogoda.js"))
    print("w środku:", os.listdir(tmp_path))
def test_brak_pliku(tmp_path):
    sciezka = os.path.join(tmp_path, "pogoda.js")
    assert wczytaj_poprzednie(sciezka) == 0
def test_tresc_pliku(tmp_path):
    sciezka = os.path.join(tmp_path, "pogoda.js")
    zapisz_js({"daty": ["2026-10-20", "2026-10-21"]}, sciezka)
    with open(sciezka, encoding="utf-8") as plik:
        tekst = plik.read()
    assert tekst == 'window.POGODA = {"daty": ["2026-10-20", "2026-10-21"]};'
def test_zapisz_i_wczytaj(tmp_path):
    sciezka = os.path.join(tmp_path, "pogoda.js")
    zapisz_js({"daty": ["2026-10-20", "2026-10-21", "2026-10-22"]}, sciezka)
    assert wczytaj_poprzednie(sciezka) == 3
def test_nadpisuje(tmp_path):
    sciezka = os.path.join(tmp_path, "pogoda.js")
    zapisz_js({"daty": ["2026-10-20", "2026-10-21", "2026-10-22"]}, sciezka)
    zapisz_js({"daty": ["2026-10-20"]}, sciezka)
    assert wczytaj_poprzednie(sciezka) == 1
def test_zepsuty_plik(tmp_path):
    sciezka = os.path.join(tmp_path, "pogoda.js")
    with open(sciezka, "w", encoding="utf-8") as plik:
        plik.write('window.POGODA = {"daty": ["2026-10-20"')
    with pytest.raises(json.JSONDecodeError):
        wczytaj_poprzednie(sciezka)
```

**Wynik `pytest test_pogoda_strona.py -v -s`** (`-s` pokazuje `print` z testów):
```
test_pogoda_strona.py::test_gdzie_jest_tmp_path tmp_path = C:\Users\gracj\AppData\Local\Temp\pytest-of-gracj\pytest-0\test_gdzie_jest_tmp_path0
plik = C:\Users\gracj\AppData\Local\Temp\pytest-of-gracj\pytest-0\test_gdzie_jest_tmp_path0\pogoda.js
w środku: []
PASSED
test_pogoda_strona.py::test_brak_pliku PASSED
test_pogoda_strona.py::test_tresc_pliku PASSED
test_pogoda_strona.py::test_zapisz_i_wczytaj PASSED
test_pogoda_strona.py::test_nadpisuje PASSED
test_pogoda_strona.py::test_zepsuty_plik PASSED
============================== 6 passed in 0.06s ==============================
```

Po biegu w `pytest-0` jest 6 folderów, po jednym na test (`test_brak_pliku0`, `test_tresc_pliku0`, …).
W `test_tresc_pliku0\pogoda.js` leży `window.POGODA = {"daty": ["2026-10-20", "2026-10-21"]};`.
Każdy bieg pytest dostaje nowy numer (`pytest-1`, `pytest-2`, …); zostają trzy ostatnie — po
kilkunastu biegach 27.10 były tylko `pytest-17`, `pytest-18`, `pytest-19`.

**Celowe pomyłki w `pogoda_strona.py`, po jednej naraz (uruchomione 27.10):**

| Pomyłka | Wynik | Który test i dlaczego |
|---|---|---|
| `"a"` zamiast `"w"` w `zapisz_js` | `1 failed, 5 passed` | `test_nadpisuje`: `JSONDecodeError` — w pliku dwa `window.POGODA = …;` |
| zapis bez `+ KONIEC` | `1 failed, 5 passed` | `test_tresc_pliku`; odczyt dalej działa, bo `removesuffix` przy braku `;` nic nie robi |
| `return 1` przy braku pliku | `1 failed, 5 passed` | `test_brak_pliku`: `assert 1 == 0` |
| odczyt bez `.removesuffix(KONIEC)` | `2 failed, 4 passed` | `test_zapisz_i_wczytaj`, `test_nadpisuje`: `Extra data` — `;` za JSON-em |
| `POCZATEK = "window.POGODA="` (bez spacji) | `1 failed, 5 passed` | `test_tresc_pliku`; odczyt dalej działa, bo zapis i odczyt biorą tę samą stałą |
| `+ "\n"` na końcu zapisu | `3 failed, 3 passed` | `test_tresc_pliku`, `test_zapisz_i_wczytaj`, `test_nadpisuje`: plik kończy się `\n`, więc `removesuffix(";")` nic nie odcina |
| `return len(dane)` | `1 failed, 5 passed` | `test_zapisz_i_wczytaj`: `assert 1 == 3`; `test_nadpisuje` przechodzi **przypadkiem** (1 klucz, 1 data) |
| `try/except json.JSONDecodeError` → `return 0` | `1 failed, 5 passed` | `test_zepsuty_plik`: `Failed: DID NOT RAISE JSONDecodeError` |
| `ensure_ascii=True` | `6 passed` | żaden — w danych nie ma polskich liter; w `dane.js` też ich nie ma, więc bez skutku |

**Przykład → projekt:**

| Przykład | Projekt |
|---|---|
| `pogoda_strona.py`, `test_pogoda_strona.py` | `kod/data_stream.py`, `kod/test_data_stream.py` |
| `window.POGODA = ` | `window.DANE = ` (stała `POCZATEK`, linia 9) |
| `pogoda.js` w `tmp_path` | `dane.js` w `tmp_path` (nigdy `strona/dane.js`) |
| `test_brak_pliku`, `test_tresc_pliku` | `test_wczytaj_brak_pliku`, `test_zapisz_js_tresc` |
| `test_zapisz_i_wczytaj` na ręcznym słowniku (3 daty) | ten sam test na `zbuduj_dane(dzienne, ranking, ticker)` (2 daty) — łapie też `len(dane)` |
| `test_nadpisuje` | `test_zapisz_nadpisuje` |
| daty 20–22.10 | daty 21–23.10 (jak w Twoich fixture) |
| `test_gdzie_jest_tmp_path` | brak — tylko do pokazania |

---

## 5. Nowe pojęcia (wejście → wyjście)

Znane już i użyte znowu: `with open(..., encoding="utf-8")`, `read()`, `os.path.join`, `assert`,
własne fixture (`dzienne`, `ranking`), `json` (`dumps`, `loads`).

- **`tmp_path`:** wbudowana fixture pytest — wystarczy dopisać ją w nawiasie testu. Każdy test dostaje
  osobny, pusty folder. `os.listdir(tmp_path)` na początku testu → `[]`; ścieżka np.
  `C:\Users\gracj\AppData\Local\Temp\pytest-of-gracj\pytest-0\test_brak_pliku0`. pytest trzyma
  foldery z trzech ostatnich biegów, starsze kasuje sam.
- **`pytest.raises(Błąd)`:** `with pytest.raises(json.JSONDecodeError):` i wcięte pod spodem
  wywołanie. Test przechodzi, **gdy** kod pod spodem rzuci ten błąd; gdy nie rzuci →
  `Failed: DID NOT RAISE JSONDecodeError`.
- **`json.JSONDecodeError`:** błąd `json.loads` przy tekście, który nie jest poprawnym JSON-em.
  `json.loads('{"daty": ["2026-10-20"')` → `Expecting ',' delimiter: line 1 column 23 (char 22)`;
  `json.loads('{"daty": ["2026-10-20"]};')` → `Extra data: line 1 column 25 (char 24)`.
- **Tryb `"a"` w `open` (tylko w pułapkach):** dopisuje na końcu pliku; `"w"` kasuje stary tekst
  i pisze od nowa. Dwa zapisy z `"a"` → `window.DANE = {…};window.DANE = {…};`.
- **Test w obie strony (zapis → odczyt):** zapisuję funkcją A, czytam funkcją B i sprawdzam liczbę.
  Łapie rozjazd między zapisem a odczytem, ale nie złapie błędu, który obie strony robią tak samo
  (np. `POCZATEK` bez spacji) — dlatego osobno test 2 z całym tekstem.

---

## 6. Na co uważać

Wyniki w nawiasach z `pytest kod/test_data_stream.py` na kopii (15 testów), uruchomione 27.10.

- **Nigdy prawdziwa ścieżka w teście** (`BASE_DIR`, `strona/dane.js`) — test nadpisałby dane strony.
  Każdy z 5 testów bierze `tmp_path`.
- **Plik testów kończy się bez znaku nowej linii** po linii 63 (sprawdzone 27.10). Dopisywanie zacznij
  od Enter na końcu ostatniej linii, inaczej nowe `def` skleja się z `assert` (`SyntaxError`, na kopii
  to się zdarzyło przy dopisywaniu skryptem).
- **Tekst w `assert` testu 2 w apostrofach `'…'`**, bo w środku są cudzysłowy `"`. Spacje dokładnie
  jak z `json.dumps`: po `:` i po `,`, ani jednej więcej.
- **Test 3 bez `dzienne, ranking` w nawiasie** → `AttributeError: 'FixtureFunctionDefinition' object has
  no attribute 'pivot'` (`1 failed, 14 passed`) — bez nawiasu `dzienne` to sama funkcja, nie tabela.
- **Test 5: wywołanie przed `with`, a nie pod nim** → błąd poleciał poza `pytest.raises`:
  `json.decoder.JSONDecodeError: Expecting ',' delimiter…` (`1 failed, 14 passed`).
- **Test 5: wywołanie pod `with` bez wcięcia** → `IndentationError: expected an indented block after
  'with' statement` — cały plik się nie wczytuje, żaden z 15 testów się nie uruchamia.
- **Brak `import json`** → `NameError: name 'json' is not defined` tylko w teście 5 (`1 failed, 14 passed`).

---

## 7. Kolejność pracy

1. **Decyzje T1 i T2.**
2. **Porcja 1:** trzy zmiany na górze pliku + testy 1 i 2 → `pytest kod/test_data_stream.py -v` →
   `12 passed`.
3. **Porcja 2:** testy 3, 4 i 5 → `15 passed`; potem `pytest kod/ -v` → `53 passed`.
4. Sprawdzenie, że prawdziwy `strona/dane.js` nietknięty: 27 931 B, data 26.10 18:32.

Kroki dostaniesz osobno, z numerem linii, wcięciem i tym, co ma wyjść. Po każdej zmianie czytam
`git diff` i opisuję każdą nową linię.

## 8. Zmiany w trakcie pisania (27.10, tego notatka wcześniej nie miała)

- **Fixture `sciezka` zamiast `os.path.join` w każdym teście** (pomysł Gracjana): w liniach 22–24, obok
  `dzienne` i `ranking`:
  `@pytest.fixture` / `def sciezka(tmp_path):` / `return os.path.join(tmp_path, "dane.js")`. Testy biorą
  `sciezka` zamiast `tmp_path` i nie mają linii `sciezka = …`. Plik ma **87 linii** (nie 89); wynik ten
  sam, `53 passed` (sprawdzone na kopii, potem u Gracjana).
- **Nazwy testów Gracjana:** `test_zapisz_js` (tu: `test_zapisz_js_tresc`) i `test_zapisz_i_nadpisz`
  (tu: `test_zapisz_nadpisuje`). Działają tak samo.
- **Tabela w części 3 okazała się dla Gracjana niezrozumiała** („kolejny raz ta tabelka nic mi nie
  mówi”). Wytłumaczenie testów linia po linii, z wartościami z uruchomienia, poszło w rozmowie po
  napisaniu testów; zasada na przyszłość w CLAUDE.md (zasada 3, 27.10).
- **Wynik u Gracjana:** `pytest kod/test_data_stream.py -v` → `15 passed`, `pytest kod/ -v` → `53 passed`;
  prawdziwy `strona/dane.js` nietknięty.

## Powiązane notatki

- [[Notatka-2026-10-24-jak-napisac-strona-dane]] — instrukcja skryptu danych strony (część 8: brak tych testów)
- [[Notatka-2026-10-26-data-stream-porcja-3]] — część główna linia po linii
