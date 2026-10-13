# Notatka 13.10: naprawy 1 i 2 — nad czym pracujemy i co piszemy

Instrukcja do [[Notatka-2026-10-12-naprawy-1-i-2]] (zatwierdzona 12.10: naprawa 1 (a), naprawa 2
(a)). Wersja krótka, na prośbę Gracjana z 13.10: najpierw dokładnie, nad czym pracujemy, potem co
zmienia się w kodzie i co robi każda funkcja, potem przykład na innych danych. Wyniki przykładu
pochodzą z uruchomienia 13.10 (Python 3.14.2, laptop). Twoich plików nie ruszałem.

---

## 1. Nad czym pracujemy

**Jak dziś działa Producent (`kod/data_ingestion.py`).** Codziennie o 18:00 pobiera z Yahoo
notowania z trzech lat. Porównuje je z pamięcią w `companies/*.WA.txt`, czyli spisem dni, które
już wysłał. Do Kafki wysyła tylko daty, których w pamięci nie ma („nowe dni”). Po potwierdzeniu
od brokera zapisuje pamięć od nowa. W zwykły dzień nowa jest jedna data — dzisiejsza.

**Co odkryliśmy 08–12.10.** Yahoo dla całej GPW podaje dobrą cenę tylko za dzień, w którym
odpowiada. Wcześniejsze dni bieżącego tygodnia po pewnym czasie dostają cenę z poprzedniego piątku
(13.10 poniedziałek 12.10 był jeszcze dobry, a 08.10 zepsute były już 05–07.10). Przykład: 07.10
Cyber_Folks zamknął na 199,20 zł (archiwum GPW), a Yahoo dzień później podawało za 07.10 201,0 —
cenę z 02.10. Poprawka przychodzi dopiero po kilku dniach (wtorek–piątek następnego tygodnia).
To nie nasz błąd: surowa odpowiedź Yahoo z laptopa jest taka sama, a Apple ma dobre ceny.

**Dlaczego dotąd nic się nie zepsuło.** Bieg o 18:00 wysyła tylko dzisiejszą świecę, a ta jest
dobra. 90 cen w S3 porównanych z GPW zgadza się co do grosza.

**Kiedy to szkodzi.** Gdy jakiś bieg nie wyśle swojego dnia: broker nie żyje, EC2 stoi, Yahoo
spóźni się ze świecą. Następnego dnia ten dzień jest dla Producenta „nowy”, ale Yahoo ma już za
niego złą cenę. Producent ją wyśle, a ona przejdzie przez S3, Silver i Gold aż na stronę. Kontrola
o 18:30 tego nie zauważy, bo data się zgadza — zła jest tylko cena.

**Naprawa 1 — co zmieniamy.** Producent wysyła **tylko dzisiejszą** świecę. Każdą inną nową datę
**wstrzymuje**: nie wysyła jej do Kafki i nie zapisuje do pamięci, więc jutro znów jest „nowa”.
W logu przy spółce pojawia się dopisek `wstrzymane`, a kontrola robi z niego awarię (mail od
stróża). Człowiek porównuje cenę z archiwum GPW i dopiero wtedy nadrabia dzień ręcznym biegiem ze
zmienną `NADROB=1`.

**Naprawa 2 — co zmieniamy.** Producent i Konsument mają dziś zapasowy adres brokera
(`13.63.105.190:9092`), używany, gdy brakuje zmiennej `KAFKA_BOOTSTRAP`. Bieg z laptopa bez tej
zmiennej połączyłby się z brokerem na EC2 i wysłał wszystko, czego nie ma w pamięci laptopa (od
02.09) — także złe ceny. Usuwamy zapasowy adres. Brak zmiennej = program kończy się komunikatem.

**Czego naprawa nie zrobi.** Złej dzisiejszej ceny nie złapie — gdyby Yahoo zaczęło psuć także ją,
potrzebne byłoby drugie źródło danych. Do czasu ręcznego nadrobienia w danych jest luka (lepsza
luka niż zła cena).

---

## 2. Dwie decyzje przed kodem

- **D1 — co ma być w dopisku.** (a) liczba wstrzymanych dni i najwyżej 5 ostatnich dat z cenami —
  rekomendacja: ceny od razu porównasz z GPW, 5 dni to cały tydzień; (b) wszystkie daty z cenami —
  przy nowej spółce linia na kilkaset dat; (c) sama liczba.
- **D2 — udawany „dziś” (`PRODUCENT_DATA`), jedna linia jak `KONTROLA_DATA`.** (a) dodać —
  rekomendacja: pozwala sprawdzić wstrzymanie na EC2 jednym ręcznym biegiem między 17:55 a 17:59;
  (b) nie dodawać — wstrzymanie sprawdzą tylko testy i bieg na laptopie bez brokera.

**Decyzje Gracjana 13.10: D1 (a), D2 (a).** Kod od porcji 1 tego samego dnia.

---

## 3. Co zmienia się w kodzie

