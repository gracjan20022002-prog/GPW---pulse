# Notatka 24.10: skrypt `kod/strona_dane.py` — nad czym pracujemy i co piszemy

Instrukcja do [[Notatka-2026-10-23-dane-na-strone]] (zatwierdzona 23.10, D1–D6 wariant a). Kształt jak
w notatce z 13.10: najpierw nad czym pracujemy, potem co powstaje w kodzie i co robi każda funkcja,
potem przykład na innych danych. Wyniki przykładu pochodzą z uruchomienia 24.10 (laptop, Python 3.14.2,
pandas 3.0.5). Nowe pojęcia sprawdzone ze słownikiem. Twoich plików nie ruszałem.

---

## 1. Nad czym pracujemy

**Jak dziś strona dostaje dane.** Wcale — szkic strony ma daty i ceny wpisane na sztywno w swoim kodzie
(sesje do 20.10, część cen przepisana z wcześniejszego szkicu). Ranking i „najbardziej zmienny miesiąc”
też są wpisane ręcznie, z lokalnego pliku Golda z 20.09.

**Co budujemy.** Most między drogą danych a stroną. Gold codziennie o 18:10 wysyła do S3 dwa pliki:
`gold/dane_dzienne/dane_dzienne.csv` (2400 wierszy: data, cena, spółka, zmiana, miesiąc) i
`gold/ranking/ranking.csv` (3 wiersze). Twój skrypt na laptopie:
1. pobiera oba pliki z S3 do `strona/pobrane/`;
2. sprawdza je — gdy coś się nie zgadza, kończy się komunikatem i **nie rusza** starego `dane.js`;
3. obraca długą tabelę w listy cen ułożone według dat;
4. zapisuje jeden plik `strona/dane.js`, który strona (piszę ją ja) tylko czyta.

**Dlaczego sprawdzenia przed zapisem.** Strona pokaże wszystko, co dostanie. Plik z S3 może być
niepełny (Athena oddała pół tabeli, Silver padł w połowie), może być z dwóch różnych biegów (pobrany
w chwili, gdy Gold wysyła), może brakować spółki. Lepiej stara strona niż zła.

**Czego skrypt nie robi.** Nie sprawdza, czy cena jest prawdziwa (to robi porównanie z archiwum GPW).
Nie publikuje strony w internecie — to drugi etap z osobną notatką. Nie chodzi w `cron` — uruchamiasz
go ręcznie po 18:15.

**Wynik.** Plik `strona/dane.js` w jednej linii, kształt (skrócone):
```
window.DANE = {"daty": ["2023-08-14", …, "2026-10-23"], "ceny": {"CBF": [75.6, …, 192.0], "XTB": […], "SNT": […]}, "ranking": [{"spolka": "SNT", "miesiac": "RRRR-MM", "zmiana": 372.03}, …], "wygenerowano": "2026-10-24 18:40"};
```
i na ekranie jedna linia:
```
Strona: 800 sesji (2023-08-14 – 2026-10-23), poprzednio 0, ostatnie: CBF 192.0, XTB 137.0, SNT 334.2
```

---

## 2. Dwie decyzje przed kodem

- **D1 — gdzie zapisać pobrane pliki.** (a) `strona/pobrane/`, poza gitem — rekomendacja: osobne
  miejsce, nic nie miesza się z lokalnym Goldem; (b) lokalny `gold/` — nadpisze pliki z 20.09, a przy
  powrocie Harmonogramu Windows lokalny Gold i pobieranie pisałyby w to samo miejsce.
- **D2 — czy sprawdzać, że oba pliki są z tego samego biegu.** (a) tak: ostatnia cena każdej spółki
  w danych dziennych musi się równać kolumnie `ostatnia_cena` w rankingu — rekomendacja: łapie
  pobranie w chwili wysyłki Golda i ranking, który nie doszedł; kosztuje jedną pętlę; (b) nie, wystarczy
  zasada „nie uruchamiać przed 18:15”.

---

## 3. Co powstaje w kodzie

### `kod/strona_dane.py` — nowy plik

Układ jak `kod/path.py`: na górze importy i stałe, potem funkcje bez sieci (da się je testować),
na końcu `if __name__ == "__main__":` z pobraniem z S3.

**Stałe:** `BASE_DIR` (jak w każdym skrypcie), `POCZATEK = "window.DANE = "`, `KONIEC = ";"`.
Ten sam tekst służy do zapisu i do odczytu `dane.js` — dlatego stała, nie dwa razy wpisany napis.

