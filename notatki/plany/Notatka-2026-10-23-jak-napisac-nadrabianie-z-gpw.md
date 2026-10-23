# Notatka 23.10: nadrabianie ceną z GPW — nad czym pracujemy i co piszemy

> **Status (23.10.2026, wieczorem): odłożona razem z notatką projektową** (decyzja Gracjana). Kod nie
> powstaje; notatka zostaje jako gotowiec. Decyzje D7–D9 nierozstrzygnięte.

Instrukcja do [[Notatka-2026-10-23-nadrabianie-cena-z-gpw]] (zatwierdzona 23.10, D1–D6 w wariancie
a). Kształt jak w instrukcji z 13.10: najpierw nad czym pracujemy, potem decyzje, zmiany w kodzie
i co robi każda funkcja, przykład na innych danych, nowe pojęcia, pułapki, kolejność. Wyniki
przykładu pochodzą z uruchomienia 23.10 (Python 3.14, laptop). Twoich plików nie ruszałem.

---

## 1. Nad czym pracujemy

**Jak dziś działa Producent po naprawie 1.** O 18:00 wysyła do Kafki tylko dzisiejszą świecę. Każdy
inny nowy dzień jest **wstrzymany**: nie idzie do Kafki ani do pamięci, w linii wyniku jest dopisek
`wstrzymane: N (ostatnie: data cena, …)`, a kontrola o 18:30 robi z niego `AWARIA`.

**Co wyszło w przeglądzie 23.10.** Dzień, który nie przyszedł o 18:00 (padł bieg, Yahoo spóźniło
się ze świecą), zostaje wstrzymany, aż ktoś go nadrobi. Dziś da się to zrobić tylko przez `NADROB=1`,
a to wysyła cenę z Yahoo — tę, która za wcześniejsze dni bywa zła tygodniami (CBF i SNT za 05–06.10
do dziś). Do tego stróż wysyła mail tylko przy zmianie stanu (sprawdzone 23.10 o 17:25), więc luka po
pierwszym mailu trwa po cichu.

**Co zmieniamy.** Nowy tryb `NADROB=gpw`. Przepisujesz zamknięcia z archiwum GPW do pliku
`companies/ceny_gpw.txt` na EC2, np. `2026-10-21 CBF.WA 193,90`. Producent w tym trybie:
- dzisiejszą świecę wysyła jak zawsze (cena Yahoo);
- wstrzymany dzień **z wpisem** w pliku wysyła z ceną z pliku;
- wstrzymany dzień **bez wpisu** dalej wstrzymuje;
- wpis dla dnia, który nie jest wstrzymany, pomija i wypisuje (nigdy nie wysyła dnia drugi raz);
- cenę różną od ceny Yahoo z tego dnia o ponad 25% odrzuca (literówka) — dzień zostaje wstrzymany;
- zły wiersz w pliku albo brak pliku = komunikat i koniec, zanim cokolwiek pobierze.

`NADROB=1` zostaje jak jest (nowa spółka, stara historia), ale też wypisze wysłane dni z cenami
(decyzja 2 z przeglądu).

**Czego to nie zrobi.** Nie nadrabia samo — to jest ręczny bieg. Automat (drugi bieg tego samego
wieczoru) to osobna, późniejsza notatka (decyzja 23.10, wariant 1).

---

## 2. Trzy decyzje przed kodem

- **D7 — co przy cenie ponad progiem.** (a) dzień zostaje wstrzymany, w linii wyniku dopisek
  `odrzucone z GPW …`, reszta biegu idzie dalej; kontrola i tak da `AWARIA`, bo dzień jest wstrzymany
  — rekomendacja; (b) dosłownie jak D3: bieg kończy się przy pierwszej spółce z taką ceną. Cenę Yahoo
  spółki znamy dopiero w pętli, więc spółki wcześniejsze w pętli byłyby już wysłane, a ich linie wyniku
  by się nie wypisały. **To zmienia szczegół zatwierdzonego D3** — dlatego pytam.
