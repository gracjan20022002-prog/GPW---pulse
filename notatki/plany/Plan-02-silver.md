# Etap 2 — SILVER: plan i wprowadzenie do pandas

Data utworzenia: 2026-07-27

---

## Najpierw: co to znaczy „silver"

W etapie BRONZE mówiliśmy: bronze to szuflada z paragonami. Wrzucasz je,
nie ruszasz, nie poprawiasz.

**Silver to ten sam stos paragonów, ale teraz siadasz i robisz z niego porządek.**
Przepisujesz je do jednego zeszytu. Poprawiasz literówki. Wyrzucasz te same
paragony, jeśli przypadkiem wpadły dwa razy. Jeśli na jakimś brakuje kwoty —
decydujesz, czy go pominąć, czy dopisać szacunkową wartość.

Czego **nie robisz** jeszcze w zeszycie: nie liczysz sumy wydatków, nie
sprawdzasz, w którym miesiącu wydałeś najwięcej. To dopiero etap GOLD.

Silver to same porządki. Ale to najważniejsze porządki w całym projekcie —
każdy błąd, który tu przeoczysz, zepsuje wszystkie dalsze wyliczenia.

---

## Co dokładnie jest „brudne" w naszych danych

Sprawdziłem pliki w `companies/`. Konkretne rzeczy do naprawienia w etapie Silver:

1. **Data i cena to tekst, nie prawdziwe typy danych.** Plik zawiera linie
   jak `2023-07-24 00:00:00, 12.34`. Dla komputera to na razie ciąg liter,
   nie data i nie liczba — mimo że tak wygląda dla Ciebie.
2. **Możliwe braki danych.** Yahoo Finance czasem nie ma ceny zamknięcia dla
   jakiegoś dnia (zwraca `null` w JSON) — po zapisie do pliku wygląda to jak
   tekst `None` zamiast liczby. Zobaczymy, czy to się zdarza w Twoich plikach.
3. **Trzy osobne pliki zamiast jednej tabeli.** Masz `CBF.WA.txt`, `XTB.WA.txt`,
   `SNT.WA.txt` — każdy osobno. Do dalszej pracy (i do etapu GOLD) potrzebujemy
   **jednej** tabeli ze wszystkimi trzema spółkami, z kolumną mówiącą, który
   wiersz do kogo należy.
4. **Godzina zawsze `00:00:00`.** To niepotrzebny balast w dacie — dane są
   dzienne, godzina nic nie wnosi. Nie musimy jej koniecznie usuwać, ale
   warto to zauważyć.
5. **Brak nazw kolumn.** Plik `.txt` nie mówi, że pierwsza wartość to data,
   a druga to cena — to wiesz tylko Ty, bo pisałeś program. Tabela powinna
   mieć nazwane kolumny.
6. **Duplikaty (do sprawdzenia).** Obecnie plik się nadpisuje przy każdym
   pobraniu, więc duplikatów raczej nie będzie — ale nauczymy się je wykrywać,
   bo to standardowa umiejętność przy pracy z danymi.

---

## Wielka nowa idea: „wektoryzacja" zamiast pętli `for`

To jest **najważniejsza zmiana myślenia** w tym etapie, więc poświęćmy jej
osobną sekcję.

Do tej pory, żeby coś zrobić z każdym elementem listy, pisałeś pętlę:

```python
ceny_tekst = ["12.34", "15.60", "9.80"]
ceny_liczby = []
for c in ceny_tekst:
    ceny_liczby.append(float(c))
```

W pandas **nie piszesz pętli**. Mówisz: „zamień całą kolumnę na liczby" —
i pandas robi to za Ciebie, dla wszystkich wierszy naraz:

```python
tabela["cena"] = tabela["cena"].astype(float)
```

To się nazywa **wektoryzacja** (ang. *vectorized operation*) — operacja na
całej kolumnie na raz, zamiast na jednym elemencie po drugim. Jest szybsza
i kod jest krótszy. Ale to zmiana przyzwyczajenia: zamiast myśleć
„co zrobić z jednym elementem, żeby powtórzyć to w pętli", myślisz
„co zrobić z całą kolumną naraz".

To będzie się przewijać przez cały etap Silver.

---

