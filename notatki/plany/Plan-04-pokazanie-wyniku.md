# Etap 4 — Pokazanie wyniku (i rozbudowa projektu)

Data utworzenia: 2026-08-10

---

## Uwaga na start: ten plan jest większy niż zapowiadał `Plan-ogolny.md`

`Plan-ogolny.md` opisywał Etap 4 jako coś małego: „wykres i krótki opis,
plus porządny README" — 3 dni. Gracjan poprosił o rozszerzenie: wykresy
w Pythonie **i** w Power BI, wstęp do automatyzacji pobierania danych, i
ogólną rozbudowę projektu pod portfolio. To już nie mieści się w 3 dniach —
realistycznie to około **3 tygodnie** przy dotychczasowym tempie (patrz
„Ile to potrwa" na końcu).

**Ten plan jest żywy.** Cztery części poniżej to punkt startowy — Gracjan
będzie dopisywał kolejne pomysły w rozmowie, ten plik będzie rósł.

---

## Najpierw: co to znaczy „pokazanie wyniku"

Bronze to była szuflada z paragonami. Silver — poukładany zeszyt. Gold —
policzone sumy w tym zeszycie. Ale zeszyt z liczbami wciąż leży tylko na
Twoim biurku. **Etap 4 to moment, w którym ktoś inny — pracodawca, kolega,
Ty za pół roku — otwiera ten zeszyt i musi zrozumieć go bez pytania Cię
o nic.**

To dwa osobne zadania, i osobno je nazwiemy:

1. **Od kodu do komunikatu.** Liczba `408.47` nic nie mówi sama z siebie.
   Wykres, na którym widać, że jedna linia wystrzeliwuje w górę, mówi to
   samo w pół sekundy. Wykresy (Część A, B) i opis wniosków (Część D) to
   nie „dodatek na koniec" — to tłumaczenie Twojej pracy na język, który
   rozumie ktoś, kto nigdy nie widział Twojego kodu.
2. **Program, który działa bez Ciebie.** Do tej pory zawsze Ty klikałeś
   „uruchom". Automatyzacja (Część C) to zmiana tego myślenia: komputer sam
   wie, kiedy ma pobrać nowe dane, Ty tylko sprawdzasz wynik.

---

## Struktura tego etapu — cztery części

| Część | Co | Ile sesji |
|---|---|---|
| **A** | Wykresy w Pythonie (`matplotlib`) | 5 |
| **B** | Wykresy i dashboard w Power BI | 4 |
| **C** | Wstęp do automatyzacji pobierania danych | 3 |
| **D** | Domknięcie: README pod portfolio, opis wniosków | 3 |

Kolejność A → B → C → D jest zalecana (najpierw fundament w Pythonie, bo
na nim opiera się reszta), ale nieprzymuszona — jeśli w trakcie zechcesz
przeskoczyć, to nie problem.

---

# Część A — Wykresy w Pythonie (`matplotlib`)

## Skąd bierzemy dane

Wszystko, czego potrzebujesz, już istnieje w `gold/dane_dzienne.csv`
(cena, zmiana procentowa, miesiąc — dzień po dniu) i `gold/ranking.csv`
(gotowe podsumowanie na spółkę). Żadnego nowego liczenia w pandas nie
trzeba — Część A to wyłącznie **pokazywanie** tego, co już policzyłeś.

**Pułapka, którą już znasz z Gold Sesji 1:** CSV nie pamięta typów danych.
Kolumna `data` wróci jako tekst — znowu `pd.to_datetime(...)`, zanim
cokolwiek narysujesz.

## Instalacja

```bash
pip install matplotlib
```

```python
import matplotlib.pyplot as plt
```

`plt` to, tak jak `pd` dla pandas, przyjęty w całym świecie Pythona skrót.

## Ściąga — `matplotlib` na przykładzie budki z lodami

Ten sam przykład co w Silver i Gold, żeby nie mieszać nowej biblioteki
z nowymi danymi naraz:

```python
import pandas as pd
import matplotlib.pyplot as plt

dane = {
    "data": pd.to_datetime(["2026-06-01", "2026-06-02", "2026-06-03", "2026-06-04"]),
    "wanilia":   [12, 15, 9, 20],
    "czekolada": [8, 10, 14, 11],
}
lody = pd.DataFrame(dane)
```

### 1. Pierwszy wykres

```python
plt.plot(lody["data"], lody["wanilia"])
plt.show()
```
`plt.plot(x, y)` rysuje linię, `plt.show()` otwiera okno z wykresem.

### 2. Podpisy — żeby ktoś obcy zrozumiał, na co patrzy

```python
plt.plot(lody["data"], lody["wanilia"])
plt.title("Sprzedaż lodów waniliowych")
plt.xlabel("Data")
plt.ylabel("Sztuk sprzedanych")
plt.grid(True)
plt.show()
```

### 3. Kilka linii na jednym wykresie + legenda

```python
plt.plot(lody["data"], lody["wanilia"], label="Wanilia")
plt.plot(lody["data"], lody["czekolada"], label="Czekolada")
plt.legend()
plt.show()
```
`label=` nadaje nazwę serii, `plt.legend()` rysuje na wykresie skrzynkę,
która mówi, która linia to który smak.

### 4. Zapis do pliku

```python
plt.plot(lody["data"], lody["wanilia"])
plt.savefig("wykres.png", dpi=150)
plt.show()
```
**Kolejność ma znaczenie:** `savefig()` musi być **przed** `show()` —
`show()` czyści rysunek po zamknięciu okna, więc `savefig()` po nim
zapisałby pustą kartkę. `dpi=150` to jakość obrazu (więcej = ostrzejszy,
ale większy plik).

### 5. Wykres słupkowy — inny typ pytania, inny typ wykresu

```python
plt.bar(["Wanilia", "Czekolada"], [lody["wanilia"].sum(), lody["czekolada"].sum()])
plt.show()
```
Linia (`plot`) dobrze pokazuje **zmianę w czasie**. Słupki (`bar`) dobrze
pokazują **porównanie kilku kategorii obok siebie** — np. „która spółka
urosła najbardziej", nie „jak cena szła dzień po dniu".

---

## Podział na sesje — Część A

### Sesja A1 — Pierwszy wykres

**Co robisz:** instalujesz `matplotlib`, wczytujesz `gold/dane_dzienne.csv`,
naprawiasz `data` przez `pd.to_datetime`, filtrujesz jedną spółkę (np.
`dane[dane["spolka"] == "CBF.WA"]`), rysujesz `plt.plot(...)`.

**Co już umiesz:** filtrowanie wierszy — z Silver.

**Nowa rzecz:** `matplotlib`, `plt.plot`, `plt.show`.

**Skąd wiesz, że gotowe:** otwiera się okno z linią ceny CBF.WA w czasie.

---

### Sesja A2 — Podpisy i czytelność

**Co robisz:** dodajesz `plt.title`, `plt.xlabel`, `plt.ylabel`, `plt.grid`.

**Nowa rzecz:** myślenie o odbiorcy, który nie zna Twoich danych.

**Skąd wiesz, że gotowe:** wykres ma tytuł, opisane osie, siatkę —
zrozumiały bez patrzenia w kod.

---

### Sesja A3 — Trzy spółki na jednym wykresie

**Co robisz:** pętla `for spolka in dane["spolka"].unique():`, w każdym
obiegu `plt.plot(...)` dla jednej spółki z `label=spolka`, na końcu
`plt.legend()`.

**Co już umiesz:** pętla `for` po unikalnych wartościach.

**Nowa rzecz:** kilka serii na jednym wykresie, legenda.

**Skąd wiesz, że gotowe:** jeden wykres, trzy linie w różnych kolorach,
legenda mówi która jest która.

---

### Sesja A4 — Zapis do pliku

**Co robisz:** nowy folder `wykresy/`, `plt.savefig("wykresy/ceny.png",
dpi=150)` przed `plt.show()`.

**Nowa rzecz:** zapis wykresu jako plik zamiast tylko podglądu na ekranie.

**Skąd wiesz, że gotowe:** plik PNG istnieje w `wykresy/`, otwiera się,
wygląda tak samo jak okno z podglądu.

---

### Sesja A5 — Wykres słupkowy: która spółka urosła najbardziej

**Co robisz:** wczytujesz `gold/ranking.csv`, `plt.bar(...)` z kolumnami
`spolka` i `zmiana_caly_okres`, zapisujesz do `wykresy/`.

**Nowa rzecz:** `plt.bar`, wybór typu wykresu pod typ pytania (patrz ściąga
punkt 5).

**Skąd wiesz, że gotowe:** wykres słupkowy porównujący trzy spółki,
zapisany jako plik.

---

# Część B — Wykresy i dashboard w Power BI

## Co to jest Power BI, po ludzku

Wyobraź sobie Excela, który sam rysuje wykresy z Twoich danych i pozwala
Ci **klikać**, żeby je filtrować — bez pisania wzorów. To robi Power BI:
darmowe narzędzie od Microsoftu do budowania wykresów i „dashboardów"
(jedna strona z kilkoma wykresami naraz) przez przeciąganie myszką, nie
przez kod.

To inny sposób odpowiadania na te same pytania, które już umiesz zadać
w pandas — nie nowa teoria danych, tylko nowe narzędzie.

## Instalacja

Power BI Desktop — bezpłatny, do pobrania z Microsoft Store albo ze strony
`powerbi.microsoft.com/desktop`. Wymaga Windows (masz).

## Ściąga — nawigacja zamiast kodu

Power BI nie ma linijek kodu do ściągi — ma miejsca, w które klikasz:

| Chcesz zrobić | Gdzie szukać |
|---|---|
| Wczytać plik CSV | **Home → Get Data → Text/CSV** |
| Zobaczyć wczytane tabele | panel **Data** (ikona tabeli, prawy pasek) |
| Dodać wykres | panel **Visualizations** → wybierz typ (np. Line chart) |
| Powiedzieć wykresowi, jakie dane pokazać | przeciągnij nazwę kolumny z panelu **Data** w pole **Axis** / **Legend** / **Values** pod wizualizacją |
| Dodać filtr klikalny na całej stronie | wizualizacja **Slicer** |
| Zapisać/udostępnić | **File → Export** (PDF/obraz) albo **File → Publish** (konto Power BI, opcjonalne) |

## Podział na sesje — Część B

### Sesja B1 — Instalacja i import danych

**Co robisz:** instalujesz Power BI Desktop, `Get Data → Text/CSV`,
wczytujesz `gold/dane_dzienne.csv` i `gold/ranking.csv`.

**Nowa rzecz:** narzędzie BI zamiast kodu — dane importujesz klikaniem.

**Skąd wiesz, że gotowe:** obie tabele widoczne w panelu **Data**.

---

### Sesja B2 — Pierwszy wykres (Line chart)

**Co robisz:** dodajesz wizualizację **Line chart**, przeciągasz `data` na
**Axis**, `cena` na **Values**, `spolka` na **Legend**.

**Co już umiesz:** to samo pytanie co w Sesji A3 („cena w czasie, dla
każdej spółki") — inny sposób odpowiedzi.

**Nowa rzecz:** budowanie wykresu przeciąganiem pól (drag-and-drop).

**Skąd wiesz, że gotowe:** interaktywny wykres liniowy, trzy spółki, najazd
myszką pokazuje dokładną wartość.

---

### Sesja B3 — Dashboard: kilka wykresów i filtr

**Co robisz:** na tej samej stronie dodajesz drugi wizual (np. **Bar
chart** z `ranking.csv`), dodajesz **Slicer** filtrujący po `spolka`.

**Nowa rzecz:** kilka wykresów na jednej stronie, filtr działający na
wszystkie naraz (kliknięcie w jedną spółkę w Slicerze zmienia oba wykresy).

**Skąd wiesz, że gotowe:** jedna strona, 2+ wykresy, filtr, kliknięcie
w filtr widocznie zmienia oba wykresy jednocześnie.

---

### Sesja B4 — Eksport / publikacja

**Co robisz:** `File → Export → PDF` (albo obraz), lub — jeśli zechcesz
założyć darmowe konto Power BI — `File → Publish`.

**Nowa rzecz:** dzielenie się wynikiem z kimś, kto nie ma Power BI
zainstalowanego.

**Skąd wiesz, że gotowe:** masz plik albo link, który możesz pokazać
komuś bez instalowania czegokolwiek.

---

# Część C — Wstęp do automatyzacji pobierania danych

To jest **wstęp**, nie produkcyjny system z monitoringiem i alertami —
„powoli", jak zapowiedziałeś. Cel: zrozumieć ideę, zobaczyć, że działa.

## Ściąga — pojęcia

| Słowo | Co znaczy |
|---|---|
| **Pipeline** | łańcuch kroków, gdzie wyjście jednego jest wejściem następnego. U Ciebie: `Data ingestion 2.py` → `silver 1.py` → `gold 1.py`. Robiłeś to już ręcznie, tu to nazywamy. |
| **Harmonogram zadań (Task Scheduler)** | wbudowane w Windows narzędzie, które uruchamia program o wybranej porze — bez Twojego udziału. |
| **Wyzwalacz (trigger)** | reguła „kiedy": codziennie o 18:00, co tydzień w niedzielę, itd. |
| **Akcja** | reguła „co": jaki program/skrypt ma się uruchomić. |

## Podział na sesje — Część C

### Sesja C1 — Pipeline jako całość

**Co robisz:** bez nowego kodu — ręcznie uruchamiasz po kolei wszystkie
trzy skrypty (`Data ingestion 2.py` → `silver 1.py` → `gold 1.py`) od
zera, sprawdzasz że wynik się zgadza, zapisujesz gdzieś (np. na górze
`Data ingestion 2.py` w komentarzu, albo w README) dokładną kolejność.

**Nowa rzecz:** pojęcie „pipeline" — potwierdzasz, że cały łańcuch działa
od początku do końca bez ręcznych poprawek pomiędzy krokami.

**Skąd wiesz, że gotowe:** potrafisz odtworzyć cały łańcuch bez błędów,
od pustego stanu do świeżego `gold/`.

---

### Sesja C2 — Harmonogram Windows — pierwszy test

**Co robisz:** otwierasz Harmonogram zadań w Windows, tworzysz proste
testowe zadanie: uruchamia mały, nieszkodliwy skrypt (np. dopisujący
linijkę z aktualną datą/godziną do pliku tekstowego) o wybranej porze.

**Nowa rzecz:** harmonogram na poziomie systemu operacyjnego — wyzwalacze
i akcje, zupełnie osobne od Pythona.

**Skąd wiesz, że gotowe:** zadanie uruchomiło się samo, widzisz nową
linijkę w pliku testowym — bez klikania czegokolwiek ręcznie.

---

### Sesja C3 — Prawdziwy pipeline pod harmonogramem

**Co robisz:** podpinasz harmonogram pod prawdziwy skrypt (albo cały
łańcuch z Sesji C1), ustawiasz częstotliwość (codziennie albo raz
w tygodniu — dane giełdowe i tak się nie zmieniają w weekend, Twoja
decyzja).

**Nowa rzecz:** łączenie realnego kodu projektu z harmonogramem;
sprawdzanie, czy zadziałało, przez już istniejący `errors.log` i daty
modyfikacji plików w `companies/`.

**Skąd wiesz, że gotowe:** harmonogram uruchomił prawdziwy skrypt
samodzielnie przynajmniej raz — widać to po dacie modyfikacji plików.

---

# Część D — Domknięcie: portfolio

### Sesja D1 — README pod kątem pracodawcy

**Co robisz:** rozbudowujesz górę `README.md` — jasny, krótki opis „co to
za projekt i po co", wstawiasz jeden z zapisanych wykresów jako obrazek.

**Nowa rzecz:** pisanie dla kogoś, kto nigdy nie widział Twojego kodu i ma
30 sekund uwagi.

**Skąd wiesz, że gotowe:** ktoś obcy, czytając tylko początek README,
rozumie co robi projekt i widzi przynajmniej jeden wynik.

---

### Sesja D2 — Krótki opis wniosków

**Co robisz:** nowy plik (np. `notatki/Wnioski.md`) albo sekcja
w README — kilka zdań po ludzku: która spółka urosła najbardziej, który
miesiąc był najbardziej „nerwowy", co to może znaczyć.

**Nowa rzecz:** przejście od liczb do zdań — to, co w prawdziwej pracy
nazywa się „insight"/wniosek.

**Skąd wiesz, że gotowe:** tekst istnieje, napisany Twoimi słowami, ktoś
nietechniczny zrozumiałby go bez patrzenia w tabelę obok.

---

### Sesja D3 — Ostateczne porządki i zamknięcie etapu

**Co robisz:** przegląd `kod/` (zbędne `print()`, sensowne nazwy), commit
+ push wszystkiego, ostatnia aktualizacja README/CLAUDE.md/dziennika.

**Nowa rzecz:** brak — porządki, tak jak ostatnia sesja w Bronze/Silver/Gold.

**Skąd wiesz, że gotowe:** repo na GitHubie pokazuje kompletny projekt —
dane, kod, wykresy, dashboard, README, które broni się samo.

---

## Ile to potrwa

15 sesji, 1,5–2 h każda → **około 22–30 godzin**. Przy dotychczasowym
tempie to około **3 tygodnie** — znacznie więcej niż 3 dni z pierwotnego
`Plan-ogolny.md`, bo zakres jest teraz dużo większy (świadoma decyzja
Gracjana, nie poślizg).

---

## Gdzie zapisać wynik

- `wykresy/` — nowy folder, pliki `.png` z Części A.
- Plik Power BI (`.pbix`) z Części B — gdzie dokładnie (w repo czy poza
  nim) do ustalenia przy Sesji B1, kiedy będzie wiadomo, ile waży.
- `notatki/Wnioski.md` — opis wniosków z Sesji D2.

---

## Czego NIE robimy w tym etapie

- ❌ Databricks — osobny, późniejszy krok (to migracja całego pipeline'u
  do chmury, nie wykres — już był na liście „co dalej po miesiącu"
  w `Plan-ogolny.md`).
- ❌ więcej niż trzy spółki — jw., późniejszy krok.
- ❌ pełna produkcyjna automatyzacja (monitoring, powiadomienia o
  błędach, restarty) — Część C to świadomie tylko wstęp.
- ❌ przewidywanie przyszłych cen / modele ML — osobny temat, nie ma go
  jeszcze na mapie projektu.
- ❌ klasy — dalej niepotrzebne.

---

## Powiązane notatki

- [[Plan-ogolny]] — cały projekt, tu pierwotny (mniejszy) zarys Etapu 4
- [[Plan-03-gold]] — poprzedni etap, dane wejściowe do Części A i B
- [[Slownik]] — dopisuj tu nowe słowa: `matplotlib`, pipeline, harmonogram
  zadań, wyzwalacz, Power BI, slicer, dashboard