- **D8 — nieznana wartość `NADROB`** (np. literówka `gwp`). (a) koniec z komunikatem, zanim cokolwiek
  pobierze — rekomendacja; (b) jak dziś: zwykły bieg (dzień dalej wstrzymany, alarm dalej).
- **D9 — wpis dla spółki spoza listy** (np. `CBF` bez `.WA`). (a) błąd pliku, koniec przed biegiem —
  rekomendacja (tak jest w notatce projektowej); (b) pomijać.

---

## 3. Co zmienia się w kodzie

### `kod/session.py` — dwie nowe funkcje, czyste (bez sieci, plików i `print`)

**`wczytaj_ceny_gpw(tekst, spolki)`**
- **Dostaje:** całą treść pliku jako jeden tekst i listę spółek (`ticker` z `config.py`).
- **Robi:** idzie po liniach; pustą i zaczynającą się od `#` pomija; każdą inną dzieli na trzy części
  (data, spółka, cena); cenę z przecinkiem zamienia na kropkę; sprawdza datę (`date.fromisoformat`),
  liczbę, spółkę z listy i cenę większą od zera.
- **Zwraca dwie rzeczy:** słownik cen z kluczem `(spółka, data)` i listę błędów (tekstów). Pusta lista
  błędów = plik dobry.
- Potrzebuje `date` z `datetime` — dopisać do pierwszej linii `session.py`.

**`wybierz_z_gpw(spolka, wstrzymane, ceny_gpw, ceny_yahoo)`**
- **Dostaje:** spółkę (`"CBF.WA"`), listę jej wstrzymanych dat, słownik z `wczytaj_ceny_gpw` i
  słownik `dane` Producenta (data → cena Yahoo).
- **Robi:** dla każdej wstrzymanej daty: brak wpisu → dalej wstrzymana; wpis różny od Yahoo o ponad
  25% → odrzucony i dalej wstrzymany; inaczej → nadrobiony. Osobno zbiera daty z pliku dla tej spółki,
  które nie są wstrzymane (pominięte).
- **Zwraca cztery rzeczy:** `nadrobione` (lista par `(data, cena)`), `wstrzymane` (daty dalej
  wstrzymane, razem z odrzuconymi), `odrzucone` (pary `(data, cena)`), `pominiete` (daty, posortowane).

### `kod/data_ingestion.py` — Producent

1. Import obu funkcji z `session`, obok `podziel_daty`.
2. W miejsce linii z `nadrob`: `tryb` z `NADROB` (domyślnie `""`); wartość spoza `""`, `"1"`, `"gpw"`
   → `sys.exit` z komunikatem (D8); `nadrob` (`tryb` == `"1"`) i `z_gpw` (`tryb` == `"gpw"`).
3. Gdy `z_gpw`: odczyt `companies/ceny_gpw.txt` (brak pliku → `sys.exit`), potem
   `wczytaj_ceny_gpw`; niepusta lista błędów → `sys.exit("Plik cen GPW: " + …)`.
4. W pętli spółek, **między** `podziel_daty` a linią `posortowane`: gdy `z_gpw` —
   `wybierz_z_gpw(…)`, nowe `wstrzymane`, ceny z GPW wpisane do `dane` dla nadrobionych dat, nadrobione
   daty dołożone do `do_wyslania`. Pętla wysyłki zostaje bez zmian (bierze ceny z `dane`).
5. Na końcu linii wyniku, po dopisku `wstrzymane`: `nadrobione z GPW` albo `nadrobione z Yahoo`
   (zaległe daty wysłane w tym biegu, do 5 ostatnich, tylko gdy `stan: zapisane`), `odrzucone z GPW`,
   `z pliku GPW pominięte`.

### `kod/control.py` — bez zmian

Nowe dopiski nie mają słowa `wstrzymane`, więc linia z samym `nadrobione` daje `OK`. Dzień odrzucony
albo bez wpisu dalej jest w dopisku `wstrzymane`, więc daje `AWARIA`.

