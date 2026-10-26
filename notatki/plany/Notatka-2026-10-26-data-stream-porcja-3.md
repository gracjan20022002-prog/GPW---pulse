# Notatka 26.10: część główna `kod/data_stream.py` (porcja 3) — co robi każda linia

Ciąg dalszy [[Notatka-2026-10-25-data-stream-porcje-1-i-2]]. Tamta notatka opisuje funkcje (linie 1–63),
ta — kod napisany 26.10: linie 64–83 i dwie linie w `.gitignore`. Kod cytowany dokładnie tak, jak jest
w pliku. **Wartości w tabelach to prawdziwe dane z dziś:** pliki pobrane z S3 o 17:01 (Gold z biegu
25.10, sesje do 23.10), policzone na kopii w katalogu roboczym Claude'a (Python 3.14.2, pandas 3.0.5).

---

## 1. Po co jest ta część

Funkcje z porcji 1 i 2 to **narzędzia**: każda umie jedną rzecz, ale żadna nie wie, skąd wziąć dane
ani kiedy ruszyć. Część główna to **przepis**, który bierze te narzędzia i używa ich po kolei:

| Krok | Po ludzku | Linie |
|---|---|---|
| A | „uruchamiaj mnie tylko wtedy, gdy ktoś woła mnie bezpośrednio” | 64 |
| B | przygotuj folder na pobrane pliki | 65–66 |
| C | pobierz dwa pliki Golda z S3 | 67–69 |
| D | wczytaj je do tabel i przygotuj (dzień bez godziny, kolejność) | 70–73 |
| E | zajrzyj do starego `dane.js` i sprawdź nowe pliki | 74–76 |
| F | coś nie gra → zatrzymaj się, stary `dane.js` zostaje | 77–78 |
| G | wszystko gra → zbuduj dane dla strony i zapisz `dane.js` | 79–81 |
| H | powiedz na ekranie, co zrobiłeś | 82–83 |

Kolejność jest najważniejsza: **najpierw sprawdzenie (E), dopiero potem zapis (G)**. Dzięki temu zły plik
z S3 nigdy nie nadpisze dobrego `dane.js` — zasada „lepiej stara strona niż zła”.

---

## 2. Kawałek po kawałku

### A. Linia 64 — „tylko przy uruchomieniu”

```python
if __name__ == "__main__":
```

**Po ludzku:** wszystko, co jest pod tą linią z wcięciem, wykona się tylko po komendzie
`python kod/data_stream.py`. Gdy plik jest **importowany** (tak robią testy: `from data_stream import …`),
ta część jest pomijana.

| Jak plik jest użyty | `__name__` | Co się dzieje |
|---|---|---|
| `python kod/data_stream.py` | `"__main__"` | warunek prawdziwy → pobiera z S3, zapisuje `dane.js` |
| `pytest` (import w testach) | `"data_stream"` (sprawdzone dziś) | warunek fałszywy → tylko funkcje, bez S3 |

**Bez tej linii:** każdy `pytest` łączyłby się z S3 i nadpisywał `dane.js`. Dlatego po dopisaniu porcji 3
testów dalej było `48 passed` — część główna w testach w ogóle się nie wykonuje.

### B. Linie 65–66 — folder na pobrane pliki

```python
    pobrane = os.path.join(BASE_DIR, "strona", "pobrane")
    os.makedirs(pobrane, exist_ok=True)
```

| Linia | Co robi | Dziś |
|---|---|---|
| 65 | skleja ścieżkę: folder projektu + `strona` + `pobrane`. To tylko tekst, nic jeszcze nie powstaje | `C:\Users\gracj\OneDrive\Dokumenty\DE\GPW - pulse\strona\pobrane` |
| 66 | zakłada folder. Gdy nie ma też `strona\`, zakłada oba naraz. `exist_ok=True` = „jak już jest, to w porządku” | bieg 1: powstały `strona\` i `strona\pobrane\`; bieg 2: folder był, bez błędu |

**Bez `exist_ok=True`:** pierwszy bieg by przeszedł, drugi skończyłby się `FileExistsError`.

### C. Linie 67–69 — pobranie z S3

```python
    s3 = boto3.client("s3")
    for nazwa in ["dane_dzienne", "ranking"]:
        s3.download_file(BUCKET, f"gold/{nazwa}/{nazwa}.csv", os.path.join(pobrane, f"{nazwa}.csv"))
