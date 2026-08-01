# Etap 3 — GOLD: liczenie i gotowe odpowiedzi

Data utworzenia: 2026-08-01

---

## Najpierw: co to znaczy „gold"

W etapie SILVER mówiliśmy: to ten sam stos paragonów, ale przepisany do
jednego zeszytu, poprawiony, posortowany. Zeszyt był czysty — ale niczego
z niego jeszcze nie policzyłeś.

**Gold to moment, w którym otwierasz ten zeszyt i liczysz.** Ile wydałeś
w sumie. W którym miesiącu najwięcej. Czy wydatki rosły czy malały.
U nas, na danych giełdowych, to te same pytania w innym przebraniu:

- o ile procent zmieniła się cena każdej spółki,
- która spółka rosła najszybciej,
- w którym miesiącu było najwięcej wahań.

Jak podsumowuje `Plan-ogolny.md`: *„Efekt: tabela z gotowymi odpowiedziami,
nie z surowymi liczbami."* To jest różnica między Silver a Gold — Silver
dawał Ci czyste dane, Gold ma dać Ci **wnioski**.

---

## Co dokładnie policzymy w naszych danych

Sprawdziłem `silver/clean_data.csv`. Kilka faktów, które warto znać, zanim
zaczniesz liczyć:

- **2250 wierszy, trzy spółki, po 750 dni każda**, dokładnie ten sam zakres
  dat dla wszystkich trzech: 24.07.2023–24.07.2026.
- **Ceny są w zupełnie różnych skalach.** XTB.WA: 29,62–138,00 zł. CBF.WA:
  70,00–215,50 zł. SNT.WA: 58,00–394,00 zł.
- W danych są już widoczne pojedyncze duże skoki dzienne — np. SNT.WA
  spadło jednego dnia w czerwcu 2025 o około 16%, XTB.WA urosło jednego
  dnia w styczniu 2024 o ponad 14%. To nie błędy w danych — małe i średnie
  spółki GPW potrafią się tak zachowywać. Zobaczysz te liczby sam w Sesji 2,
  kiedy policzysz zmianę dzienną — nie zdziw się nimi.

### Dlaczego procent, nie złotówki?

SNT.WA kosztuje kilka razy więcej niż XTB.WA. Gdyby obie spółki zyskały
„10 zł" jednego dnia, dla XTB byłby to ogromny skok (kilkanaście procent),
a dla SNT prawie nic (kilka procent). Same złotówki nie dają się uczciwie
porównać między spółkami o różnej cenie. **Zmiana procentowa** nie zależy
od tego, ile kosztuje jedna akcja — dlatego to jej będziemy liczyć przez
cały ten etap, nie różnic w złotówkach.

---

## Wielka nowa idea: `groupby` — myślenie w grupach

To jest **najważniejsza zmiana myślenia** w tym etapie, tak jak wektoryzacja
była nią w Silver.

Do tej pory liczyłeś na całej kolumnie naraz (wektoryzacja) albo wczytywałeś
pliki w pętli po liście tickerów. `groupby` to trzeci sposób myślenia:
**„podziel tabelę na grupy, policz coś osobno w każdej grupie, złóż wynik
z powrotem w jedną tabelę"** — bez pisania pętli samemu, pandas robi to za
Ciebie.

Przykład na budce z lodami (ten sam przykład, którego już znasz z Silver):

```python
lody.groupby("smak")["ilosc"].sum()
```

Jedna linijka — a dostajesz sumę sprzedaży osobno dla waniliowych, osobno
dla czekoladowych. Bez pętli `for smak in smaki: ...`.

**Pułapka, o której musisz wiedzieć zawczasu.** Twoja tabela `dane` ma trzy
spółki sklejone jedna pod drugą (`pd.concat` z Silver). Jeśli policzysz
zmianę procentową na całej kolumnie `cena` **bez** grupowania, pandas
policzy „zmianę" także tam, gdzie kończy się jedna spółka a zaczyna druga —
np. porówna ostatni dzień CBF.WA z pierwszym dniem SNT.WA, jakby to był ten
sam ciąg cen. To nie jest realna zmiana, to dwie różne firmy obok siebie.
**Zasada: zawsze `groupby("spolka")` przed liczeniem zmiany.**