### Testy

- `kod/test_session.py`, 14 nowych testów:
  - `wczytaj_ceny_gpw` (8): plik z komentarzem i pustą linią, przecinek, nieznana spółka, zły wiersz,
    zła cena, zła data, cena zero, dwa błędy naraz;
  - `wybierz_z_gpw` (6): wpis dla wstrzymanego, wstrzymany bez wpisu, wpis dla niewstrzymanego, ponad
    25%, dokładnie 25% (przechodzi), wpis innej spółki.
- `kod/test_control.py`, 1 test: blok z dopiskiem `nadrobione z GPW` → 0 błędów.
- Razem `pytest kod/ -v` → `53 passed` (dziś 38).

### Jak to wygląda w logu (ręczny bieg z `NADROB=gpw`, wieczorem po kontroli)

```
CBF.WA: nowych dni: 1, wysłane: 1, stan: zapisane, nadrobione z GPW: 1 (ostatnie: 2026-10-21 193.9)
XTB.WA: nowych dni: 1, wysłane: 0, stan: zapisane, wstrzymane: 1 (ostatnie: 2026-10-21 137.84)
SNT.WA: nowych dni: 0, wysłane: 0, stan: zapisane, z pliku GPW pominięte: 1 (2026-10-21)
```
CBF nadrobiony; XTB bez wpisu w pliku, więc dalej wstrzymany; SNT nie miał luki, wpis pominięty.

---

## 4. Przykład na innych danych: stacja pogodowa

Stacja zapisuje dzienne temperatury. Dzień bez pomiaru jest wstrzymany. Operator przepisuje wartości
z archiwum IMGW do pliku. Funkcje mają ten sam kształt co w projekcie:

```python
from datetime import date

def wczytaj_wartosci(tekst, stacje):
    wartosci = {}
    bledy = []
    for linia in tekst.splitlines():
        linia = linia.strip()
        if not linia or linia.startswith("#"):
            continue
        czesci = linia.split()
        if len(czesci) != 3:
            bledy.append(f"zły wiersz: {linia}")
            continue
        dzien, stacja, liczba = czesci
        try:
            date.fromisoformat(dzien)
            wartosc = float(liczba.replace(",", "."))
        except ValueError:
            bledy.append(f"zła data albo liczba: {linia}")
            continue
        if stacja not in stacje:
            bledy.append(f"nieznana stacja: {linia}")
        elif wartosc <= 0:
            bledy.append(f"wartość nie większa od zera: {linia}")
        else:
            wartosci[(stacja, dzien)] = wartosc
    return wartosci, bledy

def wybierz_z_imgw(stacja, wstrzymane, wartosci, czujnik):
    nadrobione = []
    dalej = []
    odrzucone = []
    for d in wstrzymane:
        if (stacja, d) not in wartosci:
            dalej.append(d)
            continue
        w = wartosci[(stacja, d)]
        if abs(w / czujnik[d] - 1) > 0.25:
            odrzucone.append((d, w))
            dalej.append(d)
        else:
            nadrobione.append((d, w))
    pominiete = sorted([d for (s, d) in wartosci if s == stacja and d not in wstrzymane])
    return nadrobione, dalej, odrzucone, pominiete
```

**`wczytaj_wartosci`** (stacje `["KRK.PL", "GDA.PL"]`):