**`sprawdz_pliki(dzienne, ranking, spolki, dzis, poprzednie)`** — jak `sprawdz_daty` w `path.py`:
zbiera problemy na listę i ją zwraca; pusta lista = wszystko dobrze. Bez `print` i bez plików.
- **Dostaje:** tabelę dzienną z dodaną kolumną `dzien` (`"RRRR-MM-DD"`), tabelę rankingu, listę `ticker`,
  dzisiejszą datę jako tekst i liczbę sesji z poprzedniego `dane.js` (0, gdy go nie ma).
- **Sprawdza po kolei:**
  1. zbiór spółek w danych dziennych = zbiór `ticker`; to samo w rankingu — przy błędzie **od razu
     zwraca** listę (dalsze sprawdzenia szukałyby spółek, których nie ma);
  2. pusta cena (`isna`);
  3. powtórzony dzień spółki (`duplicated` z `subset`);
  4. każda spółka ma każdy dzień: liczba wierszy = liczba dni × liczba spółek;
  5. ostatni dzień nie jest późniejszy niż `dzis` (tekst porównany z tekstem);
  6. dni nie mniej niż `poprzednie` (ochrona przed „pół tabeli”);
  7. (D2 a) ostatnia cena spółki = `ostatnia_cena` w rankingu, obie zaokrąglone do 2 miejsc.
- **Zwraca:** listę tekstów, np. `["Mniej sesji niż poprzednio: 799 < 800"]`.

**`zbuduj_dane(dzienne, ranking, spolki)`** — robi z dwóch tabel jeden słownik dla strony.
- `pivot` (wiersze: `dzien`, kolumny: `spolka`, wartości: `cena`) i `reset_index`;
- `daty` = kolumna `dzien` jako lista;
- `ceny` = słownik: klucz to spółka bez `.WA`, wartość to lista cen zaokrąglonych do 2 miejsc;
- `ranking` = lista słowników `spolka`, `miesiac`, `zmiana`, ułożona malejąco wg `zmiana_caly_okres`.
- **Zwraca:** `{"daty": […], "ceny": {…}, "ranking": […]}`.

**`wczytaj_poprzednie(sciezka)`** — ile sesji miał poprzedni `dane.js`. Gdy pliku nie ma — `0`.
Gdy jest — czyta tekst, odcina `POCZATEK` i `KONIEC`, `json.loads` i długość listy `daty`.

**`zapisz_js(dane, sciezka)`** — zapisuje `POCZATEK + json.dumps(dane, ensure_ascii=False) + KONIEC`
w UTF-8.

**Część główna (`if __name__ == "__main__":`):**
1. `os.makedirs` na `strona/pobrane` z `exist_ok=True` (jak w `compaction.py`);
2. `boto3.client("s3")` i pętla po `["dane_dzienne", "ranking"]` z `download_file` — lustro pętli
   `upload_file` z `gold.py`, linie 29–31;
3. `read_csv` obu plików, kolumna `dzien` = `data` przycięte do 10 znaków, `sort_values(["spolka", "dzien"])`;
4. `poprzednie = wczytaj_poprzednie(...)`, potem `sprawdz_pliki(..., str(date.today()), poprzednie)`;
5. są problemy → `sys.exit("Strona: problem - " + "; ".join(problemy))` — kod 1, `dane.js` nietknięty;
6. `zbuduj_dane`, dopisanie `"wygenerowano"` (`strftime("%Y-%m-%d %H:%M")`), `zapisz_js`;
7. linia wyniku (kształt w części 1).

### `kod/test_strona_dane.py` — nowy plik, 8 testów

Na zmyślonych danych, jak `test_path.py` (`pd.DataFrame` w teście, `ticker` z `config`), bez S3:
komplet → `[]`; brak dnia u jednej spółki; pusta cena; dzień z przyszłości; mniej sesji niż poprzednio;
ranking z innego dnia; obca spółka (jeden problem dzięki wczesnemu `return`); `zbuduj_dane` (kolejność
dat, ceny bez `.WA` i zaokrąglone, ranking malejąco). Razem `pytest kod/ -v` → `46 passed` (dziś 38).

### `.gitignore` — dwie linie

`strona/dane.js` i `strona/pobrane/` (D3 z 23.10: plik generowany, poza gitem).

---

## 4. Przykład na innych danych: stacja pogodowa

