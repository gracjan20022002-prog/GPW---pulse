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
**Etap: przygotowanie środowiska. Sesja 1–5 (BRONZE) ukończone, Sesja 6 w trakcie.**

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

**Do zrobienia (Sesja 6, kontynuacja):**
- Sprawdzenie #3 (liczba danych) i #4 (poprawny format/typ danych) w `test_plikow.py`.

**Ważna zasada pracy (potwierdzona 2026-07-22):** Gracjan robi **wszystko sam** —
nie tylko kod Pythona, ale też komendy gita i terminala. Ja tłumaczę i podaję
dokładne polecenia do wpisania, nie wykonuję ich za niego (poza czytaniem
plików/stanu, żeby wiedzieć, co się dzieje).

## Gdzie co jest

Kod, dane i notatki (plany, słownik, dziennik) są teraz razem w folderze
projektu: `kod/`, `companies/`, `notatki/` (dziennik i `.obsidian` poza
gitem, tylko lokalnie). Nauka Pythona (osobny projekt, niepowiązany):
`DE/Python_l/`.
