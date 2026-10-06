# Notatka 04.10: jak napisać warunek „dziś za wcześnie” (wszystko w jednym miejscu)

To instrukcja do [[Notatka-2026-10-04-producent-przed-zamknieciem]] (zatwierdzona 04.10,
wszystkie decyzje (a)). Tu jest **wszystko**: kroki, zasady, nowe pojęcia z wejściem
i wyjściem, przypadki z wynikami, tabela błędów, przewidywania i plan wdrożenia. Przy ocenie
kodu odwołuję się tylko do tej notatki. Jeśli czegoś zabraknie — powiem wprost i dopiszę.

Przykład to sklep, który zamyka kasę o 17:00 i ma pewny raport od 17:15 — nie spółki.
**Każdy wynik z przykładu pochodzi z uruchomienia 04.10** (Python 3.14.2, laptop). Twoich
plików nie ruszałem.

**Zmiana 05.10:** Gracjan nazwał plik `kod/session.py`, a testy `kod/test_session.py` (para jak
`control.py`/`test_control.py`). Wszystkie nazwy w notatce poprawione z `sesja` na `session`.
W tabeli błędów (Część 5) dopisane wiersze z 05.10. Wynik porcji 1: `10 passed in 0.04s`.

**06.10:** porcja 2 zrobiona — pięć zmian w `kod/data_ingestion.py` (92 linie), `28 passed in
2.16s`, bieg z martwym brokerem o 16:45:35 z dopiskiem przy trzech spółkach (Część 6). Część 8
poprawiona: ręczny bieg na EC2 **przed 16:50**, nie „przed 17:55”; wdrożenie przesunięte na 07.10
(decyzja Gracjana: sesja 06.10 zaczęła się o 16:28).

---

## Część 1. Kroki (po jednej linii, szczegóły niżej)

**Porcja 1 — funkcja i testy (dziś):**
1. Nowy plik `kod/session.py`: import `datetime` i `time` z `datetime`, import `ZoneInfo` z `zoneinfo`.
2. `kod/session.py`: dwie stałe — `STREFA` (strefa `Europe/Warsaw`) i `PROG` (godzina 17:55).
3. `kod/session.py`: funkcja `dzien_do_pominiecia(teraz)` — przelicza `teraz` na `STREFA`; przed `PROG` zwraca datę, inaczej `None`.
4. Nowy plik `kod/test_session.py`: importy i `UTC = ZoneInfo("UTC")`.
5. `kod/test_session.py`: 10 testów z tabeli w Części 4.
6. `pytest kod/test_session.py -v` → `10 passed`.

**Porcja 2 — wpięcie w Producenta (dziś, po zgodnej porcji 1):**
7. `kod/data_ingestion.py`: import `dzien_do_pominiecia`, `STREFA`, `PROG` z `session`.
8. `kod/data_ingestion.py`: przed pętlą spółek — `pomin` z `datetime.now(STREFA)`.
9. `kod/data_ingestion.py`: na początku każdej spółki — `pominiete = False`.
10. `kod/data_ingestion.py`: w pętli po świecach — gdy `data == pomin`: `pominiete = True` i `continue`.
11. `kod/data_ingestion.py`: po linii `wynik[-1] = …` — gdy `pominiete`, dopisek na końcu linii.
12. `pytest kod/ -v` → `28 passed`.
13. Bieg Producenta na laptopie **z martwym brokerem** (Część 6) → `nowych dni: 23`, `stan: nietknięte`, pamięć nietknięta.
14. Commit i `git push` (Część 7).

**Porcja 3 — wdrożenie (środa 07.10, Część 8).**

---

## Część 2. Zasady, wszystkie naraz

1. **`session.py` to czysta funkcja**: bez sieci, bez plików, bez `print`. Jak `sprawdz_daty`
   w `path.py` — dostaje dane, zwraca wynik.
2. **Funkcja dostaje godzinę jako parametr `teraz`**, nie woła w środku `datetime.now()`.
   Inaczej test nie mógłby podać „wtorku 16:30” — dostałby prawdziwą godzinę.
3. **Godzinę zawsze przeliczasz na Warszawę**: `teraz.astimezone(STREFA)`. EC2 liczy w UTC,
   laptop w czasie polskim — po przeliczeniu oba dają to samo, także po 25.10.