Stacja wysyła co wieczór dwa pliki: pomiary (długa tabela, jak `dane_dzienne.csv`) i podsumowanie
(jak `ranking.csv`). Skrypt robi z nich `pogoda.js` dla strony stacji.

`pobrane/pomiary.csv`:
```
data,temp,miasto,zmiana_proc,miesiac
2026-10-20 12:00:00,10.199999809265137,GDA.PL,,2026-10
2026-10-21 12:00:00,8.699999809265137,GDA.PL,-14.705882,2026-10
2026-10-22 12:00:00,9.300000190734863,GDA.PL,6.896552,2026-10
2026-10-20 12:00:00,11.300000190734863,KRK.PL,,2026-10
2026-10-21 12:00:00,9.899999618530273,KRK.PL,-12.389381,2026-10
2026-10-22 12:00:00,12.100000381469727,KRK.PL,22.222222,2026-10
```
`pobrane/podsumowanie.csv`:
```
miasto,najcieplejszy,odchylenie,dni,pierwsza_temp,ostatnia_temp,zmiana_okres
GDA.PL,2026-10-20,1.2,3,10.199999809265137,9.300000190734863,-8.823531
KRK.PL,2026-10-22,1.1,3,11.300000190734863,12.100000381469727,7.079642
```

Skrypt `pogoda_strona.py`:
```python
import json
import os
import sys
from datetime import date, datetime
import pandas as pd
FOLDER = os.path.dirname(os.path.abspath(__file__))
MIASTA = ["KRK.PL", "GDA.PL"]
POCZATEK = "window.POGODA = "
KONIEC = ";"
def sprawdz(pomiary, podsumowanie, miasta, dzis, poprzednie):
    problemy = []
    if set(pomiary["miasto"]) != set(miasta):
        problemy.append(f"Miasta w pomiarach: {sorted(set(pomiary['miasto']))}")
    if set(podsumowanie["miasto"]) != set(miasta):
        problemy.append(f"Miasta w podsumowaniu: {sorted(set(podsumowanie['miasto']))}")
    if problemy:
        return problemy
    if pomiary["temp"].isna().sum() > 0:
        problemy.append("Pusta temperatura")
    if pomiary.duplicated(subset=["dzien", "miasto"]).sum() > 0:
        problemy.append("Powtórzony dzień")
    dni = pomiary["dzien"].nunique()
    if len(pomiary) != dni * len(miasta):
        problemy.append(f"Miasta mają różne dni: {len(pomiary)} wierszy, {dni} dni")
    if pomiary["dzien"].max() > dzis:
        problemy.append(f"Pomiar z przyszłości: {pomiary['dzien'].max()}, dziś: {dzis}")
    if dni < poprzednie:
        problemy.append(f"Mniej dni niż poprzednio: {dni} < {poprzednie}")
    for m in miasta:
        ostatnia = pomiary[pomiary["miasto"] == m]["temp"].tolist()[-1]
        w_podsumowaniu = podsumowanie[podsumowanie["miasto"] == m]["ostatnia_temp"].tolist()[0]
        if round(ostatnia, 2) != round(w_podsumowaniu, 2):
            problemy.append(f"{m}: ostatnia temperatura {round(ostatnia, 2)}, w podsumowaniu {round(w_podsumowaniu, 2)}")
    return problemy
def zbuduj(pomiary, podsumowanie, miasta):
    tabela = pomiary.pivot(index="dzien", columns="miasto", values="temp").reset_index()
    temp = {}
    for m in miasta:
        temp[m.replace(".PL", "")] = [round(t, 2) for t in tabela[m].tolist()]
    podsumowanie = podsumowanie.sort_values(by="zmiana_okres", ascending=False)
    lista = [{"miasto": m.replace(".PL", ""), "najcieplejszy": n, "zmiana": round(z, 2)}
             for m, n, z in zip(podsumowanie["miasto"], podsumowanie["najcieplejszy"], podsumowanie["zmiana_okres"])]
    return {"daty": tabela["dzien"].tolist(), "temp": temp, "podsumowanie": lista}
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
if __name__ == "__main__":
    pomiary = pd.read_csv(os.path.join(FOLDER, "pobrane", "pomiary.csv"))
    podsumowanie = pd.read_csv(os.path.join(FOLDER, "pobrane", "podsumowanie.csv"))
    pomiary["dzien"] = pomiary["data"].str[:10]
    pomiary = pomiary.sort_values(["miasto", "dzien"])
    sciezka = os.path.join(FOLDER, "pogoda.js")
    poprzednie = wczytaj_poprzednie(sciezka)
    problemy = sprawdz(pomiary, podsumowanie, MIASTA, str(date.today()), poprzednie)
    if problemy:
        sys.exit("Pogoda: problem - " + "; ".join(problemy))
    dane = zbuduj(pomiary, podsumowanie, MIASTA)
    dane["wygenerowano"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    zapisz_js(dane, sciezka)
    ostatnie = ", ".join([f"{m} {dane['temp'][m][-1]}" for m in dane["temp"]])
    print(f"Pogoda: {len(dane['daty'])} dni ({dane['daty'][0]} – {dane['daty'][-1]}), poprzednio {poprzednie}, ostatnie: {ostatnie}")
```