### `kod/session.py` — nowa funkcja `podziel_daty(nowe_daty, dzis, nadrob)`

Stoi obok `dzien_do_pominiecia`, bo też dotyczy „dzisiaj po polsku”. Czysta funkcja: bez sieci,
plików i `print`.
- **Dostaje:** zbiór nowych dat (teksty `"RRRR-MM-DD"`), dzisiejszą datę **jako tekst** i
  `True`/`False` dla nadrabiania.
- **Robi:** gdy `nadrob` — wszystkie nowe daty idą do wysłania (po kolei), nic nie jest wstrzymane.
  Gdy nie — do wysłania tylko data równa `dzis`, każda inna nowa data jest wstrzymana.
- **Zwraca dwie listy naraz:** `do_wyslania` i `wstrzymane` (posortowane).

### `kod/data_ingestion.py` — Producent

1. `import sys` i import `podziel_daty` z `session`.
2. `BOOTSTRAP` bez zapasowego adresu; gdy pusty — `sys.exit("Brak zmiennej KAFKA_BOOTSTRAP …")`.
3. Przed pętlą spółek (obok `pomin`): `dzis` (z `PRODUCENT_DATA` albo dzisiejsza data polska) i
   `nadrob` (`True`, gdy `NADROB` = `"1"`).
4. Po `nowe_daty = …`: `do_wyslania, wstrzymane = podziel_daty(nowe_daty, dzis, nadrob)`.
5. Pętla wysyłki idzie po `do_wyslania` zamiast po `nowe_daty`.
6. Zapis pamięci pomija daty z `wstrzymane`.
7. Na końcu linii wyniku, gdy coś wstrzymano: `, wstrzymane: N (ostatnie: data cena, …)`.

### `kod/kafka_consumer.py` — Konsument

Tak jak punkt 2 Producenta: bez zapasowego adresu, brak zmiennej = koniec z komunikatem.

### `kod/control.py` — kontrola

W `sprawdz_blok`, na wzór sprawdzania `stan: zapisane`: każda linia spółki ze słowem `wstrzymane`
daje błąd `"<spółka>: wstrzymane dni"`. Błąd = `Kontrola: AWARIA` i mail od stróża.

### Testy

- `kod/test_session.py`: 8 testów `podziel_daty` (zwykły dzień, weekend, zaległy + dziś, sam
  zaległy, kilka zaległych po kolei, nadrabianie, nadrabianie bez nowych, data z przyszłości).
- `kod/test_control.py`: 2 testy (dopisek przy jednej spółce → 1 błąd, przy trzech → 3 błędy).
- Razem `pytest kod/ -v` → `38 passed` (dziś 28).

### Jak to wygląda w logu

Zwykły dzień — bez zmian, blok dalej ma 28 linii:
```
CBF.WA: nowych dni: 1, wysłane: 1, stan: zapisane
```
Dzień po nieudanym biegu (wczoraj nie wyszło, dziś tak):
```
CBF.WA: nowych dni: 2, wysłane: 1, stan: zapisane, wstrzymane: 1 (ostatnie: 2026-10-12 200.0)
Kontrola: AWARIA - CBF.WA: wstrzymane dni
```

---

## 4. Przykład na innych danych: lodziarnia

Lodziarnia co wieczór dostaje od dostawcy raport sprzedaży z całego tygodnia. Dobra jest tylko
liczba z dzisiaj. Do zeszytu wpisuje więc tylko dzisiejszy dzień; inny nowy dzień wstrzymuje i
dzwoni do szefa. Szef po sprawdzeniu w kasie mówi „nadrób”.

```python
def podziel_dni(nowe_dni, dzis, nadrob):
    if nadrob:
        return sorted(nowe_dni), []
    do_ksiegi = [d for d in nowe_dni if d == dzis]
    wstrzymane = sorted([d for d in nowe_dni if d != dzis])
    return do_ksiegi, wstrzymane
```

| Sytuacja | `nowe_dni` | `dzis` | `nadrob` | Wynik |
|---|---|---|---|---|
| zwykły dzień | `{"2026-06-16"}` | `"2026-06-16"` | `False` | `(['2026-06-16'], [])` |
| nic nowego | `set()` | `"2026-06-14"` | `False` | `([], [])` |
| wczoraj nie wyszło | `{"2026-06-17", "2026-06-18"}` | `"2026-06-18"` | `False` | `(['2026-06-18'], ['2026-06-17'])` |
| szef: „nadrób” | `{"2026-06-19", "2026-06-17"}` | `"2026-06-21"` | `True` | `(['2026-06-17', '2026-06-19'], [])` |