4. **Porównanie ostre `<`**: o 17:55 równo dzień jest już brany (`None`). Tak samo w przykładzie
   (17:15 → `None`, przypadek C).
5. **Funkcja zwraca `date` albo `None`**, nic innego.
6. **Stałe `STREFA` i `PROG` stoją tylko w `session.py`**, a `data_ingestion.py` je importuje.
   Jedno miejsce na próg — tekst dopisku też bierze go z `PROG`, więc zmiana progu nie zostawi
   kłamiącego komunikatu.
7. **W Producencie `pomin` liczysz raz, przed pętlą spółek**, z `datetime.now(STREFA)`.
8. **Porównujesz `data` (typ `date`, ta z linii z `fromtimestamp`) z `pomin` (też `date`).**
   Nie `str(data)` — tekst nigdy nie równa się dacie, warunek po cichu nic by nie robił
   (przypadek M).
9. **`continue` stoi przed `dane[str(data)] = c`**. Za nim dzisiejsza cena już byłaby w `dane`.
10. **`pominiete = False` na początku każdej spółki** (obok `dane = {}`), `True` tylko wtedy, gdy
    świeca z dziś naprawdę przyszła i została pominięta. W weekend świecy z dziś nie ma, więc
    dopisku nie będzie.
11. **Dopisek tylko przy pominięciu, na końcu linii spółki, przez `+=`**, z tekstem
    `, dziś pominięte (przed 17:55)`, gdzie `17:55` pochodzi z `PROG.strftime('%H:%M')`.
    Początek linii (`… stan: zapisane`) zostaje — kontrola o 18:30 go szuka.
12. **W testach każda data ma `tzinfo=`** (`STREFA` albo `UTC`). Wynik sprawdzasz
    `== date(…)` albo `is None`.
13. **Nie nazywaj zmiennych `time`, `date`, `datetime`** — to nazwy z importu (zasada 13
    z [[Notatka-2026-10-03-jak-przepiac-wykresy]]).
14. **Producenta na laptopie uruchamiasz tylko z `KAFKA_BOOTSTRAP=localhost:9999`**
    i sprawdzeniem `echo` przed biegiem. Bez tego Producent ma w kodzie adres brokera na EC2
    i wysłałby prawdziwe wiadomości.
15. Nazwy testów zaczynają się od `test_`.

---

## Część 3. Nowe pojęcia i przypadki (uruchomione 04.10)

Kod przykładu (`sklep.py`):

```python
from datetime import datetime, time, date
from zoneinfo import ZoneInfo

STREFA = ZoneInfo("Europe/Warsaw")
RAPORT = time(17, 15)

def dzien_niepewny(teraz):
    polska = teraz.astimezone(STREFA)
    if polska.time() < RAPORT:
        return polska.date()
    return None
```

### `ZoneInfo("Europe/Warsaw")` — strefa czasowa z regułami zmiany czasu

`ZoneInfo` (moduł `zoneinfo`, wbudowany w Pythona) to strefa po nazwie. `Europe/Warsaw` wie,
że latem jest UTC+2, a od 25.10 UTC+1. `ZoneInfo("UTC")` to czas bez przesunięcia.

### Godzina „ze strefą” (`tzinfo=`) i godzina „goła”

`datetime(2026, 10, 6, 15, 0, tzinfo=UTC)` to konkretna chwila na świecie. `datetime(2026, 10,
6, 15, 0)` bez `tzinfo` to „15:00 nie wiadomo gdzie” (*naive*, „naiwna”). Python nie pozwala ich
porównać:
```
datetime(2026,10,6,15,0) < datetime(2026,10,6,15,0,tzinfo=UTC)
→ TypeError: can't compare offset-naive and offset-aware datetimes
```

### `.astimezone(strefa)` — ta sama chwila w innej strefie

```python
a = datetime(2026, 10, 6, 15, 0, tzinfo=UTC).astimezone(STREFA)
b = datetime(2026, 10, 26, 15, 0, tzinfo=UTC).astimezone(STREFA)
print(a)
print(b)
print(a.time(), a.date())
```
Wyjście:
```
2026-10-06 17:00:00+02:00
2026-10-26 16:00:00+01:00
17:00:00 2026-10-06
```
Ta sama godzina UTC (15:00) to 17:00 w październiku przed zmianą czasu i 16:00 po niej.
`+02:00` na końcu to przesunięcie względem UTC. `.time()` daje samą godzinę, `.date()` samą
datę.