**Sidekick do zapamiętania:** po `groupby(...)` kolumna, po której
grupowałeś, staje się nowym **indeksem** tabeli wynikowej, nie zwykłą
kolumną. `.reset_index()` zamienia ją z powrotem w zwykłą kolumnę. Będzie
Ci to potrzebne w Sesji 3 i 6 — jeśli zapomnisz, `.merge()` czy
`.sort_values()` na tej kolumnie nie zadziała tak, jak oczekujesz.

---

## Ściąga — najważniejsze funkcje pandas na Gold

Przykłady znowu na budce z lodami, nie na danych giełdowych:

```python
import pandas as pd

dane = {
    "data":  ["2026-06-01", "2026-06-02", "2026-06-03", "2026-06-01", "2026-06-02", "2026-06-03"],
    "smak":  ["waniliowe", "waniliowe", "waniliowe", "czekoladowe", "czekoladowe", "czekoladowe"],
    "cena":  [8.50, 9.00, 8.80, 9.00, 9.20, 8.90],
}
lody = pd.DataFrame(dane)
lody["data"] = pd.to_datetime(lody["data"])
```

### 1. `groupby` — dzielenie na grupy

```python
lody.groupby("smak")["cena"].mean()
```
Średnia cena osobno dla każdego smaku. Patrz sekcja wyżej.

### 2. `pct_change()` — zmiana procentowa

```python
lody["zmiana"] = lody.groupby("smak")["cena"].pct_change() * 100
```
Zmiana względem **poprzedniego wiersza w tej samej grupie**. Pierwszy dzień
każdego smaku dostaje `NaN` — nie ma dnia wcześniej, więc nie ma z czym
porównać.

### 3. `.dt.to_period("M")` — wyciąganie miesiąca

```python
lody["miesiac"] = lody["data"].dt.to_period("M")
```
Z pełnej daty zostaje „rok-miesiąc" (np. `2026-06`). Ważne przy danych na
kilka lat: dzięki temu marzec 2024 i marzec 2025 liczą się jako dwa różne
miesiące, nie jeden.

### 4. `.std()` — odchylenie standardowe

```python
lody.groupby("smak")["zmiana"].std()
```
Jedna liczba mówiąca, jak bardzo wartości „skaczą" wokół średniej. Mała
`.std()` = ceny/zmiany są stabilne. Duża `.std()` = dużo wahań.

### 5. `.agg(["first", "last"])` — pierwsza i ostatnia wartość w grupie

```python
lody.groupby("smak")["cena"].agg(["first", "last"])
```
Dostajesz małą tabelę: dla każdego smaku pierwsza i ostatnia zanotowana
cena. Stąd już blisko do policzenia zmiany całkowitej (jak we wzorze
z Sesji 3).

### 6. `.reset_index()` — indeks z powrotem jako kolumna

```python
wynik = lody.groupby("smak")["cena"].mean()   # "smak" jest teraz indeksem
wynik = wynik.reset_index()                   # "smak" wraca jako zwykła kolumna
```

### 7. `.merge()` — sklejanie tabel obok siebie

```python
srednie = lody.groupby("smak")["cena"].mean().reset_index()
sprzedaz = lody.groupby("smak")["cena"].count().reset_index()
polaczone = srednie.merge(sprzedaz, on="smak")
```
Różnica względem `pd.concat` z Silver: `concat` sklejał tabele **jedna pod
drugą** (więcej wierszy, te same kolumny). `merge` skleja **obok siebie**
(te same wiersze co do klucza, więcej kolumn) — dopasowując wiersze po
wspólnej kolumnie (tu: `smak`).

### 8. `.round()` — zaokrąglanie

```python
lody["zmiana"] = lody["zmiana"].round(2)
```
Dwa miejsca po przecinku wystarczą dla procentów — czytelniejszy wynik
końcowy.

---

## Podział na sesje

Jedna sesja = jeden dzień = 1,5–2 godziny. **Jedna nowa rzecz na sesję** —
tak jak w Bronze i Silver.

### Sesja 1 — Wczytanie danych z Silver

**Co robisz:** nowy plik `kod/gold 1.py`. Wczytujesz `silver/clean_data.csv`
przez `pd.read_csv(...)`. Sprawdzasz `.shape` i `.dtypes`.

**Co już umiesz:** `pd.read_csv`, `.head()`, `.info()` — z Silver Sesja 1.

