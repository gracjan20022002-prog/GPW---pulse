# CLAUDE.md — zasady pracy nad projektem GPW Pulse

## Kim jest użytkownik

Gracjan, uczy się data engineeringu. GitHub: `gracjan20022002-prog`.

**Zna:** `if/else`, pętle `for`, listy, słowniki, funkcje `def` z typami,
`try/except`, `logging`, `requests` i API, zapis do plików, list comprehensions,
`lambda`, `map`/`filter`/`zip`.

**Nie zna:** klas, pandas w praktyce, struktury programu, testów, `venv`.
Nigdy nie zbudował całego programu od początku do końca.

## Zasady — obowiązkowe

1. **Nie piszesz kodu do tego projektu.** Kod pisze Gracjan. Ty tłumaczysz
   i dajesz przykłady na **innych** danych niż jego zadanie. Kod pomocniczy —
   tylko po jego prośbie i za zgodą.
2. **Testy pisze Gracjan**, sam, po swoim kodzie. Nie dostarczasz gotowych.
3. **Prosty język.** Krótkie zdania. Każde trudne słowo tłumacz od razu.
4. **Małe kroki.** Jedna nowa rzecz na sesję. Sesja to 1,5–2 h dziennie.
5. **Po każdej sesji** dopisz co się zmieniło: tutaj i w dzienniku Obsidiana.

## Stan projektu

Repo robocze: folder lokalny `GPW - pulse`, połączony z repozytorium na GitHubie:
`https://github.com/gracjan20022002-prog/GPW---pulse`.
Stare repo `gpw-pulse` zostaje tylko jako podgląd.
**Etap BRONZE ukończony (Sesja 1–7). Następny etap: SILVER (czyszczenie danych, `pandas`).**

**Zrobione (2026-07-22):**
- `.venv` utworzone lokalnie, `requests` zainstalowany.
- Sesja 1: sprawdzone stooq.pl, ręcznie pobrane pliki CSV dla trzech spółek —
  **XTB, Cyber_Folks, Synektik** (zamiast PKN/PKO/CDR z planu — dozwolona
  zmiana, plan mówił „możesz wybrać inne"). Pliki w `companies/`
  (`xtb_d.csv`, `cbf_d.csv`, `snt_d.csv`).
  Link do danych: `https://stooq.pl/q/d/?f=20230722&t=20260722&s=xtb&c=0`
  (to strona z tabelą/eksportem, nie bezpośredni plik — trzeba kliknąć „pobierz").
  Kolumny w pliku: Data, Otwarcie, Najwyzszy, Najnizszy, Zamkniecie, Wolumen.
  748 wierszy (747 danych + nagłówek), zakres dat 24.07.2023–22.07.2026 (~3 lata).
- Sesja 2: `.gitignore` (wyklucza `.venv/`), `git init`, pierwszy commit,
  repozytorium `GPW---pulse` założone na GitHubie i połączone (`git remote add origin`,
  `git push -u origin main`) — **udało się, dane są na GitHubie.**

**Zrobione (2026-07-23):**
- Sesja 3: stooq.pl zablokował programowe pobieranie (zabezpieczenie
  antybotowe, zagadka JS pod `/q/d/l/`) — zmiana źródła danych na
  **Yahoo Finance** (`https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}.WA`,
  `.WA` = GPW). Wymaga nagłówka `User-Agent` (np. `"Mozilla/5.0"`),
  dane w formacie JSON.
- Napisany program: pobiera dane jednej spółki (CBF.WA) przez `requests`,
  wyciąga `timestamp` i `close` z zagnieżdżonego JSON-a, zamienia timestamp
  na datę (`datetime.fromtimestamp()`), łączy przez `zip()`, wypisuje
  5 dni danych (data + cena zamknięcia).
- Nauczona eksploracja nieznanej struktury JSON: `type()`, `.keys()`, `len()`.

**Zrobione (2026-07-25):**
- Sesja 4: rozszerzony zakres danych o `params = {"range": "3y", "interval": "1d"}`
  (750 dni zamiast 5). Wyciąganie cen zamknięcia z zagnieżdżonego JSON-a
  (`indicators.quote[0].close`), pętla `for tick in ticker:` po liście
  trzech spółek (`CBF.WA`, `XTB.WA`, `SNT.WA`), zapis do osobnego pliku
  `.txt` na spółkę przez `with open(...) as plik: ... plik.write(...)`.
- Duża reorganizacja projektu: kod (`kod/`) i notatki (`notatki/`) przeniesione
  do folderu projektu `GPW - pulse` (wcześniej rozjechane między dwoma
  miejscami w `Obsidian-DE`, częściowo zdublowane). `.gitignore` wyklucza
  `notatki/dziennik/` (prywatny) i `notatki/.obsidian/` (config aplikacji)
  z GitHuba. `README.md` zaktualizowany pod nową strukturę. Stare CSV ze
  stooq usunięte z `companies/`, zastąpione plikami `.txt` z Yahoo Finance.

**Zrobione (2026-07-26):**
- Sesja 5: `try/except` + `logging` w `kod/Data ingestion 2.py` — pojedynczy zły
  ticker (test: `676.WA`, status 404) loguje się do `errors.log` i nie zatrzymuje
  pobierania pozostałych spółek.
- Sesja 6 (start): nowy plik `kod/test_plikow.py` — sprawdzenie #1 (czy plik
  istnieje) i #2 (czy ma prawidłowy format: 2 elementy po `split(",")`, data
  długości 19 znaków). Wprowadzone `BASE_DIR` liczone przez `__file__`, żeby
  ścieżki nie zależały od working directory terminala.