### `time(17, 15)` i porównanie godzin

`time(godzina, minuta)` z modułu `datetime` to sama godzina, bez daty.
```
time(17, 14) < time(17, 15)  → True
time(17, 15) < time(17, 15)  → False
```

### Przypadki funkcji z przykładu (próg 17:15)

| Przypadek | `teraz` | Wynik `dzien_niepewny` |
|---|---|---|
| A | wt 06.10 16:30, `tzinfo=STREFA` | `2026-10-06` |
| B | wt 06.10 18:00, `STREFA` | `None` |
| C | wt 06.10 17:15, `STREFA` (granica) | `None` |
| D | wt 06.10 17:14, `STREFA` | `2026-10-06` |
| E | wt 06.10 15:14, `tzinfo=UTC` (= 17:14 polskiego, lato) | `2026-10-06` |
| F | wt 06.10 15:15, `UTC` (= 17:15) | `None` |
| G | pn 26.10 16:00, `UTC` (= 17:00 polskiego, zima) | `2026-10-26` |
| H | pn 26.10 16:15, `UTC` (= 17:15) | `None` |
| I | wt 06.10 23:30, `UTC` (= 01:30 polskiego **07.10**) | `2026-10-07` |
| J | sob 10.10 10:00, `STREFA` | `2026-10-10` (zwraca datę, ale w sobotę dnia i tak nie ma) |

Przypadek I pokazuje, że data też się przelicza: w UTC jest jeszcze wtorek, w Polsce już środa.

### Pętla z `continue`, flaga i dopisek

`continue` (znasz) przeskakuje resztę obrotu pętli. Flaga zapamiętuje, że to się stało.
```python
pomin = date(2026, 10, 6)
utargi = [(date(2026, 10, 5), 1700.0), (date(2026, 10, 6), 1200.0)]
zeszyt = {}
pominiete = False
for dzien, kwota in utargi:
    if dzien == pomin:
        pominiete = True
        continue
    zeszyt[str(dzien)] = kwota
print(zeszyt, pominiete)
linia = f"Sklep A: wpisane dni: {len(zeszyt)}"
if pominiete:
    linia += f", dziś pominięte (przed {RAPORT.strftime('%H:%M')})"
print(linia)
```
Wyjście:
```
{'2026-10-05': 1700.0} True
Sklep A: wpisane dni: 1, dziś pominięte (przed 17:15)
```
`RAPORT.strftime('%H:%M')` działa na samej godzinie tak jak na dacie (`strftime` znasz).

### Pułapki (K–N), wszystkie uruchomione

```
K: date(2026,10,6) == "2026-10-06"            → False
L: date(2026,10,6) == None                     → False   (gdy funkcja zwróci None, nic nie pominie — dobrze)
M: if str(dzien) == pomin: …  (w pętli wyżej)  → {'2026-10-05': 1700.0, '2026-10-06': 1200.0} False
N: ZoneInfo("Europe/Warszawa")                 → ZoneInfoNotFoundError: 'No time zone found with key Europe/Warszawa'
O: import time;  time.time(17, 15)             → TypeError: time.time() takes no arguments (2 given)
```
M to najgroźniejsza: nic nie wybucha, a dzisiejsza cena przechodzi dalej. O: `import time` to
inny moduł (zegar systemu) — potrzebny jest `from datetime import time`.

### Test w przykładzie

```python
from datetime import datetime, date
from zoneinfo import ZoneInfo
from sklep import dzien_niepewny, STREFA

def test_przed_raportem():
    assert dzien_niepewny(datetime(2026, 10, 6, 16, 30, tzinfo=STREFA)) == date(2026, 10, 6)

def test_po_raporcie():
    assert dzien_niepewny(datetime(2026, 10, 6, 18, 0, tzinfo=STREFA)) is None
```
Wynik: `2 passed in 0.02s`.

---

## Część 4. Przykład → projekt