## Instalacja

W aktywnym `.venv` (tym samym, gdzie masz `requests`):

```bash
pip install pandas
```

Import na górze pliku, zwyczajowo pod skróconą nazwą:

```python
import pandas as pd
```

`pd` to tylko **przyjęty w całym świecie Pythona skrót** — każdy, kto zna
pandas, rozpozna `pd.` i będzie wiedział, o co chodzi.

---

## Podstawy: `DataFrame` i `Series`

Dwa nowe słowa, których będziesz używał bez przerwy:

- **`DataFrame`** — cała tabela. Wiersze i kolumny, jak w Excelu. To główny
  obiekt, na którym pracujesz.
- **`Series`** — **jedna kolumna** z tabeli (albo jeden wiersz). Kiedy
  wyciągasz z `DataFrame` jedną kolumnę, dostajesz `Series`.

```python
tabela["cena"]        # to jest Series (jedna kolumna)
tabela[["cena", "data"]]   # to jest DataFrame (dwie kolumny, podwójny nawias!)
```

Zapamiętaj: **jeden nawias kwadratowy z jedną nazwą → Series. Lista nazw
w nawiasie → DataFrame.** To częsty błąd na start.

Każda kolumna w `DataFrame` ma **jeden typ danych** (ang. `dtype`) — albo
same liczby, albo same daty, albo same teksty. Nie może być pomieszane
w jednej kolumnie. `.dtypes` pokazuje Ci, jaki typ ma każda kolumna.

---

## Ściąga — najważniejsze funkcje pandas na Silver

Przykłady na **innych danych** niż Twój projekt — wyobraź sobie budkę
z lodami nad morzem, która zapisuje sprzedaż:

```python
import pandas as pd

dane = {
    "data":  ["2026-06-01", "2026-06-01", "2026-06-02", "2026-06-02", "2026-06-02"],
    "smak":  ["waniliowe", "czekoladowe", "waniliowe", "czekoladowe", "waniliowe"],
    "cena":  ["8.50", "9.00", "8.50", None, "8.50"],
    "ilosc": [12, 8, 15, 10, 15],
}
lody = pd.DataFrame(dane)
```

### 1. Wczytanie danych z pliku

```python
tabela = pd.read_csv("plik.txt", header=None, names=["data", "cena"])
```
- `header=None` — mówi pandas, że plik **nie ma** wiersza z nazwami kolumn
  (dokładnie jak Twoje pliki w `companies/`).
- `names=[...]` — Ty nadajesz nazwy kolumn.
- Uwaga na Twój format: piszesz `f"{data}, {c}\n"` — po przecinku jest
  **spacja**. Dodaj `skipinitialspace=True`, żeby pandas ją zignorował.

### 2. Pierwsze spojrzenie na dane

| Funkcja | Co pokazuje |
|---|---|
| `lody.head()` | pierwsze 5 wierszy |
| `lody.tail()` | ostatnie 5 wierszy |
| `lody.info()` | liczba wierszy, nazwy kolumn, ile brakuje danych, jaki typ ma kolumna |
| `lody.describe()` | dla kolumn liczbowych: średnia, min, max, itd. — szybki test „czy dane wyglądają sensownie" |
| `lody.shape` | krotka `(liczba_wierszy, liczba_kolumn)` |
| `lody.dtypes` | typ danych każdej kolumny |
| `lody.columns` | lista nazw kolumn |

### 3. Wybieranie kolumn i wierszy

```python
lody["cena"]                      # jedna kolumna (Series)
lody[["data", "cena"]]            # kilka kolumn (DataFrame)
lody.loc[0]                       # wiersz o indeksie 0
lody.iloc[0]                      # wiersz na pozycji 0 (to samo, gdy indeks jest domyślny)
lody[lody["ilosc"] > 10]          # tylko wiersze, gdzie sprzedano więcej niż 10 sztuk
```
Ten ostatni przykład to **filtrowanie** — bardzo częsta operacja. Czytaj to
tak: „z tabeli `lody` weź tylko te wiersze, gdzie `ilosc` jest większa niż 10".

### 4. Naprawa typów danych