**Trzy biegi (uruchomione 24.10):**

| Bieg | Na ekranie | Kod | `pogoda.js` |
|---|---|---|---|
| 1, pliku jeszcze nie ma | `Pogoda: 3 dni (2026-10-20 – 2026-10-22), poprzednio 0, ostatnie: KRK 12.1, GDA 9.3` | 0 | zapisany |
| 2, te same pliki | `… poprzednio 3, …` (reszta jak wyżej) | 0 | ten sam |
| 3, `pomiary.csv` bez 22.10 | `Pogoda: problem - Mniej dni niż poprzednio: 2 < 3; KRK.PL: ostatnia temperatura 9.9, w podsumowaniu 12.1; GDA.PL: ostatnia temperatura 8.7, w podsumowaniu 9.3` | 1 | **nietknięty** (ten sam skrót pliku) |

Zawartość `pogoda.js` po biegu 1:
```
window.POGODA = {"daty": ["2026-10-20", "2026-10-21", "2026-10-22"], "temp": {"KRK": [11.3, 9.9, 12.1], "GDA": [10.2, 8.7, 9.3]}, "podsumowanie": [{"miasto": "KRK", "najcieplejszy": "2026-10-22", "zmiana": 7.08}, {"miasto": "GDA", "najcieplejszy": "2026-10-20", "zmiana": -8.82}], "wygenerowano": "2026-10-24 15:33"};
```

**`sprawdz` w każdym przypadku (uruchomione 24.10, dane jak wyżej, `dzis = "2026-10-24"`):**

| Przypadek | Wynik |
|---|---|
| komplet, `poprzednie = 3` | `[]` |
| brak 21.10 w GDA | `['Miasta mają różne dni: 5 wierszy, 3 dni']` |
| pusta temperatura KRK 21.10 | `['Pusta temperatura']` |
| `dzis = "2026-10-21"` | `['Pomiar z przyszłości: 2026-10-22, dziś: 2026-10-21']` |
| `poprzednie = 4` | `['Mniej dni niż poprzednio: 3 < 4']` |
| podsumowanie z 21.10 (KRK `ostatnia_temp` 9.9) | `['KRK.PL: ostatnia temperatura 12.1, w podsumowaniu 9.9']` |
| KRK 22.10 zamienione na WAW | `["Miasta w pomiarach: ['GDA.PL', 'KRK.PL', 'WAW.PL']"]` — tylko to, wczesny `return` |
| GDA 20.10 dwa razy | `['Powtórzony dzień', 'Miasta mają różne dni: 7 wierszy, 3 dni']` |

| Przykład | Projekt |
|---|---|
| `pogoda_strona.py` | `kod/strona_dane.py` |
| `pobrane/pomiary.csv`, `pobrane/podsumowanie.csv` | `strona/pobrane/dane_dzienne.csv`, `strona/pobrane/ranking.csv` (z S3 przez `download_file`) |
| `MIASTA` | `ticker` z `config.py` |
| `miasto`, `temp` | `spolka`, `cena` |
| `.PL` | `.WA` |
| `ostatnia_temp` | `ostatnia_cena` (stara nazwa w nagłówku pliku; w Athenie `aktualna_cena`) |
| `najcieplejszy`, `zmiana_okres` | `miesiac`, `zmiana_caly_okres` |
| `"temp"`, `"podsumowanie"`, `"miasto"`, `"najcieplejszy"` | `"ceny"`, `"ranking"`, `"spolka"`, `"miesiac"` |
| `window.POGODA = ` | `window.DANE = ` |
| `pogoda.js` w folderze skryptu | `strona/dane.js` (`BASE_DIR`) |
| `sprawdz`, `zbuduj` | `sprawdz_pliki`, `zbuduj_dane` |
| linia `Pogoda: … dni` | linia `Strona: … sesji` |
| czyta pliki z dysku | najpierw pobiera je z S3 (pętla jak w `gold.py`) |