| Przykład | Projekt |
|---|---|
| `sklep.py` | `kod/session.py` |
| `RAPORT = time(17, 15)` | `PROG = time(17, 55)` |
| `dzien_niepewny(teraz)` | `dzien_do_pominiecia(teraz)` |
| `test_sklep.py` | `kod/test_session.py` |
| pętla po `utargi`, `zeszyt` | pętla `for t, c in con:` w `data_ingestion.py`, słownik `dane` |
| `dzien` | `data` (z `datetime.fromtimestamp(t).date()`) |
| `linia += …` | `wynik[-1] += …` |

**Dziesięć testów do `kod/test_session.py`** (wyniki sprawdzone 04.10 na tej samej logice z progiem
17:55; nazwy do wyboru, te są propozycją):

| # | Nazwa | `teraz` | Ma zwrócić |
|---|---|---|---|
| 1 | `test_wtorek_przed_progiem` | 2026-10-06 16:30, `STREFA` | `date(2026, 10, 6)` |
| 2 | `test_wtorek_po_progu` | 2026-10-06 18:00, `STREFA` | `None` |
| 3 | `test_dokladnie_prog` | 2026-10-06 17:55, `STREFA` | `None` |
| 4 | `test_minuta_przed_progiem` | 2026-10-06 17:54, `STREFA` | `date(2026, 10, 6)` |
| 5 | `test_utc_lato_przed` | 2026-10-06 15:54, `UTC` | `date(2026, 10, 6)` |
| 6 | `test_utc_lato_po` | 2026-10-06 15:55, `UTC` | `None` |
| 7 | `test_utc_zima_przed` | 2026-10-26 16:00, `UTC` | `date(2026, 10, 26)` |
| 8 | `test_utc_zima_po` | 2026-10-26 16:55, `UTC` | `None` |
| 9 | `test_po_polnocy_w_polsce` | 2026-10-06 23:30, `UTC` | `date(2026, 10, 7)` |
| 10 | `test_sobota_rano` | 2026-10-10 10:00, `STREFA` | `date(2026, 10, 10)` |

Testy 5–8 to sedno: udają EC2 (UTC) latem i zimą.

---

## Część 5. Błędy, które możesz zobaczyć, i co znaczą

| Co widzisz | Co to znaczy |
|---|---|
| `ModuleNotFoundError: No module named 'pyathena'` przy `pytest kod/` | `(.venv)` nie jest włączone |
| `ModuleNotFoundError: No module named 'session'` | plik nie leży w `kod/` albo ma inną nazwę |
| `ImportError: cannot import name 'PROG' from 'session'` | literówka w nazwie stałej albo jej brak w `session.py` |
| `ZoneInfoNotFoundError: 'No time zone found with key …'` | literówka w nazwie strefy — ma być `Europe/Warsaw` (przypadek N) |
| `TypeError: time.time() takes no arguments` | `import time` zamiast `from datetime import time` (przypadek O) |
| `NameError: name 'time' is not defined` | brak `time` w imporcie z `datetime` |
| `TypeError: 'str' object cannot be interpreted as an integer`, a w `pytest` `ERROR collecting …` i `Interrupted: 1 error during collection` (dopisane 05.10) | godzina podana jako tekst w cudzysłowie, np. `time("17, 55")`. `time` przyjmuje dwie liczby: `time(17, 55)`. Błąd wybucha już przy imporcie pliku, więc nie rusza żaden test (uruchomione 05.10 na przykładzie sklepu) |
| `SyntaxError: leading zeros in decimal integer literals are not permitted` (dopisane 05.10) | liczba z zerem z przodu, np. `datetime(2026, 10, 6, 9, 05)`. Minuty i godziny pisz bez zera: `5`, `9`. Wyjątek: samo `00` Python przyjmuje jako `0` (uruchomione 05.10) |
| test 3 (`test_dokladnie_prog`) nie przechodzi | `<=` zamiast `<` (zasada 4) |
| testy 5–8 nie przechodzą, 1–4 tak | brak `.astimezone(STREFA)` w funkcji |
| nie przechodzą testy 6, 8 i 9, a 5 i 7 przechodzą (dopisane 05.10) | w testach 5–9 `tzinfo=STREFA` zamiast `tzinfo=UTC` — test udaje laptop zamiast EC2; 5 i 7 przechodzą przypadkiem i niczego nie sprawdzają |
| test przechodzi na laptopie, choć data w teście bez `tzinfo=` | przypadek: „goła” godzina liczy się jako czas tej maszyny — na EC2 dałaby inny wynik; dopisz `tzinfo=` (zasada 12) |
| `IndentationError` | wcięcia w nowych liniach `data_ingestion.py` — liczby spacji są w krokach |
| `NameError: name 'pomin' is not defined` (dopisane 05.10) | brak linii `pomin = …` albo stoi ona pod pętlą spółek, a nie nad nią |
| `NameError: name 'pominiete' is not defined` (dopisane 05.10) | brak `pominiete = False` przy `dane = {}` — w biegu, w którym nic nie pominięto, `if pominiete:` nie ma czego sprawdzić |
| `pytest kod/ -v` → `28 passed`, a Producent i tak wybucha (dopisane 05.10) | żaden test nie importuje `data_ingestion.py`, więc błędy w nim widać dopiero przy biegu — dlatego bieg z martwym brokerem jest obowiązkowy |
| bieg na laptopie w dzień roboczy przed 17:55: brak dopisku, `nowych dni` o 1 większe | warunek nie działa: `str(data) == pomin` (przypadek M) albo `continue` za `dane[str(data)] = c` |
| bieg na laptopie: `wysłane:` większe od 0 albo `stan: zapisane` | **Producent połączył się z prawdziwym brokerem** — `KAFKA_BOOTSTRAP` nieustawione. Zatrzymaj się i napisz mi, nic więcej nie uruchamiaj |