```python
lody["data"] = pd.to_datetime(lody["data"])
lody["cena"] = pd.to_numeric(lody["cena"], errors="coerce")
```
- `pd.to_datetime(...)` — zamienia tekst na prawdziwą datę. To odpowiednik
  `datetime.strptime()`, którego już używałeś w `test_plikow.py`, tylko
  działa na **całej kolumnie naraz**, nie na jednym tekście.
- `pd.to_numeric(..., errors="coerce")` — zamienia tekst na liczbę.
  `errors="coerce"` znaczy: „jeśli coś się nie da zamienić, nie wywalaj
  programu — wstaw `NaN` (brak danych) w to miejsce". To bezpieczniejsze
  niż `.astype(float)`, które przy złej wartości rzuci błąd i przerwie program.

### 5. Braki danych (`NaN`)

`NaN` (*Not a Number*) to specjalna wartość pandas oznaczająca „tu nic nie ma".

```python
lody.isna()                # tabela True/False — gdzie są braki
lody["cena"].isna().sum()  # ile braków w kolumnie "cena"
lody.dropna()              # usuń wiersze, gdzie jest jakikolwiek brak
lody.fillna(0)             # wstaw 0 zamiast braków (albo inną wartość)
```
`dropna()` czy `fillna()`? To decyzja, nie ma jednej dobrej odpowiedzi —
zależy, czy wolisz stracić dzień danych, czy wstawić coś w zastępstwie.
Zdecydujesz sam, gdy zobaczysz, ile braków faktycznie masz.

### 6. Duplikaty

```python
lody.duplicated()           # True przy wierszu, który jest kopią wcześniejszego
lody.duplicated().sum()     # ile duplikatów
lody.drop_duplicates()      # usuń powtórzone wiersze
```

### 7. Łączenie kilku tabel w jedną

```python
cbf = pd.read_csv("companies/CBF.WA.txt", header=None, names=["data", "cena"])
cbf["spolka"] = "CBF"

xtb = pd.read_csv("companies/XTB.WA.txt", header=None, names=["data", "cena"])
xtb["spolka"] = "XTB"

wszystko = pd.concat([cbf, xtb], ignore_index=True)
```
- `tabela["spolka"] = "CBF"` — dodaje **nową kolumnę**, z tą samą wartością
  w każdym wierszu. Przyda się, żeby po połączeniu wiedzieć, który wiersz
  do kogo należy.
- `pd.concat([...])` — skleja kilka tabel jedna pod drugą (tyle samo kolumn,
  więcej wierszy).
- `ignore_index=True` — ponumeruj wiersze na nowo od zera, zamiast zachować
  stare numery z każdej osobnej tabeli (inaczej miałbyś np. dwa wiersze
  o numerze `0`).

### 8. Sortowanie

```python
lody.sort_values("data")                    # rosnąco po dacie
lody.sort_values(["smak", "data"])          # najpierw po smaku, potem po dacie
```

### 9. Zapis wyniku

```python
lody.to_csv("czyste_dane.csv", index=False)
```
`index=False` jest ważne — bez tego pandas dopisze dodatkową kolumnę
z numerami wierszy, której nie chcesz w pliku wynikowym.

---

## Podział na sesje

Jedna sesja = jeden dzień = 1,5–2 godziny. **Jedna nowa rzecz na sesję** —
tak jak w Bronze.

### Sesja 1 — Pierwsze wczytanie danych

**Co robisz:** instalujesz pandas, wczytujesz **jeden** plik (np. `CBF.WA.txt`)
przez `pd.read_csv(...)`, oglądasz wynik przez `.head()`, `.info()`, `.dtypes`.

**Nowa rzecz:** `DataFrame`, `pd.read_csv` z `header=None` i `names=[...]`.

**Skąd wiesz, że gotowe:** widzisz tabelę z dwiema nazwanymi kolumnami.
Prawdopodobnie zauważysz, że `cena` ma typ `object` (czyli tekst), nie
`float` — to normalne, naprawiamy to w następnej sesji.

---

### Sesja 2 — Naprawa typów danych

**Co robisz:** zamieniasz kolumnę z datą przez `pd.to_datetime`, kolumnę
z ceną przez `pd.to_numeric(..., errors="coerce")`.

