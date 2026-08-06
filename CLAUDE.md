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
**Etap BRONZE i SILVER ukończone. Etap GOLD — Sesje 1–7 z 7 zrobione, dane
zapisane w `gold/`; commit i push jeszcze do wykonania (patrz „Do zrobienia").**

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

**Zrobione (2026-08-01, Sesje 5–6 etapu SILVER):**
- Sesja 5: w `kod/silver 1.py` — pętla `for t in ticker:` po trzech
  spółkach, wczytanie każdego pliku przez f-string (`f"companies/{t}.txt"`),
  naprawa typów jak w Sesji 1–2, dodanie kolumny `df["spolka"] = t`,
  zbieranie tabel w liście przez `.append()`, połączenie przez
  `pd.concat(dft, ignore_index=True)`. Wynik: `dane.shape` → `(2250, 3)`,
  `dane["spolka"].unique()` → `['CBF.WA', 'XTB.WA', 'SNT.WA']`.
- Po drodze poprawione: brak `errors="coerce"` w pętli (niespójność z
  górnym blokiem), i przypadkowe zakomentowanie `import pandas as pd` przy
  zamianie górnego bloku (Sesje 1–4) na komentarz-dokumentację —
  `NameError: name 'pd' is not defined`, poprawione.
- Sesja 6: `dane.sort_values(["spolka", "data"])` (sortowanie po dwóch
  kolumnach — grupowanie po spółce, potem chronologicznie), `dane.describe()`
  jako test sensowności (`cena` min `29.62`, max `394.00`, bez zer/ujemnych).
  Zauważone: `.describe()` liczy też `data`, `std` dla dat wychodzi `NaN` —
  normalne zachowanie pandas, nic do naprawiania.

**Zrobione (2026-08-01, Sesja 7 etapu SILVER — część 1):**
- `dane.to_csv("silver/clean_data.csv", index=False)` — nowy folder
  `silver/`, plik `clean_data.csv` (własna nazwa, zamiast roboczej
  `dane_czyste.csv` z planu). `index=False`, żeby nie dopisywać kolumny
  z numerami wierszy. Sprawdzone: plik istnieje, dane się zgadzają.

**Zrobione (2026-08-01, dokończenie Sesji 7 — zamknięcie etapu SILVER):**
- `README.md` zaktualizowany: sekcja o etapie Silver, `silver/` w strukturze,
  `silver 1.py` w tabeli skryptów, format danych wyjściowych. Poprawione też
  dwie stare nieścisłości: usunięty z tabeli nieistniejący już `Bronze.py`,
  przykładowa godzina w danych `companies/` poprawiona na `09:00:00`.
- Commit `768cf77` i push wykonane przez Gracjana — `git status` czysty,
  `main` zsynchronizowany z `origin/main`.

**Etap SILVER zamknięty.**

**Zrobione (2026-08-01, dodatkowo — werdykt Silver + plan Gold):**
- Na prośbę Gracjana sprawdzone (przez dwóch agentów Explore, bezpośrednio
  na plikach i historii gita), czy etap SILVER jest w 100% kompletny.
  Werdykt: **dane są w 100% czyste** (2250 wierszy = 750×3, zero braków,
  zero duplikatów, zero cen ≤ 0 — sprawdzone wprost na `clean_data.csv`),
  ale **proces ma dwie dziury**: (1) sprawdzenia `isna().sum()` /
  `duplicated().sum()` z Sesji 3–4 istniały tylko na wersji
  jednospółkowej (`plik`, CBF.WA) w commicie `c5f993f` — przy przepisaniu
  na pętlę + `pd.concat` w commicie `768cf77` zostały zakomentowane razem
  ze starym blokiem i nigdy nie odtworzone na finalnej tabeli `dane`;
  (2) ścieżki nadal na sztywno, nie przez `BASE_DIR` (zauważone już
  31.07, odłożone do "Sesji 7"). **Gracjan poprawił obie rzeczy od razu
  tego samego dnia**, sam, w `kod/silver 1.py`: dodał `BASE_DIR` (wzorzec
  z `Data ingestion 2.py`) i przywrócił `dane.isna().sum()` /
  `dane.duplicated().sum()` na finalnej tabeli przed `to_csv`. Sprawdzone
  uruchomieniem: oba wypisują zero.
- Napisany szczegółowy plan etapu GOLD: `notatki/plany/Plan-03-gold.md`,
  w tym samym stylu i szczegółowości co `Plan-02-silver.md` (siedem sesji,
  „wielka nowa idea" = `groupby`, ściąga z przykładami na budce z lodami,
  zakres zgodny z `Plan-ogolny.md`: zmiana procentowa, która spółka rosła
  najszybciej, który miesiąc miał najwięcej wahań — bez wykresów, te są
  w Etapie 4).

**Zrobione (2026-08-01, dodatkowo — porządki przed startem Gold):**
- Słownik (`notatki/Slownik.md`) domknięty (na prośbę Gracjana, wpisy
  napisał Claude): zaległe z Silver (`Series`, `dtype`, `NaN`,
  wektoryzacja) i nowe z Gold (`groupby`, `pct_change`, `merge`,
  odchylenie standardowe, zmienność/wolatylność).
- Bug znaleziony w `kod/Data ingestion 2.py`: `logging.basicConfig()` bez
  `encoding="utf-8"` psuł polskie znaki w `companies/errors.log`. Gracjan
  poprawił sam; po drodze brakujący przecinek (`SyntaxError`), złapany
  przez `python -m py_compile` (bezpieczne — sama składnia, bez
  uruchamiania pobierania i bez ruszania `companies/*.txt`). Poprawione.
- Commit `67e5644`, push — `git status` czysty.

**Zrobione (2026-08-03, Sesje 1–3 etapu GOLD):**
- Nowy plik `kod/gold 1.py`. Sesja 1: wczytanie `silver/clean_data.csv` przez
  `pd.read_csv(...)` (z `BASE_DIR`). Po drodze poprawione dwa błędy
  w parametrach, skopiowanych z Silver (tam plik surowy, bez nagłówka,
  2 kolumny): (1) `header=None, names=["data","cena"]` na pliku, który **ma**
  już nagłówek i **3** kolumny (`data,cena,spolka`) — nagłówek wpadał jako
  wiersz danych, trzecia kolumna się gubiła; (2) nawet po usunięciu
  `header=None`, samo podanie `names=` bez jawnego `header=` dalej zachowuje
  się jak `header=None` — udokumentowana, nieoczywista cecha pandas.
  Ostateczne rozwiązanie: `pd.read_csv(...)` bez `names=` w ogóle, bo plik
  już ma właściwe nazwy kolumn w nagłówku. Sprawdzone: `gold.shape` →
  `(2250, 3)`, `dtypes` przed konwersją pokazuje `data` jako tekst (u
  Gracjana pandas nazywa to `str`, nowsze wersje biblioteki inaczej niż
  starsze `object` — ta sama koncepcja), po `pd.to_datetime()` →
  `datetime64[us]`.
- Sesja 2: `gold["zmiana_proc"] = gold.groupby("spolka")["cena"].pct_change()
  * 100` — dzienna zmiana procentowa, liczona osobno w każdej spółce (żeby
  nie było fałszywej "zmiany" na granicy dwóch spółek sklejonych przez
  `concat` z Silver). Po drodze poprawiony poważniejszy błąd: pierwsza wersja
  przypadkiem nadpisywała kolumnę `cena` wynikiem `pct_change()` zamiast
  zapisać go w nowej kolumnie — oryginalne ceny by zniknęły, a są potrzebne
  w Sesji 3. Sprawdzone na granicy CBF.WA/SNT.WA (`gold.iloc[748:753]`):
  pierwszy wiersz każdej spółki ma `NaN`, reszta wartości zgodna
  matematycznie.
- Sesja 3: `gold.groupby("spolka")["cena"].agg(["first", "last"])
  .reset_index()` — pierwsza i ostatnia cena na spółkę (nowość:
  `.agg([...])` liczy kilka podsumowań na grupę naraz; `.reset_index()`
  przywraca `spolka` z indeksu na zwykłą kolumnę), plus nowa kolumna
  z całkowitą zmianą procentową `(last - first) / first * 100` (nawias
  wokół różnicy obowiązkowy — bez niego kolejność działań w Pythonie
  policzyłaby dzielenie przed odejmowaniem). Po drodze kilka błędów: wynik
  `agg`/`reset_index()` najpierw tylko wypisywany, nigdzie niezapisany (ten
  sam wzorzec co w Sesji 2 z `pct_change`); próba zapisania wyniku do pustej
  listy zamiast tabeli; odwołania do kolumn `first`/`last` zrobione przez
  pomyłkę na `gold` zamiast na nowej, osobnej tabeli (3 wiersze, nie 2250);
  `sort_values` bez `by=`. Finalny wynik, posortowany malejąco: **SNT.WA**
  70,80→360,00 zł (**+408,47%**), **XTB.WA** 40,02→137,00 zł (**+242,33%**),
  **CBF.WA** 78,80→192,50 zł (**+144,29%**) — zgodne z tym, co plan
  zapowiadał o dużej zmienności SNT.WA.
- Nazewnictwo kolumn miejscami odbiega od planu — świadomy wybór Gracjana:
  `roznica` zamiast `zmiana_calkowita_proc` w Sesji 3 (ta tabela w planie
  nazywa się `wzrost` — do pamiętania w Sesji 6 przy `merge`).
- `kod/gold 1.py` jeszcze niezacommitowany na koniec dnia.

**Zrobione (2026-08-06, Sesje 4–7 etapu GOLD — zapis wyników):**
- Sesja 4: `gold["max_zmienny_miesiac"] = gold["data"].dt.to_period("M")` —
  miesiąc wyciągnięty z daty przez akcesor `.dt`. Sprawdzone: `nunique()`
  dało **37**, nie ~36 jak zakładał pierwszy szacunek (3 lata × 12) — zakres
  dat zaczyna i kończy się w połowie lipca (24.07.2023–24.07.2026), nie na
  granicy roku: 6 miesięcy z 2023 + 12 z 2024 + 12 z 2025 + 7 z 2026 = 37.
  Nie błąd, tylko dokładniejsze liczenie zakresu.
- Sesja 5: `zmiana_msc = gold.groupby(["spolka", "max_zmienny_miesiac"])
  ["zmiana_proc"].std().reset_index().sort_values(by="zmiana_proc",
  ascending=False)` — odchylenie standardowe dziennej zmiany, osobno dla
  każdej pary spółka+miesiąc. Po drodze trzy błędy: (1) `sort_values()`
  policzone i nigdzie niezapisane — ten sam wzorzec „policzone i zapomniane"
  co w Sesji 2–3; (2) `sort_values(by=...)` wywołane na Series (przed
  `.reset_index()`) — `by=` istnieje tylko dla DataFrame, Series ma jeden
  zestaw wartości i nie trzeba mu mówić, po czym sortować; poprawiona
  kolejność: `.std()` → `.reset_index()` → `.sort_values(by=...)`;
  (3) przypadkowe `.head(1)` wsadzone w środek tej linii (między wybraniem
  kolumny a `.std()`) — dawało jedną liczbę (`numpy.float64`) na całą
  tabelę zamiast wyniku na grupę, stąd `AttributeError: 'numpy.float64'
  object has no attribute 'reset_index'`.
- Wyjaśnione przy tej okazji: `pct_change()` zachowuje kształt tabeli (tyle
  samo wierszy), `.std()` po `groupby` go zwija (jeden wiersz na grupę) —
  wyniku takiej operacji nie da się wsadzić jako nowej kolumny do `gold`
  (2250 wierszy vs ~111 grup spółka+miesiąc), długości się nie zgadzają.
- Sesja 6: `sp_rank = zmiana_msc.groupby("spolka").head(1).merge(calk_zmiana,
  on="spolka")` — wybranie najbardziej zmiennego miesiąca każdej spółki
  (tabela już posortowana, więc pierwszy wiersz w grupie = rekord) i
  sklejenie z tabelą z Sesji 3. Po drodze błędy: `.groupby(...).head(1)`
  wywołane na `gold` (surowe dane dzienne) zamiast na `zmiana_msc`; `.merge()`
  wywołane z dwiema tabelami podanymi jako tekst w cudzysłowie, zamiast
  jedną prawdziwą tabelą jako argumentem.
- Sesja 7 — nazewnictwo i decyzja o strukturze: długa dyskusja, czy końcowa
  tabela ma sens dla osoby z zewnątrz. Rozważone i odrzucone: jedna wielka
  tabela ze wszystkim naraz; tabela z wszystkimi wierszami + flaga przez
  `.transform("max")` (rozsmarowanie maksimum grupy na każdy wiersz, bez
  zwijania — inne niż `.agg()`/`.std()`). **Decyzja: dwie końcowe tabele** —
  dzienna (`gold`: cena + zmiana % dzień po dniu) i podsumowująca (`sp_rank`:
  jeden wiersz na spółkę) — czyli to, co już zakładał `Plan-03-gold.md`.
- Kolumny w `calk_zmiana` przemianowane: `first`/`last`→`pierwsza_cena`/
  `ostatnia_cena`, `calk_roznica`→`zmiana_caly_okres`. Kolumna `zmiana_proc`
  w `zmiana_msc` (odchylenie miesięczne) **świadomie zostawiona** pod tą
  samą nazwą co dzienna `zmiana_proc` w `gold` — Gracjan zdecydował się nie
  zmieniać, mimo znanej kolizji nazw (dwa różne znaczenia, jedna nazwa).
- Błędy przy `.rename()`/`.agg()` po drodze: (1) `.agg(["cena_pocz",
  "cena_konc"])` — nieprawidłowe, `.agg([...])` przyjmuje tylko prawdziwe
  nazwy funkcji (`"first"`, `"last"`), własne nazwy nadaje się później przez
  `.rename()`; (2) `.rename(columns={"first":...})` wywołane na `zmiana_msc`,
  gdzie te kolumny w ogóle nie istnieją — pandas po cichu ignoruje
  niedopasowane nazwy (bez błędu), więc nic się nie zmieniało; (3) wynik
  `.rename()` na `calk_zmiana` policzony, ale nieprzypisany z powrotem do
  zmiennej — kolejne „policzone i zapomniane".
- Rozważone i **odłożone na później** (nie zrobione teraz, żeby domknąć
  zapis): różnica ceny w złotówkach (`ostatnia_cena - pierwsza_cena`) i
  najbardziej zmienny **pojedynczy dzień** (nie tylko miesiąc). Do tego
  wprowadzona koncepcja `.idxmax()` (numer wiersza z maksimum w grupie, nie
  sama wartość) + `.loc[]` (wyciągnięcie całego wiersza po tym numerze) —
  jeszcze niezaimplementowane.
- Poprawione ścieżki zapisu w `gold 1.py`: brak `BASE_DIR` w dwóch liniach
  `.to_csv()` na końcu pliku, a potem źle domknięty nawias — `index=False`
  wpadło do wnętrza `os.path.join(...)` zamiast być osobnym argumentem
  `.to_csv()` (`os.path.join()` nie ma parametru `index`, stąd `TypeError`).
- **Zapisane pliki:** `gold/dane_dzienne.csv` (pełna tabela dzienna, 2250
  wierszy) i `gold/ranking.csv` (`sp_rank`, 3 wiersze — jeden na spółkę;
  kolumny: `spolka`, `max_zmienny_miesiac`, `zmiana_proc` [odchylenie w tym
  miesiącu], `pierwsza_cena`, `ostatnia_cena`, `zmiana_caly_okres`). Wartości
  `zmiana_caly_okres` niezmienione względem Sesji 3 (rename nie zmienia
  danych): SNT.WA **+408,47%**, XTB.WA **+242,33%**, CBF.WA **+144,29%**.
- Po drodze też naprawiony `kod/silver 1.py`: `.to_csv("silver/clean_data.csv"...)`
  używał ścieżki względnej — dokończone użycie `BASE_DIR` (wzorzec
  wprowadzony do tego pliku 01.08, ale wtedy nie doprowadzony do tej
  konkretnej linii zapisu) na `os.path.join(BASE_DIR, "silver",
  "clean_data.csv")`.
- Drobna, niepilna uwaga zauważona w `silver 1.py`: `dane.isna().sum()` /
  `dane.duplicated().sum()` wykonują się **po** `.to_csv()`, nie przed —
  nie psuje danych (to tylko odczyt), ale sens tych sprawdzeń to złapanie
  problemu przed zapisem, nie po. Nieporuszane teraz, do rozważenia później.

**Do zrobienia:** commit i push zmian z dzisiejszej sesji (`kod/gold 1.py`,
`kod/silver 1.py`, nowe pliki `gold/dane_dzienne.csv`, `gold/ranking.csv`) —
to zamknie etap GOLD. Opcjonalnie później: różnica ceny w zł i najbardziej
zmienny dzień w `sp_rank` (`.idxmax()` + `.loc[]`, patrz wyżej); aktualizacja
`README.md` o etap Gold (jeszcze nie zrobiona).

**Ważna zasada pracy (potwierdzona 2026-07-22):** Gracjan robi **wszystko sam** —
nie tylko kod Pythona, ale też komendy gita i terminala. Ja tłumaczę i podaję
dokładne polecenia do wpisania, nie wykonuję ich za niego (poza czytaniem
plików/stanu, żeby wiedzieć, co się dzieje).

## Gdzie co jest

Kod, dane i notatki (plany, słownik, dziennik) są teraz razem w folderze
projektu: `kod/`, `companies/`, `notatki/` (dziennik i `.obsidian` poza
gitem, tylko lokalnie). Nauka Pythona (osobny projekt, niepowiązany):
`DE/Python_l/`.