| Plik | Wynik |
|---|---|
| `# z archiwum IMGW`, `2026-10-21 KRK.PL 12,1`, pusta linia, `2026-10-19 KRK.PL 9.0`, `2026-10-21 GDA.PL 8,7` | `({('KRK.PL', '2026-10-21'): 12.1, ('KRK.PL', '2026-10-19'): 9.0, ('GDA.PL', '2026-10-21'): 8.7}, [])` |
| `2026-10-21 KRK 12,1` | `({}, ['nieznana stacja: 2026-10-21 KRK 12,1'])` |
| `2026-10-21 KRK.PL` | `({}, ['zły wiersz: 2026-10-21 KRK.PL'])` |
| `2026-10-21 KRK.PL 12,1,5` | `({}, ['zła data albo liczba: 2026-10-21 KRK.PL 12,1,5'])` |
| `2026-13-01 KRK.PL 12,1` | `({}, ['zła data albo liczba: 2026-13-01 KRK.PL 12,1'])` |
| `2026-10-21 KRK.PL 0` | `({}, ['wartość nie większa od zera: 2026-10-21 KRK.PL 0'])` |

**`wybierz_z_imgw`** (czujnik: 20.10 → 10,4, 21.10 → 11,0):

| Sytuacja | Wywołanie (skrót) | Wynik |
|---|---|---|
| dwa wstrzymane, wpis dla jednego, wpis dla 19.10 | `("KRK.PL", ["2026-10-20", "2026-10-21"], plik z góry)` | `([('2026-10-21', 12.1)], ['2026-10-20'], [], ['2026-10-19'])` |
| literówka 121 | `({("KRK.PL", "2026-10-21"): 121.0})` | `([], ['2026-10-21'], [('2026-10-21', 121.0)], [])` |
| dokładnie 25% (13,75 przy 11,0) | `({("KRK.PL", "2026-10-21"): 13.75})` | `([('2026-10-21', 13.75)], [], [], [])` |
| stacja bez luki, wpis w pliku | `("GDA.PL", [], plik z góry)` | `([], [], [], ['2026-10-21'])` |

**Cały wieczór stacji KRK** (wstrzymane 20 i 21.10, dziś 22.10, tryb z IMGW):
```python
nadrobione, wstrzymane, odrzucone, pominiete = wybierz_z_imgw("KRK.PL", wstrzymane, wartosci, dane)
for d, w in nadrobione:
    dane[d] = w
do_wyslania = sorted(do_wyslania + [d for d, w in nadrobione])
zapis = [d for d in sorted(dane.keys()) if d not in wstrzymane]
```
Wyjście:
```
do wysłania: ['2026-10-21', '2026-10-22']
zeszyt: ['2026-10-21', '2026-10-22']
KRK.PL: nowych dni: 3, wysłane: 2, stan: zapisane, wstrzymane: 1 (ostatnie: 2026-10-20 10.4), nadrobione z IMGW: 1 (2026-10-21 12.1), z pliku pominięte: 1 (2026-10-19)
```
(W zeszycie przykładu nie ma starszych dni, żeby było krócej.) 20.10 dalej wstrzymany, więc jutro znów
„nowy” i znów alarm — aż operator dopisze go do pliku.

| Przykład | Projekt |
|---|---|
| `wczytaj_wartosci` | `wczytaj_ceny_gpw` w `kod/session.py` |
| `wybierz_z_imgw` | `wybierz_z_gpw` w `kod/session.py` |
| stacja `KRK.PL` | spółka `CBF.WA` |
| `czujnik` | `dane` Producenta (ceny Yahoo) |
| plik operatora | `companies/ceny_gpw.txt` na EC2 |
| `zeszyt` | pamięć `companies/*.WA.txt` |
| `nadrobione z IMGW` | `nadrobione z GPW` |

---

## 5. Nowe rzeczy w Pythonie (wejście → wyjście)

- **`split()` bez argumentu** dzieli po dowolnej liczbie spacji i tabulatorów:
  `"2026-10-21  CBF.WA 193,90".split()` → `['2026-10-21', 'CBF.WA', '193,90']`;
  `"a  b".split(" ")` → `['a', '', 'b']` (dlatego bez argumentu).
- **Słownik z kluczem-krotką:** `c = {("CBF.WA", "2026-10-21"): 193.9}`;
  `("CBF.WA", "2026-10-21") in c` → `True`; `("2026-10-21", "CBF.WA") in c` → `False` (kolejność
  w krotce ma znaczenie); `c[("CBF.WA", "2026-10-21")]` → `193.9`.