**Co już umiesz:** ideę konwersji typu znasz z `test_plikow.py`
(`datetime.strptime`, `float(...)`). Tu robisz to samo, ale na całej kolumnie.

**Nowa rzecz:** wektoryzacja (patrz sekcja wyżej), `errors="coerce"`.

**Skąd wiesz, że gotowe:** `.dtypes` pokazuje `datetime64` dla daty
i `float64` dla ceny.

---

### Sesja 3 — Braki danych

**Co robisz:** sprawdzasz przez `.isna().sum()`, ile braków jest w każdej
kolumnie. Decydujesz — i wykonujesz — `.dropna()` albo `.fillna(...)`.

**Nowa rzecz:** `NaN`, różnica między `dropna` a `fillna`.

**Skąd wiesz, że gotowe:** `.isna().sum()` pokazuje zero braków (po naprawie).

---

### Sesja 4 — Duplikaty

**Co robisz:** sprawdzasz `.duplicated().sum()`, usuwasz duplikaty jeśli
jakieś są przez `.drop_duplicates()`.

**Nowa rzecz:** wykrywanie identycznych wierszy.

**Skąd wiesz, że gotowe:** `.duplicated().sum()` daje `0`.

---

### Sesja 5 — Trzy spółki w jednej tabeli

**Co robisz:** wczytujesz trzy pliki (pętla `for tick in ticker`, którą już
znasz), dla każdej tabeli dodajesz kolumnę `spolka` z nazwą tickera, potem
`pd.concat([...])`.

**Co już umiesz:** pętlę `for` po liście tickerów — to nic nowego.

**Nowa rzecz:** dodawanie nowej kolumny (`tabela["spolka"] = tick`),
`pd.concat`.

**Skąd wiesz, że gotowe:** jedna tabela, `.shape` pokazuje sumę wierszy
z trzech plików, kolumna `spolka` ma trzy różne wartości.

---

### Sesja 6 — Sortowanie i sprawdzenie całości

**Co robisz:** sortujesz połączoną tabelę przez `.sort_values(["spolka", "data"])`.
Patrzysz na `.describe()` — czy ceny wyglądają sensownie (np. żadna nie jest
ujemna albo zerowa).

**Nowa rzecz:** sortowanie po kilku kolumnach naraz, `.describe()` jako
szybki test sensowności danych.

**Skąd wiesz, że gotowe:** dane w tabeli idą chronologicznie w obrębie
każdej spółki, `.describe()` nie pokazuje nic dziwnego.

---

### Sesja 7 — Zapis i zamknięcie etapu

**Co robisz:** zapisujesz czystą tabelę przez `.to_csv(..., index=False)`.
Aktualizujemy `README.md`, dziennik, `CLAUDE.md`. Commit i push.

**Nowa rzecz:** `index=False` przy zapisie.

**Skąd wiesz, że gotowe:** nowy plik z czystą tabelą leży w repo i jest
widoczny na GitHubie.

---

## Ile to potrwa

Siedem sesji, około 10–14 godzin. Przy 1,5–2 h dziennie: **około tygodnia** —
zgodnie z pierwotnym szacunkiem z `Plan-ogolny.md`.

Jeśli któraś sesja zajmie dwa dni — to normalne, tak samo jak w Bronze.

---

## Gdzie zapisać wynik

Do ustalenia na Sesji 1 lub 7 — propozycja: nowy folder `silver/` w folderze
projektu, jeden plik `dane_czyste.csv` z połączoną tabelą trzech spółek.
Nazwa robocza, można zmienić.

---

## Czego NIE robimy na tym etapie

- ❌ liczenie zmian procentowych, średnich, trendów — to etap **GOLD**
- ❌ wykresy — to etap 4 („Pokazanie wyniku")
- ❌ nowe spółki — zostajemy przy trzech
- ❌ automatyczne, cykliczne pobieranie — nie teraz
- ❌ klasy — dalej niepotrzebne

---

## Powiązane notatki

- [[Plan-ogolny]] — cały projekt
- [[Plan-01-bronze]] — poprzedni etap, dla porównania stylu pracy
- [[Slownik]] — dopisuj tu nowe słowa (`DataFrame`, `Series`, `NaN`, `dtype`, `wektoryzacja`...)