**Zrobione (2026-07-27):**
- Sesja 6 (dokończona): w `kod/test_plikow.py` dodane sprawdzenie #3 (liczba
  danych — licznik poprawnych wierszy porównywany z progiem 700) i #4
  (typ danych — `datetime.strptime(...)` i `float(...)` w `try/except
  ValueError`, sprawdzają, czy tekst da się naprawdę odczytać jako data
  i liczba, nie tylko czy ma odpowiedni kształt).
- Po drodze znalezione i poprawione dwa bugi: (1) sprawdzenie liczby wierszy
  było wewnątrz pętli zamiast po niej, (2) licznik zwiększał się nawet przy
  nieudanej konwersji typu, bo `licznik += 1` było poza `try`.
- Znaleziony i poprawiony bug przy ręcznym teście złego tickera:
  `os.path.exists()` był tylko wypisywany, nigdy nie użyty do decyzji —
  program wywalał się `FileNotFoundError`. Dodane `if result: ... else: ...`.
- Potwierdzona wcześniejsza poprawka w `Data ingestion 2.py`: zapis danych
  i `errors.log` liczą ścieżkę przez `BASE_DIR`.

**Zrobione (2026-07-27, Sesja 7 — zamknięcie etapu BRONZE):**
- Przejrzany cały kod z `kod/` (Claude — przegląd, bez pisania kodu za Gracjana).
  Znalezione: `Bronze.py` i `Data ingestion.py` były identyczną kopią
  (eksploracja z Sesji 3).
- `README.md` zaktualizowany: opis etapu BRONZE, tabela skryptów w `kod/`,
  opis formatu danych w `companies/`.
- Commit `7a800ae` ("Sesja 6: sprawdzenia #3 i #4...") wypchnięty na GitHub.
- Gracjan usunął `kod/Bronze.py` (duplikat) własną decyzją i wypchnął zmianę —
  potwierdzone: `git status` czysty, `main` zsynchronizowany z `origin/main`.
- `kod/Data ingestion.py` (drugi duplikat) **zostaje** — świadoma decyzja
  Gracjana, żeby zachować go jako materiał referencyjny z Sesji 3.
- Testowy zły ticker `676.WA` w `kod/Data ingestion 2.py` — zostawiony,
  nieporuszany dalej (nie było wyraźnej decyzji o usunięciu).

**Etap BRONZE zamknięty.**