```

**Po ludzku:** otwórz połączenie z S3 i dwa razy zrób to samo — raz dla danych dziennych, raz dla
rankingu. To odbicie lustrzane `gold.py` (linie 28–30): tam pętla **wysyła** te pliki, tu je **pobiera**.

| Linia | Co robi | Dziś |
|---|---|---|
| 67 | tworzy „klienta” S3 — obiekt, przez który się z S3 rozmawia. Używa klucza AWS z laptopa | klucz z laptopa ma dostęp do `gold/` (sprawdzone dziś, wcześniej niepewne) |
| 68 | pętla z dwoma obrotami | `nazwa` = `"dane_dzienne"`, potem `"ranking"` |
| 69 | pobiera jeden plik: **skąd** (bucket i klucz w S3) → **dokąd** (plik na dysku). Plik na dysku jest nadpisywany przy każdym biegu | obrót 1: `gold/dane_dzienne/dane_dzienne.csv` → `strona\pobrane\dane_dzienne.csv` (160749 B); obrót 2: `gold/ranking/ranking.csv` → `strona\pobrane\ranking.csv` (337 B) |

**Kolejność argumentów:** `download_file(bucket, klucz_w_S3, plik_na_dysku)`, a w `gold.py`
`upload_file(plik_na_dysku, bucket, klucz_w_S3)`. Zapamiętanie: **pierwszy argument to zawsze „skąd”**.

**Gdy S3 odmówi albo nie ma sieci:** `Traceback` w linii 69, dalsze linie się nie wykonają, więc `dane.js`
zostaje stary (to wynika z kolejności linii; na żywo niesprawdzone).

### D. Linie 70–73 — wczytanie i przygotowanie tabel

```python
    dzienne = pd.read_csv(os.path.join(pobrane, "dane_dzienne.csv"))
    ranking = pd.read_csv(os.path.join(pobrane, "ranking.csv"))
    dzienne["dzien"] = dzienne["data"].str[:10]
    dzienne = dzienne.sort_values(["spolka", "dzien"])
```

**Linia 70** — plik dzienny jako tabela, **2400 wierszy × 5 kolumn**. Pierwsze wiersze:
```
                  data       cena  spolka  zmiana_proc  miesiac
0  2023-08-14 17:00:00  75.599998  CBF.WA          NaN  2023-08
1  2023-08-16 17:00:00  77.000000  CBF.WA     1.851854  2023-08
2  2023-08-17 17:00:00  76.000000  CBF.WA    -1.298701  2023-08
```

**Linia 71** — ranking jako tabela, **3 wiersze × 7 kolumn** (nagłówek z pliku, stare nazwy cen):
```
   spolka  miesiac  odchylenie_standardowe  dni  pierwsza_cena  ostatnia_cena  zmiana_caly_okres
0  CBF.WA  2024-11                3.914546   19      75.599998     192.000000         153.968259
1  SNT.WA  2025-06                4.086839   20      70.800003     334.200012         372.033895
2  XTB.WA  2025-01                3.701199   21      37.939999     137.000000         261.096481
```
Z tych kolumn skrypt używa czterech: `spolka`, `miesiac`, `ostatnia_cena` (sprawdzenie w linii 32),
`zmiana_caly_okres` (ranking na stronie).

**Linia 72** — nowa kolumna `dzien`: pierwsze 10 znaków z `data`, czyli data bez godziny.
```
                  data       dzien