Cały wieczór lodziarni (zeszyt ma 15 i 16.06, raport ma 15–18.06, dziś 18.06):
```python
dane = {"2026-06-15": 35.0, "2026-06-16": 41.0}
stare = set(dane.keys())
for dzien, porcje in [("2026-06-17", 28.0), ("2026-06-18", 44.0)]:
    dane[dzien] = porcje
nowe = set(dane.keys()) - stare
do_ksiegi, wstrzymane = podziel_dni(nowe, "2026-06-18", False)
zapis = [d for d in sorted(dane.keys()) if d not in wstrzymane]
linia = f"Lodziarnia A: nowych dni: {len(nowe)}, wpisane: {len(do_ksiegi)}"
if wstrzymane:
    ostatnie = ", ".join([f"{d} {round(dane[d], 2)}" for d in wstrzymane[-5:]])
    linia += f", wstrzymane: {len(wstrzymane)} (ostatnie: {ostatnie})"
print(zapis)
print(linia)
```
Wyjście:
```
['2026-06-15', '2026-06-16', '2026-06-18']
Lodziarnia A: nowych dni: 2, wpisane: 1, wstrzymane: 1 (ostatnie: 2026-06-17 28.0)
```
17.06 nie ma w zeszycie, więc jutro znów będzie nowy i znów da alarm — aż szef każe nadrobić.

| Przykład | Projekt |
|---|---|
| `podziel_dni` | `podziel_daty` w `kod/session.py` |
| `do_ksiegi` | `do_wyslania` (do Kafki) |
| zeszyt | pamięć `companies/*.WA.txt` |
| raport dostawcy | odpowiedź Yahoo |
| `linia += …` | `wynik[-1] += …` |
| szef: „nadrób” | `NADROB=1` przed ręczną komendą |

---

## 5. Nowe rzeczy w Pythonie (wejście → wyjście)

- **Dwie wartości z funkcji:** `return a, b` oddaje parę (krotkę); `x, y = f(...)` rozkłada ją na
  dwie zmienne. W teście: `== (["2026-06-16"], [])` → `True`; `== [["2026-06-16"], []]` → `False`.
- **Pięć ostatnich:** `["01", "02", "03", "04", "05", "06", "07"][-5:]` → `['03', …, '07']`;
  `["01", "02"][-5:]` → `['01', '02']` (mniej niż 5 — bez błędu).
- **Zaokrąglenie:** `round(28.000000001, 2)` → `28.0`; `round(12.345678, 2)` → `12.35`.
- **`not in`:** `"2026-06-18" not in ["2026-06-17"]` → `True`.
- **Przełącznik ze zmiennej:** zmienna jest zawsze tekstem — `"1" == "1"` → `True`,
  `"1" == 1` → `False`, `bool("0")` → `True` (dlatego porównanie z `"1"`).
- **Koniec z komunikatem:** `sys.exit("Brak zmiennej …")` wypisuje tekst na stderr (u nas do
  `errors.txt`) i kończy program z kodem 1. `not` łapie i brak zmiennej (`None`), i pustą (`""`).

---

## 6. Na co uważać

- **Pętla wysyłki zostawiona po `nowe_daty`** — nic nie wybucha, a zaległe dni dalej idą do Kafki.
- **Pamięć zapisana bez pomijania `wstrzymane`** — wstrzymany dzień już nigdy nie wróci jako nowy.
- **`dzis` jako data, nie tekst** — tekst nigdy nie równa się dacie, więc wstrzymany byłby także
  dzisiejszy dzień (codzienny alarm, nic nie idzie do Kafki).
- **Brak `import sys`** — błąd wychodzi dopiero, gdy zabraknie zmiennej; dlatego bieg bez niej.
- **`NADROB` i `PRODUCENT_DATA` tylko przed komendą**, nigdy w `crontab`.

---

## 7. Kolejność pracy

1. **Porcja 1:** `podziel_daty` i 8 testów → `pytest kod/test_session.py -v` → `18 passed`.
2. **Porcja 2:** zmiany w Producencie (lista w części 3).
3. **Porcja 3:** Konsument, `control.py`, 2 testy → `pytest kod/ -v` → `38 passed`.
4. **Porcja 4:** laptop — bieg bez `KAFKA_BOOTSTRAP` (komunikat, kod 1) i z martwym brokerem
   (`localhost:9999`: dopisek `wstrzymane`, `wysłane: 0`, pamięć nietknięta). Commit i `git push`.
5. **Porcja 5:** EC2 w dzień giełdowy — `git pull` przed 17:55; między 17:55 a 17:59 ręczny bieg
   z `PRODUCENT_DATA` = wczoraj (dzisiejsza świeca wstrzymana, nic nie idzie do Kafki); o 18:00
   zwykły `cron`; po 18:32 kontrola `OK`.

Każdy krok dostaniesz osobno, z numerem linii, wcięciem i tym, co ma wyjść.

## Powiązane notatki

- [[Notatka-2026-10-12-naprawy-1-i-2]] — notatka projektowa (co i dlaczego)
- [[Notatka-2026-10-04-jak-napisac-warunek-sesji]] — wzór: `session.py` i testy
- [[Przeglad-2026-10-08-calosc]] — punkt 1.1 i adres brokera