---

## Część 6. Uruchomienie na laptopie i co ma wyjść

**Testy:** `pytest kod/test_session.py -v` → 10 × `PASSED`, `10 passed`. Potem `pytest kod/ -v` →
`28 passed` (18 dotychczasowych + 10).

**Bieg Producenta z martwym brokerem (krok 13)** — wzór z 11.09. Adres `localhost:9999` to port,
na którym nic nie słucha, więc Producent nie połączy się z żadnym brokerem: nic nie wyśle
i nie ruszy pamięci (`stan: nietknięte`). Sprawdzone 04.10: biblioteka próbuje 30 sekund, wypisuje
3 linie `ERROR` i się poddaje.

Przewidywania na **dziś, niedziela 04.10**:
- linia startu z dzisiejszą datą i godziną (laptop: czas polski);
- po ok. 30 sekundach 4 linie `ERROR`: trzy z biblioteki (`Connection failed`, `Connection lost`,
  `Bootstrap failed`) i nasza `Wystąpił błąd łączenia z brokerem: localhost:9999.`;
- 3 × `…: nowych dni: 23, wysłane: 0, stan: nietknięte`, **bez dopisku** (w niedzielę świecy
  z dziś nie ma). Skąd 23: pamięć laptopa kończy się na 01.09 (762 wiersze), a dane sięgają
  02.10 (785 dni) — 785 − 762 = 23;
- `companies\CBF.WA.txt` z tą samą godziną zapisu co przed biegiem (3 września 19:17:54).

Ten bieg sprawdza, że Producent z nowym importem się uruchamia i liczy to samo co przedtem.
**Samego pomijania dziś nie sprawdzi** — to zrobi ten sam bieg w dzień roboczy w trakcie
sesji, 9:00–16:50 (Część 8, krok 2): wtedy `nowych dni: 23` z dopiskiem `, dziś pominięte
(przed 17:55)` (dzień bieżący pominięty, więc dalej 23, nie 24).

**Kod i testy przełożone przez Gracjana na poniedziałek 05.10**, wdrożenie wtorek 06.10.

**Przeliczone 05.10** (pamięć laptopa sprawdzona: 3 × 762 wiersze, ostatni 2026-09-01, zapis
2026-09-03 19:17:54):
- **pon. 05.10 wieczorem (po 17:55):** 3 × `nowych dni: 24, wysłane: 0, stan: nietknięte`, **bez
  dopisku** (23 dni do 02.10 + 05.10; po progu nic się nie pomija). Sprawdza tylko, że plik się
  uruchamia i liczy jak przedtem;
- **wt. 06.10 w trakcie sesji (9:00–16:50):** 3 × `nowych dni: 24, wysłane: 0, stan: nietknięte,
  dziś pominięte (przed 17:55)` — bez warunku byłoby 25.