0  2023-08-14 17:00:00  2023-08-14
```
Po co: `sprawdz_pliki` porównuje ostatni dzień z dzisiejszą datą jako **tekst**. Bez przycięcia w dniu sesji
`"2026-10-26 17:00:00" > "2026-10-26"` → `True` (dłuższy napis z tym samym początkiem jest „większy”),
czyli fałszywy problem „Sesja z przyszłości” w każdym biegu po 18:15. Z przycięciem
`"2026-10-26" > "2026-10-26"` → `False`. Na stronie daty też mają być bez `17:00:00`.

**Linia 73** — układa wiersze: najpierw po spółce (alfabetycznie: CBF, SNT, XTB), w każdej spółce po dniu
rosnąco. Ostatni wiersz CBF to wtedy na pewno ostatni dzień: `2026-10-23`, `192.0`.
- **Dziś sortowanie niczego nie zmieniło** (sprawdzone: ta sama kolejność wierszy przed i po) — Gold już
  tak układa plik. To zabezpieczenie na dzień, w którym kolejność w pliku będzie inna.
- Co by było bez niego przy pomieszanym pliku (sprawdzone na przetasowanej kopii): „ostatni” CBF to
  `2024-07-22` zamiast `2026-10-23`, więc sprawdzenie zgodności z rankingiem dałoby fałszywy problem.
- `dzienne = …` na początku jest konieczne: `sort_values` nie zmienia tabeli w miejscu, tylko oddaje nową.

### E. Linie 74–76 — stary `dane.js` i sprawdzenie

```python
    sciezka = os.path.join(BASE_DIR, "strona", "dane.js")
    poprzednie = wczytaj_poprzednie(sciezka)
    problemy = sprawdz_pliki(dzienne, ranking, ticker, str(date.today()), poprzednie)
```

| Linia | Co robi | Dziś |
|---|---|---|
| 74 | ścieżka do pliku dla strony. Ta sama zmienna idzie do odczytu (75) i do zapisu (81) — jeden plik | `…\GPW - pulse\strona\dane.js` |
| 75 | ile sesji miał **poprzedni** `dane.js` (funkcja z porcji 2) | bieg 1: pliku nie ma → `0`; bieg 2: `800` |
| 76 | sprawdza nowe tabele (funkcja z porcji 1) i oddaje listę problemów | `str(date.today())` = `'2026-10-26'`; wynik `[]` |

**Dlaczego 75 stoi przed 81:** odczyt starego pliku musi być **przed** zapisem nowego. Odwrotnie skrypt
porównywałby nowe dane same ze sobą i sprawdzenie „mniej sesji niż poprzednio” nigdy by nie zadziałało.

**Dlaczego `str(...)`:** `date.today()` to data, a w tabeli dni są tekstem. `sprawdz_pliki` porównuje tekst
z tekstem, tak jak `path.py`.

### F. Linie 77–78 — zatrzymanie przy problemie

```python
    if problemy:
        sys.exit("Strona: problem - "+"; ".join(problemy))