**Nowa rzecz:** zrozumienie, że **CSV nie zapamiętuje typów danych**. Mimo
że w Silver kolumna `data` była już `datetime64`, po zapisie do CSV
i ponownym wczytaniu wróci jako zwykły tekst. Musisz znowu zrobić
`pd.to_datetime()` — to nie jest cofnięcie się, to po prostu tak działa
format CSV (jest tylko tekstem, nigdy nie zapisuje typów).

**Skąd wiesz, że gotowe:** `.shape` pokazuje `(2250, 3)`. Po konwersji
`.dtypes` pokazuje `cena` jako `float64` i `data` jako `datetime64`.

---

### Sesja 2 — Dzienna zmiana procentowa

**Co robisz:** dodajesz kolumnę:
```python
dane["zmiana_proc"] = dane.groupby("spolka")["cena"].pct_change() * 100
```

**Co już umiesz:** dodawanie nowej kolumny (`tabela["nazwa"] = ...`) —
z Silver Sesja 5.

**Nowa rzecz:** `groupby` razem z `pct_change` — i pułapka opisana w sekcji
„Wielka nowa idea" wyżej (dlaczego nie liczyć zmiany na całej kolumnie bez
grupowania).

**Skąd wiesz, że gotowe:** pierwszy wiersz **każdej** spółki ma `NaN`
w `zmiana_proc` (nie ma dnia wcześniej w tej grupie). Reszta wierszy ma
liczby w rozsądnym zakresie — bez żadnego „przeskoku" dokładnie w miejscu,
gdzie w tabeli kończy się jedna spółka a zaczyna druga.

---

### Sesja 3 — Która spółka rosła najszybciej

**Co robisz:**
```python
wzrost = dane.groupby("spolka")["cena"].agg(["first", "last"])
wzrost["zmiana_calkowita_proc"] = (wzrost["last"] - wzrost["first"]) / wzrost["first"] * 100
wzrost = wzrost.reset_index().sort_values("zmiana_calkowita_proc", ascending=False)
```

**Co już umiesz:** wzór na zmianę procentową (matematyka), `.sort_values()`
z Silver Sesja 6.

**Nowa rzecz:** `.agg(["first", "last"])` po `groupby` — dostajesz małą
tabelę (jeden wiersz na spółkę) z pierwszą i ostatnią ceną z całego okresu.

**Skąd wiesz, że gotowe:** tabela z 3 wierszami i kolumną
`zmiana_calkowita_proc`, posortowana malejąco. Jednym rzutem oka widzisz,
która spółka urosła najbardziej od 24.07.2023 do 24.07.2026.

---

### Sesja 4 — Wyciąganie miesiąca z daty

**Co robisz:**
```python
dane["miesiac"] = dane["data"].dt.to_period("M")
```

**Co już umiesz:** dodawanie kolumny, `pd.to_datetime` z Silver.

**Nowa rzecz:** akcesor `.dt` — sposób wyciągania części z kolumny typu
data (miesiąc, rok, dzień tygodnia...). Używasz konkretnie
`.dt.to_period("M")`, a nie samego `.dt.month`, żeby marzec 2024 i marzec
2025 liczyły się jako dwa różne miesiące, nie jeden.

**Skąd wiesz, że gotowe:** nowa kolumna `miesiac` z wartościami typu
`2023-07`, `2023-08`... `dane["miesiac"].nunique()` pokazuje około 36
(3 lata × 12 miesięcy).

---

### Sesja 5 — W którym miesiącu było najwięcej wahań

**Co robisz:**
```python
zmiennosc = dane.groupby(["spolka", "miesiac"])["zmiana_proc"].std().reset_index()
zmiennosc = zmiennosc.sort_values("zmiana_proc", ascending=False)
```

**Co już umiesz:** `groupby` z Sesji 2, `.sort_values()` i `.reset_index()`
z Sesji 3.

**Nowa rzecz:** grupowanie po **dwóch kolumnach naraz**
(`["spolka", "miesiac"]`) — osobne odchylenie standardowe dla każdej pary
spółka+miesiąc. `.std()` jako miara wahania: im większe, tym bardziej
„nerwowa" była cena w tym miesiącu.

**Skąd wiesz, że gotowe:** tabela z kolumnami `spolka`, `miesiac`,
`zmiana_proc` (tu: wartość odchylenia standardowego), posortowana malejąco.
Pierwszy wiersz pokazuje najbardziej zmienny miesiąc spośród wszystkich
spółek i miesięcy razem.

---