---

## 5. Nowe rzeczy w Pythonie (wejście → wyjście)

Znane już i użyte znowu: `pivot`, `reset_index`, `json.dumps(..., ensure_ascii=False)`, `json.loads`,
`download_file`, `os.makedirs(..., exist_ok=True)`, `.str[:10]`, `.replace`, `set`, `isna`, `nunique`,
`.max()` na tekście, `tolist()`, `zip`, `round`, `sys.exit` z tekstem, `"; ".join`, `strftime`, `with open`.

- **`removeprefix` / `removesuffix`:** odcina tekst z początku / z końca, jeśli tam jest.
  `'window.POGODA = {"a": 1};'.removeprefix("window.POGODA = ").removesuffix(";")` → `'{"a": 1}'`;
  `"abc".removeprefix("x")` → `'abc'` (nie pasuje — tekst bez zmian, bez błędu).
- **`os.path.exists(sciezka)`:** `True`, gdy plik jest, `False`, gdy go nie ma — bez błędu.
  Po biegu 1: `pogoda.js` → `True`, `brak.js` → `False`.
- **`duplicated(subset=[...])`:** `True` przy każdym wierszu, którego para kolumn już była wyżej.
  `dzien` 20, 20, 21 przy tym samym mieście → `[False, True, False]`; `.sum()` → 1.
- **Wczesny `return`:** `return` w środku funkcji kończy ją od razu; linie niżej się nie wykonają.
  Stąd przy obcym mieście tylko jeden problem.
- **`zip` z trzema kolumnami:** `for m, n, z in zip(a, b, c)` bierze po jednym z każdej naraz.
  `[(m, z) for m, z in zip(["KRK.PL", "GDA.PL"], [7.08, -8.82])]` → `[('KRK.PL', 7.08), ('GDA.PL', -8.82)]`.
- **`round` na cenie z Yahoo:** `round(334.20001220703125, 2)` → `334.2`; `round(75.5999984741211, 2)`
  → `75.6`; `round(137.0, 2)` → `137.0`.

**Dopisane 24.10 przy krokach porcji 1 (tego notatka wcześniej nie miała — potrzebne w testach):**
- **`drop(index=0)`:** jak znane `drop(columns=[...])`, ale usuwa **wiersz** o numerze 0; reszta
  numerów zostaje (1, 2, 3, …). Tabela 6 wierszy → 5 wierszy, pierwszy ma numer 1.
- **`None` na liście wpisanej do kolumny liczb:** pandas zamienia go na `NaN`.
  `pd.DataFrame({"cena": [100.0, None]})` → wiersz 1 ma `NaN`; `isna().sum()` → 1.
- **Funkcja pomocnicza w pliku testów:** zwykłe `def dane():` bez `test_` na początku — pytest jej nie
  uruchamia jako testu; każdy test woła ją i dostaje świeże tabele (`dzienne, ranking = dane()`),
  więc zmiana w jednym teście nie przechodzi do następnego.

---

## 6. Na co uważać

- **Brak `sort_values(["spolka", "dzien"])` przed `sprawdz_pliki`** — „ostatnia cena” to wtedy ostatni
  wiersz pliku, nie ostatni dzień; zgodność z rankingiem zależy od przypadku.
- **`data` bez przycięcia** — daty na stronie z `17:00:00`, a porównanie z `dzis` zawsze „z przyszłości”
  (`"2026-10-23 17:00:00" > "2026-10-23"` → `True`).
- **`zbuduj_dane` przed `sprawdz_pliki`** — `pivot` przy powtórzonym dniu kończy się `ValueError`, a przy
  braku dnia zostawia `NaN` w cenach. Najpierw sprawdzenie, potem budowa.
- **`POCZATEK` w zapisie inny niż w odczycie** (np. bez spacji) — `removeprefix` nic nie odetnie i
  `json.loads` padnie. Dlatego jedna stała.
- **Kolumna z rankingu po nazwie z Atheny** (`aktualna_cena`) — plik ma w nagłówku `ostatnia_cena`;
  `KeyError` przy pierwszym biegu.
- **Uruchomienie przed 18:15** — strona pokaże wczorajszą sesję (to widać po dacie); w chwili wysyłki
  Golda łapie to sprawdzenie z D2 (a).
- **Niesprawdzone:** czy klucz AWS na laptopie może pobierać z `gold/` (z `bronze/` pobierał 09.10).
  Pierwszy bieg to pokaże: `ClientError … (403)`.