```

| Linia | Co robi | Dziś |
|---|---|---|
| 77 | pusta lista znaczy w `if` „fałsz”, niepusta „prawda” | `[]` → fałsz → linia 78 pominięta |
| 78 | skleja wszystkie problemy w jeden tekst i kończy program: tekst na ekran, kod wyjścia **1**, dalsze linie (zapis!) się nie wykonają | nie wykonana |

`"; ".join(lista)` wstawia `"; "` **między** elementy: `["A", "B"]` → `"A; B"`, `["A"]` → `"A"`.

Jak to wygląda, gdy problem jest (sprawdzone na kopii: dzisiejszy plik bez 23.10, `poprzednie` = 800):
```
Strona: problem - Mniej sesji niż poprzednio: 799 < 800; CBF.WA: ostatnia cena: 195.1, w rankingu: 192.0; XTB.WA: ostatnia cena: 135.4, w rankingu: 137.0; SNT.WA: ostatnia cena: 336.0, w rankingu: 334.2
```
Kod 1 widać w PowerShellu przez `$LASTEXITCODE`. Kiedyś, gdy skrypt będzie chodził sam (drugi etap),
właśnie ten kod powie automatowi, że bieg się nie udał.

### G. Linie 79–81 — budowa i zapis

```python
    dane = zbuduj_dane(dzienne, ranking, ticker)
    dane["wygenerowano"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    zapisz_js(dane, sciezka)
```

| Linia | Co robi | Dziś |
|---|---|---|
| 79 | robi z dwóch tabel jeden słownik dla strony (funkcja z porcji 2) | `daty`: 800; `ceny`: CBF, XTB, SNT po 800; `ranking`: 3, pierwszy `{'spolka': 'SNT', 'miesiac': '2025-06', 'zmiana': 372.03}` |
| 80 | dopisuje do słownika czwarty klucz: kiedy plik powstał (data i godzina z laptopa) | bieg 1: `'2026-10-26 17:02'` |
| 81 | zapisuje słownik jako `window.DANE = {…};` (funkcja z porcji 2) | `strona\dane.js`, 27867 B, jedna linia |

**Po co `wygenerowano`:** strona pokaże „dane z …”. Data ostatniej sesji mówi, z którego dnia są ceny,
a `wygenerowano` — kiedy ostatnio uruchomiłeś skrypt.

### H. Linie 82–83 — linia wyniku na ekranie

```python
    ostatnie = ", ".join([f"{t} {dane['ceny'][t][-1]}" for t in dane["ceny"]])
    print(f"Strona: {len(dane['daty'])} sesji ({dane['daty'][0]} - {dane['daty'][-1]}), poprzednio {poprzednie}, ostatnie: {ostatnie}")
```

**Linia 82** krok po kroku:
1. `for t in dane["ceny"]` — po kluczach słownika cen: `"CBF"`, `"XTB"`, `"SNT"` (kolejność z `ticker`);
2. `dane['ceny'][t][-1]` — ostatnia cena tej spółki;
3. `f"{t} {…}"` — kawałek tekstu: `['CBF 192.0', 'XTB 137.0', 'SNT 334.2']`;
4. `", ".join(...)` — sklejenie przecinkami: `'CBF 192.0, XTB 137.0, SNT 334.2'`.

W środku f-napisu cudzysłowy są pojedyncze (`'ceny'`), bo cały napis jest w podwójnych.

**Linia 83** wstawia w zdanie cztery liczby: `len(dane['daty'])` → `800`, `dane['daty'][0]` →
`2023-08-14`, `dane['daty'][-1]` → `2026-10-23`, `poprzednie` → `0` albo `800`. Wynik z dziś:
```
Strona: 800 sesji (2023-08-14 - 2026-10-23), poprzednio 0, ostatnie: CBF 192.0, XTB 137.0, SNT 334.2
```
Po co ta linia: po jednym spojrzeniu wiesz, czy liczby się zgadzają z kontrolą (`Kontrola: Dane 2400`
/ 3 = 800) i z archiwum GPW. Ta linia to **dowód biegu**, jak linie `stan: zapisane` u Producenta.

---

## 3. `.gitignore` — linie 18–19

```
strona/dane.js
strona/pobrane/
```

| Linia | Co robi |
|---|---|
| 18 | git pomija jeden plik: `strona/dane.js`. Robi go skrypt przy każdym biegu, więc wersji w gicie nie potrzeba |
| 19 | git pomija **cały folder** `strona/pobrane/` (ukośnik na końcu = folder) — to kopie plików z S3 |

Sprawdzone dziś `git check-ignore` (tylko odczyt): `dane.js` pomija linia 18, `pobrane/dane_dzienne.csv`
linia 19, a przyszły `strona/index.html` **nie jest** pomijany — trafi do gita. `git status --short` po
biegach: bez żadnej linii ze `strona`.

---

## 4. Co pokazały dzisiejsze biegi

| Bieg | Na ekranie | Kod | `dane.js` |
|---|---|---|---|
| 1 (17:01), pliku nie było | `Strona: 800 sesji (2023-08-14 - 2026-10-23), poprzednio 0, ostatnie: CBF 192.0, XTB 137.0, SNT 334.2` | 0 | powstał, 27867 B |
| 2 (17:02), te same pliki | to samo, tylko `poprzednio 800` | 0 | 27867 B |

- Ceny z 22 i 23.10 w `dane.js` zgadzają się z archiwum GPW; ranking (SNT 372.03, XTB 261.1, CBF 153.97)
  z rankingiem Golda z 23.10.
- Bieg 2 udowodnił, że `zapisz_js` i `wczytaj_poprzednie` pasują do siebie (zapis → odczyt → `800`).
  Tych dwóch funkcji nie sprawdza żaden test w pytest.
- **Bieg 3 (po 18:15) — jeszcze nie było:** przewidywane `801 sesji (… - 2026-10-26), poprzednio 800`.

---

## 5. Pojęcia użyte w części głównej (wejście → wyjście)

- **`if __name__ == "__main__":`** — `python plik.py` → część się wykonuje; `import plik` → pomijana.
- **`os.makedirs(folder, exist_ok=True)`** — brak folderu → zakłada (z folderami po drodze); jest → nic.
- **`download_file(bucket, klucz, plik)`** — kopia pliku z S3 na dysk; plik na dysku nadpisany.
- **`.str[:10]`** — `"2023-08-14 17:00:00"` → `"2023-08-14"`.
- **`sort_values([a, b])`** — po `a`, a przy równym `a` po `b`; oddaje nową tabelę (trzeba przypisać).
- **`str(date.today())`** — dzisiejsza data jako tekst: `'2026-10-26'`.
- **`if lista:`** — `[]` → fałsz, `["x"]` → prawda.
- **`"; ".join(lista)`** — `["A", "B"]` → `"A; B"`; `[]` → `""`.
- **`sys.exit("tekst")`** — tekst na ekran, kod wyjścia 1 (sprawdzone dziś: `kod: 1`), koniec programu.
- **`datetime.now().strftime("%Y-%m-%d %H:%M")`** — `'2026-10-26 17:02'`.
- **`lista[-1]`, `lista[0]`** — ostatni / pierwszy element.
- **`$LASTEXITCODE`** (PowerShell) — kod wyjścia ostatniego programu: `0` sukces, `1` problem.
- **`folder/` w `.gitignore`** — ukośnik na końcu znaczy cały folder z zawartością.

---

## 6. Gdyby coś się zmieniło — co by się stało

| Zmiana w kodzie | Skutek |
|---|---|
| zapis (81) przed sprawdzeniem (76–78) | zły plik z S3 nadpisuje dobry `dane.js` — tego chroni cała kolejność |
| odczyt poprzednich (75) po zapisie (81) | `poprzednie` zawsze = nowa liczba sesji, ochrona przed „pół tabeli” martwa |
| bez linii 72 | po 18:15 w dniu sesji zawsze „Sesja z przyszłości”, kod 1 |
| bez linii 73 przy pomieszanym pliku | fałszywy problem zgodności z rankingiem (ostatni CBF `2024-07-22`) |
| bez `exist_ok=True` | drugi bieg: `FileExistsError` (sprawdzone dziś na pustym folderze próbnym) |
| zła kolejność argumentów w 69 | błąd przy pobieraniu, `dane.js` stary; dokładnego komunikatu nie sprawdzałem |

---

## 7. Stan według zasady 9 („zrobione”) — 26.10, przed biegiem 3

- (a) prawdziwa droga danych: **tak**, biegi 1 i 2 na plikach z S3;
- (b) sprawdzenie z liczbą policzoną przed biegiem: **tak**, 800 sesji i ceny przewidziane i potwierdzone;
- (c) głośna awaria: **tak**, `sys.exit` z kodem 1 (sprawdzone na kopii, na prawdziwym biegu jeszcze nie);
- (d) wdrożone tam, gdzie ma działać: pierwszy etap to laptop — **tak**; strony czytającej `dane.js` **nie ma**;
- (e) opis: ta notatka; README, CLAUDE.md i słownik — na koniec sesji.

Kod nie jest jeszcze w gicie. Nie ma testów `wczytaj_poprzednie` i `zapisz_js` w pytest.

## Powiązane notatki

- [[Notatka-2026-10-25-data-stream-porcje-1-i-2]] — funkcje z porcji 1 i 2, testy
- [[Notatka-2026-10-24-jak-napisac-strona-dane]] — instrukcja do całego skryptu
- [[Notatka-2026-10-23-dane-na-strone]] — notatka projektowa (D1–D6)