**Zrobione (2026-07-27, dodatkowo — plan Silver):**
Na prośbę Gracjana napisany szczegółowy plan całego etapu SILVER:
`notatki/plany/Plan-02-silver.md`. Zawiera: konkretne problemy w danych
z `companies/` do naprawienia w tym etapie (typy zapisane jako tekst,
możliwe braki cen, trzy osobne pliki zamiast jednej tabeli, brak nazw
kolumn), wyjaśnienie „wektoryzacji" (operacje na całej kolumnie pandas
zamiast pętli `for`), ściągę funkcji pandas potrzebnych na tym etapie
(`read_csv`, `head`/`info`/`describe`/`dtypes`, wybieranie kolumn/wierszy,
`to_datetime`/`to_numeric`, `isna`/`dropna`/`fillna`, `duplicated`/
`drop_duplicates`, `concat`, `sort_values`, `to_csv`) z przykładami na
danych **spoza** projektu (zgodnie z zasadą #1), oraz podział na 7 sesji
w stylu `Plan-01-bronze.md` (jedna nowa rzecz na sesję).

**Zrobione (2026-07-31, Sesje 1–4 etapu SILVER):**
- Domknięte zaległości z 27-go: `.gitignore` dodany o `GPW - Python.code-workspace`
  (plik lokalnego edytora, nietrafiający do repo), commit zamknięcia Sesji 7
  i planu Silver wypchnięty na GitHub.
- Nowy plik `kod/silver 1.py`. Sesja 1: `pd.read_csv("companies/CBF.WA.txt",
  header=None, names=["data", "cena"], skipinitialspace=True)` — pierwsze
  wczytanie danych jednej spółki do `DataFrame`, obejrzane przez `.head()`,
  `.info()`, `.dtypes`.
- Sesja 2: naprawa typów przez wektoryzację — `pd.to_datetime(plik["data"])`,
  `pd.to_numeric(plik["cena"], errors="coerce")`. Wynik: `data` →
  `datetime64[us]`, `cena` → `float64`.
- Sesja 3: `plik.isna().sum()` — zero braków w obu kolumnach.
- Sesja 4: `plik.duplicated().sum()` — zero duplikatów.
- Wszystkie cztery sesje zrobione w jednej rozmowie (Gracjan sam zdecydował
  jechać bez przerwy) — jedna nowa rzecz na sesję nadal zachowana, tylko
  bez przerwy między sesjami tego dnia.
- **Odkrycie po drodze:** `cena` wyszła z `read_csv` od razu jako `float64`
  (automatyczne wnioskowanie typu przez pandas, bo brak było braków w danych)
  — inaczej niż zakładał plan Silver, który spodziewał się tekstu do
  ręcznej konwersji. `pd.to_numeric` i tak zastosowany, jako zabezpieczenie
  na wypadek innych plików spółek.
- **Poprawiona nieścisłość w dokumentacji:** `notatki/plany/Plan-02-silver.md`
  (problem #4) twierdził, że godzina w danych to zawsze `00:00:00` — dane
  z `CBF.WA.txt` pokazują konsekwentnie `09:00:00`. Poprawione w tym pliku.
- Drobna uwaga na później (nie zrobione teraz, żeby nie przeciążać sesji):
  `kod/silver 1.py` wczytuje plik ścieżką względną (`"companies/CBF.WA.txt"`),
  nie przez `BASE_DIR` jak `test_plikow.py` — działa tylko przy odpaleniu
  z folderu głównego repo. Do rozważenia przy porządkach w Sesji 7 Silver.

**Do zrobienia:** Sesja 5 etapu SILVER — wczytanie trzech plików spółek w
pętli, dodanie kolumny `spolka` do każdej tabeli, połączenie przez
`pd.concat([...], ignore_index=True)`. Szczegóły w
`notatki/plany/Plan-02-silver.md`.

**Ważna zasada pracy (potwierdzona 2026-07-22):** Gracjan robi **wszystko sam** —
nie tylko kod Pythona, ale też komendy gita i terminala. Ja tłumaczę i podaję
dokładne polecenia do wpisania, nie wykonuję ich za niego (poza czytaniem
plików/stanu, żeby wiedzieć, co się dzieje).

## Gdzie co jest

Kod, dane i notatki (plany, słownik, dziennik) są teraz razem w folderze
projektu: `kod/`, `companies/`, `notatki/` (dziennik i `.obsidian` poza
gitem, tylko lokalnie). Nauka Pythona (osobny projekt, niepowiązany):
`DE/Python_l/`.