- **Pętla po kluczach-krotkach z rozpakowaniem:** `[d for (s, d) in c if s == "CBF.WA"]` →
  `['2026-10-21']`.
- **`abs()`** — wartość bez znaku: `abs(-0.3)` → `0.3`; `abs(193.9 / 201.0 - 1)` → `0.0353…`
  (3,5% różnicy); `abs(1939 / 201.0 - 1)` → `8.646…` (literówka).
- **Cena z przecinkiem:** `float("193,90")` → `ValueError`; `float("193,90".replace(",", "."))` → `193.9`.
- **Sprawdzenie daty w `try`:** `date.fromisoformat("2026-13-01")` → `ValueError` (miesiąc 13) —
  łapane tym samym `except ValueError` co zła liczba.
- **Cztery wartości z funkcji:** `a, b, c, d = f()`; trzy nazwy przy czterech wartościach →
  `ValueError: too many values to unpack (expected 3)`.
- **Łączenie list:** `["2026-10-22"] + ["2026-10-21"]` → `['2026-10-22', '2026-10-21']`; `sorted(…)`
  → `['2026-10-21', '2026-10-22']`.

---

## 6. Na co uważać

- **Nowe `wstrzymane` przed linią `posortowane`.** Odwrotnie nadrobiony dzień nie trafi do pamięci,
  jutro znów będzie „nowy” i wróci jako wstrzymany.
- **`wybierz_z_gpw` dostaje `dane`, zanim wpiszesz do nich ceny z GPW.** Odwrotnie porównasz cenę
  z GPW z nią samą i próg nigdy nie zadziała.
- **Klucz `(spółka, data)` w tej samej kolejności w obu funkcjach.** `(data, spółka)` w jednej z nich
  sprawi, że żaden wpis nie zostanie znaleziony — wszystko „wstrzymane”, bez błędu.
- **W nowych dopiskach nie może paść słowo `wstrzymane`** — kontrola zrobiłaby z nich `AWARIA`.
- **`NADROB=gpw` tylko przed ręczną komendą**, nigdy w `crontab`; plik `companies/ceny_gpw.txt` jest
  poza gitem (`companies/*.txt` w `.gitignore`) i nie łapie go maska `*.WA.txt` w kontroli.
- **`"1"` i `"gpw"` jako tekst** — porównanie z `==`, jak w linii z 16.10 (wniosek 15 w CLAUDE.md).

---

## 7. Kolejność pracy

1. **Porcja 1:** obie funkcje w `session.py` i 14 testów → `pytest kod/test_session.py -v` →
   `32 passed`.
2. **Porcja 2:** zmiany w Producencie (lista w części 3) i 1 test kontroli → `pytest kod/ -v` →
   `53 passed`.
3. **Porcja 3:** Claude uruchamia kopię Twojego Producenta z udawanym Yahoo i Kafką (jak 16.10):
   zwykły dzień, `NADROB=gpw` z wpisem, bez wpisu, z literówką, wpis niewstrzymany, zły plik, brak
   pliku, `NADROB=gwp`. Commit i `git push`.
4. **Porcja 4:** EC2 — `git pull` poza oknem 17:55–18:35, zwykły bieg `cron` (blok 28 linii, bez
   zmian), kontrola `OK`. README i CLAUDE.md (dwa tryby nadrabiania, zasada na czas luki).

Każdy krok dostaniesz osobno, z numerem linii, wcięciem i tym, co ma wyjść.

## Powiązane notatki

- [[Notatka-2026-10-23-nadrabianie-cena-z-gpw]] — notatka projektowa (co i dlaczego)
- [[Notatka-2026-10-13-jak-napisac-naprawy-1-i-2]] — wzór: `podziel_daty` i testy
- [[Przeglad-2026-10-23-calosc]] — punkty 1.1–1.3