---

## 7. Kolejność pracy

1. **Porcja 1:** `sprawdz_pliki` i 7 testów → `pytest kod/test_strona_dane.py -v` → `7 passed`.
2. **Porcja 2:** `zbuduj_dane`, `wczytaj_poprzednie`, `zapisz_js` i test `zbuduj_dane` → `8 passed`;
   `pytest kod/ -v` → `46 passed`.
3. **Porcja 3:** część główna, dwie linie w `.gitignore`. Pierwszy bieg na laptopie **po 18:15**, w dniu
   z kontrolą. Liczby zapisane przed biegiem: sesje = `Kontrola: Dane M wierszy` / 3, daty od
   `2023-08-14` do ostatniej sesji, ostatnie ceny z archiwum GPW, ranking z bloku Golda w `errors.txt`,
   `poprzednio 0`. Drugi bieg zaraz po nim: `poprzednio` = liczba sesji, `dane.js` ten sam (poza
   `wygenerowano`). `git status --short` — bez `strona/`.
4. **Ja:** szkic → `strona/index.html`, który czyta `dane.js` zamiast danych na sztywno; strona otwarta
   z dysku pokazuje te same liczby.
5. Commit i `git push`.

Każdy krok dostaniesz osobno, z numerem linii, wcięciem i tym, co ma wyjść.

---

## 8. Zmiany 25.10 (tego notatka wcześniej nie miała)

- **Nazwy plików:** skrypt to `kod/data_stream.py` (nazwa Gracjana z 24.10), testy `kod/test_data_stream.py`.
  Wszędzie wyżej `strona_dane` znaczy właśnie te pliki.
- **Testy na fixture zamiast `dane()`** (decyzja Gracjana 25.10): dwie funkcje `dzienne()` i `ranking()`
  z `@pytest.fixture`, testy biorą je przez parametry `(dzienne, ranking)`. Pytest woła fixture osobno dla
  każdego testu, więc zmiana tabeli w jednym teście nie przechodzi do następnego. Stała na górze pliku
  odrzucona: na kopii `3 failed, 4 passed` (pusta cena z `test_pusta_cena` widoczna w następnych testach).
- **Dwa testy więcej**, bo plan z 24.10 ich nie miał (przeoczenie Claude'a): `test_powtorzony_dzien`
  (CBF ma 22.10 dwa razy, a 23.10 wcale — liczba wierszy się zgadza, łapie to tylko `duplicated`) i
  `test_obca_spolka_w_rankingu`. Razem w pliku **10 testów**, w całym `kod/` **`48 passed`** (nie 8 i 46).
- **`zbuduj_dane`: ranking pętlą z `append`** zamiast listy składanej rozbitej na dwie linie (przykład pogody
  w części 4) — ten sam wynik, bez łamania linii w nawiasie. Przykład pogody w tym kształcie uruchomiony 25.10:
  `podsumowanie` → `[{'miasto': 'KRK', 'najcieplejszy': '2026-10-22', 'zmiana': 7.08}, {'miasto': 'GDA', …, 'zmiana': -8.82}]`.
- **`test_zbuduj_dane`:** cena SNT z 23.10 ustawiona na `334.20001220703125` (ogon jak z Yahoo), potem cztery
  `assert`: daty `["2026-10-22", "2026-10-23"]`, ceny bez `.WA` i zaokrąglone (SNT `334.2`), pierwszy w rankingu
  XTB (`zmiana` 30.0), ostatni CBF. Na kopii każda z pięciu celowych pomyłek (bez `.replace`, bez `round`,
  `ascending=True`, bez `reset_index`, sortowanie bez przypisania) daje `1 failed, 9 passed`.
- **`wczytaj_poprzednie` i `zapisz_js` nie mają testu w pytest** — sprawdza je porcja 3 (pierwszy bieg
  `poprzednio 0`, drugi `poprzednio` = liczba sesji). Na kopii 25.10, na lokalnym Goldzie z 20.09: przed zapisem
  `0`, po zapisie `775`, plik 26 980 B.

## Powiązane notatki

- [[Notatka-2026-10-23-dane-na-strone]] — notatka projektowa (co i dlaczego, D1–D6)
- [[Notatka-2026-10-13-jak-napisac-naprawy-1-i-2]] — wzór kształtu instrukcji
- [[Notatka-2026-10-19-strona-nowy-kierunek]] — strona, decyzje 19–23.10