### Sesja 6 — Złożenie gotowych odpowiedzi w jedną tabelę

**Co robisz:** z tabeli `zmiennosc` wyciągasz **jeden**, najbardziej zmienny
miesiąc na spółkę:
```python
najbardziej_zmienne = zmiennosc.sort_values("zmiana_proc", ascending=False).groupby("spolka").head(1)
```
Potem łączysz to z tabelą `wzrost` z Sesji 3:
```python
podsumowanie = wzrost.merge(najbardziej_zmienne, on="spolka")
```

**Co już umiesz:** `groupby`, `.sort_values()` — wszystko z poprzednich
sesji.

**Nowa rzecz:** `.merge()` — sklejenie dwóch tabel **obok siebie** po
wspólnej kolumnie (`spolka`). Różnica względem `pd.concat` z Silver:
`concat` sklejał tabele jedna pod drugą (więcej wierszy), `merge` skleja
je bok w bok (więcej kolumn), dopasowując wiersze po kluczu.

**Skąd wiesz, że gotowe:** jedna tabela, 3 wiersze (po jednym na spółkę),
z kolumnami: zmiana całkowita, najbardziej zmienny miesiąc, wartość
odchylenia w tym miesiącu.

---

### Sesja 7 — Zapis wyników i zamknięcie etapu

**Co robisz:** zapisujesz dwa pliki:
```python
dane.to_csv("gold/dane_z_wskaznikami.csv", index=False)
podsumowanie.to_csv("gold/podsumowanie.csv", index=False)
```
Pierwszy to pełna tabela (2250 wierszy) z dodaną kolumną `zmiana_proc` —
przyda się w Etapie 4 do wykresów. Drugi to gotowe odpowiedzi z Sesji 6.
Aktualizujesz `README.md`, dziennik, `CLAUDE.md`. Commit i push.

**Co już umiesz:** `.to_csv(..., index=False)` z Silver Sesja 7.

**Nowa rzecz:** brak — ta sesja to wykonanie i porządki, nie nowa koncepcja
pandas (tak samo jak Sesja 7 w Silver).

**Skąd wiesz, że gotowe:** oba pliki leżą w `gold/`, widoczne na GitHubie
po pushu. **Etap GOLD zamknięty.**

---

## Ile to potrwa

Siedem sesji, podobnie jak Silver — około 10–14 godzin. Przy 1,5–2 h
dziennie to około tygodnia, choć pasuje też do szacunku 4–5 dni
z `Plan-ogolny.md`, jeśli pójdzie kilka sesji dziennie (tak jak Sesje 1–4
Silver zrobione jednego dnia).

Jeśli któraś sesja zajmie dwa dni — to normalne, tak samo jak dotąd.

---

## Gdzie zapisać wynik

Propozycja (nazwa robocza, można zmienić): nowy folder `gold/`, dwa pliki —
`dane_z_wskaznikami.csv` (pełne dane plus dzienna zmiana procentowa, baza
pod przyszłe wykresy) i `podsumowanie.csv` (3 wiersze gotowych odpowiedzi —
to jest ta „tabela z gotowymi odpowiedziami" z `Plan-ogolny.md`).

---

## Czego NIE robimy na tym etapie

- ❌ wykresy — to etap 4 („Pokazanie wyniku")
- ❌ przewidywanie przyszłych cen — to zupełnie inny temat (modele
  predykcyjne), nie ma go jeszcze na mapie projektu
- ❌ więcej niż trzy spółki — to plan „co dalej po miesiącu"
  z `Plan-ogolny.md`
- ❌ automatyczne, codzienne odświeżanie danych — jw., późniejszy etap
- ❌ poprawki w `kod/silver 1.py` — osobna, opcjonalna sprawa (zobacz
  rozmowę o zamknięciu Silver), nie część nauki Gold

---

## Powiązane notatki

- [[Plan-ogolny]] — cały projekt, tu zdefiniowany zakres etapu Gold
- [[Plan-02-silver]] — poprzedni etap, dane wejściowe do Gold
- [[Slownik]] — dopisuj tu nowe słowa: `groupby`, `pct_change`, odchylenie
  standardowe, `merge`, zmienność/wolatylność. Przy okazji warto domknąć
  też zaległe z Silver: `Series`, `NaN`, `dtype`, wektoryzacja — plan Silver
  o nich wspominał, ale nie trafiły jeszcze do słownika.