**Wynik 06.10:** `pytest kod/ -v` → `28 passed in 2.16s`; bieg o 16:45:35, po 30 s cztery linie
`ERROR`, potem 3 × `nowych dni: 24, wysłane: 0, stan: nietknięte, dziś pominięte (przed 17:55)`;
`companies\CBF.WA.txt` dalej z zapisem `2026-09-03 19:17:54`. Zgodne co do słowa.

---

## Część 7. Commit

W commicie: `kod/session.py`, `kod/test_session.py`, `kod/data_ingestion.py`, obie notatki z 04.10
o Producencie i dokumentacja z dzisiejszej sesji. Liczby podam przed komendą, po
`git status --short`. Na EC2 nic nie zmieniamy do środy 07.10.

---

## Część 8. Wdrożenie (środa 07.10, w dzień giełdowy; część ręczna przed 16:50)

Kolejność, każdy krok z przewidywaniem podanym przed komendą:

1. **Kontrola biegów z 04 i 05.10** (tabela „Przewidywania od 04.10” w CLAUDE.md) — musi być
   zgodna, zanim cokolwiek zmienimy. ✅ 05.10 (bieg 06.10 też zgodny).
2. **Laptop, martwy broker, w trakcie sesji (9:00–16:50):** `nowych dni: N` z dopiskiem
   `, dziś pominięte (przed 17:55)` przy trzech spółkach (N = dni od 02.09 do wczoraj). To
   pierwszy dowód, że warunek działa na prawdziwych danych z Yahoo — bez ryzyka, bo nic nie
   idzie do Kafki. **Dlaczego w trakcie sesji, a nie „przed 17:55”:** w trakcie sesji Yahoo na
   pewno ma dzisiejszą świecę (08.09 o 16:43 była), a między 17:00 a 18:00 może jej nie być
   (11.09 o 17:45 nie było) — wtedy dopisek się nie pojawi i nie będzie to błąd, tylko brak
   czego pomijać. Ten sam bieg można zrobić już w poniedziałek 05.10 (EC2 go nie dotyka).
   ✅ **06.10 o 16:45:35:** 3 × `nowych dni: 24, wysłane: 0, stan: nietknięte, dziś pominięte
   (przed 17:55)`, pamięć nietknięta.
3. **EC2, przed 16:50** (poprawione 06.10, było „przed 17:55”): `git pull` (z `4aca12d` do
   commita z 06.10), `git status --short` pusty przed i po, plik `kod/session.py` jest.
4. **EC2, ręczny bieg Producenta bez `>>`, w trakcie sesji (9:00–16:50)**, z
   `KAFKA_BOOTSTRAP=localhost:9094`: 3 × `nowych dni: 0, wysłane: 0, stan: zapisane, dziś
   pominięte (przed 17:55)`; `LOG-END-OFFSET` dalej 2390 (nic nie poszło do Kafki); w pamięci
   spółek dalej 787 wierszy, ostatni `2026-10-06`. **Dlaczego przed 16:50 (dopisane 06.10):** jak
   w kroku 2 — po 17:00 Yahoo może nie mieć świecy, wtedy dopisku nie będzie. To nie błąd, ale
   bieg nie dowiedzie pominięcia. `nowych dni: 1, wysłane: 1` znaczy, że warunek nie działa — stop.
5. **EC2, wieczorem po 18:32 (07.10):** blok z `cron` 28 linii, start 1140, `wc -l` 1167, 3 ×
   `nowych dni: 1, wysłane: 1, stan: zapisane` (bez dopisku, bo 18:00 > 17:55), `Odebrano 3`,
   `Kontrola: Dane 2364 wierszy`, `Kontrola: OK`, zakładka 2393, pliki 788 × 3. To dowód na
   prawdziwej drodze: dzień pominięty po południu przyszedł o 18:00.
6. **26.10 (pierwszy dzień giełdowy po zmianie czasu):** blok bez dopisku, `nowych dni: 1` — strefa
   liczy się dobrze także zimą.

Nie w oknie 17:55–18:35. `crontab` bez zmian. Powrót: commit cofający zmianę
(`git revert`) zrobiony na laptopie, `git push`, potem `git pull` na EC2 — bez ręcznych zmian
plików na EC2 (żeby `git status --short` tam został pusty). Szczegóły w krokach, jeśli będzie
potrzeba.
